"""
Safe mathematical parser for QuantumLab using Python AST.
Enforces strict node whitelists, limits on depth and length, and safe evaluation.
Protects against arbitrary Python execution, __import__, attribute access, and denial of service.
Addresses DEF-01 (structured error codes) and DEF-08 (complex exponent evaluation & power validation).
"""

import ast
import re
import math
from typing import Optional
import sympy as sp
import numpy as np

from .errors import (
    QuantumLabError,
    MathParseError,
    ParseSecurityError,
    ScientificValidationError,
)


class SafeASTParser:
    MAX_LENGTH = 500
    MAX_DEPTH = 25
    MAX_NODES = 100
    MAX_POWER = 100
    MAX_INT_DIGITS = 100

    ALLOWED_FUNCS = {
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "asin": sp.asin,
        "acos": sp.acos,
        "atan": sp.atan,
        "sinh": sp.sinh,
        "cosh": sp.cosh,
        "tanh": sp.tanh,
        "exp": sp.exp,
        "log": sp.log,
        "ln": sp.log,
        "sqrt": sp.sqrt,
        "abs": sp.Abs,
    }

    # Standard symbols used in the physics engine
    x = sp.Symbol("x", real=True)
    hbar = sp.Symbol("ℏ", positive=True, real=True)
    m = sp.Symbol("m", positive=True, real=True)
    w = sp.Symbol("ω", positive=True, real=True)
    L = sp.Symbol("L", positive=True, real=True)
    n = sp.Symbol("n", integer=True, positive=True)
    k = sp.Symbol("k", positive=True, real=True)
    a = sp.Symbol("a", positive=True, real=True)
    V0 = sp.Symbol("V0", real=True)
    E = sp.Symbol("E", real=True)
    t = sp.Symbol("t", real=True)

    ALLOWED_SYMBOLS = {
        "x": x,
        "hbar": hbar,
        "m": m,
        "w": w,
        "omega": w,
        "L": L,
        "n": n,
        "k": k,
        "a": a,
        "V0": V0,
        "E": E,
        "t": t,
        "pi": sp.pi,
        "oo": sp.oo,
        "I": sp.I,
        "i": sp.I,
        "j": sp.I,
    }

    @classmethod
    def normalize_input(cls, text: str) -> str:
        """Pre-normalizes Unicode math symbols and shorthand operators."""
        text = text.strip()
        replacements = {
            "ħ": "hbar",
            "ω": "w",
            "π": "pi",
            "∞": "oo",
            "·": "*",
            "×": "*",
            "^": "**",
        }
        for orig, target in replacements.items():
            text = text.replace(orig, target)
        return text

    @classmethod
    def _try_eval_const_expr(cls, node: ast.AST) -> Optional[float]:
        """
        DEF-08: Safely pre-evaluates pure constant arithmetic sub-trees without eval() or SymPy.
        Returns float/int value if pure constant arithmetic, or None if it contains variables/functions.
        Enforces MAX_INT_DIGITS and MAX_POWER on intermediate results to prevent combinatorial explosion.
        """
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                if isinstance(node.value, int) and len(str(abs(node.value))) > cls.MAX_INT_DIGITS:
                    raise ParseSecurityError("error.int_too_large", max_digits=cls.MAX_INT_DIGITS)
                return float(node.value)
            return None

        elif isinstance(node, ast.UnaryOp):
            val = cls._try_eval_const_expr(node.operand)
            if val is None:
                return None
            if isinstance(node.op, ast.USub):
                return -val
            elif isinstance(node.op, ast.UAdd):
                return val
            return None

        elif isinstance(node, ast.BinOp):
            left_val = cls._try_eval_const_expr(node.left)
            right_val = cls._try_eval_const_expr(node.right)
            if left_val is None or right_val is None:
                return None

            if isinstance(node.op, ast.Add):
                return left_val + right_val
            elif isinstance(node.op, ast.Sub):
                return left_val - right_val
            elif isinstance(node.op, ast.Mult):
                res = left_val * right_val
                if abs(res) > 10**cls.MAX_INT_DIGITS:
                    raise ParseSecurityError("error.int_too_large", max_digits=cls.MAX_INT_DIGITS)
                return res
            elif isinstance(node.op, ast.Div):
                if right_val == 0:
                    return None
                return left_val / right_val
            elif isinstance(node.op, ast.Pow):
                if abs(right_val) > cls.MAX_POWER:
                    raise ParseSecurityError("error.exponent_too_large", exp=right_val, max_exp=cls.MAX_POWER)
                try:
                    return left_val ** right_val
                except OverflowError:
                    raise ParseSecurityError("error.exponent_too_large", exp=right_val, max_exp=cls.MAX_POWER)
            return None

        return None

    @classmethod
    def parse(cls, expr_str: str, custom_symbols: dict = None) -> sp.Expr:
        """
        Parses mathematical expressions safely via Python AST.
        Only whitelisted mathematical functions, operators, and symbols are permitted.
        """
        if not expr_str or not expr_str.strip():
            raise MathParseError("error.empty_expression")

        if len(expr_str) > cls.MAX_LENGTH:
            raise ParseSecurityError(
                "error.input_too_long",
                length=len(expr_str),
                max_len=cls.MAX_LENGTH
            )

        norm_text = cls.normalize_input(expr_str)

        try:
            tree = ast.parse(norm_text, mode="eval")
        except SyntaxError as e:
            raise MathParseError("error.syntax_invalid", detail=e.msg) from e

        node_count = sum(1 for _ in ast.walk(tree))
        if node_count > cls.MAX_NODES:
            raise ParseSecurityError(
                "error.too_complex_nodes",
                count=node_count,
                max_nodes=cls.MAX_NODES
            )

        symbols = dict(cls.ALLOWED_SYMBOLS)
        if custom_symbols:
            symbols.update(custom_symbols)

        cls._validate_and_check_depth(tree.body, 1)
        return cls._eval_ast_node(tree.body, symbols)

    @classmethod
    def _validate_and_check_depth(cls, node: ast.AST, depth: int):
        if depth > cls.MAX_DEPTH:
            raise ParseSecurityError("error.ast_too_deep", max_depth=cls.MAX_DEPTH)

        # DEF-08: Rigorous power validation
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
            # 1. Any nested power in base or exponent sub-trees (e.g. x**y**z, (x**y)**z, x**(2**3))
            for subnode in ast.walk(node.left):
                if subnode is not node and isinstance(subnode, ast.BinOp) and isinstance(subnode.op, ast.Pow):
                    raise ParseSecurityError("error.power_nested_too_deep")
            for subnode in ast.walk(node.right):
                if subnode is not node and isinstance(subnode, ast.BinOp) and isinstance(subnode.op, ast.Pow):
                    raise ParseSecurityError("error.power_nested_too_deep")

            # 2. Evaluate constant exponent sub-trees (e.g. x**(50*3), 2**(25*8), x**(10+95))
            const_exp = cls._try_eval_const_expr(node.right)
            if const_exp is not None:
                if abs(const_exp) > cls.MAX_POWER:
                    raise ParseSecurityError("error.exponent_too_large", exp=const_exp, max_exp=cls.MAX_POWER)

            # 3. Check combinatorial growth when base is constant (e.g. 100**60)
            const_base = cls._try_eval_const_expr(node.left)
            if const_base is not None and const_exp is not None:
                if abs(const_base) > 1 and const_exp > 0:
                    if const_exp * math.log10(abs(const_base)) > cls.MAX_INT_DIGITS:
                        raise ParseSecurityError("error.int_too_large", max_digits=cls.MAX_INT_DIGITS)

        # Large integer digit limit
        if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
            if len(str(abs(node.value))) > cls.MAX_INT_DIGITS:
                raise ParseSecurityError("error.int_too_large", max_digits=cls.MAX_INT_DIGITS)

        # Disallow attribute access, imports, lambdas, subscripts, comprehensions, etc.
        disallowed_types = (
            ast.Attribute,
            ast.Subscript,
            ast.List,
            ast.Dict,
            ast.Set,
            ast.Tuple,
            ast.ListComp,
            ast.DictComp,
            ast.SetComp,
            ast.GeneratorExp,
            ast.Lambda,
            ast.IfExp,
            ast.NamedExpr,
        )
        if isinstance(node, disallowed_types):
            raise ParseSecurityError("error.forbidden_node", node=type(node).__name__)

        for child in ast.iter_child_nodes(node):
            cls._validate_and_check_depth(child, depth + 1)

    @classmethod
    def _eval_ast_node(cls, node: ast.AST, symbols: dict) -> sp.Expr:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float, complex)):
                return sp.sympify(node.value)
            else:
                raise ParseSecurityError("error.forbidden_node", node=type(node.value).__name__)

        elif isinstance(node, ast.Name):
            name = node.id
            if name in symbols:
                return symbols[name]
            elif name in cls.ALLOWED_FUNCS:
                raise MathParseError("error.func_without_parens", name=name)
            else:
                raise ParseSecurityError("error.forbidden_variable", name=name)

        elif isinstance(node, ast.UnaryOp):
            operand = cls._eval_ast_node(node.operand, symbols)
            if isinstance(node.op, ast.USub):
                return -operand
            elif isinstance(node.op, ast.UAdd):
                return operand
            else:
                raise MathParseError("error.unsupported_unary", op=type(node.op).__name__)

        elif isinstance(node, ast.BinOp):
            left = cls._eval_ast_node(node.left, symbols)
            right = cls._eval_ast_node(node.right, symbols)

            if isinstance(node.op, ast.Add):
                return left + right
            elif isinstance(node.op, ast.Sub):
                return left - right
            elif isinstance(node.op, ast.Mult):
                return left * right
            elif isinstance(node.op, ast.Div):
                return left / right
            elif isinstance(node.op, ast.Pow):
                if isinstance(node.right, ast.Constant) and isinstance(node.right.value, (int, float)):
                    if abs(node.right.value) > cls.MAX_POWER:
                        raise ParseSecurityError(
                            "error.exponent_too_large",
                            exp=node.right.value,
                            max_exp=cls.MAX_POWER
                        )
                return left ** right
            else:
                raise MathParseError("error.unsupported_binary", op=type(node.op).__name__)

        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ParseSecurityError("error.invalid_call")
            func_name = node.func.id
            if func_name not in cls.ALLOWED_FUNCS:
                raise ParseSecurityError("error.forbidden_function", func=func_name)

            sympy_func = cls.ALLOWED_FUNCS[func_name]
            if node.keywords:
                raise ParseSecurityError("error.invalid_call_kwargs")

            args = [cls._eval_ast_node(arg, symbols) for arg in node.args]
            return sympy_func(*args)

        else:
            raise ParseSecurityError("error.forbidden_node", node=type(node).__name__)


