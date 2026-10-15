"""
Pure scientific and quantum physics computational engine for QuantumLab.
Decoupled from Tkinter and GUI representations.
Implements rigorous physical invariants, domain checks, stable numerical methods.
Addresses DEF-01 (structured ScientificValidationError exceptions),
DEF-05 (natural units for Hamiltonian), DEF-06 (renormalized state presentation),
and DEF-07 (consistent parameter L substitution and propagation).
"""

from dataclasses import dataclass
from typing import Optional, List, Tuple
import sympy as sp
import numpy as np

from .errors import ScientificValidationError
from .parser import SafeASTParser, parse_parameters, parse_matrix, parse_state_vector

# Physical constants in SI
HBAR_SI = 1.054571817e-34       # J*s
M_ELECTRON_SI = 9.1093837e-31   # kg
EV_TO_JOULE = 1.602176634e-19    # J / eV
NM_TO_M = 1e-9                  # m / nm


@dataclass
class WaveFunctionResult:
    psi_raw: sp.Expr
    a: sp.Expr
    b: sp.Expr
    norm_integral: sp.Expr
    constante_A: sp.Expr
    psi_norm: sp.Expr
    exp_x: sp.Expr
    exp_x2: sp.Expr
    delta_x: sp.Expr
    d_psi: sp.Expr
    d2_psi: sp.Expr
    exp_p: sp.Expr
    exp_p2: sp.Expr
    delta_p: sp.Expr
    exp_T: sp.Expr
    delta_x_delta_p: sp.Expr
    heisenberg_cumple: bool
    heisenberg_nota: str
    es_autoadjunto_p: bool
    frontera_nota: str
    heisenberg_codigo: str = "fulfilled"


@dataclass
class Schrodinger1DResult:
    psi: sp.Expr
    V: sp.Expr
    d2_psi: sp.Expr
    termino_cinetico: sp.Expr
    termino_potencial: sp.Expr
    H_psi: sp.Expr
    energia: sp.Expr
    es_autoestado_formal: bool
    es_estado_fisico_ligado: bool
    mensaje_interpretacion: str


@dataclass
class InfiniteWellResult:
    n: int
    L: sp.Expr
    a_in: sp.Expr
    b_in: sp.Expr
    a_eff: sp.Expr
    b_eff: sp.Expr
    prob_simbolica: sp.Expr
    prob_numerica: float
    psi_n: sp.Expr
    energia_n: sp.Expr
    nota_dominio: str


@dataclass
class HarmonicOscillatorResult:
    n: int
    psi_n: sp.Expr
    An: sp.Expr
    energia_n: sp.Expr
    d2_psi: sp.Expr
    H_psi: sp.Expr
    residuo_cero: bool


@dataclass
class TunnelingResult:
    E_ev: float
    V0_ev: float
    ancho_nm: float
    masa_kg: float
    regimen: str
    kappa_m_inv: float
    kappa_a: float
    T: float
    R: float
    explicacion_fisica: str


@dataclass
class HamiltonianResult:
    H: np.ndarray
    es_hermitica: bool
    residual_hermitico: float
    energias: np.ndarray
    autovectores: np.ndarray
    brecha: Optional[float]
    es_degenerado: bool
    max_residuo_autovector: float = 0.0
    evolucion_t: Optional[float] = None
    psi_0: Optional[np.ndarray] = None
    psi_t: Optional[np.ndarray] = None
    norma_psi_t: Optional[float] = None
    psi_0_norm: Optional[np.ndarray] = None
    norma_psi_0: Optional[float] = None


