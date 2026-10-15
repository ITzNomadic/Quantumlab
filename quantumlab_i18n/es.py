"""
Spanish (Español) Translations for QuantumLab.
Contiene todos los textos de interfaz, salidas científicas, descripciones y mensajes de error.
"""

STRINGS_ES = {
    # -------------------------------------------------------------
    # General UI / Encabezado
    # -------------------------------------------------------------
    "app.title": "QuantumLab  |  Calculadora Cuántica Pro Max",
    "header.brand_title": "QUANTUM",
    "header.brand_accent": "LAB",
    "header.brand_sub": "ESTUDIO DE MECÁNICA CUÁNTICA  /  PRO MAX (SECURED)",
    "header.engine_verified": "MOTOR CIENTÍFICO VERIFICADO",
    "header.engine_libs": "SymPy  •  NumPy  •  AST Parser",
    "header.language_label": "Language",

    # -------------------------------------------------------------
    # Sidebar / Navegación
    # -------------------------------------------------------------
    "sidebar.workspace_title": "ESPACIO DE TRABAJO",
    "sidebar.modules_title": "Módulos de cálculo",
    "sidebar.modules_sub": "Selecciona un sistema",
    "sidebar.shortcuts_title": "ATAJOS DE TECLADO",
    "sidebar.shortcut_calc": "Ctrl + Enter   Resolver",
    "sidebar.shortcut_export": "Ctrl + S       Exportar",
    "sidebar.shortcut_clear": "Ctrl + L       Limpiar",

    # Módulo 0: Función de onda
    "module.0.name": "Función de onda",
    "module.0.sub": "Normalización y Heisenberg",
    "module.0.desc": "Analiza ψ(x), valores esperados e incertidumbres cuánticas rigurosas.",
    "module.0.combo": "1. Análisis Completo de Función de Onda ψ(x): Normalización, ⟨x⟩, ⟨p⟩, ⟨T⟩ y Heisenberg",

    # Módulo 1: Schrödinger 1D
    "module.1.name": "Schrödinger 1D",
    "module.1.sub": "Autoestados y energía",
    "module.1.desc": "Comprueba autoestados de Schrödinger, normalizabilidad y energía.",
    "module.1.combo": "2. Ecuación de Schrödinger 1D: Verificar autoestado y extraer Energía E(x)",

    # Módulo 2: Pozo infinito
    "module.2.name": "Pozo infinito",
    "module.2.sub": "Probabilidad en una región",
    "module.2.desc": "Calcula estados cuantizados n≥1 y probabilidades exactas en el pozo.",
    "module.2.combo": "3. Sistema Completo: Pozo de Potencial Infinito 1D y Probabilidad en Región",

    # Módulo 3: Oscilador armónico
    "module.3.name": "Oscilador armónico",
    "module.3.sub": "Niveles de energía",
    "module.3.desc": "Estudia el estado fundamental y niveles excitados n≥0 con Hermite.",
    "module.3.combo": "4. Sistema Completo: Oscilador Armónico Cuántico y Niveles de Energía",

    # Módulo 4: Efecto túnel
    "module.4.name": "Efecto túnel",
    "module.4.sub": "Barrera de potencial",
    "module.4.desc": "Estima transmisión cuántica y reflexión en todas las energías E, V₀.",
    "module.4.combo": "5. Efecto Túnel Cuántico: Transmisión a través de Barrera de Potencial",

    # Módulo 5: Hamiltoniano
    "module.5.name": "Hamiltoniano",
    "module.5.sub": "Autovalores y autovectores",
    "module.5.desc": "Diagonaliza matrices hermíticas/no-hermíticas y calcula evolución temporal.",
    "module.5.combo": "6. Diagonalización de Hamiltoniano Matricial (H|ψ⟩ = E|ψ⟩) y Evolución Temporal",

    # -------------------------------------------------------------
    # Editor de Entrada (Panel Izquierdo)
    # -------------------------------------------------------------
    "editor.step_counter": "MÓDULO  {current:02d} / {total:02d}",
    "editor.label_psi": "FUNCIÓN DE ONDA  ψ(x) / ESTADO",
    "editor.label_pot": "POTENCIAL  V(x)",
    "editor.label_limits": "LÍMITES DE INTEGRACIÓN / TIEMPO",
    "editor.label_lim_a": "Límite inferior a / t",
    "editor.label_lim_b": "Límite superior b",
    "editor.label_params": "PARÁMETROS / HAMILTONIANO H",
    "editor.keyboard_title": "TECLADO SIMBÓLICO",
    "editor.keyboard_hint": "Insertar en campo activo",
    "editor.btn_solve": "⚡  RESOLVER ECUACIÓN",
    "editor.btn_clear": "Limpiar",
    "editor.btn_reset": "Restablecer",
    "editor.btn_export": "Exportar",

    # Pistas dinámicas de entrada (hints)
    "hint.0.psi": "ψ(x)",
    "hint.0.pot": "V(x) [Informativo]",
    "hint.0.lim_a": "Límite inf. a",
    "hint.0.lim_b": "Límite sup. b",
    "hint.0.params": "Parámetros [Informativo]",

    "hint.1.psi": "ψ(x)",
    "hint.1.pot": "Potencial V(x)",
    "hint.1.lim_a": "Límite inf. a (opcional)",
    "hint.1.lim_b": "Límite sup. b (opcional)",
    "hint.1.params": "Parámetros [Informativo]",

    "hint.2.psi": "ψ(x) analítica",
    "hint.2.pot": "V(x) [Informativo]",
    "hint.2.lim_a": "Región inf. a",
    "hint.2.lim_b": "Región sup. b",
    "hint.2.params": "n entero (ej. n=1, L=1.0)",

    "hint.3.psi": "ψ(x) analítica",
    "hint.3.pot": "V(x) armónico",
    "hint.3.lim_a": "Límite inf. [-oo]",
    "hint.3.lim_b": "Límite sup. [oo]",
    "hint.3.params": "Nivel n (ej. n=0, 1, 2...)",

    "hint.4.psi": "Onda incidente",
    "hint.4.pot": "Barrera V₀",
    "hint.4.lim_a": "Límite a",
    "hint.4.lim_b": "Espesor a (nm)",
    "hint.4.params": "E, V0, a (ej. E=3.2, V0=5.0, a=0.5)",

    "hint.5.psi": "Estado inicial |ψ(0)⟩",
    "hint.5.pot": "Sistema",
    "hint.5.lim_a": "Tiempo t",
    "hint.5.lim_b": "Límite b",
    "hint.5.params": "Matriz H (ej. 2, 1-1j; 1+1j, 3)",

    # -------------------------------------------------------------
    # Presets
    # -------------------------------------------------------------
    "preset.0.psi": "exp(-x**2 / 2)",
    "preset.0.pot": "0",
    "preset.0.lim_a": "-oo",
    "preset.0.lim_b": "oo",
    "preset.0.params": "Paquete Gaussiano estándar",

    "preset.1.psi": "sin(pi*x/L)",
    "preset.1.pot": "0",
    "preset.1.lim_a": "0",
    "preset.1.lim_b": "L",
    "preset.1.params": "Autoestado de caja cuántica",

    "preset.2.psi": "sqrt(2/L)*sin(n*pi*x/L)",
    "preset.2.pot": "0 (Dentro del pozo), oo (Fuera)",
    "preset.2.lim_a": "0",
    "preset.2.lim_b": "L/3",
    "preset.2.params": "n=1, L=1.0 (nm)",

    "preset.3.psi": "exp(-m*w*x**2 / (2*hbar))",
    "preset.3.pot": "(1/2)*m*w**2*x**2",
    "preset.3.lim_a": "-oo",
    "preset.3.lim_b": "oo",
    "preset.3.params": "n=0 (Estado base)",

    "preset.4.psi": "exp(I*k*x)",
    "preset.4.pot": "V0 = 5.0 eV",
    "preset.4.lim_a": "0",
    "preset.4.lim_b": "0.5",
    "preset.4.params": "E=3.2, V0=5.0, a=0.5 (E, V0 en eV; ancho a en nm)",

    "preset.5.psi": "[1, 0] (Estado inicial |ψ(0)⟩)",
    "preset.5.pot": "Sistema de 2 niveles acoplados",
    "preset.5.lim_a": "0",
    "preset.5.lim_b": "1",
    "preset.5.params": "2, 1-1j; 1+1j, 3",

    # -------------------------------------------------------------
    # Consola de Resultados (Panel Derecho)
    # -------------------------------------------------------------
    "results.console_title": "CONSOLA DE RESULTADOS",
    "results.sheet_title": "Hoja de resultados",
    "results.step_by_step": "Desarrollo matemático paso a paso",
    "results.empty_title": "Tu espacio de resultados",
    "results.empty_desc": "Selecciona un módulo, ajusta las entradas\ny ejecuta el cálculo para ver los pasos.",
    "results.footer_info": "SALIDA SIMBÓLICA  •  MOTOR MATEMÁTICO VERIFICADO  •  EXPORTACIÓN .TXT",

    # Estados de cálculo
    "status.no_results": "SIN RESULTADOS",
    "status.calculating": "CALCULANDO...",
    "status.available": "RESULTADOS DISPONIBLES",
    "status.syntax_error": "ERROR DE SINTAXIS/SEGURIDAD",
    "status.param_error": "ERROR EN PARÁMETROS",
    "status.calc_error": "ERROR DE CÁLCULO",

    # Pie de ventana
    "footer.brand": "QUANTUMLAB  /  WORKSPACE",
    "footer.security": "Motor científico riguroso  ·  Seguridad AST activa",

    # Cuadros de diálogo y confirmaciones
    "dialog.preset_restored_title": "Preset restablecido",
    "dialog.preset_restored_msg": "Se cargó el ejemplo predeterminado para '{name}'.",
    "dialog.export_title": "Guardar resultados de QuantumLab",
    "dialog.export_success_title": "Hoja Exportada",
    "dialog.export_success_msg": "Se guardó exitosamente el desarrollo científico en:\n{path}",
    "dialog.export_empty_title": "Hoja vacía",
    "dialog.export_empty_msg": "No hay resultados calculados para exportar.",
    "dialog.export_error_title": "Error al exportar",
    "dialog.export_error_msg": "No se pudo guardar el archivo:\n{error}",
    "dialog.error_syntax_title": "Error de Sintaxis / Seguridad Matemática",
    "dialog.error_param_title": "Parámetro o Dominio Inválido",
    "dialog.error_calc_title": "Error de Cálculo Científico",
    "dialog.error_calc_prefix": "Ocurrió un error al procesar el sistema:\n",

    # -------------------------------------------------------------
    # Formateo Científico: Módulo 0 (Función de Onda)
    # -------------------------------------------------------------
    "wave.title": "📘 ANÁLISIS CUÁNTICO COMPLETO DE LA FUNCIÓN DE ONDA ψ(x)",
    "wave.intro": (
        "Vamos a analizar paso a paso el estado cuántico propuesto. Primero verificaremos la condición "
        "de normalización de Born, analizaremos las condiciones de contorno y extraeremos los observables "
        "físicos mediante operadores cuánticos autoadjuntos."
    ),
    "wave.initial_state": "  ψ_inicial(x) = {psi}   en el dominio [{a}, {b}]",
    "wave.step1_title": "🔹 PASO 1: Condición de Normalización de Born y Cuadrado Integrable",
    "wave.step1_desc": (
        "En mecánica cuántica, la probabilidad total de encontrar la partícula en el dominio debe ser estrictamente 1 (100%). "
        "Verificamos que la función sea de cuadrado integrable en el dominio:"
    ),
    "wave.step1_formula": (
        "  ∫ |ψ(x)|² dx = {norm_integral}\n"
        "  Constante de normalización: A = 1 / √({norm_integral}) = {constante_A}\n"
        "  Función de onda normalizada: ψ(x) = {psi_norm}"
    ),
    "wave.step2_title": "🔹 PASO 2: Valor Esperado de la Posición ⟨x⟩ y Dispersión Cuántica Δx",
    "wave.step2_desc": "Calculamos la posición media aplicando el operador posición x̂ en la base de coordenadas:",
    "wave.step2_formula": (
        "  ⟨x⟩  = ∫ ψ*(x) · x · ψ(x) dx  = {exp_x}\n"
        "  ⟨x²⟩ = ∫ ψ*(x) · x² · ψ(x) dx = {exp_x2}\n"
        "  Incertidumbre en posición: Δx = √(⟨x²⟩ - ⟨x⟩²) = {delta_x}"
    ),
    "wave.step3_title": "🔹 PASO 3: Operador Momento Lineal p̂ = -iℏ(d/dx) y Energía Cinética ⟨T⟩",
    "wave.step3_desc": "Derivamos analíticamente la función de onda para aplicar el operador de momento y el Laplaciano unidimensional:",
    "wave.step3_formula": (
        "  dψ/dx   = {d_psi}\n"
        "  d²ψ/dx² = {d2_psi}\n"
        "  ⟨p⟩  = ∫ ψ*(x) · (-iℏ·d/dx) · ψ(x) dx = {exp_p}\n"
        "  ⟨p²⟩ = ∫ ψ*(x) · (-ℏ²·d²/dx²) · ψ(x) dx = {exp_p2}\n"
        "  Incertidumbre en momento: Δp = √(⟨p²⟩ - ⟨p⟩²) = {delta_p}\n"
        "  Energía cinética media: ⟨T⟩ = ⟨p²⟩ / (2m) = {exp_T}"
    ),
    "wave.step4_title": "🔹 PASO 4: Principio de Incertidumbre de Heisenberg y Validación de Dominio",
    "wave.step4_formula": (
        "  Producto de incertidumbres: Δx · Δp = {product}\n"
        "  Límite fundamental canónico: ℏ/2"
    ),
    "wave.interpretation_prefix": "💡 INTERPRETACIÓN CIENTÍFICA: Posición media ⟨x⟩ = {exp_x}, momento promedio ⟨p⟩ = {exp_p}.\n\n",
    "wave.boundary_selfadjoint": "El término de contorno [|ψ|²] desaparece en los extremos del dominio (autoadjunción compatible).",
    "wave.boundary_warning": (
        "ADVERTENCIA DE CONTORNO: [|ψ|²] no se anula en los extremos. En intervalos acotados sin "
        "condiciones de contorno periódicas o Dirichlet, el operador p̂ = -iℏ∂x no es autoadjunto estándar, "
        "lo cual puede falsear los momentos calculados."
    ),
    "wave.heisenberg_fulfilled": "El estado satisface rigurosamente el Principio de Incertidumbre de Heisenberg: Δx·Δp ≥ ℏ/2.",
    "wave.heisenberg_zero_dispersion": (
        "NO VERIFICABLE / DISPERSIÓN NULA: Uno de los desvíos calculados formalmente es cero "
        "(Δp = 0 o Δx = 0). En un dominio finito, p̂ no posee autovectores en el dominio autoadjunto, "
        "por lo que el producto nulo NO satisface el principio de incertidumbre canónico (Δx·Δp ≥ ℏ/2)."
    ),
    "wave.heisenberg_open_boundary": (
        "CONDICIONES DE CONTORNO NO ESTÁNDAR: El principio canónico Δx·Δp ≥ ℏ/2 presupone autoadjunción "
        "en toda la recta ℝ o condiciones de frontera periódicas. En un intervalo acotado con frontera abierta, "
        "el producto formal no es una prueba concluyente del principio de Heisenberg."
    ),
    "wave.heisenberg_violated": "El producto de incertidumbres formal viola la cota ℏ/2 debido a las condiciones de frontera o dominio.",
    "wave.heisenberg_indeterminate": (
        "INDETERMINADO: No se pudo demostrar formalmente la desigualdad canónica Δx·Δp ≥ ℏ/2 "
        "debido a parámetros libres o integrales no resueltas analíticamente."
    ),

    # -------------------------------------------------------------
    # Formateo Científico: Módulo 1 (Schrödinger 1D)
    # -------------------------------------------------------------
    "schrodinger.title": "🔬 RESOLUCIÓN DE LA ECUACIÓN DE SCHRÖDINGER INDEPENDIENTE DEL TIEMPO (1D)",
    "schrodinger.intro": (
        "Evaluamos rigurosamente si la función propuesta ψ(x) es un autoestado del operador Hamiltoniano "
        "Ĥ = - (ℏ²/2m) d²/dx² + V(x), verificando si satisface Ĥψ(x) = Eψ(x)."
    ),
    "schrodinger.system_inputs": "  ψ(x) = {psi}\n  V(x) = {V}",
    "schrodinger.step1_title": "🔹 PASO 1: Derivadas espaciales de la función de onda",
    "schrodinger.step1_formula": (
        "  dψ/dx   = {d_psi}\n"
        "  d²ψ/dx² = {d2_psi}"
    ),
    "schrodinger.step2_title": "🔹 PASO 2: Aplicación del Hamiltoniano Ĥψ(x)",
    "schrodinger.step2_formula": (
        "  T̂ψ(x) = - (ℏ²/2m) d²ψ/dx² = {T_psi}\n"
        "  V̂ψ(x) = V(x)·ψ(x) = {V_psi}\n"
        "  Ĥψ(x) = T̂ψ + V̂ψ = {H_psi}"
    ),
    "schrodinger.step3_title": "🔹 PASO 3: Extracción y verificación del valor propio de Energía E",
    "schrodinger.step3_formula": "  Cociente espectral: E(x) = Ĥψ(x) / ψ(x) = {energia}",
    "schrodinger.conclusion_eigenstate_bound": (
        "💡 CONCLUSIÓN FÍSICA: ¡ψ(x) ES UN AUTOESTADO LIGADO ESTRICTO! El cociente E = {energia} es una "
        "constante escalar real y la función pertenece a L² (cuadrado integrable). El sistema posee energía propia definida E = {energia}."
    ),
    "schrodinger.conclusion_eigenstate_formal": (
        "⚠️ CONCLUSIÓN FÍSICA: SOLUCIÓN FORMAL LOCAL. ψ(x) es una solución local formal con energía E = {energia}, pero NO es "
        "un estado ligado normalizable en L²(ℝ) (integral divergente o no nula en el infinito). Pertenece al espectro continuo o representa una onda libre/dispersiva no acotada."
    ),
    "schrodinger.conclusion_non_eigenstate": (
        "💡 INTERPRETACIÓN FÍSICA: El cociente E(x) = {energia} depende explícitamente de la coordenada 'x'. "
        "Por tanto, ψ(x) NO es un estado estacionario del potencial V(x). Representa un estado dinámico no elemental o una combinación que evolucionará temporalmente."
    ),

    # -------------------------------------------------------------
    # Formateo Científico: Módulo 2 (Pozo Infinito)
    # -------------------------------------------------------------
    "well.title": "📙 PARTÍCULA EN UNA CAJA CUÁNTICA 1D (POZO DE POTENCIAL INFINITO)",
    "well.intro": (
        "Una partícula confinada entre paredes impenetrables en x = 0 y x = L solo puede existir "
        "en ondas estacionarias cuantizadas con soporte físico estrictamente en [0, L]."
    ),
    "well.step1_title": "🔹 PASO 1: Funciones propias y Cuantización de la Energía",
    "well.step1_formula": (
        "  Nivel cuántico seleccionado: n = {n}, Ancho del pozo: L = {L}\n"
        "  ψₙ(x) = √(2/L) · sin(n·π·x / L)   para 0 ≤ x ≤ L (0 fuera)\n"
        "  Eₙ    = (n² · π² · ℏ²) / (2 · m · L²)"
    ),
    "well.step2_title": "🔹 PASO 2: Probabilidad de hallar la partícula entre [{a}, {b}] para el estado n={n}",
    "well.step2_formula": (
        "  Intervalo solicitado: [{a_in}, {b_in}]\n"
        "  Intervalo físico efectivo en el pozo: [{a_eff}, {b_eff}]\n"
        "  P({a_eff} ≤ x ≤ {b_eff}) = ∫ |ψₙ(x)|² dx = {prob_simbolica}\n"
        "  Probabilidad calculada: P = {prob_num:.6f} ({prob_percent:.2f}%)"
    ),
    "well.domain_note": (
        "ACUMULACIÓN FÍSICA: El pozo infinito tiene paredes impenetrables en x=0 y x=L. "
        "La densidad de probabilidad es estrictamente 0 fuera de [0, L]. "
        "La integral sobre [{a}, {b}] se evalúa eficazmente en la intersección con el pozo."
    ),
    "well.interpretation": (
        "💡 INTERPRETACIÓN FÍSICA: En una caja clásica la probabilidad sería estrictamente geométrica (Δx/L). "
        "En mecánica cuántica, debido a los nodos de interferencia de la onda estacionaria n={n}, "
        "la probabilidad real de hallar la partícula en la región es del {prob_percent:.2f}%."
    ),

    # -------------------------------------------------------------
    # Formateo Científico: Módulo 3 (Oscilador Armónico)
    # -------------------------------------------------------------
    "oscillator.title": "📕 OSCILADOR ARMÓNICO CUÁNTICO (NIVEL n = {n})",
    "oscillator.intro": "El oscilador armónico modela vibraciones moleculares y campos cuánticos con el potencial parabólico V(x) = ½ m ω² x².",
    "oscillator.step1_title": "🔹 PASO 1: Autoestado ψₙ(x) y Constante de Normalización",
    "oscillator.step1_formula": (
        "  Nivel cuántico: n = {n}\n"
        "  Aₙ = (m·ω / (π·ℏ))^(1/4) · 1 / √(2ⁿ · n!) = {An}\n"
        "  ψₙ(x) = {psi_n}"
    ),
    "oscillator.step2_title": "🔹 PASO 2: Verificación con el Hamiltoniano Ĥ = - (ℏ²/2m) d²/dx² + ½ m ω² x²",
    "oscillator.step2_formula": (
        "  d²ψₙ/dx² = {d2_psi}\n"
        "  Ĥψₙ(x)   = {H_psi}\n"
        "  Energía propia del nivel: E_{n} = {energia_n}   (Eₙ = ℏω(n + ½))"
    ),
    "oscillator.interpretation_ground": (
        "💡 INTERPRETACIÓN FÍSICA: Incluso en el cero absoluto (n = 0), la partícula NO puede quedarse quieta en el fondo del pozo "
        "porque violaría el Principio de Incertidumbre de Heisenberg. Posee una 'Energía de Punto Cero' inquebrantable de E₀ = ½ ℏω."
    ),
    "oscillator.interpretation_excited": (
        "💡 INTERPRETACIÓN FÍSICA: Para el nivel excitado n = {n}, el estado presenta exactamente {n} nodos "
        "espaciales donde la densidad de probabilidad se anula. Su energía exacta es E_{n} = {coeff} ℏω."
    ),

    # -------------------------------------------------------------
    # Formateo Científico: Módulo 4 (Efecto Túnel)
    # -------------------------------------------------------------
    "tunnel.title": "🔮 EFECTO TÚNEL CUÁNTICO A TRAVÉS DE UNA BARRERA DE POTENCIAL RECTANGULAR",
    "tunnel.intro": (
        "Calculamos la transmisión cuántica para una partícula de masa m = {m:.3e} kg con energía E = {E_ev:.4f} eV "
        "que incide sobre una barrera de potencial V₀ = {V0_ev:.4f} eV y espesor a = {ancho_nm:.4f} nm."
    ),
    "tunnel.step1_title": "🔹 PASO 1: Parámetro de Onda y Atenuación en la Barrera",
    "tunnel.step1_subbarrier": (
        "  Régimen: Sub-barrera (E < V₀)\n"
        "  Constante de decaimiento: κ = √[2m(V₀ - E)] / ℏ = {kappa:.4e} m⁻¹\n"
        "  Factor adimensional: κ·a = {kappa_a:.4f}"
    ),
    "tunnel.step1_overbarrier": (
        "  Régimen: Sobre-barrera (E > V₀)\n"
        "  Vector de onda dentro de la barrera: k₂ = √[2m(E - V₀)] / ℏ = {kappa:.4e} m⁻¹\n"
        "  Factor adimensional: k₂·a = {kappa_a:.4f}"
    ),
    "tunnel.step1_resonance": (
        "  Régimen Crítico: Resonancia de borde (E = V₀)\n"
        "  Dentro de la barrera la función de onda degenera en una solución lineal ψ(x) = C·x + D."
    ),
    "tunnel.step2_title": "🔹 PASO 2: Coeficientes Exactos de Transmisión (T) y Reflexión (R)",
    "tunnel.step2_formula": (
        "  Probabilidad de Transmisión (Túnel) : T = {T:.6e}  ({T_percent:.4f}%)\n"
        "  Probabilidad de Reflexión           : R = {R:.6f}  ({R_percent:.4f}%)\n"
        "  Conservación de flujo de probabilidad: T + R = {TR_sum:.6f}"
    ),
    "tunnel.regime_zero_width": "Barrera de ancho nulo (a = 0): Transmisión perfecta T = 1.",
    "tunnel.regime_zero_energy": "Energía de partícula nula (E = 0): Transmisión imposible T = 0.",
    "tunnel.regime_subbarrier_explanation": (
        "💡 INTERPRETACIÓN FÍSICA: Clásicamente la partícula rebotaría con 100% de certeza porque carece de "
        "energía para superar la barrera (E < V₀). En mecánica cuántica, la función de onda decae exponencialmente e^(-κx) "
        "dentro del obstáculo, permitiendo una probabilidad finita de escape por efecto túnel del {T_percent:.4f}%."
    ),
    "tunnel.regime_resonance_explanation": (
        "💡 INTERPRETACIÓN FÍSICA: En el límite exacto E = V₀, el coeficiente de transmisión depende "
        "inversamente del espesor de la barrera según T = [1 + m·V₀·a² / (2ℏ²)]⁻¹."
    ),
    "tunnel.regime_overbarrier_explanation": (
        "💡 INTERPRETACIÓN FÍSICA: Aunque la partícula tiene suficiente energía para cruzar clásicamente (E > V₀), "
        "el cambio abrupto en el potencial produce reflexiones de onda cuánticas, dando T = {T_percent:.4f}% y R = {R_percent:.4f}%."
    ),

    # -------------------------------------------------------------
    # Formateo Científico: Módulo 5 (Hamiltoniano Matricial)
    # -------------------------------------------------------------
    "hamiltonian.title": "📘 DIAGONALIZACIÓN DE HAMILTONIANO MATRICIAL Y EVOLUCIÓN TEMPORAL",
    "hamiltonian.intro": (
        "Analizamos el operador Hamiltoniano matricial Ĥ, verificando su carácter autoadjunto, "
        "calculando sus autovalores y autovectores, la brecha espectral y la evolución temporal."
    ),
    "hamiltonian.matrix_repr": "  Matriz Hamiltoniana H:\n{matrix}",
    "hamiltonian.step1_title": "🔹 PASO 1: Verificación de Hermiticidad (H = H†)",
    "hamiltonian.residual_line": "  Residual de Hermiticidad: ||H - H†||_max = {res:.2e}",
    "hamiltonian.hermitian_yes": "  ¿Es Hermítica?: SÍ (Sistema cerrado con autovalores 100% reales)",
    "hamiltonian.hermitian_no": "  ¿Es Hermítica?: NO (Matriz no autoadjunta; modelo de sistema abierto / disipativo)",
    "hamiltonian.hermitian_exact": "  ¿Es Hermítica?: SÍ (Autoadjunta exacta, autovalores reales garantizados)",
    "hamiltonian.hermitian_approx": "  ¿Es Hermítica?: CASI HERMÍTICA (Residuo numérico ||H - H†|| = {res:.2e})",
    "hamiltonian.non_hermitian": "  ¿Es Hermítica?: NO (Modelo efectivo no hermítico / disipativo o con ganancia)",
    "hamiltonian.step2_title": "🔹 PASO 2: Niveles de Energía (Autovalores) y Autoestados (|Eₙ⟩)",
    "hamiltonian.eigen_residual_info": "  Residuo espectral máximo del par propio ||Hv - λv||: {res:.2e}",
    "hamiltonian.eigen_level_real": "  Nivel E_{idx} = {val:+.6f}   -->   Autoestado |E_{idx}⟩ = [ {vec} ]ᵀ\n",
    "hamiltonian.eigen_level_complex": "  Autovalor λ_{idx} = {val_str}   -->   Vector propio = [ {vec} ]ᵀ\n",
    "hamiltonian.step3_title": "🔹 PASO 3: Brecha de Excitación Cuántica (Gap ΔE)",
    "hamiltonian.gap_info": (
        "  Estado fundamental E₀ = {E0:.6f}\n"
        "  Brecha cuántica al primer nivel excitado distinto: ΔE = {gap:.6f}\n"
        "  Frecuencia de Bohr asociada: ω = ΔE / ℏ = {freq:.6e} rad/s"
    ),
    "hamiltonian.gap_degenerate_note": "  (Se detectó degeneración en el nivel fundamental; el gap se midió al siguiente nivel distinto).",
    "hamiltonian.gap_degenerate_spectrum": "0.0000 (Espectro completamente degenerado; no hay nivel excitado superior distinto).",
    "hamiltonian.non_hermitian_warning": (
        "⚠️ ATENCIÓN: Al tratarse de una matriz no Hermítica, los autovalores poseen partes complejas "
        "o el operador no es autoadjunto. Las partes imaginarias corresponden a tasas de amortiguamiento/decaimiento "
        "o ganancia en sistemas cuánticos abiertos o efectivos."
    ),
    "hamiltonian.step4_title": "🔹 PASO 4: Dinámica Cuántica y Evolución Temporal |ψ(t)⟩ = exp(-iHt/ℏ)|ψ(0)⟩",
    "hamiltonian.evolution_unitary": (
        "  Tiempo transcurrido: t = {t} (en unidades ℏ = 1)\n"
        "  Estado inicial:    |ψ(0)⟩ = [ {psi_0} ]ᵀ  (Norma = {norm_0:.6f})\n"
        "  Estado evolucionado: |ψ(t)⟩ = [ {psi_t} ]ᵀ  (Norma = {norm_t:.6f})\n"
        "  Conservación unitaria: La norma del estado se conserva estrictamente."
    ),
    "hamiltonian.evolution_non_unitary": (
        "  Tiempo transcurrido: t = {t} (en unidades ℏ = 1)\n"
        "  Estado inicial:    |ψ(0)⟩ = [ {psi_0} ]ᵀ  (Norma = {norm_0:.6f})\n"
        "  Estado evolucionado: |ψ(t)⟩ = [ {psi_t} ]ᵀ  (Norma = {norm_t:.6f})\n"
        "  Evolución no unitaria (disipación / ganancia cuántica): La norma varía debido a la no-hermiticidad de H."
    ),

    # -------------------------------------------------------------
    # Mensajes de Error Científicos y del Parser
    # -------------------------------------------------------------
    "error.empty_expression": "La expresión matemática no puede estar vacía.",
    "error.input_too_long": "La expresión excede la longitud máxima permitida ({max_len} caracteres).",
    "error.ast_too_deep": "La expresión es excesivamente compleja o anidada (profundidad > {max_depth}).",
    "error.exponent_too_large": "El exponente numérico ({exp}) excede el límite seguro ({max_exp}).",
    "error.power_nested_too_deep": "Potencias anidadas excesivas detectadas en la expresión.",
    "error.forbidden_node": "Estructura sintáctica no permitida: {node}.",
    "error.forbidden_function": "Función matemática no permitida: '{func}'.",
    "error.forbidden_variable": "Variable o constante no permitida: '{name}'.",
    "error.unsafe_attribute": "Acceso a atributos no permitido.",
    "error.syntax_invalid": "Sintaxis matemática inválida: {detail}",
    "error.null_state_rejected": "El estado cuántico no puede ser la función nula (ψ = 0). La norma sería cero.",
    "error.norm_zero_or_negative": "La integral de densidad |ψ|² es nula o no positiva; la función no es normalizable.",
    "error.norm_divergent": "La integral de normalización diverge (∞) o no converge analíticamente en el dominio especificado. ψ ∉ L².",
    "error.asymptotic_divergence_neg_inf": "La función de onda diverge hacia infinito cuando x -> -oo; no es normalizable en L².",
    "error.asymptotic_divergence_pos_inf": "La función de onda diverge hacia infinito cuando x -> +oo; no es normalizable en L².",
    "error.well_inverted_limits": "Límites invertidos en el pozo de potencial: se requiere a < b, pero se ingresó a={a} > b={b}.",
    "error.quantum_number_integer_positive": "El número cuántico 'n' debe ser un entero positivo (n >= 1).",
    "error.quantum_number_integer_non_negative": "El número cuántico 'n' debe ser un entero no negativo (n >= 0).",
    "error.quantum_number_fractional": "El número cuántico 'n' no puede ser fraccionario. Ingrese un entero válido.",
    "error.well_width_positive": "El ancho del pozo 'L' debe ser un número real estrictamente positivo (L > 0).",
    "error.tunnel_param_finite": "Los parámetros del efecto túnel (E, V0, a) deben ser números reales finitos.",
    "error.tunnel_param_positive": "Los parámetros del efecto túnel deben ser no negativos (E >= 0, V0 >= 0, a >= 0).",
    "error.matrix_not_square": "La matriz ingresada no es cuadrada ({rows} filas x {cols} columnas).",
    "error.matrix_empty": "La matriz Hamiltoniana no puede estar vacía.",
    "error.matrix_invalid_format": "Formato de matriz inválido. Ingrese filas separadas por ';' y elementos por ','.",
    "error.state_vector_dimension_mismatch": "Dimensión del vector de estado ({vec_len}) no coincide con la dimensión del Hamiltoniano ({mat_dim}).",
    "error.state_vector_invalid": "Vector de estado inicial inválido: {detail}",
    "error.time_invalid": "Valor de tiempo 't' inválido: {detail}",
    "error.time_must_be_finite": "El tiempo 't' debe ser un número real finito.",
}
