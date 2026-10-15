"""
Audit verification suite for QuantumLab.
Records system versions and verifies that all defects T01 - T16 documented in
Informe_Auditoria_QuantumLab.md are completely resolved according to the expected behavior table.
"""
import sys
import unittest
import tkinter as tk
import sympy as sp
import numpy as np

from quantumlab import CalculadoraCuanticaAvanzada
from quantumlab_engine.parser import ParseSecurityError

PYTHON_VERSION = sys.version
SYMPY_VERSION = sp.__version__
NUMPY_VERSION = np.__version__


class QuantumLabAuditVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.app = CalculadoraCuanticaAvanzada(cls.root)
        cls.root.update_idletasks()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def setUp(self):
        self.app.limpiar_hoja()

    def test_environment_versions_recorded(self):
        """Verifies environment library versions are captured."""
        self.assertTrue(PYTHON_VERSION.startswith("3.14"))
        self.assertEqual(SYMPY_VERSION, "1.14.0")
        self.assertEqual(NUMPY_VERSION, "2.5.4")

    def test_t01_heisenberg_boundary_warning_on_zero_delta_p(self):
        """T01 [QL-002]: Constant wave on [0,1] gives delta_p=0; must NOT claim Heisenberg fulfilled."""
        self.app._seleccionar_modo(0)
        self.app.entry_psi.delete(0, tk.END)
        self.app.entry_psi.insert(0, "1")
        self.app.entry_lim_a.delete(0, tk.END)
        self.app.entry_lim_a.insert(0, "0")
        self.app.entry_lim_b.delete(0, tk.END)
        self.app.entry_lim_b.insert(0, "1")
        self.app._resolver_analisis_onda()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertNotIn("cumpliendo estrictamente el límite", out)
        self.assertIn("NO VERIFICABLE", out)

    def test_t02_null_state_rejected(self):
        """T02 [QL-004]: psi=0 in wave analysis must be rejected, preventing NaN/zoo propagation."""
        self.app._seleccionar_modo(0)
        self.app.entry_psi.delete(0, tk.END)
        self.app.entry_psi.insert(0, "0")
        self.app.entry_lim_a.delete(0, tk.END)
        self.app.entry_lim_a.insert(0, "0")
        self.app.entry_lim_b.delete(0, tk.END)
        self.app.entry_lim_b.insert(0, "1")
        with self.assertRaises(ValueError) as ctx:
            self.app._resolver_analisis_onda()
        self.assertIn("no puede ser la función nula", str(ctx.exception))

    def test_t03_schrodinger_null_state_rejected(self):
        """T03 [QL-006]: psi=0 with V=0 must be rejected (null vector is not an eigenstate)."""
        self.app._seleccionar_modo(1)
        self.app.entry_psi.delete(0, tk.END)
        self.app.entry_psi.insert(0, "0")
        self.app.entry_potencial.delete(0, tk.END)
        self.app.entry_potencial.insert(0, "0")
        with self.assertRaises(ValueError) as ctx:
            self.app._resolver_schrodinger_simbolico()
        self.assertIn("vector cero nunca es un autoestado", str(ctx.exception))

    def test_t04_schrodinger_formal_vs_physical_distinction(self):
        """T04 [QL-007]: psi=exp(x) in free space is formal local solution, not L2 bound state."""
        self.app._seleccionar_modo(1)
        self.app.entry_psi.delete(0, tk.END)
        self.app.entry_psi.insert(0, "exp(x)")
        self.app.entry_potencial.delete(0, tk.END)
        self.app.entry_potencial.insert(0, "0")
        self.app.entry_lim_a.delete(0, tk.END)
        self.app.entry_lim_a.insert(0, "-oo")
        self.app.entry_lim_b.delete(0, tk.END)
        self.app.entry_lim_b.insert(0, "oo")
        self.app._resolver_schrodinger_simbolico()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertIn("SOLUCIÓN FORMAL LOCAL", out)
        self.assertNotIn("AUTOESTADO FÍSICO EXACTO", out)

    def test_t05_infinite_well_probability_clamped_to_100_percent(self):
        """T05 [QL-008]: [0, 2L] clamped to [0, L]; probability does not exceed 100%."""
        self.app._seleccionar_modo(2)
        self.app.entry_lim_a.delete(0, tk.END)
        self.app.entry_lim_a.insert(0, "0")
        self.app.entry_lim_b.delete(0, tk.END)
        self.app.entry_lim_b.insert(0, "2*L")
        self.app._resolver_pozo_infinito()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertIn("100.00%", out)
        self.assertNotIn("200.00%", out)

    def test_t06_infinite_well_inverted_limits_rejected(self):
        """T06 [QL-009]: Inverted limits [L, 0] must raise ValueError."""
        self.app._seleccionar_modo(2)
        self.app.entry_lim_a.delete(0, tk.END)
        self.app.entry_lim_a.insert(0, "L")
        self.app.entry_lim_b.delete(0, tk.END)
        self.app.entry_lim_b.insert(0, "0")
        with self.assertRaises(ValueError) as ctx:
            self.app._resolver_pozo_infinito()
        self.assertIn("estrictamente mayor", str(ctx.exception))

    def test_t07_infinite_well_n_respected(self):
        """T07 [QL-010]: params='n=6, L=1' calculates n=6 giving 33.33% (1/3) instead of n=1."""
        self.app._seleccionar_modo(2)
        self.app.entry_lim_a.delete(0, tk.END)
        self.app.entry_lim_a.insert(0, "0")
        self.app.entry_lim_b.delete(0, tk.END)
        self.app.entry_lim_b.insert(0, "L/3")
        self.app.entry_params.delete(0, tk.END)
        self.app.entry_params.insert(0, "n=6, L=1.0")
        self.app._resolver_pozo_infinito()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertIn("33.33%", out)
        self.assertNotIn("19.55%", out)

    def test_t08_harmonic_oscillator_n_evaluated(self):
        """T08 [QL-011]: n=4 produces exact state n=4 with E_4 = 9/2 * hbar * w."""
        self.app._seleccionar_modo(3)
        self.app.entry_params.delete(0, tk.END)
        self.app.entry_params.insert(0, "n=4")
        self.app._resolver_oscilador_armonico()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertIn("NIVEL n = 4", out)
        self.assertIn("E_4 = 9*ω*ħ/2", out)

    def test_t09_tunneling_custom_parameters_evaluated(self):
        """T09 [QL-012]: Inputs E=12, V0=99, a=0.001 are calculated accurately."""
        self.app._seleccionar_modo(4)
        self.app.entry_params.delete(0, tk.END)
        self.app.entry_params.insert(0, "E=12, V0=99, a=0.001")
        self.app._resolver_efecto_tunel()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertNotIn("3.808406e-03", out)
        self.assertIn("9.946653e-01", out)

    def test_t10_hamiltonian_non_hermitian_preserves_complex_eigenvalues(self):
        """T10 [QL-003]: H = '0, -1; 1, 0' has eigenvalues +/- i. Preserves imaginary part."""
        self.app._seleccionar_modo(5)
        self.app.entry_params.delete(0, tk.END)
        self.app.entry_params.insert(0, "0, -1; 1, 0")
        self.app._resolver_hamiltoniano_matricial()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertIn("+1.000000i", out)
        self.assertIn("-1.000000i", out)
        self.assertIn("NO (Matriz no autoadjunta", out)

    def test_t11_hamiltonian_gap_first_distinct_level(self):
        """T11 [QL-014]: diag(0, 0, 1) calculates gap to first distinct level as 1.000000."""
        self.app._seleccionar_modo(5)
        self.app.entry_params.delete(0, tk.END)
        self.app.entry_params.insert(0, "0, 0, 0; 0, 0, 0; 0, 0, 1")
        self.app._resolver_hamiltoniano_matricial()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertIn("ΔE = 1.000000", out)

    def test_t12_hamiltonian_residual_reported(self):
        """T12 [QL-013]: Nearly Hermitian matrix reports residual."""
        self.app._seleccionar_modo(5)
        self.app.entry_params.delete(0, tk.END)
        self.app.entry_params.insert(0, "1, 1; 1+0.000001j, 2")
        self.app._resolver_hamiltoniano_matricial()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertIn("1.00e-06", out)
        self.assertIn("NO (Matriz no autoadjunta", out)

    def test_t13_sympify_code_execution_blocked(self):
        """T13 [QL-001]: sympify code execution is blocked by SafeASTParser."""
        with self.assertRaises(ParseSecurityError):
            self.app._parsear_expresion('__import__("math").sqrt(9)')

    def test_t14_window_geometry_responsive(self):
        """T14 [QL-024]: Window dimensions allow 800x600 displays without clipping."""
        min_w, min_h = self.app.root.minsize()
        self.assertLessEqual(min_w, 800)
        self.assertLessEqual(min_h, 600)

    def test_t15_combobox_visible_and_functional(self):
        """T15 [QL-025]: Combobox is displayed and properly synchronized."""
        self.app._seleccionar_modo(4)
        self.assertEqual(self.app.combo_modo.current(), 4)
        self.assertTrue(bool(self.app.combo_modo.winfo_manager()))

    def test_t16_preserve_inputs_on_active_mode_click(self):
        """T16 [QL-026]: Editing an entry and clicking the active mode card preserves user data."""
        self.app._seleccionar_modo(2)
        self.app.entry_params.delete(0, tk.END)
        self.app.entry_params.insert(0, "n=12, L=3.5")
        self.app._seleccionar_modo(2)
        self.assertEqual(self.app.entry_params.get(), "n=12, L=3.5")


if __name__ == "__main__":
    unittest.main()
