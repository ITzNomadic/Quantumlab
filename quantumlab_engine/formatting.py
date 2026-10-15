"""
Decoupled formatting engine for QuantumLab.
Produces structured, human-readable step-by-step educational explanations
with tagged output blocks ('titulo', 'paso', 'explicacion', 'formula', 'conclusion', 'advertencia').
Fully localized in English and Spanish via quantumlab_i18n.
"""

from typing import List, Tuple, Optional
import sympy as sp
import numpy as np

from quantumlab_i18n import t
from .physics import (
    WaveFunctionResult,
    Schrodinger1DResult,
    InfiniteWellResult,
    HarmonicOscillatorResult,
    TunnelingResult,
    HamiltonianResult,
    HBAR_SI,
)
from .parser import SafeASTParser


def formatear_analisis_onda(res: WaveFunctionResult, lang: Optional[str] = None) -> List[Tuple[str, str]]:
    bloques = [
        (t("wave.title", lang=lang), "titulo"),
        (t("wave.intro", lang=lang), "explicacion"),
        (t("wave.initial_state", lang=lang, psi=sp.pretty(res.psi_raw), a=res.a, b=res.b), "formula"),

        (t("wave.step1_title", lang=lang), "paso"),
        (t("wave.step1_desc", lang=lang), "explicacion"),
        (
            t(
                "wave.step1_formula",
                lang=lang,
                norm_integral=res.norm_integral,
                constante_A=res.constante_A,
                psi_norm=res.psi_norm,
            ),
            "formula",
        ),
        (
            t("wave.boundary_selfadjoint", lang=lang) if res.es_autoadjunto_p else t("wave.boundary_warning", lang=lang),
            "advertencia" if not res.es_autoadjunto_p else "explicacion",
        ),

        (t("wave.step2_title", lang=lang), "paso"),
        (t("wave.step2_desc", lang=lang), "explicacion"),
        (
            t("wave.step2_formula", lang=lang, exp_x=res.exp_x, exp_x2=res.exp_x2, delta_x=res.delta_x),
            "formula",
        ),

        (t("wave.step3_title", lang=lang), "paso"),
        (t("wave.step3_desc", lang=lang), "explicacion"),
        (
            t(
                "wave.step3_formula",
                lang=lang,
                d_psi=res.d_psi,
                d2_psi=res.d2_psi,
                exp_p=res.exp_p,
                exp_p2=res.exp_p2,
                delta_p=res.delta_p,
                exp_T=res.exp_T,
            ),
            "formula",
        ),

        (t("wave.step4_title", lang=lang), "paso"),
        (t("wave.step4_formula", lang=lang, product=res.delta_x_delta_p), "formula"),
    ]

    heis_code = getattr(res, "heisenberg_codigo", "fulfilled" if res.heisenberg_cumple else "indeterminate")
    heis_msg = t(f"wave.heisenberg_{heis_code}", lang=lang)
    prefix = t("wave.interpretation_prefix", lang=lang, exp_x=res.exp_x, exp_p=res.exp_p)
    bloques.append((prefix + heis_msg, "conclusion" if res.heisenberg_cumple else "advertencia"))
    return bloques


def formatear_schrodinger(res: Schrodinger1DResult, lang: Optional[str] = None) -> List[Tuple[str, str]]:
    bloques = [
        (t("schrodinger.title", lang=lang), "titulo"),
        (t("schrodinger.intro", lang=lang), "explicacion"),
        (t("schrodinger.system_inputs", lang=lang, psi=res.psi, V=res.V), "formula"),

        (t("schrodinger.step1_title", lang=lang), "paso"),
        (
            t("schrodinger.step1_formula", lang=lang, d_psi=sp.diff(res.psi, SafeASTParser.x), d2_psi=res.d2_psi),
            "formula",
        ),

        (t("schrodinger.step2_title", lang=lang), "paso"),
        (
            t(
                "schrodinger.step2_formula",
                lang=lang,
                T_psi=res.termino_cinetico,
                V_psi=res.termino_potencial,
                H_psi=res.H_psi,
            ),
            "formula",
        ),

        (t("schrodinger.step3_title", lang=lang), "paso"),
        (t("schrodinger.step3_formula", lang=lang, energia=res.energia), "formula"),
    ]

    if res.es_autoestado_formal:
        if res.es_estado_fisico_ligado:
            concl = t("schrodinger.conclusion_eigenstate_bound", lang=lang, energia=res.energia)
            tag = "conclusion"
        else:
            concl = t("schrodinger.conclusion_eigenstate_formal", lang=lang, energia=res.energia)
            tag = "advertencia"
    else:
        concl = t("schrodinger.conclusion_non_eigenstate", lang=lang, energia=res.energia)
        tag = "advertencia"

    bloques.append((concl, tag))
    return bloques


