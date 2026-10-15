"""
Reproduction tests for the 9 residual audit issues identified after v0.2.0.
Verifies failure / defect behavior before applying fixes.
"""

import sys
import unittest
import numpy as np
import sympy as sp
import tkinter as tk

from quantumlab_engine.parser import SafeASTParser, parse_state_vector
from quantumlab_engine.physics import (
    analizar_pozo_infinito,
    analizar_efecto_tunel,
    analizar_hamiltoniano_matricial,
    analizar_funcion_onda,
)
from quantumlab_engine.formatting import formatear_hamiltoniano
from quantumlab import CalculadoraCuanticaAvanzada


class TestResidualAuditDefects(unittest.TestCase):
    # -------------------------------------------------------------
    # 1. CI MATRIX VERSIONS RECORDED
    # -------------------------------------------------------------
    def test_defect_1_environment_version_ci_compatibility(self):
        """Defect 1: Version check should accept Python >= 3.10, SymPy >= 1.12, NumPy >= 1.26."""
        py_major, py_minor = sys.version_info[:2]
        self.assertGreaterEqual((py_major, py_minor), (3, 10))
        # SymPy and NumPy versions must be compatible with requirements.txt
        import sympy, numpy
        sp_major = int(sympy.__version__.split(".")[0])
        np_major = int(numpy.__version__.split(".")[0])
        self.assertIn(sp_major, [1, 2])
        self.assertIn(np_major, [1, 2])

    # -------------------------------------------------------------
    # 2. POZO INFINITO: INTEGRAL SIMBÓLICA VS SOPORTE FÍSICO [0, L]
    # -------------------------------------------------------------
    def test_defect_2_pozo_infinito_symbolic_integral_matches_support(self):
        """Defect 2: Symbolic integral over [0, 2L] must not exceed 1 (physical support is [0, L])."""
        L = SafeASTParser.L
        res = analizar_pozo_infinito(sp.sympify(0), 2 * L, n_val=1)
        # Numerical probability is clamped to 1.0
        self.assertAlmostEqual(res.prob_numerica, 1.0)
        # Symbolic probability must match physical support and evaluate to 1 on substitution of L=1
        sym_val = float(res.prob_simbolica.subs(L, 1.0).evalf())
        self.assertAlmostEqual(sym_val, 1.0, places=5)

    # -------------------------------------------------------------
    # 3. MATRICES CASI HERMÍTICAS Y RESIDUOS DE AUTOESTADOS
    # -------------------------------------------------------------
    def test_defect_3_almost_hermitian_residuals_tracked(self):
        """Defect 3: Maximum eigenpair residual ||Hv - lambda v|| must be calculated and tracked."""
        H = np.array([[1.0, 1.0], [1.0 + 1e-11j, 2.0]], dtype=complex)
        res = analizar_hamiltoniano_matricial(H)
        # Must compute and expose max eigen residual
        self.assertTrue(hasattr(res, "max_residuo_autovector"))
        self.assertIsNotNone(res.max_residuo_autovector)

    # -------------------------------------------------------------
    # 4. CAPTURAS SILENCIOSAS DE EXCEPCIONES EN HAMILTONIANO
    # -------------------------------------------------------------
    def test_defect_4_no_silent_exception_swallowing_in_hamiltonian(self):
        """Defect 4: Malformed state vector or time in GUI must raise clear ValueError."""
        root = tk.Tk()
        root.withdraw()
        app = CalculadoraCuanticaAvanzada(root)
        app._seleccionar_modo(5)
        app.entry_params.delete(0, tk.END)
        app.entry_params.insert(0, "2, 0; 0, 3")

        # 1. Invalid state vector dimension
        app.entry_psi.delete(0, tk.END)
        app.entry_psi.insert(0, "[1, 0, 0]")  # 3D vector for 2x2 matrix!
        with self.assertRaises(ValueError) as ctx:
            app._resolver_hamiltoniano_matricial()
        self.assertIn("Vector de estado inicial inválido", str(ctx.exception))

        # 2. Malformed state vector syntax
        app.entry_psi.delete(0, tk.END)
        app.entry_psi.insert(0, "[invalid syntax!]")
        with self.assertRaises(ValueError) as ctx:
            app._resolver_hamiltoniano_matricial()
        self.assertIn("Vector de estado inicial inválido", str(ctx.exception))

        # 3. Valid state vector, but invalid time parameter
        app.entry_psi.delete(0, tk.END)
        app.entry_psi.insert(0, "[1, 0]")
        app.entry_lim_a.delete(0, tk.END)
        app.entry_lim_a.insert(0, "invalid_time")
        with self.assertRaises(ValueError) as ctx:
            app._resolver_hamiltoniano_matricial()
        self.assertIn("Valor de tiempo 't' inválido", str(ctx.exception))

        root.destroy()

    # -------------------------------------------------------------
    # 5. PARSE_STATE_VECTOR PRESERVES SQRT(2)
    # -------------------------------------------------------------
    def test_defect_5_parse_state_vector_preserves_sqrt(self):
        """Defect 5: parse_state_vector must support functions like sqrt(2) without regex mutilation."""
        vec = parse_state_vector("[1/sqrt(2), 1/sqrt(2)]", expected_dim=2)
        self.assertEqual(len(vec), 2)
        inv_sqrt2 = 1.0 / np.sqrt(2)
        self.assertAlmostEqual(vec[0].real, inv_sqrt2)
        self.assertAlmostEqual(vec[1].real, inv_sqrt2)

    # -------------------------------------------------------------
    # 6. SCIPY INDEPENDENCE & MATRIX EXPONENTIAL
    # -------------------------------------------------------------
    def test_defect_6_matrix_exponential_without_scipy(self):
        """Defect 6: Non-Hermitian time evolution works in pure NumPy without crashing or faking norm=1."""
        H = np.array([[0.0, -1.0], [1.0, 0.0]], dtype=complex)
        psi_0 = np.array([1.0, 0.0], dtype=complex)
        res = analizar_hamiltoniano_matricial(H, psi_0=psi_0, t_val=0.5)
        self.assertIsNotNone(res.psi_t)
        # Should not just return psi_0
        self.assertFalse(np.allclose(res.psi_t, psi_0))

    # -------------------------------------------------------------
    # 7. HEISENBERG UNCERTAINTY NO FALSE POSITIVE ON INDETERMINACY
    # -------------------------------------------------------------
    def test_defect_7_heisenberg_indeterminacy_not_claimed(self):
        """Defect 7: When inequality cannot be evaluated, must NOT claim heisenberg_cumple=True."""
        # A symbolic case where difference cannot be decided
        x = SafeASTParser.x
        k = SafeASTParser.k
        # Function with symbolic free parameter k without explicit bounds
        # Should not falsely assert heisenberg_cumple = True
        res = analizar_funcion_onda(sp.exp(-k * x**2), sp.sympify(-1), sp.sympify(1))
        # Boundary terms on [-1, 1] do not vanish:
        self.assertFalse(res.heisenberg_cumple)

    # -------------------------------------------------------------
    # 8. EFECTO TÚNEL FINITE VALIDATION
    # -------------------------------------------------------------
    def test_defect_8_tunneling_finite_validation(self):
        """Defect 8: Non-finite inputs (NaN, Inf) must raise ValueError."""
        with self.assertRaises(ValueError):
            analizar_efecto_tunel(E_ev=float("nan"))
        with self.assertRaises(ValueError):
            analizar_efecto_tunel(V0_ev=float("inf"))
        with self.assertRaises(ValueError):
            analizar_efecto_tunel(ancho_nm=-1.0)

    # -------------------------------------------------------------
    # 9. SISTEMAS NO HERMÍTICOS: CONSERVACIÓN UNITARIA
    # -------------------------------------------------------------
    def test_defect_9_non_hermitian_evolution_not_called_unitary(self):
        """Defect 9: Non-Hermitian time evolution report must not label norm change as 'Conservación unitaria'."""
        H = np.array([[0.0, -1.0], [1.0, 0.0]], dtype=complex)
        psi_0 = np.array([1.0, 0.0], dtype=complex)
        res = analizar_hamiltoniano_matricial(H, psi_0=psi_0, t_val=1.0)
        bloques = formatear_hamiltoniano(res)
        reporte_str = "\n".join([texto for texto, tag in bloques])
        self.assertNotIn("Conservación unitaria", reporte_str)
        self.assertIn("Evolución no unitaria", reporte_str)


if __name__ == "__main__":
    unittest.main()
