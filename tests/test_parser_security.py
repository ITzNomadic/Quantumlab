"""
Comprehensive security and validation tests for SafeASTParser and parameter/matrix parsers.
Addresses QL-001, QL-017, QL-019.
"""
import unittest
import numpy as np
import sympy as sp

from quantumlab_engine.parser import (
    SafeASTParser,
    ParseSecurityError,
    parse_parameters,
    parse_matrix,
    parse_state_vector,
)


class TestSafeASTParser(unittest.TestCase):
    def test_valid_presets_and_expressions(self):
        """All legitimate preset expressions must parse cleanly into valid SymPy expressions."""
        cases = [
            "exp(-x**2 / 2)",
            "sin(pi*x/L)",
            "sqrt(2/L)*sin(n*pi*x/L)",
            "exp(-m*w*x**2 / (2*hbar))",
            "(1/2)*m*w**2*x**2",
            "exp(I*k*x)",
            "0",
            "1",
            "-oo",
            "oo",
            "L/3",
            "sin(x) + cos(x)",
            "sinh(k*x) + cosh(k*x)",
            "abs(x)",
            "ln(x)",
        ]
        for expr in cases:
            with self.subTest(expr=expr):
                parsed = SafeASTParser.parse(expr)
                self.assertIsNotNone(parsed)

    def test_unicode_normalization(self):
        """Mathematical Unicode symbols must normalize correctly."""
        parsed1 = SafeASTParser.parse("ħ * ω")
        parsed2 = SafeASTParser.parse("hbar * w")
        self.assertEqual(parsed1, parsed2)

        parsed_pi = SafeASTParser.parse("π * x")
        self.assertEqual(parsed_pi, sp.pi * SafeASTParser.x)

    def test_reject_arbitrary_python_and_code_execution(self):
        """QL-001: Execution of arbitrary Python, __import__, builtins, or eval must fail."""
        malicious_inputs = [
            '__import__("math").sqrt(9)',
            '__import__("os").system("echo pwned")',
            'open("test.txt", "w")',
            'eval("1 + 1")',
            'exec("x = 1")',
            'sum([1, 2, 3])',
            'globals()',
            'locals()',
            '__builtins__',
            '(lambda y: y*2)(x)',
            '[i for i in range(10)]',
            '{"a": 1}',
            '(1, 2)',
            'x.__class__.__bases__',
            'x[0]',
            'getattr(x, "real")',
        ]
        for attack in malicious_inputs:
            with self.subTest(attack=attack):
                with self.assertRaises(ParseSecurityError):
                    SafeASTParser.parse(attack)

    def test_reject_excessive_length(self):
        """QL-017: Long inputs exceeding MAX_LENGTH must be rejected."""
        long_expr = "x + " * 300 + "x"
        with self.assertRaises(ParseSecurityError) as ctx:
            SafeASTParser.parse(long_expr)
        self.assertIn("excede el límite permitido", str(ctx.exception))

    def test_reject_excessive_depth(self):
        """QL-017: Deeply nested expressions must be rejected."""
        deep_expr = "sin(" * 30 + "x" + ")" * 30
        with self.assertRaises(ParseSecurityError) as ctx:
            SafeASTParser.parse(deep_expr)
        self.assertIn("demasiado compleja", str(ctx.exception))

    def test_reject_extreme_exponent(self):
        """QL-017: Giant exponents that could cause DoS must be rejected."""
        extreme_power = "x**9999999"
        with self.assertRaises(ParseSecurityError) as ctx:
            SafeASTParser.parse(extreme_power)
        self.assertIn("excede el límite máximo", str(ctx.exception))

    def test_parameter_parsing(self):
        """QL-018: Structured parameter parsing."""
        params = parse_parameters("n=6, L=1.0 nm, E=3.2 eV, V0=5.0 eV, a=0.5 nm")
        self.assertEqual(params["n"], 6)
        self.assertAlmostEqual(params["L"], 1.0)
        self.assertAlmostEqual(params["E"], 3.2)
        self.assertAlmostEqual(params["V0"], 5.0)
        self.assertAlmostEqual(params["a"], 0.5)

    def test_matrix_parsing_valid(self):
        """QL-019: Parse valid Hermitian and non-Hermitian square matrices."""
        h_str = "2, 1-1j; 1+1j, 3"
        H = parse_matrix(h_str)
        self.assertEqual(H.shape, (2, 2))
        self.assertEqual(H[0, 0], 2.0 + 0j)
        self.assertEqual(H[0, 1], 1.0 - 1j)
        self.assertEqual(H[1, 0], 1.0 + 1j)
        self.assertEqual(H[1, 1], 3.0 + 0j)

    def test_matrix_parsing_invalid(self):
        """QL-019: Irregular, non-square, empty, or non-finite matrices must fail cleanly."""
        invalid_matrices = [
            ("", "vacía"),
            ("1, 2; 3", "Fila irregular"),
            ("1, 2, 3; 4, 5, 6", "debe ser cuadrada"),
            ("nan, 1; 1, 2", "no finito"),
            ("inf, 1; 1, 2", "no finito"),
            ("invalid, 1; 1, 2", "no válido"),
        ]
        for mat_str, err_snippet in invalid_matrices:
            with self.subTest(mat_str=mat_str):
                with self.assertRaises(ValueError) as ctx:
                    parse_matrix(mat_str)
                self.assertIn(err_snippet, str(ctx.exception))

    def test_state_vector_parsing(self):
        """QL-015: Parse initial state vectors."""
        vec = parse_state_vector("[1, 0] (Estado inicial)", expected_dim=2)
        self.assertEqual(len(vec), 2)
        self.assertEqual(vec[0], 1.0 + 0j)
        self.assertEqual(vec[1], 0.0 + 0j)

        with self.assertRaises(ValueError):
            parse_state_vector("[0, 0]")  # Null vector rejected

        with self.assertRaises(ValueError):
            parse_state_vector("[1, 0, 0]", expected_dim=2)  # Dimension mismatch


if __name__ == "__main__":
    unittest.main()
