"""
Automated unit tests for QuantumLab v0.3.0 Internationalization (i18n).
Verifies:
  1. Exact dictionary key parity (100% match, 0 missing keys).
  2. No empty or whitespace-only translation strings.
  3. 100% English outputs across all 6 physics modules with ZERO residual Spanish words.
  4. 100% Spanish outputs across all 6 physics modules.
  5. Permanent invariance of the 'Language' header label across all modes and language toggles.
  6. Non-destructive dynamic real-time language switching without losing user input expressions.
  7. User language preference persistence.
"""

import unittest
import os
import tempfile
import json
import tkinter as tk
import sympy as sp
import numpy as np

from quantumlab_i18n import get_i18n, t, I18NManager
from quantumlab_i18n.es import STRINGS_ES
from quantumlab_i18n.en import STRINGS_EN

from quantumlab_engine.physics import (
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
from quantumlab_engine.parser import SafeASTParser
from quantumlab import CalculadoraCuanticaAvanzada


class TestQuantumLabI18N(unittest.TestCase):
    def setUp(self):
        self.i18n = get_i18n()
        self.original_lang = self.i18n.current_language

    def tearDown(self):
        self.i18n.set_language(self.original_lang)

    def test_key_parity_and_completeness(self):
        """Verify 100% key parity between Spanish and English dictionaries."""
        keys_es = set(STRINGS_ES.keys())
        keys_en = set(STRINGS_EN.keys())

        missing_in_en = keys_es - keys_en
        missing_in_es = keys_en - keys_es

        self.assertEqual(missing_in_en, set(), f"Keys in ES missing in EN: {missing_in_en}")
        self.assertEqual(missing_in_es, set(), f"Keys in EN missing in ES: {missing_in_es}")
        self.assertGreater(len(keys_es), 240, "Dictionary must contain full UI & scientific keys")

    def test_no_empty_translation_strings(self):
        """Verify no empty or whitespace strings exist in any dictionary."""
        for lang, d in [("es", STRINGS_ES), ("en", STRINGS_EN)]:
            for k, val in d.items():
                self.assertIsInstance(val, str, f"[{lang}] Key '{k}' is not a string")
                self.assertTrue(bool(val.strip()), f"[{lang}] Key '{k}' is empty or whitespace")

    def test_all_modules_english_output_has_no_residual_spanish(self):
        """
        Verify that formatting all 6 physics modules in English outputs ZERO residual Spanish scientific words.
        """
        spanish_telltales = [
            "ANÁLISIS", "PASO", "FUNCIÓN", "CONCLUSIÓN", "INTERPRETACIÓN",
            "Ecuación", "Pozo", "Potencial", "Oscilador", "Armónico",
            "Efecto Túnel", "Barrera", "Espesor", "Autovalor", "Autoestado",
            "Derivada", "Momento", "Posición", "Incertidumbre", "Cálculo",
            "Conservación unitaria", "Disipación", "Espectro",
        ]

        # 1. Wave function
        psi = SafeASTParser.parse("exp(-x**2/2)")
        res0 = analizar_funcion_onda(psi, sp.sympify("-oo"), sp.sympify("oo"))
        out0 = "\n".join([txt for txt, _ in formatear_analisis_onda(res0, lang="en")])
        for word in spanish_telltales:
            self.assertNotIn(word, out0, f"Residual Spanish '{word}' found in Module 0 English output")

        # 2. Schrodinger
        res1 = analizar_schrodinger_1d(psi, sp.sympify("0"))
        out1 = "\n".join([txt for txt, _ in formatear_schrodinger(res1, lang="en")])
        for word in spanish_telltales:
            self.assertNotIn(word, out1, f"Residual Spanish '{word}' found in Module 1 English output")

        # 3. Infinite well
        res2 = analizar_pozo_infinito(sp.sympify("0"), sp.sympify("1"), n_val=2, L_val=1.0)
        out2 = "\n".join([txt for txt, _ in formatear_pozo_infinito(res2, lang="en")])
        for word in spanish_telltales:
            self.assertNotIn(word, out2, f"Residual Spanish '{word}' found in Module 2 English output")

        # 4. Harmonic oscillator
        res3 = analizar_oscilador_armonico(n_val=1)
        out3 = "\n".join([txt for txt, _ in formatear_oscilador(res3, lang="en")])
        for word in spanish_telltales:
            self.assertNotIn(word, out3, f"Residual Spanish '{word}' found in Module 3 English output")

        # 5. Tunneling
        res4 = analizar_efecto_tunel(E_ev=3.2, V0_ev=5.0, ancho_nm=0.5)
        out4 = "\n".join([txt for txt, _ in formatear_tunel(res4, lang="en")])
        for word in spanish_telltales:
            self.assertNotIn(word, out4, f"Residual Spanish '{word}' found in Module 4 English output")

        # 6. Hamiltonian
        H = np.array([[2.0, 1.0 - 1.0j], [1.0 + 1.0j, 3.0]], dtype=complex)
        res5 = analizar_hamiltoniano_matricial(H, psi_0=np.array([1.0, 0.0], dtype=complex), t_val=1.0)
        out5 = "\n".join([txt for txt, _ in formatear_hamiltoniano(res5, lang="en")])
        for word in spanish_telltales:
            self.assertNotIn(word, out5, f"Residual Spanish '{word}' found in Module 5 English output")

    def test_all_modules_spanish_output_integrity(self):
        """Verify that all 6 physics modules format cleanly and completely in Spanish."""
        # Module 0
        psi = SafeASTParser.parse("exp(-x**2/2)")
        res0 = analizar_funcion_onda(psi, sp.sympify("-oo"), sp.sympify("oo"))
        out0 = "\n".join([txt for txt, _ in formatear_analisis_onda(res0, lang="es")])
        self.assertIn("ANÁLISIS CUÁNTICO COMPLETO", out0)
        self.assertIn("PASO 1", out0)

        # Module 1
        res1 = analizar_schrodinger_1d(psi, sp.sympify("0"))
        out1 = "\n".join([txt for txt, _ in formatear_schrodinger(res1, lang="es")])
        self.assertIn("ECUACIÓN DE SCHRÖDINGER", out1)

        # Module 2
        res2 = analizar_pozo_infinito(sp.sympify("0"), sp.sympify("1"), n_val=1, L_val=1.0)
        out2 = "\n".join([txt for txt, _ in formatear_pozo_infinito(res2, lang="es")])
        self.assertIn("POZO DE POTENCIAL INFINITO", out2)

        # Module 3
        res3 = analizar_oscilador_armonico(n_val=0)
        out3 = "\n".join([txt for txt, _ in formatear_oscilador(res3, lang="es")])
        self.assertIn("OSCILADOR ARMÓNICO CUÁNTICO", out3)

        # Module 4
        res4 = analizar_efecto_tunel(E_ev=3.2, V0_ev=5.0, ancho_nm=0.5)
        out4 = "\n".join([txt for txt, _ in formatear_tunel(res4, lang="es")])
        self.assertIn("EFECTO TÚNEL CUÁNTICO", out4)

        # Module 5
        H = np.array([[2.0, 1.0 - 1.0j], [1.0 + 1.0j, 3.0]], dtype=complex)
        res5 = analizar_hamiltoniano_matricial(H, psi_0=np.array([1.0, 0.0], dtype=complex), t_val=1.0)
        out5 = "\n".join([txt for txt, _ in formatear_hamiltoniano(res5, lang="es")])
        self.assertIn("DIAGONALIZACIÓN DE HAMILTONIANO", out5)

    def test_language_label_permanently_invariable(self):
        """
        Verify the non-negotiable requirement:
        The 'Language' label must permanently display 'Language' (never translated)
        across both Spanish and English modes.
        """
        root = tk.Tk()
        root.withdraw()
        try:
            app = CalculadoraCuanticaAvanzada(root)

            # Test in Spanish
            app._cambiar_idioma("es")
            self.assertIn("Language", app.lbl_language.cget("text"))

            # Test in English
            app._cambiar_idioma("en")
            self.assertIn("Language", app.lbl_language.cget("text"))

            # Test across all 6 modes
            for mode_idx in range(6):
                app._seleccionar_modo(mode_idx)
                self.assertIn("Language", app.lbl_language.cget("text"))
        finally:
            root.destroy()

    def test_dynamic_language_switch_preserves_user_inputs_and_rerenders(self):
        """
        Verify that toggling language dynamically:
          1. Does NOT erase user input expressions.
          2. Preserves active calculation mode.
          3. Re-renders existing results in the newly selected language without recalculating.
        """
        root = tk.Tk()
        root.withdraw()
        try:
            app = CalculadoraCuanticaAvanzada(root)
            app._cambiar_idioma("es")

            # Custom user input in Mode 0
            custom_expr = "exp(-x**2)"
            app.entry_psi.delete(0, tk.END)
            app.entry_psi.insert(0, custom_expr)

            # Run calculation in Spanish
            app.resolver_ecuacion()
            out_es = app.hoja.get("1.0", tk.END)
            self.assertIn("ANÁLISIS CUÁNTICO", out_es)

            # Switch to English
            app._cambiar_idioma("en")

            # 1. Input expression is still intact!
            self.assertEqual(app.entry_psi.get(), custom_expr)

            # 2. Results sheet has re-rendered in English!
            out_en = app.hoja.get("1.0", tk.END)
            self.assertIn("COMPREHENSIVE QUANTUM ANALYSIS", out_en)
            self.assertNotIn("ANÁLISIS CUÁNTICO", out_en)

            # 3. UI elements are localized
            self.assertEqual(app.btn_solve.cget("text"), STRINGS_EN["editor.btn_solve"])
            self.assertEqual(app.lbl_rotulo_psi.cget("text"), STRINGS_EN["editor.label_psi"])

            # Switch back to Spanish
            app._cambiar_idioma("es")
            self.assertEqual(app.entry_psi.get(), custom_expr)
            out_es2 = app.hoja.get("1.0", tk.END)
            self.assertIn("ANÁLISIS CUÁNTICO", out_es2)
        finally:
            root.destroy()

    def test_preference_persistence_in_config_file(self):
        """Verify that language preferences are correctly saved and loaded from config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_config_file = os.path.join(tmpdir, "config.json")
            # Create a mock manager instance targeting tmpdir
            from quantumlab_i18n import manager
            old_file = manager.CONFIG_FILE
            old_dir = manager.CONFIG_DIR
            try:
                manager.CONFIG_FILE = test_config_file
                manager.CONFIG_DIR = tmpdir

                mgr = I18NManager()
                self.assertEqual(mgr.current_language, "es")

                mgr.set_language("en")
                self.assertEqual(mgr.current_language, "en")

                # Verify file was written
                self.assertTrue(os.path.exists(test_config_file))
                with open(test_config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.assertEqual(data.get("language"), "en")

                # New manager loads the preference
                mgr2 = I18NManager()
                self.assertEqual(mgr2.current_language, "en")
            finally:
                manager.CONFIG_FILE = old_file
                manager.CONFIG_DIR = old_dir


if __name__ == "__main__":
    unittest.main()
