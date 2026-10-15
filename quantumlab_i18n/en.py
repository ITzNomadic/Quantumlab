"""
English Translations for QuantumLab.
Contains all user interface strings, step-by-step scientific derivations,
physical interpretations, and error messages translated into standard technical English.
"""

STRINGS_EN = {
    # -------------------------------------------------------------
    # General UI / Header
    # -------------------------------------------------------------
    "app.title": "QuantumLab  |  Advanced Quantum Mechanics Calculator",
    "header.brand_title": "QUANTUM",
    "header.brand_accent": "LAB",
    "header.brand_sub": "QUANTUM MECHANICS RESEARCH  /  PRO MAX (SECURED)",
    "header.engine_verified": "VERIFIED SCIENTIFIC ENGINE",
    "header.engine_libs": "SymPy  •  NumPy  •  AST Parser",
    "header.language_label": "Language",

    # -------------------------------------------------------------
    # Sidebar / Navigation
    # -------------------------------------------------------------
    "sidebar.workspace_title": "WORKSPACE",
    "sidebar.modules_title": "Calculation Modules",
    "sidebar.modules_sub": "Select a quantum system",
    "sidebar.shortcuts_title": "KEYBOARD SHORTCUTS",
    "sidebar.shortcut_calc": "Ctrl + Enter   Solve",
    "sidebar.shortcut_export": "Ctrl + S       Export",
    "sidebar.shortcut_clear": "Ctrl + L       Clear",

    # Module 0: Wave function
    "module.0.name": "Wave Function",
    "module.0.sub": "Normalization & Heisenberg",
    "module.0.desc": "Analyzes ψ(x), expectation values, and rigorous quantum uncertainties.",
    "module.0.combo": "1. Full Wave Function ψ(x) Analysis: Normalization, ⟨x⟩, ⟨p⟩, ⟨T⟩ & Heisenberg",

    # Module 1: 1D Schrödinger
    "module.1.name": "1D Schrödinger",
    "module.1.sub": "Eigenstates & Energy",
    "module.1.desc": "Verifies Schrödinger eigenstates, square-integrability, and energy.",
    "module.1.combo": "2. 1D Schrödinger Equation: Eigenstate Verification & Energy Extraction E(x)",

    # Module 2: Infinite well
    "module.2.name": "Infinite Potential Well",
    "module.2.sub": "Probability in Region",
    "module.2.desc": "Computes quantized states n≥1 and exact spatial probabilities in the well.",
    "module.2.combo": "3. Full System: 1D Infinite Potential Well & Spatial Probability",

    # Module 3: Harmonic oscillator
    "module.3.name": "Harmonic Oscillator",
    "module.3.sub": "Energy Levels",
    "module.3.desc": "Examines ground state and excited states n≥0 via Hermite polynomials.",
    "module.3.combo": "4. Full System: Quantum Harmonic Oscillator & Energy Levels",

    # Module 4: Tunneling
    "module.4.name": "Quantum Tunneling",
    "module.4.sub": "Potential Barrier",
    "module.4.desc": "Estimates quantum transmission and reflection across energy regimes E, V₀.",
    "module.4.combo": "5. Quantum Tunneling: Transmission through a Finite Potential Barrier",

    # Module 5: Hamiltonian
    "module.5.name": "Matrix Hamiltonian",
    "module.5.sub": "Eigenvalues & Eigenvectors",
    "module.5.desc": "Diagonalizes Hermitian/non-Hermitian matrices and computes time evolution.",
    "module.5.combo": "6. Matrix Hamiltonian Diagonalization (H|ψ⟩ = E|ψ⟩) & Time Evolution",

    # -------------------------------------------------------------
    # Input Editor (Left Panel)
    # -------------------------------------------------------------
    "editor.step_counter": "MODULE  {current:02d} / {total:02d}",
    "editor.label_psi": "WAVE FUNCTION  ψ(x) / STATE",
    "editor.label_pot": "POTENTIAL  V(x)",
    "editor.label_limits": "INTEGRATION BOUNDS / TIME",
    "editor.label_lim_a": "Lower bound a / t",
    "editor.label_lim_b": "Upper bound b",
    "editor.label_params": "PARAMETERS / HAMILTONIAN H",
    "editor.keyboard_title": "SYMBOLIC KEYBOARD",
    "editor.keyboard_hint": "Insert into active field",
    "editor.btn_solve": "⚡  SOLVE EQUATION",
    "editor.btn_clear": "Clear",
    "editor.btn_reset": "Reset",
    "editor.btn_export": "Export",

    # Dynamic hints
    "hint.0.psi": "ψ(x)",
    "hint.0.pot": "V(x) [Informational]",
    "hint.0.lim_a": "Lower bound a",
    "hint.0.lim_b": "Upper bound b",
    "hint.0.params": "Parameters [Informational]",

    "hint.1.psi": "ψ(x)",
    "hint.1.pot": "Potential V(x)",
    "hint.1.lim_a": "Lower bound a (optional)",
    "hint.1.lim_b": "Upper bound b (optional)",
    "hint.1.params": "Parameters [Informational]",

    "hint.2.psi": "Analytical ψ(x)",
    "hint.2.pot": "V(x) [Informational]",
    "hint.2.lim_a": "Region start a",
    "hint.2.lim_b": "Region end b",
    "hint.2.params": "Integer n (e.g. n=1, L=1.0)",

    "hint.3.psi": "Analytical ψ(x)",
    "hint.3.pot": "Harmonic V(x)",
    "hint.3.lim_a": "Lower bound [-oo]",
    "hint.3.lim_b": "Upper bound [oo]",
    "hint.3.params": "Level n (e.g. n=0, 1, 2...)",

    "hint.4.psi": "Incident wave",
    "hint.4.pot": "Barrier V₀",
    "hint.4.lim_a": "Bound a",
    "hint.4.lim_b": "Width a (nm)",
    "hint.4.params": "E, V0, a (e.g. E=3.2, V0=5.0, a=0.5)",

    "hint.5.psi": "Initial state |ψ(0)⟩",
    "hint.5.pot": "System",
    "hint.5.lim_a": "Time t",
    "hint.5.lim_b": "Bound b",
    "hint.5.params": "Matrix H (e.g. 2, 1-1j; 1+1j, 3)",

    # -------------------------------------------------------------
    # Presets
    # -------------------------------------------------------------
    "preset.0.psi": "exp(-x**2 / 2)",
    "preset.0.pot": "0",
    "preset.0.lim_a": "-oo",
    "preset.0.lim_b": "oo",
    "preset.0.params": "Standard Gaussian wave packet",

    "preset.1.psi": "sin(pi*x/L)",
    "preset.1.pot": "0",
    "preset.1.lim_a": "0",
    "preset.1.lim_b": "L",
    "preset.1.params": "Particle in a box eigenstate",

    "preset.2.psi": "sqrt(2/L)*sin(n*pi*x/L)",
    "preset.2.pot": "0 (Inside well), oo (Outside)",
    "preset.2.lim_a": "0",
    "preset.2.lim_b": "L/3",
    "preset.2.params": "n=1, L=1.0 (nm)",

    "preset.3.psi": "exp(-m*w*x**2 / (2*hbar))",
    "preset.3.pot": "(1/2)*m*w**2*x**2",
    "preset.3.lim_a": "-oo",
    "preset.3.lim_b": "oo",
    "preset.3.params": "n=0 (Ground state)",

    "preset.4.psi": "exp(I*k*x)",
    "preset.4.pot": "V0 = 5.0 eV",
    "preset.4.lim_a": "0",
    "preset.4.lim_b": "0.5",
    "preset.4.params": "E=3.2, V0=5.0, a=0.5 (E, V0 in eV; width a in nm)",

    "preset.5.psi": "[1, 0] (Initial state |ψ(0)⟩)",
    "preset.5.pot": "Coupled 2-level quantum system",
    "preset.5.lim_a": "0",
    "preset.5.lim_b": "1",
    "preset.5.params": "2, 1-1j; 1+1j, 3",

    # -------------------------------------------------------------
    # Results Console (Right Panel)
    # -------------------------------------------------------------
    "results.console_title": "RESULTS CONSOLE",
    "results.sheet_title": "Results Worksheet",
    "results.step_by_step": "Step-by-step mathematical derivation",
    "results.empty_title": "Your Results Workspace",
    "results.empty_desc": "Select a module, configure your inputs,\nand solve the equation to view the steps.",
    "results.footer_info": "SYMBOLIC OUTPUT  •  VERIFIED MATHEMATICAL ENGINE  •  .TXT EXPORT",

    # Execution statuses
    "status.no_results": "NO RESULTS",
    "status.calculating": "CALCULATING...",
    "status.available": "RESULTS AVAILABLE",
    "status.syntax_error": "SYNTAX/SECURITY ERROR",
    "status.param_error": "PARAMETER ERROR",
    "status.calc_error": "CALCULATION ERROR",

    # Window footer
    "footer.brand": "QUANTUMLAB  /  WORKSPACE",
    "footer.security": "Rigorous scientific engine  ·  Active AST security",

    # Dialogs & confirmations
    "dialog.preset_restored_title": "Preset Restored",
    "dialog.preset_restored_msg": "Loaded the default preset example for '{name}'.",
    "dialog.export_title": "Save QuantumLab Worksheet",
    "dialog.export_success_title": "Worksheet Exported",
    "dialog.export_success_msg": "Scientific derivation successfully saved to:\n{path}",
    "dialog.export_empty_title": "Empty Worksheet",
    "dialog.export_empty_msg": "No calculated results available to export.",
    "dialog.export_error_title": "Export Error",
    "dialog.export_error_msg": "Could not save worksheet file:\n{error}",
    "dialog.error_syntax_title": "Syntax / Mathematical Security Error",
    "dialog.error_param_title": "Invalid Parameter or Domain",
    "dialog.error_calc_title": "Scientific Calculation Error",
    "dialog.error_calc_prefix": "An error occurred while processing the system:\n",

    # -------------------------------------------------------------
    # Scientific Formatting: Module 0 (Wave Function)
    # -------------------------------------------------------------
    "wave.title": "📘 COMPREHENSIVE QUANTUM ANALYSIS OF WAVE FUNCTION ψ(x)",
    "wave.intro": (
        "We systematically analyze the proposed quantum state step by step. We first verify Born's "
        "normalization condition, analyze boundary terms, and extract physical observables "
        "using self-adjoint quantum operators."
    ),
    "wave.initial_state": "  ψ_initial(x) = {psi}   on domain [{a}, {b}]",
    "wave.step1_title": "🔹 STEP 1: Born Normalization Condition & Square Integrability",
    "wave.step1_desc": (
        "In quantum mechanics, the total probability of finding the particle across the domain must be strictly 1 (100%). "
        "We verify that the wave function is square-integrable (L²) over the domain:"
    ),
    "wave.step1_formula": (
        "  ∫ |ψ(x)|² dx = {norm_integral}\n"
        "  Normalization constant: A = 1 / √({norm_integral}) = {constante_A}\n"
        "  Normalized wave function: ψ(x) = {psi_norm}"
    ),
    "wave.step2_title": "🔹 STEP 2: Position Expectation Value ⟨x⟩ & Quantum Dispersion Δx",
    "wave.step2_desc": "We evaluate the mean position by applying the position operator x̂ in the coordinate representation:",
    "wave.step2_formula": (
        "  ⟨x⟩  = ∫ ψ*(x) · x · ψ(x) dx  = {exp_x}\n"
        "  ⟨x²⟩ = ∫ ψ*(x) · x² · ψ(x) dx = {exp_x2}\n"
        "  Position uncertainty: Δx = √(⟨x²⟩ - ⟨x⟩²) = {delta_x}"
    ),
    "wave.step3_title": "🔹 STEP 3: Linear Momentum Operator p̂ = -iℏ(d/dx) & Kinetic Energy ⟨T⟩",
    "wave.step3_desc": "We analytically differentiate the wave function to apply the momentum operator and the one-dimensional Laplacian:",
    "wave.step3_formula": (
        "  dψ/dx   = {d_psi}\n"
        "  d²ψ/dx² = {d2_psi}\n"
        "  ⟨p⟩  = ∫ ψ*(x) · (-iℏ·d/dx) · ψ(x) dx = {exp_p}\n"
        "  ⟨p²⟩ = ∫ ψ*(x) · (-ℏ²·d²/dx²) · ψ(x) dx = {exp_p2}\n"
        "  Momentum uncertainty: Δp = √(⟨p²⟩ - ⟨p⟩²) = {delta_p}\n"
        "  Mean kinetic energy:  ⟨T⟩ = ⟨p²⟩ / (2m) = {exp_T}"
    ),
    "wave.step4_title": "🔹 STEP 4: Heisenberg Uncertainty Principle & Domain Validation",
    "wave.step4_formula": (
        "  Uncertainty product: Δx · Δp = {product}\n"
        "  Canonical fundamental bound: ℏ/2"
    ),
    "wave.interpretation_prefix": "💡 SCIENTIFIC INTERPRETATION: Mean position ⟨x⟩ = {exp_x}, average momentum ⟨p⟩ = {exp_p}.\n\n",
    "wave.boundary_selfadjoint": "The boundary term [|ψ|²] vanishes at the domain boundaries (compatible with self-adjointness).",
    "wave.boundary_warning": (
        "BOUNDARY WARNING: [|ψ|²] does not vanish at the domain endpoints. On bounded intervals without "
        "periodic or Dirichlet boundary conditions, the momentum operator p̂ = -iℏ∂x is not standard self-adjoint, "
        "which can yield formal anomalies in computed moments."
    ),
    "wave.heisenberg_fulfilled": "The state strictly satisfies the Heisenberg Uncertainty Principle: Δx·Δp ≥ ℏ/2.",
    "wave.heisenberg_zero_dispersion": (
        "NON-VERIFIABLE / ZERO DISPERSION: One of the formally calculated uncertainties is zero "
        "(Δp = 0 or Δx = 0). On a finite interval, p̂ possesses no eigenstates within the self-adjoint domain, "
        "so the zero product does NOT satisfy the canonical uncertainty principle (Δx·Δp ≥ ℏ/2)."
    ),
    "wave.heisenberg_open_boundary": (
        "NON-STANDARD BOUNDARY CONDITIONS: The canonical relation Δx·Δp ≥ ℏ/2 assumes self-adjointness "
        "over the entire real line ℝ or periodic boundary conditions. On a bounded open interval, "
        "the formal product is not conclusive proof of the Heisenberg uncertainty principle."
    ),
    "wave.heisenberg_violated": "The formal uncertainty product violates the ℏ/2 bound due to boundary or domain conditions.",
    "wave.heisenberg_indeterminate": (
        "INDETERMINATE: Could not formally prove the canonical inequality Δx·Δp ≥ ℏ/2 "
        "due to free symbolic parameters or non-elementary integrals."
    ),

    # -------------------------------------------------------------
    # Scientific Formatting: Module 1 (1D Schrödinger)
    # -------------------------------------------------------------
    "schrodinger.title": "🔬 RESOLUTION OF THE TIME-INDEPENDENT SCHRÖDINGER EQUATION (1D)",
    "schrodinger.intro": (
        "We rigorously evaluate whether the proposed wave function ψ(x) is an eigenstate of the Hamiltonian operator "
        "Ĥ = - (ℏ²/2m) d²/dx² + V(x), verifying whether it satisfies Ĥψ(x) = Eψ(x)."
    ),
    "schrodinger.system_inputs": "  ψ(x) = {psi}\n  V(x) = {V}",
    "schrodinger.step1_title": "🔹 STEP 1: Spatial Derivatives of the Wave Function",
    "schrodinger.step1_formula": (
        "  dψ/dx   = {d_psi}\n"
        "  d²ψ/dx² = {d2_psi}"
    ),
    "schrodinger.step2_title": "🔹 STEP 2: Application of the Hamiltonian Operator Ĥψ(x)",
    "schrodinger.step2_formula": (
        "  T̂ψ(x) = - (ℏ²/2m) d²ψ/dx² = {T_psi}\n"
        "  V̂ψ(x) = V(x)·ψ(x) = {V_psi}\n"
        "  Ĥψ(x) = T̂ψ + V̂ψ = {H_psi}"
    ),
    "schrodinger.step3_title": "🔹 STEP 3: Energy Eigenvalue Extraction & Verification E",
    "schrodinger.step3_formula": "  Spectral quotient: E(x) = Ĥψ(x) / ψ(x) = {energia}",
    "schrodinger.conclusion_eigenstate_bound": (
        "💡 PHYSICAL CONCLUSION: ψ(x) IS A STRICT BOUND EIGENSTATE! The quotient E = {energia} is a "
        "real scalar constant and the function belongs to L² (square-integrable). The system possesses a well-defined eigenenergy E = {energia}."
    ),
    "schrodinger.conclusion_eigenstate_formal": (
        "⚠️ PHYSICAL CONCLUSION: FORMAL LOCAL SOLUTION. ψ(x) is a formal local solution with energy E = {energia}, but is NOT "
        "a normalizable bound state in L²(ℝ) (divergent integral or non-vanishing at infinity). It belongs to the continuous spectrum or represents an unbounded scattering state."
    ),
    "schrodinger.conclusion_non_eigenstate": (
        "💡 PHYSICAL INTERPRETATION: The quotient E(x) = {energia} depends explicitly on the coordinate 'x'. "
        "Therefore, ψ(x) is NOT a stationary state of potential V(x). It represents a non-stationary wave packet or superposition that will undergo dynamical time evolution."
    ),

    # -------------------------------------------------------------
    # Scientific Formatting: Module 2 (Infinite Potential Well)
    # -------------------------------------------------------------
    "well.title": "📙 PARTICLE IN A 1D QUANTUM BOX (INFINITE POTENTIAL WELL)",
    "well.intro": (
        "A particle confined between impenetrable walls at x = 0 and x = L can only exist "
        "in quantized standing waves with physical support strictly on [0, L]."
    ),
    "well.step1_title": "🔹 STEP 1: Eigenfunctions and Energy Quantization",
    "well.step1_formula": (
        "  Selected quantum level: n = {n}, Well width: L = {L}\n"
        "  ψₙ(x) = √(2/L) · sin(n·π·x / L)   for 0 ≤ x ≤ L (0 elsewhere)\n"
        "  Eₙ    = (n² · π² · ℏ²) / (2 · m · L²)"
    ),
    "well.step2_title": "🔹 STEP 2: Probability of Finding the Particle Between [{a}, {b}] for State n={n}",
    "well.step2_formula": (
        "  Requested interval: [{a_in}, {b_in}]\n"
        "  Effective physical interval in well: [{a_eff}, {b_eff}]\n"
        "  P({a_eff} ≤ x ≤ {b_eff}) = ∫ |ψₙ(x)|² dx = {prob_simbolica}\n"
        "  Calculated probability: P = {prob_num:.6f} ({prob_percent:.2f}%)"
    ),
    "well.domain_note": (
        "PHYSICAL ACCUMULATION: The infinite potential well has impenetrable walls at x=0 and x=L. "
        "The probability density is strictly 0 outside [0, L]. "
        "The integral over [{a}, {b}] is effectively evaluated on its intersection with the well."
    ),
    "well.interpretation": (
        "💡 PHYSICAL INTERPRETATION: In a classical box, the probability would be purely geometric (Δx/L). "
        "In quantum mechanics, due to the interference nodes of the standing wave n={n}, "
        "the actual probability of finding the particle in the region is {prob_percent:.2f}%."
    ),

    # -------------------------------------------------------------
    # Scientific Formatting: Module 3 (Harmonic Oscillator)
    # -------------------------------------------------------------
    "oscillator.title": "📕 QUANTUM HARMONIC OSCILLATOR (LEVEL n = {n})",
    "oscillator.intro": "The quantum harmonic oscillator models molecular vibrations and quantum fields using the parabolic potential V(x) = ½ m ω² x².",
    "oscillator.step1_title": "🔹 STEP 1: Eigenstate ψₙ(x) and Normalization Constant",
    "oscillator.step1_formula": (
        "  Quantum level: n = {n}\n"
        "  Aₙ = (m·ω / (π·ℏ))^(1/4) · 1 / √(2ⁿ · n!) = {An}\n"
        "  ψₙ(x) = {psi_n}"
    ),
    "oscillator.step2_title": "🔹 STEP 2: Verification with Hamiltonian Ĥ = - (ℏ²/2m) d²/dx² + ½ m ω² x²",
    "oscillator.step2_formula": (
        "  d²ψₙ/dx² = {d2_psi}\n"
        "  Ĥψₙ(x)   = {H_psi}\n"
        "  Level eigenenergy: E_{n} = {energia_n}   (Eₙ = ℏω(n + ½))"
    ),
    "oscillator.interpretation_ground": (
        "💡 PHYSICAL INTERPRETATION: Even at absolute zero (n = 0), the particle CANNOT remain motionless at the bottom of the well, "
        "as that would violate the Heisenberg Uncertainty Principle. It possesses an unavoidable 'Zero-Point Energy' of E₀ = ½ ℏω."
    ),
    "oscillator.interpretation_excited": (
        "💡 PHYSICAL INTERPRETATION: For excited level n = {n}, the wave function has exactly {n} spatial nodes "
        "where the probability density vanishes. Its exact energy is E_{n} = {coeff} ℏω."
    ),

    # -------------------------------------------------------------
    # Scientific Formatting: Module 4 (Quantum Tunneling)
    # -------------------------------------------------------------
    "tunnel.title": "🔮 QUANTUM TUNNELING THROUGH A RECTANGULAR POTENTIAL BARRIER",
    "tunnel.intro": (
        "We calculate the quantum transmission for a particle of mass m = {m:.3e} kg with energy E = {E_ev:.4f} eV "
        "incident upon a potential barrier V₀ = {V0_ev:.4f} eV of width a = {ancho_nm:.4f} nm."
    ),
    "tunnel.step1_title": "🔹 STEP 1: Wave Parameter and Attenuation Inside Barrier",
    "tunnel.step1_subbarrier": (
        "  Regime: Sub-barrier (E < V₀)\n"
        "  Decay constant: κ = √[2m(V₀ - E)] / ℏ = {kappa:.4e} m⁻¹\n"
        "  Dimensionless factor: κ·a = {kappa_a:.4f}"
    ),
    "tunnel.step1_overbarrier": (
        "  Regime: Over-barrier (E > V₀)\n"
        "  Wave vector inside barrier: k₂ = √[2m(E - V₀)] / ℏ = {kappa:.4e} m⁻¹\n"
        "  Dimensionless factor: k₂·a = {kappa_a:.4f}"
    ),
    "tunnel.step1_resonance": (
        "  Critical Regime: Threshold Resonance (E = V₀)\n"
        "  Inside the barrier, the wave function degenerates into a linear solution ψ(x) = C·x + D."
    ),
    "tunnel.step2_title": "🔹 STEP 2: Exact Transmission (T) & Reflection (R) Coefficients",
    "tunnel.step2_formula": (
        "  Transmission probability (Tunneling) : T = {T:.6e}  ({T_percent:.4f}%)\n"
        "  Reflection probability               : R = {R:.6f}  ({R_percent:.4f}%)\n"
        "  Probability current conservation: T + R = {TR_sum:.6f}"
    ),
    "tunnel.regime_zero_width": "Zero barrier width (a = 0): Perfect transmission T = 1.",
    "tunnel.regime_zero_energy": "Zero particle energy (E = 0): Transmission impossible T = 0.",
    "tunnel.regime_subbarrier_explanation": (
        "💡 PHYSICAL INTERPRETATION: Classically, the particle would reflect with 100% certainty because it lacks "
        "sufficient energy to overcome the barrier (E < V₀). In quantum mechanics, the wave function decays exponentially e^(-κx) "
        "through the barrier, yielding a finite tunneling probability of {T_percent:.4f}%."
    ),
    "tunnel.regime_resonance_explanation": (
        "💡 PHYSICAL INTERPRETATION: In the threshold limit E = V₀, the transmission coefficient depends "
        "inversely on barrier width according to T = [1 + m·V₀·a² / (2ℏ²)]⁻¹."
    ),
    "tunnel.regime_overbarrier_explanation": (
        "💡 PHYSICAL INTERPRETATION: Even though the particle has sufficient energy to classically cross the barrier (E > V₀), "
        "the abrupt potential discontinuity produces quantum wave reflections, yielding T = {T_percent:.4f}% and R = {R_percent:.4f}%."
    ),

    # -------------------------------------------------------------
    # Scientific Formatting: Module 5 (Matrix Hamiltonian)
    # -------------------------------------------------------------
    "hamiltonian.title": "📘 MATRIX HAMILTONIAN DIAGONALIZATION & TIME EVOLUTION",
    "hamiltonian.intro": (
        "We analyze the matrix Hamiltonian operator Ĥ, verifying self-adjointness, "
        "computing eigenvalues and eigenvectors, the spectral excitation gap, and time evolution."
    ),
    "hamiltonian.matrix_repr": "  Hamiltonian Matrix H:\n{matrix}",
    "hamiltonian.step1_title": "🔹 STEP 1: Hermiticity Verification (H = H†)",
    "hamiltonian.residual_line": "  Hermiticity Residual: ||H - H†||_max = {res:.2e}",
    "hamiltonian.hermitian_yes": "  Is it Hermitian?: YES (Closed system with 100% real eigenvalues)",
    "hamiltonian.hermitian_no": "  Is it Hermitian?: NO (Non-self-adjoint matrix; open / dissipative system model)",
    "hamiltonian.hermitian_exact": "  Is it Hermitian?: YES (Exact self-adjoint, guaranteed real eigenvalues)",
    "hamiltonian.hermitian_approx": "  Is it Hermitian?: NEARLY HERMITIAN (Numerical residual ||H - H†|| = {res:.2e})",
    "hamiltonian.non_hermitian": "  Is it Hermitian?: NO (Effective non-Hermitian model / dissipative or gain dynamics)",
    "hamiltonian.step2_title": "🔹 STEP 2: Energy Levels (Eigenvalues) & Eigenstates (|Eₙ⟩)",
    "hamiltonian.eigen_residual_info": "  Maximum eigenpair residual ||Hv - λv||: {res:.2e}",
    "hamiltonian.eigen_level_real": "  Level E_{idx} = {val:+.6f}   -->   Eigenstate |E_{idx}⟩ = [ {vec} ]ᵀ\n",
    "hamiltonian.eigen_level_complex": "  Eigenvalue λ_{idx} = {val_str}   -->   Eigenvector = [ {vec} ]ᵀ\n",
    "hamiltonian.step3_title": "🔹 STEP 3: Quantum Excitation Gap (ΔE)",
    "hamiltonian.gap_info": (
        "  Ground state E₀ = {E0:.6f}\n"
        "  Quantum gap to first distinct excited level: ΔE = {gap:.6f}\n"
        "  Associated Bohr frequency: ω = ΔE / ℏ = {freq:.6f} rad / time unit (natural units ℏ = 1)"
    ),
    "hamiltonian.gap_degenerate_note": "  (Ground level degeneracy detected; gap measured to the first distinct higher level).",
    "hamiltonian.gap_degenerate_spectrum": "0.0000 (Fully degenerate spectrum; no distinct higher excited level).",
    "hamiltonian.non_hermitian_warning": (
        "⚠️ ATTENTION: As this is a non-Hermitian matrix, eigenvalues possess complex parts "
        "or the operator is not self-adjoint. Imaginary parts correspond to damping/decay rates "
        "or gain in open or effective quantum systems."
    ),
    "hamiltonian.step4_title": "🔹 STEP 4: Quantum Dynamics & Time Evolution |ψ(t)⟩ = exp(-iHt/ℏ)|ψ(0)⟩",
    "hamiltonian.evolution_unitary": (
        "  Elapsed time: t = {t} (in units ℏ = 1)\n"
        "  Initial state:   |ψ(0)⟩ = [ {psi_0} ]ᵀ  (Norm = {norm_0:.6f})\n"
        "  Evolved state:   |ψ(t)⟩ = [ {psi_t} ]ᵀ  (Norm = {norm_t:.6f})\n"
        "  Unitary conservation: State norm is strictly conserved."
    ),
    "hamiltonian.evolution_non_unitary": (
        "  Elapsed time: t = {t} (in units ℏ = 1)\n"
        "  Initial state:   |ψ(0)⟩ = [ {psi_0} ]ᵀ  (Norm = {norm_0:.6f})\n"
        "  Evolved state:   |ψ(t)⟩ = [ {psi_t} ]ᵀ  (Norm = {norm_t:.6f})\n"
        "  Non-unitary evolution (quantum dissipation / gain): Norm varies due to non-Hermiticity of H."
    ),
    "hamiltonian.evolution_unitary_renorm": (
        "  Elapsed time: t = {t} (in units ℏ = 1)\n"
        "  Entered vector:   |ψ_raw(0)⟩ = [ {psi_0_raw} ]ᵀ  (Norm = {norm_0:.6f})\n"
        "  Normalized state: |ψ(0)⟩     = [ {psi_0_norm} ]ᵀ  (Norm = 1.000000)\n"
        "  Evolved state:    |ψ(t)⟩     = [ {psi_t} ]ᵀ  (Norm = {norm_t:.6f})\n"
        "  Unitary conservation: Normalized state norm is strictly conserved."
    ),
    "hamiltonian.evolution_non_unitary_renorm": (
        "  Elapsed time: t = {t} (in units ℏ = 1)\n"
        "  Entered vector:   |ψ_raw(0)⟩ = [ {psi_0_raw} ]ᵀ  (Norm = {norm_0:.6f})\n"
        "  Normalized state: |ψ(0)⟩     = [ {psi_0_norm} ]ᵀ  (Norm = 1.000000)\n"
        "  Evolved state:    |ψ(t)⟩     = [ {psi_t} ]ᵀ  (Norm = {norm_t:.6f})\n"
        "  Non-unitary evolution (quantum dissipation / gain): Norm varies due to non-Hermiticity of H."
    ),

    # -------------------------------------------------------------
    # Scientific & Parser Error Messages
    # -------------------------------------------------------------
    "error.empty_expression": "Mathematical expression cannot be empty.",
    "error.input_too_long": "Expression length ({length}) exceeds allowed limit ({max_len} characters).",
    "error.ast_too_deep": "Expression is too complex or nested (depth or limit exceeded).",
    "error.too_complex_nodes": "Expression is too complex: contains {count} AST nodes (limit: {max_nodes}).",
    "error.exponent_too_large": "Numerical exponent ({exp}) exceeds maximum allowed limit ({max_exp}).",
    "error.power_nested_too_deep": "Excessive nested powers detected in expression.",
    "error.int_too_large": "Integer exceeds safe limit of {max_digits} digits.",
    "error.forbidden_node": "Disallowed syntax construct: {node}.",
    "error.forbidden_function": "Disallowed mathematical function: '{func}'.",
    "error.forbidden_variable": "Disallowed variable or constant: '{name}'.",
    "error.func_without_parens": "'{name}' is a function and must be called with parentheses, e.g. {name}(x).",
    "error.unsupported_unary": "Unsupported unary operator: {op}.",
    "error.unsupported_binary": "Unsupported binary operator: {op}.",
    "error.invalid_call": "Only direct named function calls are permitted.",
    "error.invalid_call_kwargs": "Keyword arguments are not allowed in mathematical functions.",
    "error.unsafe_attribute": "Attribute access is not allowed.",
    "error.syntax_invalid": "Invalid mathematical syntax: {detail}",
    "error.null_state_rejected": "Quantum state cannot be the null function (ψ = 0). The zero vector is never an eigenstate. Norm would be zero.",
    "error.norm_zero_or_negative": "Density integral |ψ|² is zero or non-positive; state is not normalizable.",
    "error.norm_divergent": "Normalization integral diverges (∞) or does not converge analytically on domain. ψ ∉ L².",
    "error.asymptotic_divergence_neg_inf": "Wave function diverges towards infinity as x -> -oo; not normalizable in L².",
    "error.asymptotic_divergence_pos_inf": "Wave function diverges towards infinity as x -> +oo; not normalizable in L².",
    "error.well_inverted_limits": "Lower limit a={a} is strictly greater than upper limit b={b} (a > b yields invalid probabilities).",
    "error.quantum_number_integer_positive": "Quantum number 'n' must be a strictly positive integer (n >= 1).",
    "error.quantum_number_integer_non_negative": "Quantum number 'n' must be a non-negative integer (n >= 0).",
    "error.quantum_number_fractional": "Quantum number 'n' cannot be fractional. Enter a valid integer.",
    "error.well_width_positive": "Well width 'L' must be a strictly positive real number (L > 0).",
    "error.well_width_invalid": "Well width 'L' is invalid or non-finite.",
    "error.tunnel_param_finite": "Parameter '{name}' must be a finite real numerical value.",
    "error.tunnel_param_positive": "Parameter '{name}' must be non-negative.",
    "error.matrix_not_square": "Matrix must be square (N×N), but has dimensions {rows}×{cols}.",
    "error.matrix_empty": "Matrix input is empty.",
    "error.matrix_no_rows": "No valid rows found in matrix.",
    "error.matrix_empty_row": "Row {row} of the matrix is empty.",
    "error.matrix_ragged_rows": "Irregular row: row {row} has {len} elements, but row 1 has {expected}.",
    "error.matrix_non_finite": "Non-finite matrix element detected: '{val}'.",
    "error.matrix_invalid_val": "Invalid numeric value in matrix: '{val}'.",
    "error.matrix_max_dim": "Matrix dimension ({rows}×{cols}) exceeds allowed limit ({max_dim}×{max_dim}).",
    "error.matrix_invalid_format": "Invalid matrix format. Enter rows separated by ';' and elements by ','.",
    "error.state_vector_empty": "Initial state vector is empty.",
    "error.state_vector_invalid_component": "Invalid vector component: '{token}'.",
    "error.state_vector_non_finite": "Non-finite vector component: '{token}'.",
    "error.state_vector_no_components": "Could not extract numerical components from state vector.",
    "error.state_vector_dimension_mismatch": "State vector dimension ({vec_len}) does not match Hamiltonian dimension ({mat_dim}).",
    "error.state_vector_null": "State vector cannot be the null vector (zero norm).",
    "error.state_vector_invalid": "Invalid initial state vector: {detail}",
    "error.time_invalid": "Invalid time value 't': {detail}",
    "error.time_must_be_finite": "Time 't' must be a finite real number.",
    "error.calc_timeout": "Symbolic calculation exceeded safety timeout ({timeout} s).",
    "error.calc_cancelled": "Calculation was cancelled by the user.",
}
