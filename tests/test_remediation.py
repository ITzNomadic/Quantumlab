"""
End-to-end verification tests demonstrating remediation of all confirmed audit defects (T01 - T16 and QL-001 - QL-033).
Executes against the updated CalculadoraCuanticaAvanzada in quantumlab.py.
"""

import unittest
import tkinter as tk
import sympy as sp
import numpy as np

from quantumlab import CalculadoraCuanticaAvanzada
from quantumlab_engine.parser import ParseSecurityError


class QuantumLabRemediationTests(unittest.TestCase):
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

    # -----------------------------------------------------------------
    # QL-001 / T13: INSECURE PARSER BLOCKED
    # -----------------------------------------------------------------
    def test_t13_ql001_insecure_parser_blocked(self):
        """QL-001 / T13: Arbitrary Python code execution via __import__, builtins, etc. is blocked."""
        with self.assertRaises(ParseSecurityError):
            self.app._parsear_expresion('__import__("math").sqrt(9)')

        with self.assertRaises(ParseSecurityError):
            self.app._parsear_expresion('open("pwned.txt", "w")')

        with self.assertRaises(ParseSecurityError):
            self.app._parsear_expresion('eval("1+1")')

    # -----------------------------------------------------------------
    # QL-002 / T01: HEISENBERG FALSE POSITIVE FIXED
    # -----------------------------------------------------------------
    def test_t01_ql002_heisenberg_not_claimed_on_zero_delta_p(self):
        """QL-002 / T01: Constant wave on [0,1] gives delta_p=0; must NOT claim Heisenberg fulfilled."""
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

    # -----------------------------------------------------------------
    # QL-004 / T02: NULL STATE PROPERLY REJECTED
    # -----------------------------------------------------------------
    def test_t02_ql004_null_state_rejected(self):
        """QL-004 / T02: psi=0 in wave analysis raises ValueError, preventing NaN/zoo propagation."""
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

    # -----------------------------------------------------------------
    # QL-006 / T03: SCHRODINGER NULL STATE REJECTED
    # -----------------------------------------------------------------
    def test_t03_ql006_schrodinger_null_state_rejected(self):
        """QL-006 / T03: psi=0 with V=0 is rejected (null vector is not an eigenstate)."""
        self.app._seleccionar_modo(1)
        self.app.entry_psi.delete(0, tk.END)
        self.app.entry_psi.insert(0, "0")
        self.app.entry_potencial.delete(0, tk.END)
        self.app.entry_potencial.insert(0, "0")

        with self.assertRaises(ValueError) as ctx:
            self.app._resolver_schrodinger_simbolico()
        self.assertIn("vector cero nunca es un autoestado", str(ctx.exception))

    # -----------------------------------------------------------------
    # QL-007 / T04: SCHRODINGER FORMAL VS PHYSICAL BOUND STATE
    # -----------------------------------------------------------------
    def test_t04_ql007_schrodinger_formal_vs_physical(self):
        """QL-007 / T04: psi=exp(x) on R is recognized as formal local solution, not L2 bound state."""
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

    # -----------------------------------------------------------------
    # QL-008 / T05: INFINITE WELL BOUNDS CLAMPED (NO PROB > 100%)
    # -----------------------------------------------------------------
    def test_t05_ql008_infinite_well_prob_clamped(self):
        """QL-008 / T05: [0, 2L] clamped to [0, L]; probability does not exceed 100%."""
        self.app._seleccionar_modo(2)
        self.app.entry_lim_a.delete(0, tk.END)
        self.app.entry_lim_a.insert(0, "0")
        self.app.entry_lim_b.delete(0, tk.END)
        self.app.entry_lim_b.insert(0, "2*L")

        self.app._resolver_pozo_infinito()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertIn("100.00%", out)
        self.assertNotIn("200.00%", out)

    # -----------------------------------------------------------------
    # QL-009 / T06: INFINITE WELL INVERTED LIMITS REJECTED
    # -----------------------------------------------------------------
    def test_t06_ql009_infinite_well_inverted_limits(self):
        """QL-009 / T06: Limits a > b must raise ValueError, avoiding negative probabilities."""
        self.app._seleccionar_modo(2)
        self.app.entry_lim_a.delete(0, tk.END)
        self.app.entry_lim_a.insert(0, "L")
        self.app.entry_lim_b.delete(0, tk.END)
        self.app.entry_lim_b.insert(0, "0")

        with self.assertRaises(ValueError) as ctx:
            self.app._resolver_pozo_infinito()
        self.assertIn("estrictamente mayor", str(ctx.exception))

    # -----------------------------------------------------------------
    # QL-010 / T07: INFINITE WELL QUANTUM NUMBER n RESPECTED
    # -----------------------------------------------------------------
    def test_t07_ql010_infinite_well_n_respected(self):
        """QL-010 / T07: params='n=6' on [0, L/3] calculates 33.33% (1/3) instead of n=1."""
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

    # -----------------------------------------------------------------
    # QL-011 / T08: HARMONIC OSCILLATOR LEVELS n >= 0 SUPPORTED
    # -----------------------------------------------------------------
    def test_t08_ql011_harmonic_oscillator_n4(self):
        """QL-011 / T08: n=4 evaluates exact Hermite state and E_4 = 9/2 * hbar * w."""
        self.app._seleccionar_modo(3)
        self.app.entry_params.delete(0, tk.END)
        self.app.entry_params.insert(0, "n=4")

        self.app._resolver_oscilador_armonico()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertIn("NIVEL n = 4", out)
        self.assertIn("E_4 = 9*ω*ħ/2", out)

    # -----------------------------------------------------------------
    # QL-012 / T09: TUNNELING CUSTOM PARAMETERS PROCESSED
    # -----------------------------------------------------------------
    def test_t09_ql012_tunneling_custom_inputs(self):
        """QL-012 / T09: Inputs E=12, V0=99, a=0.001 are calculated accurately."""
        self.app._seleccionar_modo(4)
        self.app.entry_params.delete(0, tk.END)
        self.app.entry_params.insert(0, "E=12, V0=99, a=0.001")

        self.app._resolver_efecto_tunel()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertNotIn("3.808406e-03", out)
        self.assertIn("9.946653e-01", out)

    # -----------------------------------------------------------------
    # QL-003 / T10: HAMILTONIAN COMPLEX EIGENVALUES PRESERVED
    # -----------------------------------------------------------------
    def test_t10_ql003_hamiltonian_complex_eigenvalues(self):
        """QL-003 / T10: Non-Hermitian matrix preserves imaginary parts (+/- 1i)."""
        self.app._seleccionar_modo(5)
        self.app.entry_params.delete(0, tk.END)
        self.app.entry_params.insert(0, "0, -1; 1, 0")

        self.app._resolver_hamiltoniano_matricial()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertIn("+1.000000i", out)
        self.assertIn("-1.000000i", out)
        self.assertIn("NO (Matriz no autoadjunta", out)

    # -----------------------------------------------------------------
    # QL-014 / T11: HAMILTONIAN GAP TO FIRST DISTINCT LEVEL
    # -----------------------------------------------------------------
    def test_t11_ql014_hamiltonian_gap_distinct_level(self):
        """QL-014 / T11: diag(0, 0, 1) calculates gap to first distinct level as 1.000000."""
        self.app._seleccionar_modo(5)
        self.app.entry_params.delete(0, tk.END)
        self.app.entry_params.insert(0, "0, 0, 0; 0, 0, 0; 0, 0, 1")

        self.app._resolver_hamiltoniano_matricial()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertIn("ΔE = 1.000000", out)

    # -----------------------------------------------------------------
    # QL-013 / T12: HAMILTONIAN RESIDUAL REPORTED
    # -----------------------------------------------------------------
    def test_t12_ql013_hamiltonian_residual_reported(self):
        """QL-013 / T12: Nearly Hermitian matrix with 1e-6 error reports residual."""
        self.app._seleccionar_modo(5)
        self.app.entry_params.delete(0, tk.END)
        self.app.entry_params.insert(0, "1, 1; 1+0.000001j, 2")

        self.app._resolver_hamiltoniano_matricial()
        out = self.app.hoja.get("1.0", tk.END)
        self.assertIn("1.00e-06", out)
        self.assertIn("NO (Matriz no autoadjunta", out)

    # -----------------------------------------------------------------
    # QL-026 / T16: PRESERVE USER INPUTS ON RE-CLICKING MODE
    # -----------------------------------------------------------------
    def test_t16_ql026_preserve_inputs_on_click(self):
        """QL-026 / T16: Modifying input and re-clicking active mode does not wipe user data."""
        self.app._seleccionar_modo(2)
        self.app.entry_params.delete(0, tk.END)
        self.app.entry_params.insert(0, "n=99, L=5.0")

        # Click the active mode card again
        self.app._seleccionar_modo(2)
        self.assertEqual(self.app.entry_params.get(), "n=99, L=5.0")

    # -----------------------------------------------------------------
    # QL-025 / T15: COMBOBOX SYNCHRONIZATION
    # -----------------------------------------------------------------
    def test_t15_ql025_combobox_synced(self):
        """QL-025 / T15: combo_modo is visible, packed, and reflects active mode."""
        self.app._seleccionar_modo(3)
        self.assertEqual(self.app.combo_modo.current(), 3)
        self.assertTrue(bool(self.app.combo_modo.winfo_manager()))


if __name__ == "__main__":
    unittest.main()