# =====================================================================
# 1. FUNCIÓN DE ONDA Y OBSERVABLES (QL-002, QL-004, QL-005, QL-020)
# =====================================================================
def analizar_funcion_onda(psi_raw: sp.Expr, a: sp.Expr, b: sp.Expr) -> WaveFunctionResult:
    x = SafeASTParser.x
    hbar = SafeASTParser.hbar
    m = SafeASTParser.m

    # QL-004: Validate non-zero state
    if psi_raw == 0 or psi_raw.is_zero:
        raise ScientificValidationError("error.null_state_rejected")

    # Rapid asymptotic divergence check for unbounded wave functions on infinite domains
    if a == -sp.oo:
        try:
            lim_neg = sp.limit(sp.Abs(psi_raw), x, -sp.oo)
            if lim_neg in (sp.oo, -sp.oo, sp.zoo):
                raise ScientificValidationError("error.asymptotic_divergence_neg_inf")
        except Exception as e:
            if isinstance(e, ScientificValidationError):
                raise
    if b == sp.oo:
        try:
            lim_pos = sp.limit(sp.Abs(psi_raw), x, sp.oo)
            if lim_pos in (sp.oo, -sp.oo, sp.zoo):
                raise ScientificValidationError("error.asymptotic_divergence_pos_inf")
        except Exception as e:
            if isinstance(e, ScientificValidationError):
                raise

    # Compute norm integral
    densidad = sp.simplify(sp.conjugate(psi_raw) * psi_raw)
    norm_integral = sp.integrate(densidad, (x, a, b))

    # Check finite, real, strictly positive integral
    if norm_integral == 0 or (norm_integral.is_number and norm_integral <= 0):
        raise ScientificValidationError("error.norm_zero_or_negative")
    if norm_integral in (sp.oo, -sp.oo, sp.zoo, sp.nan) or not norm_integral.is_finite:
        raise ScientificValidationError("error.norm_divergent")

    constante_A = sp.simplify(1 / sp.sqrt(norm_integral))
    psi_norm = sp.simplify(constante_A * psi_raw)

    # Position observables
    exp_x = sp.simplify(sp.integrate(sp.conjugate(psi_norm) * x * psi_norm, (x, a, b)))
    exp_x2 = sp.simplify(sp.integrate(sp.conjugate(psi_norm) * (x**2) * psi_norm, (x, a, b)))
    var_x = sp.simplify(exp_x2 - exp_x**2)
    delta_x = sp.simplify(sp.sqrt(var_x))

    # Derivatives
    d_psi = sp.diff(psi_norm, x)
    d2_psi = sp.diff(psi_norm, x, 2)

    # Momentum observables
    exp_p = sp.simplify(sp.integrate(sp.conjugate(psi_norm) * (-sp.I * hbar * d_psi), (x, a, b)))
    exp_p2 = sp.simplify(sp.integrate(sp.conjugate(psi_norm) * (-hbar**2 * d2_psi), (x, a, b)))
    var_p = sp.simplify(exp_p2 - exp_p**2)
    delta_p = sp.simplify(sp.sqrt(var_p))
    exp_T = sp.simplify(exp_p2 / (2 * m))

    # QL-005: Check boundary terms for momentum operator self-adjointness: [|ψ|²]_a^b
    try:
        psi_a = psi_norm.subs(x, a)
        psi_b = psi_norm.subs(x, b)
        term_frontera = sp.simplify(sp.conjugate(psi_b) * psi_b - sp.conjugate(psi_a) * psi_a)
        es_autoadjunto_p = (term_frontera == 0)
    except Exception:
        es_autoadjunto_p = False

    if es_autoadjunto_p:
        frontera_nota = "El término de contorno [|ψ|²] desaparece en los extremos del dominio (autoadjunción compatible)."
    else:
        frontera_nota = (
            "ADVERTENCIA DE CONTORNO: [|ψ|²] no se anula en los extremos. En intervalos acotados sin "
            "condiciones de contorno periódicas o Dirichlet, el operador p̂ = -iℏ∂x no es autoadjunto estándar, "
            "lo cual puede falsear los momentos calculados."
        )

    # QL-002: Heisenberg evaluation
    delta_x_delta_p = sp.simplify(delta_x * delta_p)

    heisenberg_cumple = False
    heisenberg_nota = ""
    heisenberg_codigo = "indeterminate"

    if delta_p == 0 or delta_x == 0:
        heisenberg_cumple = False
        heisenberg_codigo = "zero_dispersion"
        heisenberg_nota = (
            "NO VERIFICABLE / DISPERSIÓN NULA: Uno de los desvíos calculados formalmente es cero "
            "(Δp = 0 o Δx = 0). En un dominio finito, p̂ no posee autovectores en el dominio autoadjunto, "
            "por lo que el producto nulo NO satisface el principio de incertidumbre canónico (Δx·Δp ≥ ℏ/2)."
        )
    elif not es_autoadjunto_p and (a != -sp.oo or b != sp.oo):
        heisenberg_cumple = False
        heisenberg_codigo = "open_boundary"
        heisenberg_nota = (
            "CONDICIONES DE CONTORNO NO ESTÁNDAR: El principio canónico Δx·Δp ≥ ℏ/2 presupone autoadjunción "
            "en toda la recta ℝ o condiciones de frontera periódicas. En un intervalo acotado con frontera abierta, "
            "el producto formal no es una prueba concluyente del principio de Heisenberg."
        )
    else:
        # Check inequality delta_x * delta_p >= hbar/2
        diferencia = sp.simplify(delta_x_delta_p - hbar / 2)
        try:
            if diferencia.is_nonnegative is True or (diferencia.is_number and float(diferencia.evalf()) >= -1e-12):
                heisenberg_cumple = True
                heisenberg_codigo = "fulfilled"
                heisenberg_nota = "El estado satisface rigurosamente el Principio de Incertidumbre de Heisenberg: Δx·Δp ≥ ℏ/2."
            elif diferencia.is_negative is True or (diferencia.is_number and float(diferencia.evalf()) < -1e-12):
                heisenberg_cumple = False
                heisenberg_codigo = "violated"
                heisenberg_nota = "El producto de incertidumbres formal viola la cota ℏ/2 debido a las condiciones de frontera o dominio."
            else:
                heisenberg_cumple = False
                heisenberg_codigo = "indeterminate"
                heisenberg_nota = (
                    "INDETERMINADO: No se pudo demostrar formalmente la desigualdad canónica Δx·Δp ≥ ℏ/2 "
                    "con las hipótesis simbólicas actuales."
                )
        except Exception:
            heisenberg_cumple = False
            heisenberg_codigo = "indeterminate"
            heisenberg_nota = (
                "INDETERMINADO: No se pudo evaluar formalmente la desigualdad canónica Δx·Δp ≥ ℏ/2 "
                "para este estado."
            )

    return WaveFunctionResult(
        psi_raw=psi_raw, a=a, b=b,
        norm_integral=norm_integral, constante_A=constante_A, psi_norm=psi_norm,
        exp_x=exp_x, exp_x2=exp_x2, delta_x=delta_x,
        d_psi=d_psi, d2_psi=d2_psi,
        exp_p=exp_p, exp_p2=exp_p2, delta_p=delta_p, exp_T=exp_T,
        delta_x_delta_p=delta_x_delta_p,
        heisenberg_cumple=heisenberg_cumple,
        heisenberg_nota=heisenberg_nota,
        es_autoadjunto_p=es_autoadjunto_p,
        frontera_nota=frontera_nota,
        heisenberg_codigo=heisenberg_codigo
    )


