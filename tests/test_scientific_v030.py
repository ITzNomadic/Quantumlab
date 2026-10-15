"""
Automated unit tests for QuantumLab v0.3.0 scientific improvements and parser safety:
  1. Infinite potential well length parameter L (validation L > 0, scaling En ~ 1/L^2, domain probability).
  2. Strict non-fractional quantum number validation (no silent int() truncation).
  3. AST parser safety limits: nested power rejection, integer digit limits (>100 digits), AST node limits (>100 nodes).
  4. Rapid asymptotic divergence checks on infinite domains.
"""

import unittest
import sympy as sp
import numpy as np

from quantumlab_engine.physics import (
    analizar_pozo_infinito,
    analizar_oscilador_armonico,
    analizar_funcion_onda,
)
from quantumlab_engine.parser import (
    SafeASTParser,
    ParseSecurityError,
    parse_parameters,
)


class TestScientificV030(unittest.TestCase):
    def test_infinite_well_L_parameter_energy_scaling(self):
        """Verify that L parameter scales the energy eigenvalues En = n^2 * pi^2 * hbar^2 / (2 * m * L^2)."""
        hbar = SafeASTParser.hbar
        m = SafeASTParser.m

        # L = 1.0
        res1 = analizar_pozo_infinito(sp.sympify("0"), sp.sympify("1"), n_val=1, L_val=1.0)
        e1_expected = (1**2 * sp.pi**2 * hbar**2) / (2 * m * 1.0**2)
        self.assertEqual(sp.simplify(res1.energia_n - e1_expected), 0)

        # L = 2.0 (energy should be 1/4 of L=1)
        res2 = analizar_pozo_infinito(sp.sympify("0"), sp.sympify("2"), n_val=1, L_val=2.0)
        e2_expected = (1**2 * sp.pi**2 * hbar**2) / (2 * m * 2.0**2)
        self.assertEqual(sp.simplify(res2.energia_n - e2_expected), 0)
        ratio = float(sp.simplify(res1.energia_n / res2.energia_n).evalf())
        self.assertAlmostEqual(ratio, 4.0, places=5)

    def test_infinite_well_L_parameter_probability_support(self):
        """Verify that probability in half the box [0, L/2] is exactly 50% for any positive L."""
        for L_test in [0.5, 1.0, 2.0, 5.0]:
            half_L = sp.Float(L_test / 2.0)
            res = analizar_pozo_infinito(sp.sympify("0"), half_L, n_val=1, L_val=L_test)
            self.assertAlmostEqual(res.prob_numerica, 0.50, places=5)

    def test_infinite_well_invalid_L_rejected(self):
        """L <= 0 must be rejected with ValueError."""
        for bad_L in [0.0, -1.0, -0.5]:
            with self.assertRaises(ValueError):
                analizar_pozo_infinito(sp.sympify("0"), sp.sympify("1"), n_val=1, L_val=bad_L)

    def test_quantum_number_fractional_rejected_in_well(self):
        """Fractional quantum number n in infinite well must raise ValueError (no silent int truncation)."""
        for bad_n in [1.5, 2.7, 0.5, 3.14]:
            with self.assertRaises(ValueError):
                analizar_pozo_infinito(sp.sympify("0"), sp.sympify("1"), n_val=bad_n)

    def test_quantum_number_fractional_rejected_in_harmonic_oscillator(self):
        """Fractional quantum number n in harmonic oscillator must raise ValueError."""
        for bad_n in [0.5, 1.2, 3.99]:
            with self.assertRaises(ValueError):
                analizar_oscilador_armonico(n_val=bad_n)

    def test_parameter_parsing_fractional_n_rejected(self):
        """parse_parameters must reject fractional n such as 'n=1.5' instead of truncating to 1."""
        with self.assertRaises(ValueError):
            parse_parameters("n=1.5, L=1.0 nm")

        with self.assertRaises(ValueError):
            parse_parameters("n=2.33")

        # Integer float like 2.0 should be parsed cleanly as int 2
        params = parse_parameters("n=2.0, L=2.0")
        self.assertEqual(params["n"], 2)
        self.assertIsInstance(params["n"], int)
        self.assertEqual(params["L"], 2.0)

    def test_ast_parser_rejects_nested_powers(self):
        """AST parser must reject nested power expressions (e.g. x**y**z or (x**2)**3)."""
        nested_exprs = [
            "x**2**3",
            "2**3**4",
            "(x**2)**3",
        ]
        for expr in nested_exprs:
            with self.assertRaises(ParseSecurityError):
                SafeASTParser.parse(expr)

    def test_ast_parser_rejects_large_integer_digits(self):
        """AST parser must reject integers with > 100 digits."""
        huge_int = "9" * 105
        with self.assertRaises(ParseSecurityError):
            SafeASTParser.parse(huge_int)

        # 50 digits is allowed
        allowed_int = "1" + "0" * 20
        sym = SafeASTParser.parse(allowed_int)
        self.assertIsNotNone(sym)

    def test_ast_parser_rejects_excessive_nodes(self):
        """AST parser must reject expressions exceeding MAX_NODES (100)."""
        # Build an expression with 120 additions: x + x + x + ...
        huge_chain = " + ".join(["x"] * 120)
        with self.assertRaises(ParseSecurityError):
            SafeASTParser.parse(huge_chain)

    def test_rapid_asymptotic_divergence_check(self):
        """Functions diverging to infinity at boundaries must fail cleanly without hanging."""
        x = SafeASTParser.x
        unbounded_psi = sp.exp(x)
        # exp(x) on [0, oo] diverges as x -> +oo
        with self.assertRaises(ValueError) as ctx:
            analizar_funcion_onda(unbounded_psi, sp.sympify("0"), sp.oo)
        self.assertIn("diverge hacia infinito", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
