"""Minimal end-to-end smoke tests for the existing, unmodified calculator."""
import unittest
import tkinter as tk

from quantumlab import CalculadoraCuanticaAvanzada


class QuantumLabSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.app = CalculadoraCuanticaAvanzada(cls.root)
        cls.root.update_idletasks()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def test_symbol_compatibility(self):
        converted = self.app._texto_seguro('⟨p⟩ = ℏ/2')
        self.assertEqual(converted, '<p> = ħ/2')

    def test_all_default_modes_produce_results(self):
        expected_titles = (
            'ANÁLISIS CUÁNTICO COMPLETO',
            'ECUACIÓN DE SCHRÖDINGER',
            'PARTÍCULA EN UNA CAJA',
            'OSCILADOR ARMÓNICO',
            'EFECTO TÚNEL CUÁNTICO',
            'DIAGONALIZACIÓN DE HAMILTONIANO',
        )
        for idx, heading in enumerate(expected_titles):
            with self.subTest(module=idx):
                self.app._seleccionar_modo(idx)
                self.app.limpiar_hoja()
                # Calling the calculator itself avoids suppressing failures in
                # the button callback's GUI message-box error handler.
                handlers = (
                    self.app._resolver_analisis_onda,
                    self.app._resolver_schrodinger_simbolico,
                    self.app._resolver_pozo_infinito,
                    self.app._resolver_oscilador_armonico,
                    self.app._resolver_efecto_tunel,
                    self.app._resolver_hamiltoniano_matricial,
                )
                handlers[idx]()
                output = self.app.hoja.get('1.0', 'end')
                self.assertIn(heading, output)
                self.assertIn('PASO 1', output)


if __name__ == '__main__':
    unittest.main()