# =====================================================================
# 2. SCHRÖDINGER 1D (QL-006, QL-007, QL-021)
# =====================================================================
def analizar_schrodinger_1d(psi: sp.Expr, V: sp.Expr, a: sp.Expr = None, b: sp.Expr = None) -> Schrodinger1DResult:
    x = SafeASTParser.x
    hbar = SafeASTParser.hbar
    m = SafeASTParser.m

    # QL-006: Null state rejected
    if psi == 0 or psi.is_zero:
        raise ScientificValidationError("error.null_state_rejected")

    d2_psi = sp.diff(psi, x, 2)
    termino_cinetico = sp.simplify(-(hbar**2 / (2 * m)) * d2_psi)
    termino_potencial = sp.simplify(V * psi)
    H_psi = sp.simplify(termino_cinetico + termino_potencial)

    # Compute energy quotient E = H psi / psi
    energia = sp.simplify(H_psi / psi)
    depende_de_x = x in energia.free_symbols

    # Verify algebraic residual: H psi - E psi = 0
    residuo = sp.simplify(H_psi - energia * psi)
    es_autoestado_formal = (not depende_de_x) and (residuo == 0) and (energia not in (sp.nan, sp.zoo, sp.oo, -sp.oo))

    # QL-007: Check normalizability and physical admissibility
    es_estado_fisico_ligado = False
    if es_autoestado_formal:
        dom_a = a if a is not None else -sp.oo
        dom_b = b if b is not None else sp.oo
        try:
            norm_int = sp.integrate(sp.conjugate(psi) * psi, (x, dom_a, dom_b))
            if norm_int.is_finite and norm_int != 0 and norm_int not in (sp.oo, sp.zoo, sp.nan):
                es_estado_fisico_ligado = True
        except Exception:
            es_estado_fisico_ligado = False

    # Construct interpretation message
    if es_autoestado_formal:
        if es_estado_fisico_ligado:
            mensaje = (
                f"AUTOESTADO FÍSICO EXACTO: La energía E = {energia} es constante e independiente de 'x'. "
                f"Además, ψ(x) es de cuadrado integrable en el dominio indicado, constituyendo un estado estacionario físico ligado."
            )
        else:
            mensaje = (
                f"SOLUCIÓN FORMAL LOCAL: La función satisface formalmente Ĥψ = Eψ con autovalor E = {energia}, "
                f"pero no es un estado ligado normalizable en L²(ℝ) (puede corresponder a un estado de dispersión o solución no integrable)."
            )
    else:
        mensaje = (
            f"NO ES UNA FUNCIÓN PROPIA: El cociente E(x) = {energia} depende de la posición 'x' "
            f"(o el residuo Ĥψ - Eψ ≠ 0). Por lo tanto, ψ(x) no es un autoestado del Hamiltoniano bajo el potencial V(x). "
            f"Nota: No se puede deducir sin análisis espectral formal si el estado pertenece al espectro continuo o es una combinación lineal."
        )

    return Schrodinger1DResult(
        psi=psi, V=V, d2_psi=d2_psi,
        termino_cinetico=termino_cinetico,
        termino_potencial=termino_potencial,
        H_psi=H_psi, energia=energia,
        es_autoestado_formal=es_autoestado_formal,
        es_estado_fisico_ligado=es_estado_fisico_ligado,
        mensaje_interpretacion=mensaje
    )


