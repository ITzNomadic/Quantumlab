"""
Comprehensive physical validation and scientific invariance tests for QuantumLab.
Covers findings QL-002 through QL-015, QL-020, QL-021, QL-022, QL-023, QL-031, QL-032.
"""
import unittest
import numpy as np
import sympy as sp

from quantumlab_engine.parser import SafeASTParser
from quantumlab_engine.physics import (
    analizar_funcion_onda,
    analizar_schrodinger_1d,
    analizar_pozo_infinito,
    analizar_oscilador_armonico,
    analizar_efecto_tunel,
    analizar_hamiltoniano_matricial,
    evolucion_temporal_matricial,
)


class TestPhysicsEngine(unittest.TestCase):
    def setUp(self):
        self.x = SafeASTParser.x
        self.hbar = SafeASTParser.hbar
        self.m = SafeASTParser.m
        self.w = SafeASTParser.w
        self.L = SafeASTParser.L

    # -------------------------------------------------------------
    # 1. FUNCIÓN DE ONDA Y HEISENBERG (QL-002, QL-004, QL-005)
    # -------------------------------------------------------------
    def test_wave_null_state_rejected(self):
        """QL-004 / T02: psi=0 must raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            analizar_funcion_onda(sp.sympify(0), sp.sympify(0), sp.sympify(1))
        self.assertIn("no puede ser la función nula", str(ctx.exception))

    def test_wave_constant_finite_interval_heisenberg_not_claimed(self):
        """QL-002 / T01: psi=1 in [0, 1] gives delta_p=0; must NOT claim Heisenberg fulfilled."""
        res = analizar_funcion_onda(sp.sympify(1), sp.sympify(0), sp.sympify(1))
        self.assertEqual(res.delta_p, 0)
        self.assertFalse(res.heisenberg_cumple)
        self.assertIn("NO VERIFICABLE", res.heisenberg_nota)

    def test_wave_gaussian_satisfies_heisenberg_minimum(self):
        """Gaussian state exp(-x**2/2) in [-oo, oo] satisfies Delta_x * Delta_p = hbar/2."""
        psi = sp.exp(-self.x**2 / 2)
        res = analizar_funcion_onda(psi, -sp.oo, sp.oo)
        self.assertTrue(res.heisenberg_cumple)
        # Delta x * Delta p == hbar / 2
        diff = sp.simplify(res.delta_x_delta_p - self.hbar / 2)
        self.assertEqual(diff, 0)

    # -------------------------------------------------------------
    # 2. SCHRÖDINGER 1D (QL-006, QL-007, QL-021)
    # -------------------------------------------------------------
    def test_schrodinger_null_state_rejected(self):
        """QL-006 / T03: psi=0 with V=0 must raise ValueError (null vector is not an eigenstate)."""
        with self.assertRaises(ValueError) as ctx:
            analizar_schrodinger_1d(sp.sympify(0), sp.sympify(0))
        self.assertIn("vector cero nunca es un autoestado", str(ctx.exception))

    def test_schrodinger_formal_vs_physical_admissibility(self):
        """QL-007 / T04: psi=exp(x) in free space is formal local solution, not L2 bound state."""
        psi = sp.exp(self.x)
        V = sp.sympify(0)
        res = analizar_schrodinger_1d(psi, V, a=-sp.oo, b=sp.oo)
        self.assertTrue(res.es_autoestado_formal)
        self.assertFalse(res.es_estado_fisico_ligado)
        self.assertIn("SOLUCIÓN FORMAL LOCAL", res.mensaje_interpretacion)

    def test_schrodinger_valid_eigenstate(self):
        """Box eigenstate sin(pi*x/L) with V=0 in [0, L] is physically admissible."""
        psi = sp.sin(sp.pi * self.x / self.L)
        V = sp.sympify(0)
        res = analizar_schrodinger_1d(psi, V, a=sp.sympify(0), b=self.L)
        self.assertTrue(res.es_autoestado_formal)
        self.assertTrue(res.es_estado_fisico_ligado)
        self.assertIn("AUTOESTADO FÍSICO EXACTO", res.mensaje_interpretacion)

    def test_schrodinger_non_eigenstate_no_unproved_superposition(self):
        """QL-021: E(x) depending on x does not claim discrete level superposition without proof."""
        psi = self.x**2
        V = sp.sympify(0)
        res = analizar_schrodinger_1d(psi, V)
        self.assertFalse(res.es_autoestado_formal)
        self.assertIn("NO ES UNA FUNCIÓN PROPIA", res.mensaje_interpretacion)
        self.assertIn("No se puede deducir sin análisis espectral formal", res.mensaje_interpretacion)

    # -------------------------------------------------------------
    # 3. POZO INFINITO (QL-008, QL-009, QL-010)
    # -------------------------------------------------------------
    def test_infinite_well_probability_clamped_to_100_percent(self):
        """QL-008 / T05: [0, 2L] must not exceed 100%."""
        res = analizar_pozo_infinito(sp.sympify(0), 2 * self.L, n_val=1)
        self.assertAlmostEqual(res.prob_numerica, 1.0)
        self.assertIn("ACUMULACIÓN FÍSICA", res.nota_dominio)

    def test_infinite_well_inverted_limits_rejected(self):
        """QL-009 / T06: a > b must raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            analizar_pozo_infinito(self.L, sp.sympify(0), n_val=1)
        self.assertIn("estrictamente mayor", str(ctx.exception))

    def test_infinite_well_n_respected_analytic(self):
        """QL-010 / T07: n=6 on [0, L/3] must give exact probability 1/3 (33.33%)."""
        res = analizar_pozo_infinito(sp.sympify(0), self.L / 3, n_val=6)
        self.assertAlmostEqual(res.prob_numerica, 1.0 / 3.0, places=4)

    # -------------------------------------------------------------
    # 4. OSCILADOR ARMÓNICO (QL-011)
    # -------------------------------------------------------------
    def test_harmonic_oscillator_n_levels(self):
        """QL-011 / T08: n=0, 1, 2, 4 must calculate exact Hermite wave functions and eigenvalues."""
        for n in (0, 1, 2, 4):
            with self.subTest(n=n):
                res = analizar_oscilador_armonico(n_val=n)
                self.assertTrue(res.residuo_cero)
                expected_E = self.hbar * self.w * (n + sp.Rational(1, 2))
                self.assertEqual(sp.simplify(res.energia_n - expected_E), 0)

    def test_harmonic_oscillator_orthonormality(self):
        """Verify <psi_0 | psi_1> = 0 and <psi_0 | psi_0> = 1."""
        res0 = analizar_oscilador_armonico(n_val=0)
        res1 = analizar_oscilador_armonico(n_val=1)
        # Substitutions for numeric integration
        subs = {self.hbar: 1.0, self.m: 1.0, self.w: 1.0}
        psi0_sub = res0.psi_n.subs(subs)
        psi1_sub = res1.psi_n.subs(subs)

        norm0 = sp.integrate(psi0_sub**2, (self.x, -sp.oo, sp.oo))
        overlap = sp.integrate(psi0_sub * psi1_sub, (self.x, -sp.oo, sp.oo))
        self.assertAlmostEqual(float(norm0.evalf()), 1.0, places=5)
        self.assertAlmostEqual(float(overlap.evalf()), 0.0, places=5)

    # -------------------------------------------------------------
    # 5. EFECTO TÚNEL (QL-012, QL-022, QL-031)
    # -------------------------------------------------------------
    def test_tunneling_custom_parameters(self):
        """QL-012 / T09: Inputs E=12, V0=99, a=0.001 must not give default T."""
        res = analizar_efecto_tunel(E_ev=12.0, V0_ev=99.0, ancho_nm=0.001)
        self.assertNotAlmostEqual(res.T, 3.808406e-3)
        self.assertGreater(res.T, 0.0)
        self.assertLess(res.T, 1.0)
        self.assertAlmostEqual(res.T + res.R, 1.0, places=6)

    def test_tunneling_regimes_and_limits(self):
        """QL-022: Tunneling regimes (E < V0, E = V0, E > V0, a = 0)."""
        # a = 0 -> T = 1
        res_a0 = analizar_efecto_tunel(E_ev=3.0, V0_ev=5.0, ancho_nm=0.0)
        self.assertEqual(res_a0.T, 1.0)
        self.assertEqual(res_a0.R, 0.0)

        # E = V0 -> exact critical limit
        res_crit = analizar_efecto_tunel(E_ev=5.0, V0_ev=5.0, ancho_nm=0.5)
        self.assertIn("Umbral Crítico", res_crit.regimen)
        self.assertGreater(res_crit.T, 0.0)
        self.assertLess(res_crit.T, 1.0)

        # E > V0 -> over barrier
        res_over = analizar_efecto_tunel(E_ev=8.0, V0_ev=5.0, ancho_nm=0.5)
        self.assertIn("Transmisión sobre la Barrera", res_over.regimen)
        self.assertGreater(res_over.T, 0.0)
        self.assertLessEqual(res_over.T, 1.0)

        # Conservation of flux
        for r in (res_a0, res_crit, res_over):
            self.assertAlmostEqual(r.T + r.R, 1.0, places=6)

    # -------------------------------------------------------------
    # 6. HAMILTONIANO Y EVOLUCIÓN TEMPORAL (QL-003, QL-013, QL-014, QL-015, QL-023)
    # -------------------------------------------------------------
    def test_hamiltonian_non_hermitian_preserves_complex_eigenvalues(self):
        """QL-003 / T10: H = [[0, -1], [1, 0]] has eigenvalues +/- i. Must NOT drop imaginary part."""
        H = np.array([[0.0, -1.0], [1.0, 0.0]], dtype=complex)
        res = analizar_hamiltoniano_matricial(H)
        self.assertFalse(res.es_hermitica)
        evals = res.energias
        imag_parts = np.abs(evals.imag)
        self.assertTrue(np.allclose(imag_parts, [1.0, 1.0]))

    def test_hamiltonian_gap_under_degeneracy(self):
        """QL-014 / T11: diag(0, 0, 1) must yield gap = 1.0 to first distinct level."""
        H = np.diag([0.0, 0.0, 1.0]).astype(complex)
        res = analizar_hamiltoniano_matricial(H)
        self.assertTrue(res.es_hermitica)
        self.assertAlmostEqual(res.brecha, 1.0)

    def test_hamiltonian_exact_vs_approx_hermiticity(self):
        """QL-013 / T12: Nearly Hermitian matrix with 1e-6 asymmetry must report residual."""
        H = np.array([[1.0, 1.0], [1.0 + 1e-6j, 2.0]], dtype=complex)
        res = analizar_hamiltoniano_matricial(H)
        self.assertFalse(res.es_hermitica)
        self.assertAlmostEqual(res.residual_hermitico, 1e-6, places=8)

    def test_hamiltonian_time_evolution_unitary(self):
        """QL-015: Pauli X matrix with |psi(0)> = [1, 0] preserves norm and evolves correctly."""
        # H = [[0, 1], [1, 0]]
        H = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
        psi_0 = np.array([1.0, 0.0], dtype=complex)
        t = np.pi / 2.0  # At t = pi/2: |psi(t)> has probability 1 in |1>
        psi_t, norm_t = evolucion_temporal_matricial(H, psi_0, t)

        # Check unitary norm preservation
        self.assertAlmostEqual(norm_t, 1.0, places=6)
        # Probability in state |1> is sin^2(pi/2) = 1
        prob_1 = abs(psi_t[1])**2
        self.assertAlmostEqual(prob_1, 1.0, places=5)


if __name__ == "__main__":
    unittest.main()