def formatear_pozo_infinito(res: InfiniteWellResult, lang: Optional[str] = None) -> List[Tuple[str, str]]:
    bloques = [
        (t("well.title", lang=lang), "titulo"),
        (t("well.intro", lang=lang), "explicacion"),

        (t("well.step1_title", lang=lang), "paso"),
        (t("well.step1_formula", lang=lang, n=res.n, L=res.L), "formula"),

        (t("well.step2_title", lang=lang, a=res.a_in, b=res.b_in, n=res.n), "paso"),
        (
            t(
                "well.step2_formula",
                lang=lang,
                a_in=res.a_in,
                b_in=res.b_in,
                a_eff=res.a_eff,
                b_eff=res.b_eff,
                prob_simbolica=res.prob_simbolica,
                prob_num=res.prob_numerica,
                prob_percent=res.prob_numerica * 100.0,
            ),
            "formula",
        ),
    ]

    if res.nota_dominio:
        bloques.append((t("well.domain_note", lang=lang, a=res.a_in, b=res.b_in, L=res.L), "advertencia"))

    bloques.append((
        t("well.interpretation", lang=lang, n=res.n, prob_percent=res.prob_numerica * 100.0),
        "conclusion",
    ))
    return bloques


def formatear_oscilador(res: HarmonicOscillatorResult, lang: Optional[str] = None) -> List[Tuple[str, str]]:
    bloques = [
        (t("oscillator.title", lang=lang, n=res.n), "titulo"),
        (t("oscillator.intro", lang=lang), "explicacion"),

        (t("oscillator.step1_title", lang=lang), "paso"),
        (t("oscillator.step1_formula", lang=lang, n=res.n, An=res.An, psi_n=res.psi_n), "formula"),

        (t("oscillator.step2_title", lang=lang), "paso"),
        (
            t(
                "oscillator.step2_formula",
                lang=lang,
                d2_psi=res.d2_psi,
                H_psi=res.H_psi,
                n=res.n,
                energia_n=res.energia_n,
            ),
            "formula",
        ),
    ]

    if res.n == 0:
        concl = t("oscillator.interpretation_ground", lang=lang)
    else:
        concl = t("oscillator.interpretation_excited", lang=lang, n=res.n, coeff=f"{res.n} + 1/2")

    bloques.append((concl, "conclusion"))
    return bloques


def formatear_tunel(res: TunnelingResult, lang: Optional[str] = None) -> List[Tuple[str, str]]:
    bloques = [
        (t("tunnel.title", lang=lang), "titulo"),
        (
            t("tunnel.intro", lang=lang, m=res.masa_kg, E_ev=res.E_ev, V0_ev=res.V0_ev, ancho_nm=res.ancho_nm),
            "explicacion",
        ),
        (t("tunnel.step1_title", lang=lang), "paso"),
    ]

    if res.ancho_nm == 0.0:
        step1_txt = t("tunnel.regime_zero_width", lang=lang)
        interp_txt = t("tunnel.regime_zero_width", lang=lang)
    elif res.E_ev == 0.0:
        step1_txt = t("tunnel.regime_zero_energy", lang=lang)
        interp_txt = t("tunnel.regime_zero_energy", lang=lang)
    elif res.E_ev < res.V0_ev:
        step1_txt = t("tunnel.step1_subbarrier", lang=lang, kappa=res.kappa_m_inv, kappa_a=res.kappa_a)
        interp_txt = t("tunnel.regime_subbarrier_explanation", lang=lang, T_percent=res.T * 100.0)
    elif np.isclose(res.E_ev, res.V0_ev, atol=1e-9):
        step1_txt = t("tunnel.step1_resonance", lang=lang)
        interp_txt = t("tunnel.regime_resonance_explanation", lang=lang)
    else:
        step1_txt = t("tunnel.step1_overbarrier", lang=lang, kappa=res.kappa_m_inv, kappa_a=res.kappa_a)
        interp_txt = t("tunnel.regime_overbarrier_explanation", lang=lang, T_percent=res.T * 100.0, R_percent=res.R * 100.0)

    bloques.append((step1_txt, "formula"))

    bloques.append((t("tunnel.step2_title", lang=lang), "paso"))
    bloques.append((
        t(
            "tunnel.step2_formula",
            lang=lang,
            T=res.T,
            T_percent=res.T * 100.0,
            R=res.R,
            R_percent=res.R * 100.0,
            TR_sum=res.T + res.R,
        ),
        "formula",
    ))
    bloques.append((interp_txt, "conclusion"))
    return bloques