# =====================================================================
# 3. POZO DE POTENCIAL INFINITO (QL-008, QL-009, QL-010, DEF-07)
# =====================================================================
def analizar_pozo_infinito(a: sp.Expr, b: sp.Expr, n_val: int = 1, L_val: sp.Expr = None) -> InfiniteWellResult:
    x = SafeASTParser.x
    hbar = SafeASTParser.hbar
    m = SafeASTParser.m

    # QL-010: Validate n positive integer, rejecting fractional inputs
    if isinstance(n_val, float):
        if not n_val.is_integer():
            raise ScientificValidationError("error.quantum_number_fractional", n=n_val)
        n_val = int(n_val)

    if not isinstance(n_val, int) or n_val < 1:
        raise ScientificValidationError("error.quantum_number_integer_positive", n=n_val)

    # DEF-07: Process and propagate L_val consistently
    if L_val is not None:
        if isinstance(L_val, (int, float)):
            if L_val <= 0 or not np.isfinite(L_val):
                raise ScientificValidationError("error.well_width_positive", L=L_val)
            L_num = float(L_val)
            L = sp.Integer(int(L_val)) if float(L_val).is_integer() else sp.Float(L_val)
        elif isinstance(L_val, sp.Expr):
            try:
                L_num = float(L_val.evalf())
                if L_num <= 0 or not np.isfinite(L_num):
                    raise ScientificValidationError("error.well_width_positive", L=L_num)
            except Exception as err:
                if isinstance(err, ScientificValidationError):
                    raise
                raise ScientificValidationError("error.well_width_invalid", L=str(L_val))
            L = L_val
        else:
            try:
                L_num = float(L_val)
                if L_num <= 0 or not np.isfinite(L_num):
                    raise ScientificValidationError("error.well_width_positive", L=L_val)
                L = sp.sympify(L_val)
            except Exception as err:
                if isinstance(err, ScientificValidationError):
                    raise
                L = SafeASTParser.L
                L_num = 1.0

        # DEF-07: Propagate L to integration bounds a and b
        a_sub = sp.simplify(a.subs(SafeASTParser.L, L))
        b_sub = sp.simplify(b.subs(SafeASTParser.L, L))
    else:
        L = SafeASTParser.L
        L_num = 1.0
        a_sub = a
        b_sub = b

    # QL-009: Check a <= b with respect to L_num
    try:
        a_f = float(a_sub.subs(SafeASTParser.L, L_num).subs(L, L_num).evalf())
        b_f = float(b_sub.subs(SafeASTParser.L, L_num).subs(L, L_num).evalf())
        if a_f > b_f:
            raise ScientificValidationError("error.well_inverted_limits", a=a, b=b)
    except ScientificValidationError:
        raise
    except Exception:
        a_f, b_f = 0.0, L_num

    # QL-008: Physical domain is strictly [0, L] where density is (2/L)*sin^2(n*pi*x/L), and 0 outside.
    eff_a = max(0.0, a_f)
    eff_b = min(L_num, b_f)

    nota_dominio = ""
    if a_f < 0.0 or b_f > L_num:
        nota_dominio = (
            f"ACUMULACIÓN FÍSICA: El pozo infinito tiene paredes impenetrables en x=0 y x=L. "
            f"La densidad de probabilidad es estrictamente 0 fuera de [0, L]. "
            f"La integral sobre [{a}, {b}] se evalúa eficazmente en la intersección con el pozo."
        )

    # Normalized eigenstate and energy formula with L
    psi_n = sp.sqrt(2 / L) * sp.sin(n_val * sp.pi * x / L)
    energia_n = (n_val**2 * sp.pi**2 * hbar**2) / (2 * m * L**2)

    # Physical wave function density is strictly zero outside [0, L]
    densidad_caja = sp.Piecewise(
        (psi_n**2, sp.And(x >= 0, x <= L)),
        (0, True)
    )

    # DEF-07: Symbolic integral over [a_sub, b_sub] respecting identical physical domain [0, L]
    prob_simbolica = sp.integrate(densidad_caja, (x, a_sub, b_sub))

    # Calculate exact clamped numerical probability
    if eff_a >= eff_b:
        prob_numerica = 0.0
    else:
        def int_sin2_box(u):
            return (u / L_num) - np.sin(2.0 * n_val * np.pi * u / L_num) / (2.0 * n_val * np.pi)

        prob_numerica = float(int_sin2_box(eff_b) - int_sin2_box(eff_a))
        prob_numerica = max(0.0, min(1.0, prob_numerica))

    return InfiniteWellResult(
        n=n_val, L=L, a_in=a, b_in=b,
        a_eff=sp.sympify(eff_a), b_eff=sp.sympify(eff_b),
        prob_simbolica=prob_simbolica,
        prob_numerica=prob_numerica,
        psi_n=psi_n, energia_n=energia_n,
        nota_dominio=nota_dominio
    )


