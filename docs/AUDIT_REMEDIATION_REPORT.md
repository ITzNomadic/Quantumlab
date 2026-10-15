# Registro de Remediación de Auditoría — QuantumLab Pro Max

**Fecha:** 2026-10-15  
**Ambiente de prueba y ejecución:** Python 3.14.2, SymPy 1.14.0, NumPy 2.5.4  
**Archivo original auditado preservado:** `QuantumLab_PRO_MAX_CORREGIDO.py` (SHA-256: `005fe17a081dbbdb8825aed5ea166c01e4a1129c8056950b4baad226cb49363f`)  
**Archivos remediados:** `quantumlab.py`, `quantumlab_engine/` (`parser.py`, `physics.py`, `formatting.py`), test suite en `tests/`  

---

## Matriz de Trazabilidad: Hallazgos QL-001 a QL-033

| ID | Sev | Título del hallazgo | Módulo / Componente corregido | Test de verificación | Estado |
|---|---|---|---|---|---|
| **QL-001** | P0 | Entrada simbólica ejecuta Python arbitrario | `quantumlab_engine.parser.SafeASTParser` | `test_t13_ql001_insecure_parser_blocked`, `test_reject_arbitrary_python_and_code_execution` | **RESUELTO** |
| **QL-002** | P0 | Heisenberg declarado verdadero sin validez de dominio | `quantumlab_engine.physics.analizar_funcion_onda` | `test_t01_ql002_heisenberg_not_claimed_on_zero_delta_p`, `test_wave_constant_finite_interval_heisenberg_not_claimed` | **RESUELTO** |
| **QL-003** | P0 | Parte imaginaria de energías complejas eliminada | `quantumlab_engine.physics.analizar_hamiltoniano_matricial` | `test_t10_ql003_hamiltonian_complex_eigenvalues`, `test_hamiltonian_non_hermitian_preserves_complex_eigenvalues` | **RESUELTO** |
| **QL-004** | P1 | Normaliza estados nulos y propaga NaN/zoo | `quantumlab_engine.physics.analizar_funcion_onda` | `test_t02_ql004_null_state_rejected`, `test_wave_null_state_rejected` | **RESUELTO** |
| **QL-005** | P1 | Operadores de momento/cinética sin comprobar contornos | `quantumlab_engine.physics.analizar_funcion_onda` | `test_wave_constant_finite_interval_heisenberg_not_claimed` | **RESUELTO** |
| **QL-006** | P1 | Estado nulo ψ=0 declarado autoestado exacto | `quantumlab_engine.physics.analizar_schrodinger_1d` | `test_t03_ql006_schrodinger_null_state_rejected`, `test_schrodinger_null_state_rejected` | **RESUELTO** |
| **QL-007** | P1 | Schrödinger ignora integrabilidad y contornos L² | `quantumlab_engine.physics.analizar_schrodinger_1d` | `test_t04_ql007_schrodinger_formal_vs_physical`, `test_schrodinger_formal_vs_physical_admissibility` | **RESUELTO** |
| **QL-008** | P1 | Probabilidad del pozo excede 100% fuera de [0, L] | `quantumlab_engine.physics.analizar_pozo_infinito` | `test_t05_ql008_infinite_well_prob_clamped`, `test_infinite_well_probability_clamped_to_100_percent` | **RESUELTO** |
| **QL-009** | P1 | Orden de límites invertido produce P < 0 | `quantumlab_engine.physics.analizar_pozo_infinito` | `test_t06_ql009_infinite_well_inverted_limits`, `test_infinite_well_inverted_limits_rejected` | **RESUELTO** |
| **QL-010** | P1 | Número cuántico n del pozo infinito ignorado | `quantumlab_engine.physics.analizar_pozo_infinito` | `test_t07_ql010_infinite_well_n_respected`, `test_infinite_well_n_respected_analytic` | **RESUELTO** |
| **QL-011** | P1 | Oscilador armónico ignora entradas y no resuelve n>0 | `quantumlab_engine.physics.analizar_oscilador_armonico` | `test_t08_ql011_harmonic_oscillator_n4`, `test_harmonic_oscillator_n_levels` | **RESUELTO** |
| **QL-012** | P1 | Efecto túnel ignora parámetros introducidos | `quantumlab_engine.physics.analizar_efecto_tunel` | `test_t09_ql012_tunneling_custom_inputs`, `test_tunneling_custom_parameters` | **RESUELTO** |
| **QL-013** | P1 | Chequeo de hermiticidad aproximada sin residual | `quantumlab_engine.physics.analizar_hamiltoniano_matricial` | `test_t12_ql013_hamiltonian_residual_reported`, `test_hamiltonian_exact_vs_approx_hermiticity` | **RESUELTO** |
| **QL-014** | P1 | Brecha de excitación nula ante espectro degenerado | `quantumlab_engine.physics.analizar_hamiltoniano_matricial` | `test_t11_ql014_hamiltonian_gap_distinct_level`, `test_hamiltonian_gap_under_degeneracy` | **RESUELTO** |
| **QL-015** | P1 | Evolución temporal anunciada pero inexistente | `quantumlab_engine.physics.analizar_hamiltoniano_matricial` | `test_hamiltonian_time_evolution_unitary`, `test_state_vector_parsing` | **RESUELTO** |
| **QL-016** | P1 | Bloqueo síncrono potencial en cálculo | `quantumlab.py` (desacople y control de estado) | `test_all_default_modes_produce_results` | **RESUELTO** |
| **QL-017** | P1 | Tamaño y complejidad de entrada sin control | `quantumlab_engine.parser.SafeASTParser` | `test_reject_excessive_length`, `test_reject_excessive_depth`, `test_reject_extreme_exponent` | **RESUELTO** |
| **QL-018** | P2 | Parámetros sin estructura o unidades | `quantumlab_engine.parser.parse_parameters` | `test_parameter_parsing` | **RESUELTO** |
| **QL-019** | P2 | Matrices mal formadas sin validación previa | `quantumlab_engine.parser.parse_matrix` | `test_matrix_parsing_valid`, `test_matrix_parsing_invalid` | **RESUELTO** |
| **QL-020** | P2 | Magnitudes NaN/zoo no bloqueadas | `quantumlab_engine.physics` (todos los módulos) | `test_t02_null_state_rejected`, `test_t03_schrodinger_null_state_rejected` | **RESUELTO** |
| **QL-021** | P2 | Deducción injustificada de superposición discreta | `quantumlab_engine.physics.analizar_schrodinger_1d` | `test_schrodinger_non_eigenstate_no_unproved_superposition` | **RESUELTO** |
| **QL-022** | P2 | Túnel restringido solo a E < V₀ | `quantumlab_engine.physics.analizar_efecto_tunel` | `test_tunneling_regimes_and_limits` | **RESUELTO** |
| **QL-023** | P2 | Clasificación errónea de matriz no hermítica | `quantumlab_engine.formatting.formatear_hamiltoniano` | `test_t10_ql003_hamiltonian_complex_eigenvalues` | **RESUELTO** |
| **QL-024** | P2 | Ventana inaccesible en pantallas pequeñas (800×600) | `quantumlab.py` (__init__ responsive minsize) | `test_t14_window_geometry_responsive` | **RESUELTO** |
| **QL-025** | P2 | Combobox de modos no empaquetado ni visible | `quantumlab.py` (combo_modo visible y sincronizado) | `test_t15_combobox_visible_and_functional`, `test_t15_ql025_combobox_synced` | **RESUELTO** |
| **QL-026** | P2 | Clic en modo activo borra entradas del usuario | `quantumlab.py` (`_guardar_entradas_actuales`, persistencia) | `test_t16_preserve_inputs_on_active_mode_click`, `test_t16_ql026_preserve_inputs_on_click` | **RESUELTO** |
| **QL-027** | P2 | Resultado marcado disponible antes de validación | `quantumlab.py` (ciclo de estados y captura tipificada) | `test_all_default_modes_produce_results` | **RESUELTO** |
| **QL-028** | P2 | Exportación sin captura de errores OSError | `quantumlab.py` (`exportar_hoja` con try/except) | Verificado en revisión de código | **RESUELTO** |
| **QL-029** | P2 | Acoplamiento monolítico entre UI y motor físico | Creación de paquete `quantumlab_engine` | Suite completa desacoplada | **RESUELTO** |
| **QL-030** | P2 | Entradas no aplicables visibles sin aviso | `quantumlab.py` (`_actualizar_visual_modo` con pistas) | Verificado visual y funcionalmente | **RESUELTO** |
| **QL-031** | P3 | Explicación simplista de onda en túnel | `quantumlab_engine.formatting.formatear_tunel` | `test_tunneling_regimes_and_limits` | **RESUELTO** |
| **QL-032** | P3 | Precisión de salida insuficiente en espectros | `quantumlab_engine.formatting.formatear_hamiltoniano` | `test_t10_ql003_hamiltonian_complex_eigenvalues`, `test_t11_ql014_hamiltonian_gap_distinct_level` | **RESUELTO** |
| **QL-033** | P3 | Hoja de resultados editable documentada | `quantumlab.py` y `README.md` | `test_smoke.py` | **RESUELTO** |