def parse_parameters(text: str) -> dict:
    """
    Parses a parameter string such as:
      'n=6, L=1.0 nm, E=3.2 eV, V0=5.0 eV, a=0.5 nm'
      'n=0 (Estado base)'
      '2, 1-1j; 1+1j, 3'
    Returns a dictionary of parsed values and flags.
    """
    params = {}
    if not text or not text.strip():
        return params

    raw = text.strip()
    params["raw"] = raw

    pairs = re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([^,;()]+)", raw)
    for key, val_str in pairs:
        key = key.strip()
        val_str = val_str.strip()
        cleaned_val = re.sub(r"(?i)\s*(?:ev|nm|pm|um|mm|m|s|fs|ps|ns|kg|j)?$", "", val_str).strip()
        try:
            if "." in cleaned_val or "e" in cleaned_val.lower():
                val_num = float(cleaned_val)
                if key == "n" and not val_num.is_integer():
                    raise ScientificValidationError("error.quantum_number_fractional", n=cleaned_val)
                params[key] = int(val_num) if (key == "n" and val_num.is_integer()) else val_num
            else:
                params[key] = int(cleaned_val)
        except ValueError as e:
            if isinstance(e, ScientificValidationError):
                raise
            try:
                params[key] = SafeASTParser.parse(cleaned_val)
            except Exception:
                params[key] = val_str

    return params


