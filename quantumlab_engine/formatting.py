"""
Decoupled formatting engine for QuantumLab.
Produces structured, human-readable step-by-step educational explanations
with tagged output blocks ('titulo', 'paso', 'explicacion', 'formula', 'conclusion', 'advertencia').
"""

from typing import List, Tuple
import sympy as sp
import numpy as np

from .physics import (
    WaveFunctionResult,
    Schrodinger1DResult,
    InfiniteWellResult,
    HarmonicOscillatorResult,
    TunnelingResult,
    HamiltonianResult,
)


def formatear_analisis_onda(res: WaveFunctionResult) -> List[Tuple[str, str]]:
    bloques = [
        ("📘 ANÁLISIS CUÁNTICO COMPLETO DE LA FUNCIÓN DE ONDA ψ(x)", "titulo"),
        (
            "Vamos a analizar paso a paso el estado cuántico propuesto. Primero verificaremos la condición "
            "de normalización de Born, analizaremos las condiciones de contorno y extraeremos los observables "
            "físicos mediante operadores cuánticos autoadjuntos.",
            "explicacion"
        ),
        (f"  ψ_inicial(x) = {sp.pretty(res.psi_raw)}   en el dominio [{res.a}, {res.b}]", "formula"),

        ("🔹 PASO 1: Condición de Normalización de Born y Cuadrado Integrable", "paso"),
        (
            "En mecánica cuántica, la probabilidad total de encontrar la partícula en el dominio debe ser estrictamente 1 (100%). "
            "Verificamos que la función sea de cuadrado integrable en el dominio:",
            "explicacion"
        ),
        (
            f"  ∫ |ψ(x)|² dx = {res.norm_integral}\n"
            f"  Constante de normalización: A = 1 / √({res.norm_integral}) = {res.constante_A}\n"
            f"  Función de onda normalizada: ψ(x) = {res.psi_norm}",
            "formula"
        ),
        (f"  {res.frontera_nota}", "advertencia" if not res.es_autoadjunto_p else "explicacion"),

        ("🔹 PASO 2: Valor Esperado de la Posición ⟨x⟩ y Dispersión Cuántica Δx", "paso"),
        (
            "Calculamos la posición media aplicando el operador posición x̂ en la base de coordenadas:",
            "explicacion"
        ),
        (
            f"  ⟨x⟩  = ∫ ψ*(x) · x · ψ(x) dx  = {res.exp_x}\n"
            f"  ⟨x²⟩ = ∫ ψ*(x) · x² · ψ(x) dx = {res.exp_x2}\n"
            f"  Incertidumbre en posición: Δx = √(⟨x²⟩ - ⟨x⟩²) = {res.delta_x}",
            "formula"
        ),

        ("🔹 PASO 3: Operador Momento Lineal p̂ = -iℏ(d/dx) y Energía Cinética ⟨T⟩", "paso"),
        (
            "Derivamos analíticamente la función de onda para aplicar el operador de momento y el Laplaciano unidimensional:",
            "explicacion"
        ),
        (
            f"  dψ/dx   = {res.d_psi}\n"
            f"  d²ψ/dx² = {res.d2_psi}\n"
            f"  ⟨p⟩  = ∫ ψ*(x) · (-iℏ·d/dx) · ψ(x) dx = {res.exp_p}\n"
            f"  ⟨p²⟩ = ∫ ψ*(x) · (-ℏ²·d²/dx²) · ψ(x) dx = {res.exp_p2}\n"
            f"  Incertidumbre en momento: Δp = √(⟨p²⟩ - ⟨p⟩²) = {res.delta_p}\n"
            f"  Energía Cinética media: ⟨T⟩ = ⟨p²⟩ / (2m) = {res.exp_T}",
            "formula"
        ),

        ("🔹 PASO 4: Principio de Incertidumbre de Heisenberg y Validación de Dominio", "paso"),
        (
            f"  Producto de incertidumbres: Δx · Δp = {res.delta_x_delta_p}\n"
            f"  Cota fundamental canónica:  ℏ/2",
            "formula"
        ),
        (
            f"💡 INTERPRETACIÓN CIENTÍFICA: Posición media ⟨x⟩ = {res.exp_x}, momento promedio ⟨p⟩ = {res.exp_p}.\n"
            f"{res.heisenberg_nota}",
            "conclusion" if res.heisenberg_cumple else "advertencia"
        ),
    ]
    return bloques


