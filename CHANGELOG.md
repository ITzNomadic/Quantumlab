# Changelog

All notable changes to this project will be recorded here.

## [0.2.1] - 2026-10-15

### Fixed (Residual Audit Remediation)
- **CI / Matrix Compatibility**: Updated `test_environment_versions_recorded` to validate versions dynamically against `requirements.txt` (`numpy>=1.26,<3`, `sympy>=1.12,<2`) and Python 3.11/3.12 CI matrix instead of pinned local versions.
- **Infinite Potential Well Physical Support**: Restructured symbolic probability integration over $[0, L]$ physical support so symbolic and numerical probabilities consistently evaluate to 1.0 on $[0, 2L]$.
- **Almost-Hermitian Matrices & Eigen Residuals**: Implemented strict $\epsilon$ tolerance ($10^{-12}$) for hermiticity verification and explicit computation and reporting of maximum eigenpair residual $\|Hv - \lambda v\|_2$ against the original matrix $H$.
- **Hamiltonian Exception Handling**: Eliminated silent exception swallowing when parsing initial state vectors and evolution time $t$. Validates physical dimension and finite numeric values, emitting descriptive `ValueError`s.
- **State Vector Parser**: Fixed regex in `parse_state_vector` to preserve valid functions such as `1/sqrt(2)` without truncating parenthesized function arguments.
- **SciPy Independence**: Removed undeclared dependency on `scipy.linalg.expm` by implementing a pure NumPy scaling and squaring matrix exponential algorithm (`_expm_numpy`), without masking errors.
- **Heisenberg Uncertainty Rigor**: Prevented false-positive uncertainty claims when symbolic expressions or open/non-periodic boundaries yield indeterminate or non-self-adjoint states.
- **Tunneling Boundary & Parameter Validation**: Added finite value checks (`isfinite`) and positivity validation for $E, V_0, a, m$.
- **Unitary vs Non-Unitary Evolution**: Corrected report formatting for non-Hermitian systems to explicitly state non-unitary dissipation/gain instead of claiming unitary conservation.

## [0.2.0] - 2026-10-15

### Security & Architecture
- **QL-001 / QL-017**: Replaced insecure `sp.sympify` with a strictly sandboxed, AST-based mathematical expression parser (`SafeASTParser`). Enforces a strict whitelist of mathematical operators and functions, limits input length (500 chars), AST depth (25), and power exponents (max 100). Completely prevents code execution attacks via `__import__`, builtins, or attribute access.
- **QL-029**: Decoupled monolithic design into modular layers: `quantumlab_engine.parser`, `quantumlab_engine.physics`, and `quantumlab_engine.formatting`.

### Physics & Scientific Rigor
- **QL-002**: Fixed false positive Heisenberg claims. Evaluates operator domain and self-adjointness boundary terms $[\psi^* \psi]_a^b$ before proclaiming uncertainty relations.
- **QL-003 / QL-023**: Fixed non-Hermitian matrix handling. Preserves full complex eigenvalues without truncating imaginary parts. Correctly distinguishes conservative closed systems from open/effective dissipative models.
- **QL-004**: Null state ($\psi=0$) is rejected at entry, preventing $\text{zoo}$ and $\text{nan}$ propagation.
- **QL-005**: Added boundary checks for momentum and kinetic energy operators on finite intervals.
- **QL-006**: Null state is rejected in 1D Schrödinger equation (null vector is never an eigenvector).
- **QL-007**: Explicitly distinguishes between formal local solutions of $H\psi = E\psi$ and square-integrable $L^2$ bound physical eigenstates.
- **QL-008 / QL-009**: Infinite square well bounds strictly respect physical domain $[0, L]$. Clamps exterior intervals (preventing $P > 100\%$) and rejects inverted limits $a > b$ (preventing $P < 0\%$).
- **QL-010**: Quantum number $n \ge 1$ is parsed from parameters and accurately applied to $\psi_n(x)$ and $E_n$.
- **QL-011**: Harmonic oscillator supports arbitrary levels $n \ge 0$ with normalized Hermite wave functions and $E_n = \hbar\omega(n + 1/2)$.
- **QL-012 / QL-022 / QL-031**: Tunneling barrier fully respects user-specified parameters $(E, V_0, a)$, converts units consistently to SI, handles all regimes ($E < V_0$, $E = V_0$, $E > V_0$, $a=0$, $E=0$), employs asymptotic formulas to prevent `sinh` overflow, and accurately explains the internal wave function structure.
- **QL-014**: Fixed excitation gap computation for degenerate Hamiltonians; calculates gap to the first distinct higher eigenvalue.
- **QL-015**: Implemented unitary quantum time evolution $|\psi(t)\rangle = \exp(-iHt/\hbar)|\psi(0)\rangle$ preserving state norm.

### User Interface & Stability
- **QL-024**: Responsive layout adapting to small displays (800x600 compatible).
- **QL-025**: Synchronized mode combobox with visual sidebar navigation.
- **QL-026**: Preserves user input when re-clicking the active mode card or switching modes. Added explicit "Restablecer" preset button.
- **QL-027**: Clear calculation status progression (`CALCULANDO...`, `RESULTADOS DISPONIBLES`, `ERROR EN CÁLCULO`), avoiding false success states.
- **QL-028**: Protected file export with exception handling for disk/IO errors.
- **QL-030**: Dynamic input field hints tailored to each calculation mode.

## [0.1.0] - 2026-10-14

### Added
- Six quantum mechanics learning modules based on the existing Python/SymPy/NumPy calculation engine.
- Redesigned dark Tkinter desktop interface with sidebar navigation and a results workspace.
- Symbol-compatibility substitutions for some Windows Tkinter fonts.
- Documentation, license, CI workflow and initial GUI smoke tests.