# =====================================================================
# 4. OSCILADOR ARMÓNICO CUÁNTICO (QL-011)
# =====================================================================
def analizar_oscilador_armonico(n_val: int = 0) -> HarmonicOscillatorResult:
    x = SafeASTParser.x
    hbar = SafeASTParser.hbar
    m = SafeASTParser.m
    w = SafeASTParser.w

    if isinstance(n_val, float):
        if not n_val.is_integer():
            raise ScientificValidationError("error.quantum_number_fractional", n=n_val)
        n_val = int(n_val)

    if not isinstance(n_val, int) or n_val < 0:
        raise ScientificValidationError("error.quantum_number_integer_non_negative", n=n_val)

    # Dimensionless coordinate xi = sqrt(m*w/hbar) * x
    xi = sp.sqrt(m * w / hbar) * x
    hermite_poly = sp.hermite(n_val, xi)

    # Normalization factor
    An = (1 / sp.sqrt(2**n_val * sp.factorial(n_val))) * ((m * w / (sp.pi * hbar)) ** sp.Rational(1, 4))
    psi_n = An * sp.exp(-m * w * x**2 / (2 * hbar)) * hermite_poly
    energia_n = hbar * w * (n_val + sp.Rational(1, 2))

    # Apply Hamiltonian H = -(hbar^2 / 2m) d^2/dx^2 + (1/2) m w^2 x^2
    d2_psi = sp.diff(psi_n, x, 2)
    V = sp.Rational(1, 2) * m * w**2 * x**2
    H_psi = sp.simplify(-(hbar**2 / (2 * m)) * d2_psi + V * psi_n)

    # Verify H psi - E_n psi == 0
    residuo = sp.simplify(H_psi - energia_n * psi_n)
    residuo_cero = (residuo == 0)

    return HarmonicOscillatorResult(
        n=n_val,
        psi_n=psi_n,
        An=An,
        energia_n=energia_n,
        d2_psi=d2_psi,
        H_psi=H_psi,
        residuo_cero=residuo_cero
    )