def parse_matrix(raw_text: str, max_dim: int = 16) -> np.ndarray:
    """
    Safely parses a matrix string such as '2, 1-1j; 1+1j, 3'.
    Validates:
      - N x N square matrix, 1 <= N <= max_dim
      - Identical row lengths
      - Finite complex or real elements
    """
    if not raw_text or not raw_text.strip():
        raise ScientificValidationError("error.matrix_empty")

    raw_rows = [r.strip() for r in raw_text.strip().split(";") if r.strip()]
    if not raw_rows:
        raise ScientificValidationError("error.matrix_no_rows")

    matrix_rows = []
    expected_cols = None

    for r_idx, row_str in enumerate(raw_rows):
        tokens = [t.strip() for t in row_str.split(",") if t.strip()]
        if not tokens:
            raise ScientificValidationError("error.matrix_empty_row", row=r_idx + 1)

        if expected_cols is None:
            expected_cols = len(tokens)
        elif len(tokens) != expected_cols:
            raise ScientificValidationError(
                "error.matrix_ragged_rows",
                row=r_idx + 1,
                len=len(tokens),
                expected=expected_cols
            )

        row_vals = []
        for val_str in tokens:
            lower_token = val_str.strip().lower()
            if lower_token in ("inf", "-inf", "+inf", "nan", "-nan", "+nan", "oo", "-oo"):
                raise ScientificValidationError("error.matrix_non_finite", val=val_str)

            norm_val = val_str.replace("i", "j")
            try:
                val = complex(norm_val)
            except ValueError as e:
                try:
                    sym_val = SafeASTParser.parse(val_str)
                    val = complex(complex(sym_val.evalf()))
                except Exception:
                    raise ScientificValidationError("error.matrix_invalid_val", val=val_str) from e

            if not np.isfinite(val.real) or not np.isfinite(val.imag):
                raise ScientificValidationError("error.matrix_non_finite", val=val_str)
            row_vals.append(val)

        matrix_rows.append(row_vals)

    nrows = len(matrix_rows)
    ncols = expected_cols

    if nrows != ncols:
        raise ScientificValidationError("error.matrix_not_square", rows=nrows, cols=ncols)

    if nrows > max_dim:
        raise ScientificValidationError("error.matrix_max_dim", rows=nrows, cols=ncols, max_dim=max_dim)

    return np.array(matrix_rows, dtype=complex)