---

## Remediación de Auditoría Residual (Post-v0.2.0)

| ID Defecto | Severidad | Descripción del defecto residual | Componente remediado | Prueba de verificación reproducible | Estado |
|---|---|---|---|---|---|
| **DEF-01** | P0 | `test_environment_versions_recorded` exigía versión estricta 3.14/fija en CI matriz 3.11/3.12 | `tests/test_audit_baseline.py` | `test_defect_1_environment_version_ci_compatibility`, `test_environment_versions_recorded` | **RESUELTO** |
| **DEF-02** | P1 | Integral simbólica del pozo infinito excedía soporte físico `[0, L]` discrepando con P numérica | `quantumlab_engine/physics.py` (`analizar_pozo_infinito`) | `test_defect_2_pozo_infinito_symbolic_integral_matches_support` | **RESUELTO** |
| **DEF-03** | P1 | Matrices casi hermíticas: falta de cálculo de residuo del par propio \|\|Hv - λv\|\| y tolerancia laxa | `quantumlab_engine/physics.py`, `quantumlab_engine/formatting.py` | `test_defect_3_almost_hermitian_residuals_tracked` | **RESUELTO** |
| **DEF-04** | P1 | Capturas silenciosas de excepciones en vector de estado y tiempo de Hamiltoniano | `quantumlab.py` (`_resolver_hamiltoniano_matricial`) | `test_defect_4_no_silent_exception_swallowing_in_hamiltonian` | **RESUELTO** |
| **DEF-05** | P1 | `parse_state_vector` mutilaba funciones válidas como `sqrt(2)` por regex codiciosa | `quantumlab_engine/parser.py` (`parse_state_vector`) | `test_defect_5_parse_state_vector_preserves_sqrt` | **RESUELTO** |
| **DEF-06** | P1 | Dependencia no declarada de SciPy en evolución temporal y enmascaramiento de fallos | `quantumlab_engine/physics.py` (`_expm_numpy`) | `test_defect_6_matrix_exponential_without_scipy` | **RESUELTO** |
| **DEF-07** | P1 | Desigualdad de Heisenberg dada por cumplida falsamente ante indeterminaciones o contornos abiertos | `quantumlab_engine/physics.py` (`analizar_funcion_onda`) | `test_defect_7_heisenberg_indeterminacy_not_claimed` | **RESUELTO** |
| **DEF-08** | P2 | Falta de validación de finitud (NaN, Inf) y positividad en parámetros de efecto túnel | `quantumlab_engine/physics.py` (`analizar_efecto_tunel`) | `test_defect_8_tunneling_finite_validation` | **RESUELTO** |
| **DEF-09** | P2 | Evolución no unitaria de sistemas no hermíticos catalogada erróneamente como conservación unitaria | `quantumlab_engine/formatting.py` (`formatear_hamiltoniano`) | `test_defect_9_non_hermitian_evolution_not_called_unitary` | **RESUELTO** |

---

## Resultados de la Suite Automatizada de Pruebas

```
Ran 71 tests in 2.925s
OK
```

Todos los tests (62 pruebas de regresión base + 9 pruebas de reproducción de defectos residuales) pasan al 100% sin advertencias ni fallos.
