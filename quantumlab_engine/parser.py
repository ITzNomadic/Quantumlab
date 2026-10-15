"""
Safe mathematical parser for QuantumLab using Python AST.
Enforces strict node whitelists, limits on depth and length, and safe evaluation.
Protects against arbitrary Python execution, __import__, attribute access, and denial of service.
"""

import ast
import re
import sympy as sp
import numpy as np


class ParseSecurityError(ValueError):
    """Raised when an expression violates security or grammar restrictions."""
    pass


class SafeASTParser:
    MAX_LENGTH = 500
    MAX_DEPTH = 25
    MAX_POWER = 100

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
        # Unicode replacements
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
    def parse(cls, expr_str: str, custom_symbols: dict = None) -> sp.Expr:
        """
        Parses mathematical expressions safely via Python AST.
        Only whitelisted mathematical functions, operators, and symbols are permitted.
        """
        if not expr_str or not expr_str.strip():
            raise ParseSecurityError("La expresión está vacía.")

        if len(expr_str) > cls.MAX_LENGTH:
            raise ParseSecurityError(
                f"La longitud de la expresión ({len(expr_str)}) excede el límite permitido ({cls.MAX_LENGTH})."
            )

        norm_text = cls.normalize_input(expr_str)

        try:
            tree = ast.parse(norm_text, mode="eval")
        except SyntaxError as e:
            raise ParseSecurityError(f"Error de sintaxis matemática: {e.msg}") from e

        symbols = dict(cls.ALLOWED_SYMBOLS)
        if custom_symbols:
            symbols.update(custom_symbols)

        cls._validate_and_check_depth(tree.body, 1)
        return cls._eval_ast_node(tree.body, symbols)

    @classmethod
    def _validate_and_check_depth(cls, node: ast.AST, depth: int):
        if depth > cls.MAX_DEPTH:
            raise ParseSecurityError("La expresión es demasiado compleja (profundidad anidada excesiva).")

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
            raise ParseSecurityError(f"Elemento no permitido en expresión matemática: {type(node).__name__}")

        for child in ast.iter_child_nodes(node):
            cls._validate_and_check_depth(child, depth + 1)

    @classmethod
    def _eval_ast_node(cls, node: ast.AST, symbols: dict) -> sp.Expr:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return sp.sympify(node.value)
            elif isinstance(node.value, complex):
                return sp.sympify(node.value)
            else:
                raise ParseSecurityError(f"Tipo constante no numérico no permitido: {type(node.value).__name__}")

        elif isinstance(node, ast.Name):
            name = node.id
            if name in symbols:
                return symbols[name]
            elif name in cls.ALLOWED_FUNCS:
                raise ParseSecurityError(f"'{name}' es una función y debe invocarse con paréntesis, ej. {name}(x)")
            else:
                raise ParseSecurityError(f"Símbolo no reconocido o no permitido: '{name}'")

        elif isinstance(node, ast.UnaryOp):
            operand = cls._eval_ast_node(node.operand, symbols)
            if isinstance(node.op, ast.USub):
                return -operand
            elif isinstance(node.op, ast.UAdd):
                return operand
            else:
                raise ParseSecurityError(f"Operador unario no soportado: {type(node.op).__name__}")

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
                # Check for extreme exponent values
                if isinstance(node.right, ast.Constant) and isinstance(node.right.value, (int, float)):
                    if abs(node.right.value) > cls.MAX_POWER:
                        raise ParseSecurityError(
                            f"Exponente {node.right.value} excede el límite máximo de {cls.MAX_POWER}."
                        )
                return left ** right
            else:
                raise ParseSecurityError(f"Operador binario no soportado: {type(node.op).__name__}")

        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ParseSecurityError("Solo se permiten llamadas a funciones directas nombradas.")
            func_name = node.func.id
            if func_name not in cls.ALLOWED_FUNCS:
                raise ParseSecurityError(f"Función no permitida: '{func_name}'")

            sympy_func = cls.ALLOWED_FUNCS[func_name]
            if node.keywords:
                raise ParseSecurityError("Argumentos por clave no permitidos en funciones matemáticas.")

            args = [cls._eval_ast_node(arg, symbols) for arg in node.args]
            return sympy_func(*args)

        else:
            raise ParseSecurityError(f"Nodo AST no soportado: {type(node).__name__}")


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

    # Look for key=value pairs: key=value
    pairs = re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([^,;()]+)", raw)
    for key, val_str in pairs:
        key = key.strip()
        val_str = val_str.strip()
        # Strip unit suffixes
        cleaned_val = re.sub(r"(?i)\s*(?:ev|nm|pm|um|mm|m|s|fs|ps|ns|kg|j)?$", "", val_str).strip()
        try:
            # Try float or int
            if "." in cleaned_val or "e" in cleaned_val.lower():
                params[key] = float(cleaned_val)
            else:
                params[key] = int(cleaned_val)
        except ValueError:
            try:
                # Try sympy expression
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
        raise ValueError("La entrada de matriz está vacía.")

    # Split rows by semicolon
    raw_rows = [r.strip() for r in raw_text.strip().split(";") if r.strip()]
    if not raw_rows:
        raise ValueError("No se encontraron filas válidas en la matriz.")

    matrix_rows = []
    expected_cols = None

    for r_idx, row_str in enumerate(raw_rows):
        tokens = [t.strip() for t in row_str.split(",") if t.strip()]
        if not tokens:
            raise ValueError(f"La fila {r_idx + 1} de la matriz está vacía.")

        if expected_cols is None:
            expected_cols = len(tokens)
        elif len(tokens) != expected_cols:
            raise ValueError(
                f"Fila irregular: la fila {r_idx + 1} tiene {len(tokens)} elementos, pero la fila 1 tiene {expected_cols}."
            )

        row_vals = []
        for val_str in tokens:
            lower_token = val_str.strip().lower()
            if lower_token in ("inf", "-inf", "+inf", "nan", "-nan", "+nan", "oo", "-oo"):
                raise ValueError(f"Elemento de matriz no finito detectado: '{val_str}'")

            # Replace 'i' with 'j' for Python complex
            norm_val = val_str.replace("i", "j")
            try:
                val = complex(norm_val)
            except ValueError as e:
                # Try evaluating as safe math expression
                try:
                    sym_val = SafeASTParser.parse(val_str)
                    val = complex(complex(sym_val.evalf()))
                except Exception:
                    raise ValueError(f"Valor numérico no válido en la matriz: '{val_str}'") from e

            if not np.isfinite(val.real) or not np.isfinite(val.imag):
                raise ValueError(f"Elemento de matriz no finito detectado: '{val_str}'")
            row_vals.append(val)

        matrix_rows.append(row_vals)

    nrows = len(matrix_rows)
    ncols = expected_cols

    if nrows != ncols:
        raise ValueError(
            f"La matriz debe ser cuadrada (N×N), pero tiene dimensiones {nrows}×{ncols}."
        )

    if nrows > max_dim:
        raise ValueError(f"Dimensión de matriz ({nrows}×{ncols}) excede el límite permitido ({max_dim}×{max_dim}).")

    return np.array(matrix_rows, dtype=complex)