def parse_state_vector(raw_text: str, expected_dim: int = None) -> np.ndarray:
    """
    Parses a state vector such as '[1, 0]' or '1, 0' or '[1/sqrt(2), 1/sqrt(2)]'.
    Preserves math function calls like sqrt(2) while removing descriptive comments.
    """
    clean = raw_text.strip()
    if not clean:
        raise ScientificValidationError("error.state_vector_empty")

    bracket_match = re.search(r"\[(.*)\]", clean)
    if bracket_match:
        clean = bracket_match.group(1).strip()
    else:
        clean = re.sub(r"\s*\([^()]*[a-zA-Z\s|ψ⟩]{3,}[^()]*\)\s*$", "", clean).strip()

    tokens = [t.strip() for t in re.split(r"[,;]+", clean) if t.strip()]
    if not tokens:
        raise ScientificValidationError("error.state_vector_empty")

    values = []
    for token in tokens:
        norm_val = token.replace("i", "j")
        try:
            val = complex(norm_val)
        except ValueError:
            try:
                sym_val = SafeASTParser.parse(token)
                val = complex(sym_val.evalf())
            except Exception as e:
                raise ScientificValidationError("error.state_vector_invalid_component", token=token) from e

        if not np.isfinite(val.real) or not np.isfinite(val.imag):
            raise ScientificValidationError("error.state_vector_non_finite", token=token)
        values.append(val)

    if not values:
        raise ScientificValidationError("error.state_vector_no_components")

    vec = np.array(values, dtype=complex)
    if expected_dim is not None and len(vec) != expected_dim:
        raise ScientificValidationError(
            "error.state_vector_dimension_mismatch",
            vec_len=len(vec),
            mat_dim=expected_dim
        )

    norm = np.linalg.norm(vec)
    if norm < 1e-15:
        raise ScientificValidationError("error.state_vector_null")

    return vec
