"""
Comprehensive verification test suite for QuantumLab v0.3.1.
Verifies all defects DEF-01 through DEF-09:
- DEF-01: Structured errors and 100% English error localization (0 Spanish residue).
- DEF-02: Dynamic preset updating without overwriting user-custom input.
- DEF-03: Multi-step calculation history preservation on language switch.
- DEF-04: Strict dictionary integrity, no Spanish fallback in English, invariant selector.
- DEF-05: Hamiltonian dimensional consistency in natural units (hbar = 1).
- DEF-06: Distinct presentation of raw entered vector vs. normalized quantum state.
- DEF-07: Consistent parameter L substitution across limits, integrals, and probabilities.
- DEF-08: Pre-evaluation and bounds checking of complex exponents in SafeASTParser.
- DEF-09: Responsive execution manager, cancellation, and timeout watchdog.
"""

import unittest
import tkinter as tk
import numpy as np
import sympy as sp
import time

from quantumlab import CalculadoraCuanticaAvanzada
from quantumlab_engine import (
    QuantumLabError,
    MathParseError,
    ParseSecurityError,
    ScientificValidationError,
    AsyncCalculationManager,
    SafeASTParser,
    parse_parameters,
    parse_matrix,
    parse_state_vector,
    analizar_funcion_onda,
    analizar_schrodinger_1d,
    analizar_pozo_infinito,
    analizar_oscilador_armonico,
    analizar_efecto_tunel,
    analizar_hamiltoniano_matricial,
)
from quantumlab_engine.formatting import (
    formatear_analisis_onda,
    formatear_schrodinger,
    formatear_pozo_infinito,
    formatear_oscilador,
    formatear_tunel,
    formatear_hamiltoniano,
)
from quantumlab_i18n import get_i18n, t
from quantumlab_i18n.manager import I18NManager


SPANISH_STOP_WORDS = [
    "debe", "número", "parámetro", "función", "matriz", "vacía", "nulo",
    "estrictamente", "cuántico", "longitud", "expresión", "límite", "demasiado",
    "válido", "fila", "columna", "cuadrada", "partícula", "barrera", "espesor",
    "tiempo", "autovalor", "autovector", "pozo", "infinito", "onda", "no puede"
]


