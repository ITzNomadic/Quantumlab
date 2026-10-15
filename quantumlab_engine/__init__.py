"""
QuantumLab computational engine.
Provides decoupled AST parsing, physical simulation, and result formatting.
"""

from .errors import (
    QuantumLabError,
    MathParseError,
    ParseSecurityError,
    ScientificValidationError,
)
from .runner import AsyncCalculationManager
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
    "QuantumLabError",
    "MathParseError",
    "ParseSecurityError",
    "ScientificValidationError",
    "AsyncCalculationManager",
    "SafeASTParser",
    "parse_parameters",
    "parse_matrix",
    "parse_state_vector",
    "analizar_funcion_onda",
    "analizar_schrodinger_1d",
    "analizar_pozo_infinito",
    "analizar_oscilador_armonico",
    "analizar_efecto_tunel",
    "evolucion_temporal_matricial",
    "formatear_reporte",
    "__version__",
]

__version__ = "0.3.1"