def formatear_schrodinger(res: Schrodinger1DResult) -> List[Tuple[str, str]]:
    bloques = [
        ("📗 ECUACIÓN DE SCHRÖDINGER INDEPENDIENTE DEL TIEMPO (1D)", "titulo"),
        (
            "Evaluamos la acción del operador Hamiltoniano Ĥ = T̂ + V̂ sobre ψ(x) para verificar "
            "si se trata de un estado estacionario (autoestado) y determinar analíticamente su energía.",
            "explicacion"
        ),
        ("  Ecuación maestra:  [- (ℏ² / 2m) · d²/dx² + V(x)] ψ(x) = E · ψ(x)", "formula"),

        ("🔹 PASO 1: Derivada espacial de segundo orden", "paso"),
        (f"  ψ(x) = {res.psi}\n  d²ψ/dx² = {res.d2_psi}", "formula"),

        ("🔹 PASO 2: Acción del Operador Hamiltoniano Ĥ sobre el estado", "paso"),
        (
            f"  T̂ψ(x) = - (ℏ²/2m) · d²ψ/dx² = {res.termino_cinetico}\n"
            f"  V̂ψ(x) = V(x) · ψ(x) = {res.termino_potencial}\n"
            f"  Ĥψ(x) = T̂ψ + V̂ψ = {res.H_psi}",
            "formula"
        ),

        ("🔹 PASO 3: Análisis del Cociente de Energía E(x) = (Ĥψ) / ψ", "paso"),
        (f"  Cociente: E(x) = {res.energia}", "formula"),
        (f"💡 INTERPRETACIÓN FÍSICA: {res.mensaje_interpretacion}", "conclusion" if res.es_autoestado_formal else "advertencia"),
    ]
    return bloques


def formatear_pozo_infinito(res: InfiniteWellResult) -> List[Tuple[str, str]]:
    bloques = [
        ("📙 PARTÍCULA EN UNA CAJA CUÁNTICA 1D (POZO DE POTENCIAL INFINITO)", "titulo"),
        (
            f"Una partícula de masa m confinada entre paredes impenetrables en [0, L] "
            f"se encuentra en el estado cuantizado con número cuántico n = {res.n}.",
            "explicacion"
        ),

        ("🔹 PASO 1: Autofunción Cuantizada y Nivel de Energía Eₙ", "paso"),
        (
            f"  ψₙ(x) = √(2/L) · sin({res.n}·π·x / L)   para 0 ≤ x ≤ L (cero en el exterior)\n"
            f"  E_{res.n}    = ({res.n}² · π² · ℏ²) / (2 · m · L²)",
            "formula"
        ),

        ("🔹 PASO 2: Probabilidad de Localización en la Región", "paso"),
        (
            f"  Región solicitada: [{res.a_in}, {res.b_in}]\n"
            f"  Integral simbólica: P = ∫ |ψₙ(x)|² dx = {res.prob_simbolica}\n"
            f"  Probabilidad calculada: P = {res.prob_numerica:.6f} ({res.prob_numerica * 100:.2f}%)",
            "formula"
        ),
    ]
    if res.nota_dominio:
        bloques.append((f"⚠️ {res.nota_dominio}", "advertencia"))

    bloques.append((
        f"💡 INTERPRETACIÓN FÍSICA: Para el nivel n = {res.n}, la interferencia cuántica modula la probabilidad de detección. "
        f"La probabilidad en la región solicitada es del {res.prob_numerica * 100:.2f}% "
        f"(frente a una distribución uniforme clásica).",
        "conclusion"
    ))
    return bloques