class TestQuantumLabV031Defects(unittest.TestCase):
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
        # Reset to Spanish for standard baseline, or set per test
        get_i18n().set_language("es")
        self.app.limpiar_hoja()

    # =========================================================================
    # DEF-01: LOCALIZED SCIENTIFIC ERRORS & ZERO SPANISH RESIDUE IN ENGLISH
    # =========================================================================
    def _assert_pure_english(self, text: str):
        """Verifies text contains zero common Spanish words."""
        lower_txt = text.lower()
        for word in SPANISH_STOP_WORDS:
            self.assertNotIn(
                word, lower_txt,
                f"Residual Spanish word '{word}' found in English error message: '{text}'"
            )

    def test_def01_empty_math_expression_in_english(self):
        get_i18n().set_language("en")
        with self.assertRaises(MathParseError) as ctx:
            SafeASTParser.parse("")
        self.assertEqual(ctx.exception.code, "error.empty_expression")
        msg = ctx.exception.to_localized("en")
        self.assertIn("cannot be empty", msg)
        self._assert_pure_english(msg)

    def test_def01_unauthorized_function_in_english(self):
        get_i18n().set_language("en")
        with self.assertRaises(ParseSecurityError) as ctx:
            SafeASTParser.parse("system_exec(x)")
        self.assertEqual(ctx.exception.code, "error.forbidden_function")
        msg = ctx.exception.to_localized("en")
        self.assertIn("Disallowed mathematical function", msg)
        self._assert_pure_english(msg)

    def test_def01_unsafe_ast_node_in_english(self):
        get_i18n().set_language("en")
        with self.assertRaises(ParseSecurityError) as ctx:
            SafeASTParser.parse("[x for x in (1, 2)]")
        self.assertEqual(ctx.exception.code, "error.forbidden_node")
        msg = ctx.exception.to_localized("en")
        self.assertIn("Disallowed syntax construct", msg)
        self._assert_pure_english(msg)

    def test_def01_null_quantum_state_in_english(self):
        get_i18n().set_language("en")
        with self.assertRaises(ScientificValidationError) as ctx:
            analizar_funcion_onda(sp.sympify(0), sp.sympify(-1), sp.sympify(1))
        self.assertEqual(ctx.exception.code, "error.null_state_rejected")
        msg = ctx.exception.to_localized("en")
        self.assertIn("null function", msg)
        self._assert_pure_english(msg)

    def test_def01_divergent_norm_integral_in_english(self):
        get_i18n().set_language("en")
        with self.assertRaises(ScientificValidationError) as ctx:
            analizar_funcion_onda(sp.exp(SafeASTParser.x**2), -sp.oo, sp.oo)
        msg = ctx.exception.to_localized("en")
        self.assertTrue("diverge" in msg.lower() or "not normalizable" in msg.lower())
        self._assert_pure_english(msg)

    def test_def01_fractional_quantum_number_in_english(self):
        get_i18n().set_language("en")
        with self.assertRaises(ScientificValidationError) as ctx:
            analizar_pozo_infinito(sp.sympify(0), sp.sympify(1), n_val=1.5)
        self.assertEqual(ctx.exception.code, "error.quantum_number_fractional")
        msg = ctx.exception.to_localized("en")
        self.assertIn("fractional", msg)
        self._assert_pure_english(msg)

    def test_def01_negative_well_width_in_english(self):
        get_i18n().set_language("en")
        with self.assertRaises(ScientificValidationError) as ctx:
            analizar_pozo_infinito(sp.sympify(0), sp.sympify(1), n_val=1, L_val=-2.0)
        self.assertEqual(ctx.exception.code, "error.well_width_positive")
        msg = ctx.exception.to_localized("en")
        self.assertIn("strictly positive", msg)
        self._assert_pure_english(msg)

    def test_def01_non_square_matrix_in_english(self):
        get_i18n().set_language("en")
        with self.assertRaises(ScientificValidationError) as ctx:
            parse_matrix("1, 2; 3, 4, 5")
        self.assertEqual(ctx.exception.code, "error.matrix_ragged_rows")
        msg = ctx.exception.to_localized("en")
        self.assertIn("Irregular row", msg)
        self._assert_pure_english(msg)

    def test_def01_state_vector_dimension_mismatch_in_english(self):
        get_i18n().set_language("en")
        with self.assertRaises(ScientificValidationError) as ctx:
            parse_state_vector("[1, 0, 0]", expected_dim=2)
        self.assertEqual(ctx.exception.code, "error.state_vector_dimension_mismatch")
        msg = ctx.exception.to_localized("en")
        self.assertIn("dimension", msg)
        self._assert_pure_english(msg)

    def test_def01_tunneling_non_finite_parameter_in_english(self):
        get_i18n().set_language("en")
        with self.assertRaises(ScientificValidationError) as ctx:
            analizar_efecto_tunel(E_ev=float("nan"))
        self.assertEqual(ctx.exception.code, "error.tunnel_param_finite")
        msg = ctx.exception.to_localized("en")
        self.assertIn("finite real", msg)
        self._assert_pure_english(msg)

    # =========================================================================
    # DEF-02: DYNAMIC PRESET UPDATING ON LANGUAGE SWITCH
    # =========================================================================
    def test_def02_presets_update_dynamically_without_overwriting_user_work(self):
        # 1. Start in Spanish
        self.app._cambiar_idioma("es")
        self.app._seleccionar_modo(0)
        self.assertEqual(self.app.entry_params.get(), "Paquete Gaussiano estándar")

        # 2. Switch to English: descriptive preset updates
        self.app._cambiar_idioma("en")
        self.assertEqual(self.app.entry_params.get(), "Standard Gaussian wave packet")

        # 3. User enters a custom mathematical expression in entry_psi
        self.app.entry_psi.delete(0, tk.END)
        self.app.entry_psi.insert(0, "cos(3*x)")

        # 4. Switch back to Spanish: custom entry_psi must NOT be overwritten!
        self.app._cambiar_idioma("es")
        self.assertEqual(self.app.entry_psi.get(), "cos(3*x)", "User-custom entry was overwritten!")
        self.assertEqual(self.app.entry_params.get(), "Paquete Gaussiano estándar")

        # 5. Clean up mode 0
        self.app.restablecer_preset_actual(mostrar_dialogo=False)

    # =========================================================================
    # DEF-03: MULTI-STEP CALCULATION HISTORY PRESERVATION ON LANGUAGE SWITCH
    # =========================================================================
    def test_def03_calculation_history_preserved_on_language_switch(self):
        self.app._cambiar_idioma("es")
        self.app.limpiar_hoja()

        # Step 1: Calculate Wave Function in Mode 0
        self.app._seleccionar_modo(0)
        self.app.resolver_ecuacion()
        self.assertEqual(len(self.app.historial_calculos), 1)

        # Step 2: Calculate Infinite Well in Mode 2
        self.app._seleccionar_modo(2)
        self.app.resolver_ecuacion()
        self.assertEqual(len(self.app.historial_calculos), 2)

        # Step 3: Calculate Hamiltonian in Mode 5
        self.app._seleccionar_modo(5)
        self.app.resolver_ecuacion()
        self.assertEqual(len(self.app.historial_calculos), 3)

        # Switch to English
        self.app._cambiar_idioma("en")

        # All 3 calculations must remain in history and be displayed in English
        self.assertEqual(len(self.app.historial_calculos), 3)
        hoja_content = self.app.hoja.get("1.0", tk.END)

        self.assertIn("COMPREHENSIVE QUANTUM ANALYSIS OF WAVE FUNCTION", hoja_content)
        self.assertIn("PARTICLE IN A 1D QUANTUM BOX", hoja_content)
        self.assertIn("MATRIX HAMILTONIAN DIAGONALIZATION", hoja_content)

        # Ensure no Spanish titles remain in the re-rendered sheet
        self.assertNotIn("ANÁLISIS CUÁNTICO COMPLETO", hoja_content)
        self.assertNotIn("PARTÍCULA EN UNA CAJA", hoja_content)

        # Clean up
        self.app.limpiar_hoja()
        self.assertEqual(len(self.app.historial_calculos), 0)

    # =========================================================================
    # DEF-04: STRICT DICTIONARY INTEGRITY & SELECTOR INVARIANTS
    # =========================================================================
    def test_def04_dictionary_completeness_and_parameter_parity(self):
        errs = I18NManager.validate_dictionaries()
        self.assertEqual(errs, [], f"Dictionary validation errors found: {errs}")

    def test_def04_english_missing_key_does_not_fallback_to_spanish(self):
        marker = get_i18n().get_text("completely_invented_key_xyz", lang="en")
        self.assertTrue(marker.startswith("[Missing translation: completely_invented_key_xyz]"))
        # Strict mode raises KeyError
        with self.assertRaises(KeyError):
            get_i18n().get_text("completely_invented_key_xyz", lang="en", strict=True)

    def test_def04_selector_permanently_shows_exact_label_language(self):
        self.app._cambiar_idioma("es")
        self.assertEqual(self.app.lbl_language.cget("text"), "🌐 Language")
        self.app._cambiar_idioma("en")
        self.assertEqual(self.app.lbl_language.cget("text"), "🌐 Language")

    # =========================================================================
    # DEF-05: HAMILTONIAN UNITS CONSISTENCY (NATURAL UNITS hbar = 1)
    # =========================================================================
    def test_def05_hamiltonian_natural_units_two_and_three_level(self):
        # 2-level diagonal Hamiltonian: E0 = 1, E1 = 3 -> Gap = 2.0
        H2 = np.array([[1.0, 0.0], [0.0, 3.0]], dtype=complex)
        res2 = analizar_hamiltoniano_matricial(H2)
        self.assertEqual(res2.brecha, 2.0)

        bloques_es = formatear_hamiltoniano(res2, lang="es")
        gap_line_es = [txt for txt, tag in bloques_es if "Frecuencia de Bohr" in txt][0]
        self.assertIn("ω = ΔE / ℏ = 2.000000 rad / u.t.", gap_line_es)
        self.assertIn("unidades naturales ℏ = 1", gap_line_es)

        bloques_en = formatear_hamiltoniano(res2, lang="en")
        gap_line_en = [txt for txt, tag in bloques_en if "Bohr frequency" in txt][0]
        self.assertIn("ω = ΔE / ℏ = 2.000000 rad / time unit", gap_line_en)

        # 3-level Hamiltonian: E0 = 0, E1 = 2, E2 = 5 -> Gap = 2.0
        H3 = np.array([[0.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 5.0]], dtype=complex)
        res3 = analizar_hamiltoniano_matricial(H3)
        self.assertEqual(res3.brecha, 2.0)

    # =========================================================================
    # DEF-06: ACCURATE INITIAL STATE PRESENTATION (psi(0) = [2, 0])
    # =========================================================================
    def test_def06_initial_state_normalization_distinction(self):
        H = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
        psi_raw = np.array([2.0, 0.0], dtype=complex)

        res = analizar_hamiltoniano_matricial(H, psi_0=psi_raw, t_val=0.0)
        self.assertAlmostEqual(res.norma_psi_0, 2.0)
        self.assertAlmostEqual(float(np.linalg.norm(res.psi_0_norm)), 1.0)
        self.assertTrue(np.allclose(res.psi_0_norm, [1.0, 0.0]))

        bloques = formatear_hamiltoniano(res, lang="en")
        evo_text = [txt for txt, tag in bloques if "Entered vector" in txt][0]
        self.assertIn("Entered vector:   |ψ_raw(0)⟩ = [ +2.0000+0.0000i  +0.0000+0.0000i ]ᵀ  (Norm = 2.000000)", evo_text)
        self.assertIn("Normalized state: |ψ(0)⟩     = [ +1.0000+0.0000i  +0.0000+0.0000i ]ᵀ  (Norm = 1.000000)", evo_text)

    # =========================================================================
    # DEF-07: CONSISTENT SUBSTITUTION OF PARAMETER L
    # =========================================================================
    def test_def07_parameter_L_propagation_and_substitution(self):
        # Using L=2 and limit L/3 -> b becomes 2/3
        res = analizar_pozo_infinito(
            a=sp.sympify(0),
            b=SafeASTParser.L / 3,
            n_val=1,
            L_val=2.0
        )
        self.assertEqual(float(res.L), 2.0)
        # Symbolic integral must have no free symbols L
        free_syms = res.prob_simbolica.free_symbols
        self.assertNotIn(SafeASTParser.L, free_syms)

        # Numerical and symbolic probabilities must match
        prob_sym_float = float(res.prob_simbolica.evalf())
        self.assertAlmostEqual(prob_sym_float, res.prob_numerica, places=6)

    # =========================================================================
    # DEF-08: COMPLEX EXPONENT VALIDATION IN SAFE AST PARSER
    # =========================================================================
    def test_def08_complex_exponent_validation(self):
        # 1. Constant non-literal exponent exceeding MAX_POWER: x**(50*3) = x**150
        with self.assertRaises(ParseSecurityError) as ctx:
            SafeASTParser.parse("x**(50*3)")
        self.assertEqual(ctx.exception.code, "error.exponent_too_large")

        # 2. Base 2 with evaluated exponent: 2**(25*8) = 2**200
        with self.assertRaises(ParseSecurityError) as ctx:
            SafeASTParser.parse("2**(25*8)")
        self.assertEqual(ctx.exception.code, "error.exponent_too_large")

        # 3. Nested powers in parentheses: (x**2)**3
        with self.assertRaises(ParseSecurityError) as ctx:
            SafeASTParser.parse("(x**2)**3")
        self.assertEqual(ctx.exception.code, "error.power_nested_too_deep")

        # 4. Valid mathematical expressions from presets must pass
        self.assertIsNotNone(SafeASTParser.parse("exp(-x**2 / 2)"))
        self.assertIsNotNone(SafeASTParser.parse("(1/2)*m*w**2*x**2"))

    # =========================================================================
    # DEF-09: RESPONSIVE EXECUTION MANAGER, CANCELLATION & WATCHDOG
    # =========================================================================
    def test_def09_async_calculation_manager(self):
        manager = AsyncCalculationManager(self.root)

        # Fast calculation completes cleanly
        completed = [False]
        def calc():
            return 42

        def on_success(res):
            completed[0] = True

        manager.run_calculation(calc, on_success, lambda e: None, timeout=5.0)

        # Process events
        start = time.time()
        while not completed[0] and time.time() - start < 2.0:
            self.root.update()
            time.sleep(0.02)

        self.assertTrue(completed[0])

        # Cancellation test
        cancelled_called = [False]
        manager.run_calculation(lambda: time.sleep(0.5), lambda r: None, lambda e: None)
        self.assertTrue(manager.is_running)
        manager.cancel()
        self.assertFalse(manager.is_running)


if __name__ == "__main__":
    unittest.main()