def parse_state_vector(raw_text: str, expected_dim: int = None) -> np.ndarray:
    """
    Parses a state vector such as '[1, 0]' or '1, 0' or '1/sqrt(2), 1/sqrt(2)'.
    Normalizes or returns unit vector if valid.
    """
    clean = raw_text.strip()
    # Strip any comments or trailing annotations like '(Estado inicial)' first
    clean = re.sub(r"\(.*?\)", "", clean).strip()

    # Strip enclosing brackets/parentheses
    if clean.startswith("[") and clean.endswith("]"):
        clean = clean[1:-1].strip()
    elif clean.startswith("(") and clean.endswith(")"):
        clean = clean[1:-1].strip()

    # Split by comma or space
    tokens = [t.strip() for t in re.split(r"[,;]+", clean) if t.strip()]
    if not tokens:
        raise ValueError("El vector de estado inicial está vacío.")

    values = []
    for token in tokens:
        # Strip trailing labels, e.g. "(Estado inicial)"
        token_clean = re.sub(r"\(.*?\)", "", token).strip()
        if not token_clean:
            continue
        norm_val = token_clean.replace("i", "j")
        try:
            val = complex(norm_val)
        except ValueError:
            try:
                sym_val = SafeASTParser.parse(token_clean)
                val = complex(sym_val.evalf())
            except Exception as e:
                raise ValueError(f"Componente vectorial no válida: '{token}'") from e

        if not np.isfinite(val.real) or not np.isfinite(val.imag):
            raise ValueError(f"Componente vectorial no finita: '{token}'")
        values.append(val)

    if not values:
        raise ValueError("No se pudieron extraer componentes numéricas del vector de estado.")

    vec = np.array(values, dtype=complex)
    if expected_dim is not None and len(vec) != expected_dim:
        raise ValueError(
            f"Dimensión del vector de estado ({len(vec)}) no coincide con la dimensión del Hamiltoniano ({expected_dim})."
        )

    norm = np.linalg.norm(vec)
    if norm < 1e-15:
        raise ValueError("El vector de estado no puede ser el vector nulo (norma cero).")

    return vec