def formatear_oscilador(res: HarmonicOscillatorResult) -> List[Tuple[str, str]]:
    bloques = [
        (f"📕 OSCILADOR ARMÓNICO CUÁNTICO (NIVEL n = {res.n})", "titulo"),
        (
            "El oscilador armónico cuántico describe sistemas en potenciales parabólicos V(x) = ½ m ω² x². "
            "Sus soluciones analíticas son polinomios de Hermite modulados por una gaussiana.",
            "explicacion"
        ),

        (f"🔹 PASO 1: Autofunción Normalizada ψ_{res.n}(x)", "paso"),
        (
            f"  Factor de normalización A_{res.n} = {res.An}\n"
            f"  ψ_{res.n}(x) = {res.psi_n}",
            "formula"
        ),

        ("🔹 PASO 2: Verificación con el Hamiltoniano Ĥ = - (ℏ²/2m) d²/dx² + ½ m ω² x²", "paso"),
        (
            f"  d²ψ_{res.n}/dx² = {res.d2_psi}\n"
            f"  Ĥψ_{res.n}(x)  = {res.H_psi}\n"
            f"  Energía propia del nivel: E_{res.n} = {res.energia_n}   (Eₙ = ℏω(n + ½))",
            "formula"
        ),
        (
            f"💡 INTERPRETACIÓN FÍSICA: Para n = {res.n}, el sistema posee una energía cuantizada de E_{res.n} = {res.energia_n}. "
            + ("En el estado fundamental (n=0), la energía de punto cero E₀ = ½ℏω es una consecuencia ineludible del Principio de Incertidumbre."
               if res.n == 0 else
               f"El estado excitado n = {res.n} posee {res.n} nodos espaciales y una energía superior en {res.n}ℏω respecto al estado base."),
            "conclusion"
        ),
    ]
    return bloques


def formatear_tunel(res: TunnelingResult) -> List[Tuple[str, str]]:
    bloques = [
        ("🔮 EFECTO TÚNEL CUÁNTICO A TRAVÉS DE BARRERA RECTANGULAR", "titulo"),
        (
            f"Analizamos el paso cuántico de una partícula de masa m = {res.masa_kg:.4e} kg "
            f"con energía incidente E = {res.E_ev:.4f} eV ante una barrera de V₀ = {res.V0_ev:.4f} eV "
            f"y espesor a = {res.ancho_nm:.4f} nm.\n"
            f"Régimen físico: {res.regimen}",
            "explicacion"
        ),

        ("🔹 PASO 1: Atenuación / Vector de Onda Cuántico dentro de la Barrera", "paso"),
        (
            f"  κ (o k') = {res.kappa_m_inv:.4e} m⁻¹\n"
            f"  Factor adimensional κ·a = {res.kappa_a:.4f}",
            "formula"
        ),

        ("🔹 PASO 2: Coeficientes de Transmisión (T) y Reflexión (R)", "paso"),
        (
            f"  Probabilidad de Transmisión (T) : T = {res.T:.6e}  ({res.T * 100:.4f}%)\n"
            f"  Probabilidad de Reflexión (R)   : R = {res.R:.6e}  ({res.R * 100:.4f}%)\n"
            f"  Conservación de flujo cuántico  : T + R = {res.T + res.R:.6f} ≈ 1.0",
            "formula"
        ),

        (f"💡 INTERPRETACIÓN FÍSICA: {res.explicacion_fisica}", "conclusion"),
    ]
    return bloques


