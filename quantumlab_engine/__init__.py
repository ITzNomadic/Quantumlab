"""
QuantumLab computational engine.
Provides decoupled AST parsing, physical simulation, and result formatting.
"""

from .parser import SafeASTParser, parse_parameters, parse_matrix, parse_state_vector
from .physics import (
    analizar_funcion_onda,
    analizar_schrodinger_1d,
    analizar_pozo_infinito,
    analizar_oscilador_armonico,
    analizar_efecto_tunel,
    analizar_hamiltoniano_matricial,
    evolucion_temporal_matricial,
)
from .formatting import formatear_reporte

__all__ = [
    "SafeASTParser",
    "parse_parameters",
    "parse_matrix",
    "parse_state_vector",
    "analizar_funcion_onda",
    "analizar_schrodinger_1d",
    "analizar_pozo_infinito",
    "analizar_oscilador_armonico",
    "analizar_efecto_tunel",
    "analizar_hamiltoniano_matricial",
    "evolucion_temporal_matricial",
    "formatear_reporte",
]
