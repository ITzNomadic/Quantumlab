# QuantumLab ⚛️

**QuantumLab** is an educational desktop quantum mechanics calculator, written in Python with Tkinter, SymPy and NumPy. Its dark-themed interface combines symbolic calculations with step-by-step, human-readable explanations. The interface and mathematical engine are currently presented in Spanish.

> **Status: early public release.** Intended for exploration and education, not as a substitute for validated scientific software. See [Known limitations](#known-limitations).

![QuantumLab desktop interface](docs/quantumlab-preview.png)

## Features

- **Wave function analysis:** normalization, expected position and momentum, kinetic energy and uncertainty estimates.
- **1D time-independent Schrödinger equation:** applies the Hamiltonian and checks whether the energy quotient depends on position.
- **Infinite square well:** displays the quantized energy formula and integrates probability over a region for the ground state.
- **Quantum harmonic oscillator:** derives the ground-state energy from the Hamiltonian.
- **Quantum tunneling:** calculates reflection and transmission through a rectangular barrier using built-in example parameters.
- **Matrix Hamiltonians:** identifies Hermitian matrices and computes eigenvalues and eigenvectors with NumPy.
- **Results workspace:** formatted steps, symbolic keypad, presets and export to a UTF-8 `.txt` file.

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

## Examples

1. **Wave function:** select *Función de onda*; use the preset `exp(-x**2 / 2)` with bounds `-oo` and `oo`.
2. **Schrödinger 1D:** use `sin(pi*x/L)` for the wave function and `0` for the potential.
3. **Hamiltonian matrix:** select *Hamiltoniano* and enter `2, 1-1j; 1+1j, 3`.

Inputs are interpreted using SymPy syntax (`**` for powers, `pi`, `oo`, `I`, etc.).

## Testing

The included tests exercise the six default calculation modes and symbol-display conversion through the Tkinter interface.

On a desktop with a display:

```bash
python -m unittest discover -s tests -v
```

On a headless Linux server with Xvfb installed:

```bash
xvfb-run -a python -m unittest discover -s tests -v
```

GitHub Actions runs the same smoke tests for submitted changes.

## Known limitations

- **Educational prototype:** not all physics conclusions and boundary conditions have been independently validated. Confirm results before use in scientific work.
- **Tunneling mode:** the example currently uses fixed numerical values (`E = 3.2 eV`, `V0 = 5.0 eV`, `a = 0.5 nm`) rather than reading all entered parameters.
- **Infinite well:** the integrated example uses the ground state `n = 1` regardless of the free-form parameter text.
- **Hamiltonian mode:** computes the eigensystem but does **not** yet implement time evolution, despite the descriptive mode title. Non-Hermitian matrices also need care in physical interpretation.
- **Expression parsing:** `sympy.sympify()` is used on local user input. **Do not paste untrusted expressions** or expose this application as a remote expression-evaluation service without replacing that parser with a secured one.
- **Unicode rendering:** some mathematical symbols are displayed using more compatible alternatives on Windows; presentation differs slightly from traditional notation.

See [CONTRIBUTING.md](CONTRIBUTING.md) to help improve the project.

## Español

**QuantumLab** es una aplicación educativa para estudiar mecánica cuántica mediante cálculos simbólicos y explicaciones paso a paso. Incluye análisis de funciones de onda, Schrödinger 1D, pozo infinito, oscilador armónico, efecto túnel y diagonalización de Hamiltonianos.

**Inicio rápido en Windows:** instala Python, ejecuta `python -m pip install -r requirements.txt` y después `python quantumlab.py`.

Se trata de una **versión inicial**: varias funciones usan parámetros de ejemplo y los resultados científicos deben verificarse de forma independiente. El código y la interfaz se publican para aprendizaje y colaboración.

## License

Licensed under the [MIT License](LICENSE).