def formatear_hamiltoniano(res: HamiltonianResult) -> List[Tuple[str, str]]:
    bloques = [
        ("📘 DIAGONALIZACIÓN DE HAMILTONIANO MATRICIAL Y EVOLUCIÓN TEMPORAL", "titulo"),
        (
            "Calculamos el espectro completo del operador Hamiltoniano matricial Ĥ, verificando la condición "
            "de Hermiticidad, calculando sus autovalores y autovectores, la brecha de excitación y la evolución temporal.",
            "explicacion"
        ),
        (f"  Matriz Hamiltoniana H:\n{res.H}", "formula"),

        ("🔹 PASO 1: Verificación de Hermiticidad (H = H†)", "paso"),
        (
            f"  Residual de Hermiticidad: ||H - H†||_max = {res.residual_hermitico:.2e}\n"
            f"  ¿Es Hermítica?: {'SÍ (Sistema cerrado con autovalores 100% reales)' if res.es_hermitica else 'NO (Matriz no autoadjunta; modelo de sistema abierto / disipativo)'}",
            "formula" if res.es_hermitica else "advertencia"
        ),

        ("🔹 PASO 2: Niveles de Energía (Autovalores) y Autoestados (|Eₙ⟩)", "paso"),
    ]

    detalle = ""
    for idx, E_val in enumerate(res.energias):
        vec = res.autovectores[:, idx]
        vec_str = "  ".join([f"{v.real:+.4f}{v.imag:+.4f}i" for v in vec])
        if res.es_hermitica:
            detalle += f"  Nivel E_{idx} = {E_val.real:+.6f}   -->   Autoestado |E_{idx}⟩ = [ {vec_str} ]ᵀ\n"
        else:
            detalle += f"  Autovalor λ_{idx} = {E_val.real:+.6f}{E_val.imag:+.6f}i   -->   Vector propio = [ {vec_str} ]ᵀ\n"

    bloques.append((detalle.strip(), "formula"))

    if res.es_hermitica:
        if res.es_degenerado:
            brecha_str = "0.0000 (Espectro completamente degenerado; no hay nivel excitado superior distinto)."
        else:
            brecha_str = f"ΔE = {res.brecha:.6f}"
        bloques.append((
            f"💡 INTERPRETACIÓN FÍSICA: Estado fundamental con energía mínima E₀ = {res.energias[0].real:.6f}.\n"
            f"Brecha cuántica hacia el primer nivel distinto: {brecha_str}",
            "conclusion"
        ))
    else:
        bloques.append((
            "⚠️ ATENCIÓN: Al tratarse de una matriz no Hermítica, los autovalores poseen partes complejas "
            "o el operador no es autoadjunto. Las partes imaginarias corresponden a tasas de amortiguamiento/decaimiento "
            "o ganancia en sistemas cuánticos abiertos o efectivos.",
            "advertencia"
        ))

    # Time evolution
    if res.psi_t is not None:
        bloques.append(("🔹 PASO 3: Evolución Temporal Cuántica |ψ(t)⟩ = exp(-iHt/ℏ) |ψ(0)⟩", "paso"))
        psi_0_str = "  ".join([f"{v.real:+.4f}{v.imag:+.4f}i" for v in res.psi_0])
        psi_t_str = "  ".join([f"{v.real:+.4f}{v.imag:+.4f}i" for v in res.psi_t])
        t_str = f"{res.evolucion_t:.4f}" if res.evolucion_t is not None else "0.0000"
        bloques.append((
            f"  Estado inicial normalizado |ψ(0)⟩: [ {psi_0_str} ]ᵀ\n"
            f"  Tiempo transcurrido: t = {t_str}\n"
            f"  Estado evolucionado |ψ(t)⟩:        [ {psi_t_str} ]ᵀ\n"
            f"  Norma de |ψ(t)⟩: ||ψ(t)|| = {res.norma_psi_t:.6f} (Conservación unitaria)",
            "formula"
        ))

    return bloques


def formatear_reporte(bloques: List[Tuple[str, str]], seguro_fn=None) -> List[Tuple[str, str]]:
    if seguro_fn is None:
        return bloques
    return [(seguro_fn(txt), tag) for txt, tag in bloques]