# =====================================================================
# 5. EFECTO TÚNEL EN BARRERA RECTANGULAR (QL-012, QL-022, QL-031)
# =====================================================================
def analizar_efecto_tunel(E_ev: float = 3.2, V0_ev: float = 5.0, ancho_nm: float = 0.5, masa_kg: float = M_ELECTRON_SI) -> TunnelingResult:
    # Validate finite real values
    for val, name in [(E_ev, "E"), (V0_ev, "V0"), (ancho_nm, "a"), (masa_kg, "m")]:
        if not isinstance(val, (int, float)) or not np.isfinite(val):
            raise ScientificValidationError("error.tunnel_param_finite", name=name)

    if E_ev < 0:
        raise ScientificValidationError("error.tunnel_param_positive", name="E", val=E_ev)
    if V0_ev <= 0:
        raise ScientificValidationError("error.tunnel_param_positive", name="V0", val=V0_ev)
    if ancho_nm < 0:
        raise ScientificValidationError("error.tunnel_param_positive", name="a", val=ancho_nm)
    if masa_kg <= 0:
        raise ScientificValidationError("error.tunnel_param_positive", name="m", val=masa_kg)

    ancho_m = ancho_nm * NM_TO_M

    # Boundary cases
    if ancho_nm == 0.0:
        return TunnelingResult(
            E_ev=E_ev, V0_ev=V0_ev, ancho_nm=ancho_nm, masa_kg=masa_kg,
            regimen="Barrera de espesor nulo (a=0)",
            kappa_m_inv=0.0, kappa_a=0.0,
            T=1.0, R=0.0,
            explicacion_fisica="Con espesor a = 0 nm, la barrera no existe y la transmisión cuántica es del 100% (T=1)."
        )

    if E_ev == 0.0:
        return TunnelingResult(
            E_ev=E_ev, V0_ev=V0_ev, ancho_nm=ancho_nm, masa_kg=masa_kg,
            regimen="Partícula en reposo (E=0)",
            kappa_m_inv=0.0, kappa_a=0.0,
            T=0.0, R=1.0,
            explicacion_fisica="Con energía nula E = 0 eV, la probabilidad de transmisión a través de la barrera es 0% (T=0)."
        )

    # Regime 1: E < V0 (Quantum Tunneling)
    if E_ev < V0_ev:
        diff_j = (V0_ev - E_ev) * EV_TO_JOULE
        kappa = np.sqrt(2 * masa_kg * diff_j) / HBAR_SI
        kappa_a = kappa * ancho_m

        if kappa_a > 30.0:
            log_prefactor = np.log(16.0 * E_ev * (V0_ev - E_ev) / (V0_ev**2))
            log_T = log_prefactor - 2.0 * kappa_a
            T = float(np.exp(log_T)) if log_T > -700 else 0.0
        else:
            sinh_val = np.sinh(kappa_a)
            denom = 1.0 + (V0_ev**2 * sinh_val**2) / (4.0 * E_ev * (V0_ev - E_ev))
            T = float(1.0 / denom)

        regimen = f"Túnel Cuántico (E < V₀: {E_ev:.3f} eV < {V0_ev:.3f} eV)"
        explicacion = (
            f"En física clásica la partícula rebotaría con certeza (E < V₀). En mecánica cuántica, la función de onda "
            f"dentro de la barrera finita es una combinación lineal de ondas evanescentes e^(-κx) y reflexiones internas e^(κx), "
            f"emergiendo con una probabilidad de transmisión real no nula de T = {T:.6e} ({T*100:.4f}%)."
        )

    # Regime 2: E == V0 (Critical Threshold)
    elif np.isclose(E_ev, V0_ev, atol=1e-9):
        regimen = f"Umbral Crítico (E = V₀ = {V0_ev:.3f} eV)"
        kappa = 0.0
        kappa_a = 0.0
        V0_j = V0_ev * EV_TO_JOULE
        denom = 1.0 + (masa_kg * V0_j * ancho_m**2) / (2.0 * HBAR_SI**2)
        T = float(1.0 / denom)
        explicacion = (
            f"En el umbral exacto E = V₀, la función de onda dentro de la barrera es lineal ψ(x) = C·x + D. "
            f"El coeficiente de transmisión es T = [1 + m·V₀·a² / (2ℏ²)]⁻¹ = {T:.6f} ({T*100:.2f}%)."
        )

    # Regime 3: E > V0 (Over-the-barrier transmission / resonances)
    else:
        diff_j = (E_ev - V0_ev) * EV_TO_JOULE
        k_prime = np.sqrt(2 * masa_kg * diff_j) / HBAR_SI
        kappa = k_prime
        kappa_a = k_prime * ancho_m
        sin_val = np.sin(k_prime * ancho_m)
        denom = 1.0 + (V0_ev**2 * sin_val**2) / (4.0 * E_ev * (E_ev - V0_ev))
        T = float(1.0 / denom)
        regimen = f"Transmisión sobre la Barrera (E > V₀: {E_ev:.3f} eV > {V0_ev:.3f} eV)"
        explicacion = (
            f"Con energía superior a la barrera (E > V₀), la física clásica predeciría paso al 100%. "
            f"En mecánica cuántica se produce reflexión cuántica por discontinuidad de potencial, con resonancias "
            f"cuando k'a = nπ (T=1). Transmisión actual: T = {T:.6f} ({T*100:.2f}%)."
        )

    T = max(0.0, min(1.0, T))
    R = 1.0 - T

    return TunnelingResult(
        E_ev=E_ev, V0_ev=V0_ev, ancho_nm=ancho_nm, masa_kg=masa_kg,
        regimen=regimen, kappa_m_inv=kappa, kappa_a=kappa_a,
        T=T, R=R, explicacion_fisica=explicacion
    )