def formatear_hamiltoniano(res: HamiltonianResult, lang: Optional[str] = None) -> List[Tuple[str, str]]:
    bloques = [
        (t("hamiltonian.title", lang=lang), "titulo"),
        (t("hamiltonian.intro", lang=lang), "explicacion"),
        (t("hamiltonian.matrix_repr", lang=lang, matrix=res.H), "formula"),

        (t("hamiltonian.step1_title", lang=lang), "paso"),
    ]

    h_step1 = (
        t("hamiltonian.residual_line", lang=lang, res=res.residual_hermitico) + "\n" +
        (t("hamiltonian.hermitian_yes", lang=lang) if res.es_hermitica else t("hamiltonian.hermitian_no", lang=lang))
    )
    bloques.append((h_step1, "formula" if res.es_hermitica else "advertencia"))

    bloques.append((t("hamiltonian.step2_title", lang=lang), "paso"))

    detalle = ""
    for idx, E_val in enumerate(res.energias):
        vec = res.autovectores[:, idx]
        vec_str = "  ".join([f"{v.real:+.4f}{v.imag:+.4f}i" for v in vec])
        if res.es_hermitica:
            detalle += t("hamiltonian.eigen_level_real", lang=lang, idx=idx, val=E_val.real, vec=vec_str)
        else:
            val_str = f"{E_val.real:+.6f}{E_val.imag:+.6f}i"
            detalle += t("hamiltonian.eigen_level_complex", lang=lang, idx=idx, val_str=val_str, vec=vec_str)

    bloques.append((detalle.strip(), "formula"))
    bloques.append((t("hamiltonian.eigen_residual_info", lang=lang, res=res.max_residuo_autovector), "formula"))

    # Step 3: Gap (DEF-05: Consistent natural units hbar = 1)
    if res.es_hermitica:
        bloques.append((t("hamiltonian.step3_title", lang=lang), "paso"))
        freq = res.brecha if res.brecha is not None else 0.0
        gap_txt = t(
            "hamiltonian.gap_info",
            lang=lang,
            E0=res.energias[0].real,
            gap=res.brecha if res.brecha is not None else 0.0,
            freq=freq,
        )
        if res.es_degenerado:
            gap_txt += "\n" + t("hamiltonian.gap_degenerate_note", lang=lang)
        bloques.append((gap_txt, "conclusion"))
    else:
        bloques.append((t("hamiltonian.non_hermitian_warning", lang=lang), "advertencia"))

    # Step 4: Time evolution (DEF-06: Accurate normalization distinction)
    if res.psi_t is not None:
        bloques.append((t("hamiltonian.step4_title", lang=lang), "paso"))
        psi_0_str = "  ".join([f"{v.real:+.4f}{v.imag:+.4f}i" for v in res.psi_0])
        psi_t_str = "  ".join([f"{v.real:+.4f}{v.imag:+.4f}i" for v in res.psi_t])
        t_str = f"{res.evolucion_t:.4f}" if res.evolucion_t is not None else "0.0000"

        norm_0 = res.norma_psi_0 if res.norma_psi_0 is not None else float(np.linalg.norm(res.psi_0))
        needs_renorm_display = abs(norm_0 - 1.0) > 1e-5 and getattr(res, "psi_0_norm", None) is not None

        if needs_renorm_display:
            psi_0_norm_str = "  ".join([f"{v.real:+.4f}{v.imag:+.4f}i" for v in res.psi_0_norm])
            key = "hamiltonian.evolution_unitary_renorm" if res.es_hermitica else "hamiltonian.evolution_non_unitary_renorm"
            evo_txt = t(
                key,
                lang=lang,
                t=t_str,
                psi_0_raw=psi_0_str,
                norm_0=norm_0,
                psi_0_norm=psi_0_norm_str,
                psi_t=psi_t_str,
                norm_t=res.norma_psi_t,
            )
        else:
            key = "hamiltonian.evolution_unitary" if res.es_hermitica else "hamiltonian.evolution_non_unitary"
            evo_txt = t(
                key,
                lang=lang,
                t=t_str,
                psi_0=psi_0_str,
                psi_t=psi_t_str,
                norm_0=norm_0,
                norm_t=res.norma_psi_t,
            )
        bloques.append((evo_txt, "formula"))

    return bloques


def formatear_reporte(bloques: List[Tuple[str, str]], seguro_fn=None) -> List[Tuple[str, str]]:
    if seguro_fn is None:
        return bloques
    return [(seguro_fn(txt), tag) for txt, tag in bloques]
