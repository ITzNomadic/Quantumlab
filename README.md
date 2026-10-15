# QuantumLab ⚛️

**QuantumLab** is an educational desktop quantum mechanics calculator, written in Python with Tkinter, SymPy and NumPy. Its dark-themed interface combines symbolic calculations with step-by-step, human-readable explanations. The interface and mathematical engine are currently presented in Spanish.

> **Status: early public release.** Intended for exploration and education, not as a substitute for validated scientific software. See [Known limitations](#known-limitations).

![QuantumLab desktop interface](docs/quantumlab-preview.png)

## Features

- **Wave function analysis:** normalization, expected position and momentum, kinetic energy, boundary term self-adjointness checks, and rigorous Heisenberg uncertainty verification.
- **1D time-independent Schrödinger equation:** applies the Hamiltonian, verifies residual $H\psi - E\psi = 0$, and distinguishes formal local solutions from normalizable $L^2(\mathbb{R})$ physical bound states.
- **Infinite square well:** displays quantized energy formulas, respects quantum number $n \ge 1$, clamps integration strictly to the physical domain $[0, L]$, and computes exact probabilities.
- **Quantum harmonic oscillator:** computes exact normalized Hermite wave functions and quantized energies $E_n = \hbar\omega(n + 1/2)$ for any level $n \ge 0$.
- **Quantum tunneling:** calculates reflection and transmission through a rectangular barrier across all energy regimes ($E < V_0$, $E = V_0$, $E > V_0$, $a=0$, $E=0$) with user-defined parameters, stable asymptotic evaluations for thick barriers, and exact conservation of probability current ($T + R = 1$).
- **Matrix Hamiltonians & Time Evolution:** identifies exact vs. numerical Hermiticity, computes eigenvalues and eigenvectors (preserving full complex eigenvalues for non-Hermitian systems), calculates true excitation gaps for degenerate spectra, and computes unitary time evolution $|\psi(t)\rangle = \exp(-iHt/\hbar)|\psi(0)\rangle$.
- **Secure Sandboxed Parser:** custom AST mathematical parser (`SafeASTParser`) preventing code execution while supporting rich symbolic functions and constants.
- **Results workspace:** formatted steps, symbolic keypad, responsive layout, persistent inputs per mode, and robust export to UTF-8 `.txt` file.

## Installation

**Requirements:** Python 3.10+ and Tkinter (usually bundled with Python on Windows and macOS).

```bash
git clone https://github.com/ITzNomadic/Quantumlab.git
python -m pip install -r requirements.txt
python quantumlab.py
```

On some Linux distributions you must install Tkinter separately (e.g. `sudo apt install python3-tk`).

### Keyboard shortcuts

| Shortcut | Action |
| --- | --- |
| `Ctrl + Enter` | Calculate |
| `Ctrl + S` | Export results as `.txt` |
| `Ctrl + L` | Clear results |

## Testing

The comprehensive test suite verifies parser security, physical invariants, and GUI responsiveness across 60+ automated test cases.

On a desktop with a display:

```bash
python -m unittest discover -s tests -v
```

On a headless Linux server with Xvfb installed:

```bash
xvfb-run -a python -m unittest discover -s tests -v
```

GitHub Actions runs the test suite automatically on submitted changes.

## Security & Scientific Validation

- **AST Expression Parsing:** user inputs are parsed through `SafeASTParser`, strictly permitting only whitelist-approved mathematical operators, constants, and functions. Arbitrary Python code execution, attribute inspection, and imports are completely rejected.
- **Audit Remediation:** All 33 findings from the technical and scientific audit (`Informe_Auditoria_QuantumLab.md`) have been systematically remediated and verified. Detailed mappings and proofs are documented in [docs/AUDIT_REMEDIATION_REPORT.md](docs/AUDIT_REMEDIATION_REPORT.md).

## Español

**QuantumLab** es una aplicación educativa y de cálculo cuántico riguroso desarrollada en Python con Tkinter, SymPy y NumPy. Incluye análisis de funciones de onda con verificación de contorno, ecuación de Schrödinger 1D con distinción de estados ligados, pozo infinito con soporte estricto $[0, L]$, oscilador armónico para niveles $n \ge 0$, efecto túnel multirégimen con evaluación numéricamente estable y diagonalización de matrices hermíticas y no hermíticas con evolución temporal unitaria. Cuenta además con un analizador sintáctico seguro basado en AST.

## License

Licensed under the [MIT License](LICENSE).