def _expm_numpy(A: np.ndarray) -> np.ndarray:
    """
    Computes matrix exponential exp(A) in pure NumPy using scaling and squaring with Taylor expansion.
    Completely eliminates dependency on SciPy.
    """
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ScientificValidationError("error.matrix_not_square", rows=A.shape[0], cols=A.shape[1] if A.ndim > 1 else 1)

    norm_inf = float(np.max(np.sum(np.abs(A), axis=1)))
    if norm_inf == 0.0:
        return np.eye(A.shape[0], dtype=complex)

    s = max(0, int(np.ceil(np.log2(norm_inf / 0.5)))) if norm_inf > 0.5 else 0
    B = A / (2.0 ** s)

    p = 18
    n = A.shape[0]
    X = np.eye(n, dtype=complex)
    term = np.eye(n, dtype=complex)
    for k in range(1, p + 1):
        term = (term @ B) / k
        X = X + term

    for _ in range(s):
        X = X @ X

    return X


# =====================================================================
# 6. HAMILTONIANO MATRICIAL Y EVOLUCIÓN TEMPORAL (QL-003, QL-013, QL-014, QL-015, QL-023, QL-032, DEF-05, DEF-06)
# =====================================================================
def analizar_hamiltoniano_matricial(
    H: np.ndarray,
    psi_0: Optional[np.ndarray] = None,
    t_val: Optional[float] = None
) -> HamiltonianResult:
    if H.ndim != 2 or H.shape[0] != H.shape[1]:
        raise ScientificValidationError("error.matrix_not_square", rows=H.shape[0], cols=H.shape[1] if H.ndim > 1 else 1)

    N = H.shape[0]

    # QL-013: Measure exact residual ||H - H†||_inf
    H_dagger = H.conj().T
    residual_hermitico = float(np.max(np.abs(H - H_dagger)))
    es_hermitica = (residual_hermitico <= 1e-12)

    if es_hermitica:
        H_calc = 0.5 * (H + H_dagger) if residual_hermitico > 0 else H
        energias, autovectores = np.linalg.eigh(H_calc)

        sort_idx = np.argsort(energias)
        energias = energias[sort_idx]
        autovectores = autovectores[:, sort_idx]

        residuos = [
            float(np.linalg.norm(H @ autovectores[:, j] - energias[j] * autovectores[:, j]))
            for j in range(len(energias))
        ]
        max_residuo_autovector = float(np.max(residuos)) if residuos else 0.0

        e0 = energias[0]
        brecha = None
        es_degenerado = False

        for val in energias[1:]:
            if abs(val - e0) > 1e-7:
                brecha = float(val - e0)
                break

        if brecha is None:
            brecha = 0.0
            es_degenerado = True
    else:
        energias, autovectores = np.linalg.eig(H)
        sort_idx = np.argsort(energias.real)
        energias = energias[sort_idx]
        autovectores = autovectores[:, sort_idx]
        brecha = None
        es_degenerado = False

        residuos = [
            float(np.linalg.norm(H @ autovectores[:, j] - energias[j] * autovectores[:, j]))
            for j in range(len(energias))
        ]
        max_residuo_autovector = float(np.max(residuos)) if residuos else 0.0

    # QL-015 / DEF-06: Time evolution |psi(t)> = exp(-i H t / hbar) |psi(0)>
    psi_t = None
    norma_psi_t = None
    psi_0_norm = None
    norma_psi_0 = None

    if psi_0 is not None:
        if len(psi_0) != N:
            raise ScientificValidationError(
                "error.state_vector_dimension_mismatch",
                vec_len=len(psi_0),
                mat_dim=N
            )

        # DEF-06: Keep raw entered vector and normalize for evolution
        norm0 = float(np.linalg.norm(psi_0))
        norma_psi_0 = norm0
        if norm0 > 1e-15:
            psi_0_norm = psi_0 / norm0
        else:
            raise ScientificValidationError("error.state_vector_null")

        t = t_val if t_val is not None else 0.0

        if es_hermitica:
            c = autovectores.conj().T @ psi_0_norm
            phases = np.exp(-1j * energias * t)  # natural units hbar = 1
            c_t = c * phases
            psi_t = autovectores @ c_t
            norma_psi_t = float(np.linalg.norm(psi_t))
        else:
            U = _expm_numpy(-1j * H * t)
            psi_t = U @ psi_0_norm
            norma_psi_t = float(np.linalg.norm(psi_t))

    return HamiltonianResult(
        H=H,
        es_hermitica=es_hermitica,
        residual_hermitico=residual_hermitico,
        energias=energias,
        autovectores=autovectores,
        brecha=brecha,
        es_degenerado=es_degenerado,
        max_residuo_autovector=max_residuo_autovector,
        evolucion_t=t_val,
        psi_0=psi_0,
        psi_t=psi_t,
        norma_psi_t=norma_psi_t,
        psi_0_norm=psi_0_norm,
        norma_psi_0=norma_psi_0,
    )


def evolucion_temporal_matricial(H: np.ndarray, psi_0: np.ndarray, t: float) -> Tuple[np.ndarray, float]:
    """Helper for pure time evolution calculation."""
    res = analizar_hamiltoniano_matricial(H, psi_0=psi_0, t_val=t)
    return res.psi_t, res.norma_psi_t
