import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sympy as sp
import numpy as np

from quantumlab_engine.parser import (
    SafeASTParser,
    ParseSecurityError,
    parse_parameters,
    parse_matrix,
    parse_state_vector,
)
from quantumlab_engine.physics import (
    analizar_funcion_onda,
    analizar_schrodinger_1d,
    analizar_pozo_infinito,
    analizar_oscilador_armonico,
    analizar_efecto_tunel,
    analizar_hamiltoniano_matricial,
)
from quantumlab_engine.formatting import (
    formatear_analisis_onda,
    formatear_schrodinger,
    formatear_pozo_infinito,
    formatear_oscilador,
    formatear_tunel,
    formatear_hamiltoniano,
)


class CalculadoraCuanticaAvanzada:
    # Centralized UI palette (Dark theme)
    C = {
        "background": "#080F1D",
        "header": "#0C1627",
        "surface": "#101D31",
        "surface_alt": "#14233A",
        "surface_hover": "#1A304A",
        "active": "#19374D",
        "editor": "#0B1729",
        "border": "#25374F",
        "text": "#F1F6FE",
        "secondary": "#B4C2D5",
        "muted": "#71869F",
        "accent": "#5BE6D6",
        "accent_dark": "#062623",
        "violet": "#B8A1FF",
        "warning": "#F3C879",
        "success": "#70E4AF",
    }

    NOMBRES = [
        "Función de onda", "Schrödinger 1D", "Pozo infinito",
        "Oscilador armónico", "Efecto túnel", "Hamiltoniano",
    ]
    SUBTITULOS = [
        "Normalización y Heisenberg",
        "Autoestados y energía",
        "Probabilidad en una región",
        "Niveles de energía",
        "Barrera de potencial",
        "Autovalores y autovectores",
    ]
    DESCRIPCIONES = [
        "Analiza ψ(x), valores esperados e incertidumbres cuánticas rigurosas.",
        "Comprueba autoestados de Schrödinger, normalizabilidad y energía.",
        "Calcula estados cuantizados n≥1 y probabilidades exactas en el pozo.",
        "Estudia el estado fundamental y niveles excitados n≥0 con Hermite.",
        "Estima transmisión cuántica y reflexión en todas las energías E, V₀.",
        "Diagonaliza matrices hermíticas/no-hermíticas y calcula evolución temporal.",
    ]

    PRESETS = [
        {
            "psi": "exp(-x**2 / 2)",
            "potencial": "0",
            "lim_a": "-oo",
            "lim_b": "oo",
            "params": "Paquete Gaussiano estándar",
        },
        {
            "psi": "sin(pi*x/L)",
            "potencial": "0",
            "lim_a": "0",
            "lim_b": "L",
            "params": "Autoestado de caja cuántica",
        },
        {
            "psi": "sqrt(2/L)*sin(n*pi*x/L)",
            "potencial": "0 (Dentro del pozo), oo (Fuera)",
            "lim_a": "0",
            "lim_b": "L/3",
            "params": "n=1, L=1.0 (nm)",
        },
        {
            "psi": "exp(-m*w*x**2 / (2*hbar))",
            "potencial": "(1/2)*m*w**2*x**2",
            "lim_a": "-oo",
            "lim_b": "oo",
            "params": "n=0 (Estado base)",
        },
        {
            "psi": "exp(I*k*x)",
            "potencial": "V0 = 5.0 eV",
            "lim_a": "0",
            "lim_b": "0.5",
            "params": "E=3.2, V0=5.0, a=0.5 (E, V0 en eV; ancho a en nm)",
        },
        {
            "psi": "[1, 0] (Estado inicial |ψ(0)⟩)",
            "potencial": "Sistema de 2 niveles acoplados",
            "lim_a": "0",
            "lim_b": "1",
            "params": "2, 1-1j; 1+1j, 3",
        },
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("QuantumLab  |  Calculadora Cuántica Pro Max")
        self.root.configure(bg=self.C["background"])

        # QL-024: Responsive initial sizing adapted to screen resolution
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        w = min(1460, max(760, screen_w - 40))
        h = min(870, max(540, screen_h - 60))
        self.root.geometry(f"{w}x{h}")
        self.root.minsize(740, 500)

        # Standard physics symbols preserved for external callers
        self.x = SafeASTParser.x
        self.hbar = SafeASTParser.hbar
        self.m = SafeASTParser.m
        self.w = SafeASTParser.w
        self.L = SafeASTParser.L
        self.n = SafeASTParser.n

        # QL-026: Persistent inputs per mode so clicking modes does not erase user inputs
        self._modo_actual = 0
        self._inputs_por_modo = {i: dict(p) for i, p in enumerate(self.PRESETS)}

        self._configurar_estilos()
        self._construir_layout_dividido()
        self._cargar_modo(0, forzar_preset=True)
        self._actualizar_visual_modo()

        # Keyboard shortcuts
        self.root.bind("<Control-Return>", lambda event: self.resolver_ecuacion())
        self.root.bind("<Control-s>", lambda event: self.exportar_hoja())
        self.root.bind("<Control-l>", lambda event: self.limpiar_hoja())

    def _configurar_estilos(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "Quantum.Vertical.TScrollbar", troughcolor=self.C["editor"],
            background=self.C["border"], bordercolor=self.C["editor"],
            darkcolor=self.C["border"], lightcolor=self.C["border"],
            arrowcolor=self.C["secondary"], relief="flat", width=10
        )
        style.map("Quantum.Vertical.TScrollbar", background=[("active", self.C["surface_hover"])])
        style.configure(
            "Quantum.TCombobox", foreground=self.C["text"],
            fieldbackground=self.C["editor"], background=self.C["surface_alt"],
            bordercolor=self.C["border"], arrowsize=14
        )

    def _texto(self, parent, text, size=10, color="text", weight="normal", bg=None, **kwargs):
        return tk.Label(
            parent, text=text, font=("Segoe UI", size, weight),
            bg=bg or parent.cget("bg"), fg=self.C.get(color, color),
            **kwargs
        )

    def _linea(self, parent, color="border"):
        return tk.Frame(parent, bg=self.C[color], height=1)

    def _boton(self, parent, texto, accion, fondo, frente, fuente=10, alto=10):
        return tk.Button(
            parent, text=texto, command=accion, font=("Segoe UI", fuente, "bold"),
            bg=self.C[fondo], fg=self.C[frente], activebackground=self.C["surface_hover"],
            activeforeground=self.C["text"], bd=0, highlightthickness=0,
            cursor="hand2", relief="flat", padx=10, pady=alto
        )

    def _construir_layout_dividido(self):
        self._construir_encabezado()
        self._construir_pie()
        self.main_grid = tk.Frame(self.root, bg=self.C["background"])
        self.main_grid.pack(fill="both", expand=True, padx=18, pady=(17, 11))
        self.main_grid.grid_rowconfigure(0, weight=1)
        self.main_grid.grid_columnconfigure(0, minsize=220, weight=0)
        self.main_grid.grid_columnconfigure(1, weight=5, minsize=350)
        self.main_grid.grid_columnconfigure(2, weight=7, minsize=380)

        self._construir_sidebar()
        self._construir_editor()
        self._construir_resultados()

    def _construir_encabezado(self):
        header = tk.Frame(self.root, bg=self.C["header"], height=78)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        inner = tk.Frame(header, bg=self.C["header"])
        inner.pack(fill="both", expand=True, padx=23, pady=12)

        icon_box = tk.Frame(inner, bg=self.C["active"], width=50, height=50)
        icon_box.pack(side="left")
        icon_box.pack_propagate(False)
        self._texto(icon_box, "⚛", 24, "accent", bg=self.C["active"]).pack(expand=True)

        brand = tk.Frame(inner, bg=self.C["header"])
        brand.pack(side="left", padx=14)
        name = tk.Frame(brand, bg=self.C["header"])
        name.pack(anchor="w")
        self._texto(name, "QUANTUM", 17, "text", "bold").pack(side="left")
        self._texto(name, "LAB", 17, "accent", "bold").pack(side="left", padx=(5, 0))
        self._texto(brand, "ESTUDIO DE MECÁNICA CUÁNTICA  /  PRO MAX (SECURED)", 8, "muted", "bold").pack(anchor="w")

        right = tk.Frame(inner, bg=self.C["header"])
        right.pack(side="right", fill="y")
        self._texto(right, "MOTOR CIENTÍFICO VERIFICADO", 9, "success", "bold").pack(anchor="e", pady=(2, 3))
        self._texto(right, "SymPy  •  NumPy  •  AST Parser", 9, "secondary").pack(anchor="e")
        self._linea(self.root).pack(fill="x")

    def _construir_sidebar(self):
        sidebar = tk.Frame(
            self.main_grid, bg=self.C["surface"], width=225,
            highlightbackground=self.C["border"], highlightthickness=1
        )
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 11))
        sidebar.grid_propagate(False)

        self._texto(sidebar, "ESPACIO DE TRABAJO", 9, "muted", "bold").pack(anchor="w", padx=18, pady=(20, 6))
        self._texto(sidebar, "Módulos de cálculo", 12, "text", "bold").pack(anchor="w", padx=18)
        self._texto(sidebar, "Selecciona un sistema", 9, "secondary").pack(anchor="w", padx=18, pady=(3, 14))
        self._linea(sidebar).pack(fill="x", padx=17, pady=(0, 12))

        self.modos = [
            "1. Análisis Completo de Función de Onda ψ(x): Normalización, ⟨x⟩, ⟨p⟩, ⟨T⟩ y Heisenberg",
            "2. Ecuación de Schrödinger 1D: Verificar autoestado y extraer Energía E(x)",
            "3. Sistema Completo: Pozo de Potencial Infinito 1D y Probabilidad en Región",
            "4. Sistema Completo: Oscilador Armónico Cuántico y Niveles de Energía",
            "5. Efecto Túnel Cuántico: Transmisión a través de Barrera de Potencial",
            "6. Diagonalización de Hamiltoniano Matricial (H|ψ⟩ = E|ψ⟩) y Evolución Temporal",
        ]

        # QL-025: Fully synchronized and accessible Combobox
        self.combo_modo = ttk.Combobox(sidebar, values=self.modos, state="readonly", style="Quantum.TCombobox")
        self.combo_modo.current(0)
        self.combo_modo.pack(fill="x", padx=14, pady=(0, 10))
        self.combo_modo.bind("<<ComboboxSelected>>", lambda e: self._seleccionar_modo(self.combo_modo.current()))

        self.nav_filas = []
        for i, (nombre, subtitulo) in enumerate(zip(self.NOMBRES, self.SUBTITULOS)):
            fila = tk.Frame(sidebar, bg=self.C["surface"], cursor="hand2", height=54)
            fila.pack(fill="x", padx=8, pady=2)
            fila.pack_propagate(False)
            barra = tk.Frame(fila, bg=self.C["surface"], width=3)
            barra.pack(side="left", fill="y")
            numero = self._texto(fila, f"{i+1:02}", 10, "muted", "bold")
            numero.pack(side="left", padx=(8, 8))
            contenido = tk.Frame(fila, bg=self.C["surface"])
            contenido.pack(side="left", fill="both", expand=True)
            title = self._texto(contenido, nombre, 10, "text", "bold", anchor="w")
            title.pack(fill="x", pady=(6, 1))
            sub = self._texto(contenido, subtitulo, 8, "muted", anchor="w")
            sub.pack(fill="x")
            widgets = (fila, barra, numero, contenido, title, sub)
            for widget in widgets:
                widget.bind("<Button-1>", lambda e, idx=i: self._seleccionar_modo(idx))
                widget.bind("<Enter>", lambda e, idx=i: self._pintar_navegacion(idx))
                widget.bind("<Leave>", lambda e: self._pintar_navegacion())
            self.nav_filas.append((fila, barra, numero, contenido, title, sub))

        tk.Frame(sidebar, bg=self.C["surface"]).pack(fill="both", expand=True)
        self._linea(sidebar).pack(fill="x", padx=17, pady=(5, 12))
        self._texto(sidebar, "ATAJOS DE TECLADO", 8, "muted", "bold").pack(anchor="w", padx=18)
        self._texto(sidebar, "Ctrl + Enter   Resolver", 9, "secondary").pack(anchor="w", padx=18, pady=(7, 2))
        self._texto(sidebar, "Ctrl + S       Exportar", 9, "secondary").pack(anchor="w", padx=18, pady=2)
        self._texto(sidebar, "Ctrl + L       Limpiar", 9, "secondary").pack(anchor="w", padx=18, pady=(2, 16))

    def _guardar_entradas_actuales(self):
        """QL-026: Saves current entry contents to avoid losing work when switching modes."""
        self._inputs_por_modo[self._modo_actual] = {
            "psi": self.entry_psi.get(),
            "potencial": self.entry_potencial.get(),
            "lim_a": self.entry_lim_a.get(),
            "lim_b": self.entry_lim_b.get(),
            "params": self.entry_params.get(),
        }

    def _cargar_modo(self, idx, forzar_preset=False):
        """Loads saved or preset entries for the given mode index."""
        self.entry_psi.delete(0, tk.END)
        self.entry_potencial.delete(0, tk.END)
        self.entry_lim_a.delete(0, tk.END)
        self.entry_lim_b.delete(0, tk.END)
        self.entry_params.delete(0, tk.END)

        data = self.PRESETS[idx] if forzar_preset else self._inputs_por_modo.get(idx, self.PRESETS[idx])
        self.entry_psi.insert(0, data["psi"])
        self.entry_potencial.insert(0, data["potencial"])
        self.entry_lim_a.insert(0, data["lim_a"])
        self.entry_lim_b.insert(0, data["lim_b"])
        self.entry_params.insert(0, data["params"])

    def _seleccionar_modo(self, idx):
        """QL-026: Preserves user input when re-clicking the same mode or switching."""
        if idx == self._modo_actual:
            # Re-clicking the active card does NOT erase user inputs!
            return

        self._guardar_entradas_actuales()
        self._modo_actual = idx
        self.combo_modo.current(idx)
        self._cargar_modo(idx, forzar_preset=False)
        self._actualizar_visual_modo()
        self.canvas_entrada.yview_moveto(0)

    def restablecer_preset_actual(self):
        """Explicitly reloads the default preset for the current mode."""
        self._cargar_modo(self._modo_actual, forzar_preset=True)
        self._guardar_entradas_actuales()
        messagebox.showinfo("Preset restablecido", f"Se cargó el ejemplo predeterminado para '{self.NOMBRES[self._modo_actual]}'.")

    def _cargar_preset_ejemplo(self):
        """Backward-compatibility wrapper for test suites and presets."""
        idx = self.combo_modo.current()
        self._modo_actual = idx
        self._cargar_modo(idx, forzar_preset=True)

    def _pintar_navegacion(self, hover=None):
        active = self.combo_modo.current()
        for i, widgets in enumerate(self.nav_filas):
            fila, barra, numero, contenido, title, sub = widgets
            seleccionado = (i == active)
            fondo = self.C["active"] if seleccionado else (
                self.C["surface_hover"] if i == hover else self.C["surface"]
            )
            for w in (fila, numero, contenido, title, sub):
                w.config(bg=fondo)
            barra.config(bg=self.C["accent"] if seleccionado else fondo)
            numero.config(fg=self.C["accent"] if seleccionado else self.C["muted"])
            title.config(fg=self.C["text"] if seleccionado else self.C["secondary"])
            sub.config(fg=self.C["accent"] if seleccionado else self.C["muted"])

    def _actualizar_visual_modo(self):
        idx = self.combo_modo.current()
        self._pintar_navegacion()
        self.editor_contador.config(text=f"MÓDULO  {idx+1:02d} / 06")
        self.editor_titulo.config(text=self.NOMBRES[idx])
        self.editor_descripcion.config(text=self.DESCRIPCIONES[idx])

        # QL-030: Dynamic hints indicating which inputs are active in current mode
        hints = [
            ("ψ(x)", "V(x) [Informativo]", "Límite inf. a", "Límite sup. b", "Parámetros [Informativo]"),
            ("ψ(x)", "Potencial V(x)", "Límite inf. a (opcional)", "Límite sup. b (opcional)", "Parámetros [Informativo]"),
            ("ψ(x) analítica", "V(x) [Informativo]", "Región inf. a", "Región sup. b", "n entero (ej. n=1, L=1.0)"),
            ("ψ(x) analítica", "V(x) armónico", "Límite inf. [-oo]", "Límite sup. [oo]", "Nivel n (ej. n=0, 1, 2...)"),
            ("Onda incidente", "Barrera V₀", "Límite a", "Espesor a (nm)", "E, V0, a (ej. E=3.2, V0=5.0, a=0.5)"),
            ("Estado inicial |ψ(0)⟩", "Sistema", "Tiempo t", "Límite b", "Matriz H (ej. 2, 1-1j; 1+1j, 3)"),
        ]
        h = hints[idx]
        self.lbl_hint_psi.config(text=h[0])
        self.lbl_hint_pot.config(text=h[1])
        self.lbl_hint_params.config(text=h[4])

    def _construir_editor(self):
        self.panel_izq = tk.Frame(
            self.main_grid, bg=self.C["surface"],
            highlightbackground=self.C["border"], highlightthickness=1
        )
        self.panel_izq.grid(row=0, column=1, sticky="nsew", padx=(0, 11))
        self.panel_izq.grid_rowconfigure(1, weight=1)
        self.panel_izq.grid_columnconfigure(0, weight=1)

        title_area = tk.Frame(self.panel_izq, bg=self.C["surface"], height=115)
        title_area.grid(row=0, column=0, sticky="ew")
        title_area.pack_propagate(False)
        self.editor_contador = self._texto(title_area, "MÓDULO  01 / 06", 9, "accent", "bold")
        self.editor_contador.pack(anchor="w", padx=23, pady=(16, 3))
        self.editor_titulo = self._texto(title_area, "Función de onda", 18, "text", "bold")
        self.editor_titulo.pack(anchor="w", padx=23)
        self.editor_descripcion = self._texto(
            title_area, "", 9, "secondary", anchor="w", justify="left", wraplength=340
        )
        self.editor_descripcion.pack(anchor="w", padx=23, pady=(2, 4))
        self._linea(title_area).pack(side="bottom", fill="x")

        central = tk.Frame(self.panel_izq, bg=self.C["surface"])
        central.grid(row=1, column=0, sticky="nsew")
        central.grid_rowconfigure(0, weight=1)
        central.grid_columnconfigure(0, weight=1)
        self.canvas_entrada = tk.Canvas(
            central, bg=self.C["surface"], highlightthickness=0, bd=0, width=1, height=1
        )
        self.canvas_entrada.grid(row=0, column=0, sticky="nsew")
        barra_scroll = ttk.Scrollbar(
            central, orient="vertical", command=self.canvas_entrada.yview,
            style="Quantum.Vertical.TScrollbar"
        )
        barra_scroll.grid(row=0, column=1, sticky="ns")
        self.canvas_entrada.configure(yscrollcommand=barra_scroll.set)
        inner = tk.Frame(self.canvas_entrada, bg=self.C["surface"])
        frame_id = self.canvas_entrada.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: self.canvas_entrada.configure(
            scrollregion=self.canvas_entrada.bbox("all")
        ))
        self.canvas_entrada.bind("<Configure>", lambda e: self.canvas_entrada.itemconfigure(
            frame_id, width=e.width
        ))

        form = tk.Frame(inner, bg=self.C["surface"])
        form.pack(fill="x", padx=20, pady=(14, 16))

        self._rotulo(form, "01", "FUNCIÓN DE ONDA  ψ(x) / ESTADO")
        self.entry_psi = self._entrada(form, accent=True)
        self.lbl_hint_psi = self._texto(form, "Expresión simbólica en función de x", 8, "muted")
        self.lbl_hint_psi.pack(anchor="w", pady=(3, 10))

        self._rotulo(form, "02", "POTENCIAL  V(x)")
        self.entry_potencial = self._entrada(form)
        self.lbl_hint_pot = self._texto(form, "Admite x, m, w y hbar", 8, "muted")
        self.lbl_hint_pot.pack(anchor="w", pady=(3, 10))

        self._rotulo(form, "03", "LÍMITES DE INTEGRACIÓN / TIEMPO")
        limites = tk.Frame(form, bg=self.C["surface"])
        limites.pack(fill="x", pady=(4, 10))
        limites.grid_columnconfigure(0, weight=1, uniform="limits")
        limites.grid_columnconfigure(1, weight=1, uniform="limits")
        self._texto(limites, "Límite inferior  a / t", 9, "secondary").grid(row=0, column=0, sticky="w")
        self._texto(limites, "Límite superior  b", 9, "secondary").grid(row=0, column=1, sticky="w", padx=(8, 0))
        self.entry_lim_a = self._entrada(limites, use_grid=True, column=0, padx=(0, 8))
        self.entry_lim_b = self._entrada(limites, use_grid=True, column=1, padx=(8, 0))

        self._rotulo(form, "04", "PARÁMETROS / HAMILTONIANO H")
        self.entry_params = self._entrada(form)
        self.lbl_hint_params = self._texto(form, "Separar columnas con ',' y filas con ';'", 8, "muted", wraplength=350, justify="left")
        self.lbl_hint_params.pack(anchor="w", pady=(3, 14))

        self._linea(form).pack(fill="x", pady=(0, 12))
        ptitle = tk.Frame(form, bg=self.C["surface"])
        ptitle.pack(fill="x", pady=(0, 9))
        self._texto(ptitle, "TECLADO SIMBÓLICO", 10, "text", "bold").pack(side="left")
        self._texto(ptitle, "Insertar en campo activo", 8, "muted").pack(side="right")

        pad = tk.Frame(form, bg=self.C["surface"])
        pad.pack(fill="x")
        for i in range(4):
            pad.grid_columnconfigure(i, weight=1, uniform="keys")

        botones_simbolos = [
            ("sin(x)", "sin(x)"), ("cos(x)", "cos(x)"), ("exp(-x²)", "exp(-x**2)"), ("sqrt()", "sqrt()"),
            ("π (pi)", "pi"), ("ℏ (hbar)", "hbar"), ("∞ (oo)", "oo"), ("-∞ (-oo)", "-oo"),
            ("x²", "x**2"), ("L (Ancho)", "L"), ("ω (Omega)", "w"), ("m (Masa)", "m"),
            ("Pozo ψ₁", "sqrt(2/L)*sin(pi*x/L)"), ("Gaussiana", "exp(-x**2/2)"),
            ("Armónico n=1", "x*exp(-x**2/2)"), ("H Pauli-X", "0, 1; 1, 0")
        ]
        for i, (etiqueta, valor) in enumerate(botones_simbolos):
            boton = self._boton(
                pad, etiqueta, lambda v=valor: self._insertar_en_foco(v),
                "surface_alt", "secondary", fuente=9, alto=6
            )
            boton.grid(row=i // 4, column=i % 4, sticky="ew", padx=2, pady=2)
        self._vincular_rueda(inner)

        action_area = tk.Frame(self.panel_izq, bg=self.C["surface"])
        action_area.grid(row=2, column=0, sticky="ew")
        self._linea(action_area).pack(fill="x")
        buttons = tk.Frame(action_area, bg=self.C["surface"])
        buttons.pack(fill="x", padx=20, pady=12)

        run = self._boton(buttons, "⚡  RESOLVER ECUACIÓN", self.resolver_ecuacion,
                          "accent", "accent_dark", fuente=11, alto=9)
        run.config(activebackground="#90FFF1", activeforeground=self.C["accent_dark"])
        run.pack(fill="x", pady=(0, 7))

        row = tk.Frame(buttons, bg=self.C["surface"])
        row.pack(fill="x")
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=1)
        row.grid_columnconfigure(2, weight=1)
        self._boton(row, "Limpiar", self.limpiar_hoja,
                    "surface_alt", "secondary", alto=7).grid(row=0, column=0, sticky="ew", padx=(0, 3))
        self._boton(row, "Restablecer", self.restablecer_preset_actual,
                    "surface_alt", "secondary", alto=7).grid(row=0, column=1, sticky="ew", padx=3)
        self._boton(row, "Exportar", self.exportar_hoja,
                    "surface_alt", "secondary", alto=7).grid(row=0, column=2, sticky="ew", padx=(3, 0))

    def _rotulo(self, parent, indice, texto):
        linea = tk.Frame(parent, bg=self.C["surface"])
        linea.pack(fill="x", pady=(0, 5))
        self._texto(linea, indice, 9, "accent", "bold").pack(side="left", padx=(0, 8))
        self._texto(linea, texto, 9, "secondary", "bold").pack(side="left")

    def _entrada(self, parent, accent=False, use_grid=False, column=0, padx=0):
        campo = tk.Entry(
            parent, bg=self.C["editor"],
            fg=self.C["accent"] if accent else self.C["text"],
            insertbackground=self.C["accent"],
            selectbackground=self.C["active"], selectforeground=self.C["text"],
            relief="flat", font=("Consolas", 11), bd=0,
            highlightthickness=1, highlightbackground=self.C["border"],
            highlightcolor=self.C["accent"]
        )
        if use_grid:
            campo.grid(row=1, column=column, sticky="ew", padx=padx, pady=(4, 0), ipady=9, ipadx=8)
        else:
            campo.pack(fill="x", ipady=9, ipadx=8)
        return campo

    def _vincular_rueda(self, widget):
        widget.bind("<MouseWheel>", self._rueda_editor, add="+")
        widget.bind("<Button-4>", self._rueda_editor, add="+")
        widget.bind("<Button-5>", self._rueda_editor, add="+")
        for child in widget.winfo_children():
            self._vincular_rueda(child)

    def _rueda_editor(self, event):
        if getattr(event, "num", None) == 4:
            pasos = -2
        elif getattr(event, "num", None) == 5:
            pasos = 2
        else:
            pasos = -int(event.delta / 120)
            if pasos == 0:
                pasos = -1 if event.delta > 0 else 1
        self.canvas_entrada.yview_scroll(pasos, "units")
        return "break"

    def _construir_resultados(self):
        self.panel_der = tk.Frame(
            self.main_grid, bg=self.C["surface"],
            highlightbackground=self.C["border"], highlightthickness=1
        )
        self.panel_der.grid(row=0, column=2, sticky="nsew")
        self.panel_der.grid_rowconfigure(1, weight=1)
        self.panel_der.grid_columnconfigure(0, weight=1)

        head = tk.Frame(self.panel_der, bg=self.C["surface"], height=115)
        head.grid(row=0, column=0, sticky="ew")
        head.pack_propagate(False)
        self._texto(head, "CONSOLA DE RESULTADOS", 9, "violet", "bold").pack(anchor="w", padx=22, pady=(16, 3))
        self._texto(head, "Hoja de resultados", 18, "text", "bold").pack(anchor="w", padx=22)
        bottom = tk.Frame(head, bg=self.C["surface"])
        bottom.pack(fill="x", padx=22, pady=(2, 0))
        self._texto(bottom, "Desarrollo matemático paso a paso", 9, "secondary").pack(side="left")
        self.etiqueta_estado = self._texto(bottom, "SIN RESULTADOS", 8, "muted", "bold")
        self.etiqueta_estado.pack(side="right")
        self._linea(head).pack(side="bottom", fill="x")

        output_container = tk.Frame(self.panel_der, bg=self.C["editor"])
        output_container.grid(row=1, column=0, sticky="nsew", padx=12, pady=12)
        self.hoja = tk.Text(
            output_container, bg=self.C["editor"], fg=self.C["secondary"],
            insertbackground=self.C["accent"],
            selectbackground=self.C["active"], selectforeground=self.C["text"],
            font=("Segoe UI", 11), wrap="word", bd=0, highlightthickness=0,
            padx=15, pady=14, spacing1=3, spacing3=4, undo=True, width=1, height=1,
        )
        scroll = ttk.Scrollbar(
            output_container, command=self.hoja.yview,
            style="Quantum.Vertical.TScrollbar"
        )
        scroll.pack(side="right", fill="y")
        self.hoja.pack(side="left", fill="both", expand=True)
        self.hoja.configure(yscrollcommand=scroll.set)

        self.hoja.tag_configure(
            "titulo", font=("Segoe UI", 12, "bold"), foreground=self.C["accent"],
            spacing1=12, spacing3=10
        )
        self.hoja.tag_configure(
            "paso", font=("Segoe UI", 11, "bold"), foreground=self.C["warning"],
            spacing1=12, spacing3=6
        )
        self.hoja.tag_configure(
            "explicacion", font=("Segoe UI", 11), foreground=self.C["secondary"],
            spacing1=4, spacing3=5
        )
        self.hoja.tag_configure(
            "formula", font=("Consolas", 10, "bold"), foreground=self.C["text"],
            background=self.C["surface_alt"], lmargin1=12, lmargin2=12,
            rmargin=8, spacing1=8, spacing3=8
        )
        self.hoja.tag_configure(
            "conclusion", font=("Segoe UI", 11, "bold"), foreground=self.C["success"],
            spacing1=10, spacing3=10
        )
        self.hoja.tag_configure(
            "advertencia", font=("Segoe UI", 10, "italic"), foreground=self.C["warning"],
            spacing1=8, spacing3=8
        )
        self.hoja.tag_configure("separador", foreground=self.C["border"], spacing1=6, spacing3=6)

        self.estado_vacio = tk.Frame(output_container, bg=self.C["editor"])
        self._texto(self.estado_vacio, "⚛", 44, "accent").pack(pady=(0, 14))
        self._texto(self.estado_vacio, "Tu espacio de resultados", 15, "text", "bold").pack()
        self._texto(
            self.estado_vacio,
            "Selecciona un módulo, ajusta las entradas\ny ejecuta el cálculo para ver los pasos.",
            10, "secondary", justify="center"
        ).pack(pady=(8, 0))
        self.estado_vacio.place(relx=0.5, rely=0.45, anchor="center")

        footer = tk.Frame(self.panel_der, bg=self.C["surface"])
        footer.grid(row=2, column=0, sticky="ew")
        self._linea(footer).pack(fill="x")
        self._texto(
            footer, "SALIDA SIMBÓLICA  •  MOTOR MATEMÁTICO VERIFICADO  •  EXPORTACIÓN .TXT",
            8, "muted", "bold"
        ).pack(anchor="w", padx=22, pady=12)

    def _construir_pie(self):
        footer = tk.Frame(self.root, bg=self.C["background"])
        footer.pack(fill="x", side="bottom", padx=23, pady=(0, 9))
        self._texto(footer, "QUANTUMLAB  /  WORKSPACE", 8, "muted", "bold").pack(side="left")
        self._texto(footer, "Motor científico riguroso  ·  Seguridad AST activa", 8, "muted").pack(side="right")

    def _insertar_en_foco(self, texto):
        widget = self.root.focus_get()
        if isinstance(widget, tk.Entry):
            widget.insert(tk.INSERT, texto)
        else:
            self.entry_psi.insert(tk.INSERT, texto)

    def _texto_seguro(self, texto):
        """Convierte símbolos Unicode no compatibles con ciertas fuentes Windows."""
        reemplazos = {
            "⟨": "<",
            "⟩": ">",
            "ℏ": "ħ",
            "≤": "<=",
            "≥": ">=",
            "−": "-",
        }
        for origen, destino in reemplazos.items():
            texto = texto.replace(origen, destino)
        return texto

    def _escribir(self, texto, tag="explicacion"):
        self.estado_vacio.place_forget()
        texto = self._texto_seguro(str(texto))
        self.hoja.insert(tk.END, texto + "\n", tag)
        self.hoja.see(tk.END)

    def _escribir_bloques(self, bloques):
        self.estado_vacio.place_forget()
        for texto, tag in bloques:
            self._escribir(texto, tag)

    def limpiar_hoja(self):
        self.hoja.delete("1.0", tk.END)
        self.estado_vacio.place(relx=0.5, rely=0.45, anchor="center")
        self.etiqueta_estado.config(text="SIN RESULTADOS", fg=self.C["muted"])

    def exportar_hoja(self):
        """QL-028: Robust file export with system exception handling."""
        contenido = self.hoja.get("1.0", tk.END).strip()
        if not contenido:
            messagebox.showwarning("Hoja vacía", "Resuelve primero una ecuación antes de exportar.")
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de Texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return

        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)
            messagebox.showinfo("Exportado exitoso", f"Hoja de resultados guardada correctamente en:\n{ruta}")
        except OSError as e:
            messagebox.showerror("Error al guardar archivo", f"No se pudo escribir en la ruta especificada:\n{e}")

    def _parsear_expresion(self, texto):
        """QL-001: Safe AST parser replacing sp.sympify()."""
        return SafeASTParser.parse(texto)

    # =========================================================
    # MOTOR DE RESOLUCIÓN Y DESPACHO
    # =========================================================
    def resolver_ecuacion(self):
        """QL-027: Handles calculation with accurate status updates without false claims."""
        modo = self.combo_modo.current()
        self.etiqueta_estado.config(text="CALCULANDO...", fg=self.C["warning"])
        self.root.update_idletasks()

        try:
            if modo == 0:
                self._resolver_analisis_onda()
            elif modo == 1:
                self._resolver_schrodinger_simbolico()
            elif modo == 2:
                self._resolver_pozo_infinito()
            elif modo == 3:
                self._resolver_oscilador_armonico()
            elif modo == 4:
                self._resolver_efecto_tunel()
            elif modo == 5:
                self._resolver_hamiltoniano_matricial()

            self._escribir("═" * 68, "separador")
            self.etiqueta_estado.config(text="RESULTADOS DISPONIBLES", fg=self.C["success"])

        except ParseSecurityError as e:
            self.etiqueta_estado.config(text="ERROR DE SINTAXIS/SEGURIDAD", fg=self.C["warning"])
            messagebox.showerror("Error de Sintaxis / Seguridad Matemática", str(e))
        except ValueError as e:
            self.etiqueta_estado.config(text="ERROR EN PARÁMETROS", fg=self.C["warning"])
            messagebox.showerror("Parámetro o Dominio Inválido", str(e))
        except Exception as e:
            self.etiqueta_estado.config(text="ERROR DE CÁLCULO", fg=self.C["warning"])
            messagebox.showerror("Error de Cálculo Científico", f"Ocurrió un error al procesar el sistema:\n{e}")

    # =========================================================
    # RESOLUTORES POR MODALIDAD
    # =========================================================
    def _resolver_analisis_onda(self):
        psi_raw = self._parsear_expresion(self.entry_psi.get())
        a = self._parsear_expresion(self.entry_lim_a.get())
        b = self._parsear_expresion(self.entry_lim_b.get())

        res = analizar_funcion_onda(psi_raw, a, b)
        bloques = formatear_analisis_onda(res)
        self._escribir_bloques(bloques)

    def _resolver_schrodinger_simbolico(self):
        psi = self._parsear_expresion(self.entry_psi.get())
        V = self._parsear_expresion(self.entry_potencial.get())

        # Read optional integration bounds if provided
        a_str = self.entry_lim_a.get().strip()
        b_str = self.entry_lim_b.get().strip()
        a = self._parsear_expresion(a_str) if a_str else None
        b = self._parsear_expresion(b_str) if b_str else None

        res = analizar_schrodinger_1d(psi, V, a=a, b=b)
        bloques = formatear_schrodinger(res)
        self._escribir_bloques(bloques)

    def _resolver_pozo_infinito(self):
        a = self._parsear_expresion(self.entry_lim_a.get())
        b = self._parsear_expresion(self.entry_lim_b.get())

        params = parse_parameters(self.entry_params.get())
        n_val = int(params.get("n", 1))

        res = analizar_pozo_infinito(a, b, n_val=n_val)
        bloques = formatear_pozo_infinito(res)
        self._escribir_bloques(bloques)

    def _resolver_oscilador_armonico(self):
        params = parse_parameters(self.entry_params.get())
        n_val = int(params.get("n", 0))

        res = analizar_oscilador_armonico(n_val=n_val)
        bloques = formatear_oscilador(res)
        self._escribir_bloques(bloques)

    def _resolver_efecto_tunel(self):
        params = parse_parameters(self.entry_params.get())
        E_ev = float(params.get("E", 3.2))
        V0_ev = float(params.get("V0", 5.0))
        ancho_nm = float(params.get("a", 0.5))

        res = analizar_efecto_tunel(E_ev=E_ev, V0_ev=V0_ev, ancho_nm=ancho_nm)
        bloques = formatear_tunel(res)
        self._escribir_bloques(bloques)

    def _resolver_hamiltoniano_matricial(self):
        raw_matrix = self.entry_params.get().strip()
        H = parse_matrix(raw_matrix)

        # Parse initial state vector if provided
        raw_psi = self.entry_psi.get().strip()
        psi_0 = None
        preset_psi = self.PRESETS[5]["psi"].strip()
        if raw_psi:
            # If user left the 2-level preset untouched with an N!=2 matrix, treat as no state vector provided
            if raw_psi == preset_psi and H.shape[0] != 2:
                psi_0 = None
            else:
                try:
                    psi_0 = parse_state_vector(raw_psi, expected_dim=H.shape[0])
                except Exception as e:
                    raise ValueError(f"Vector de estado inicial inválido: {e}")

        # Parse time t if given in lim_a
        t_val = 0.0
        t_str = self.entry_lim_a.get().strip()
        if t_str:
            try:
                t_sym = self._parsear_expresion(t_str)
                t_val = float(t_sym.evalf())
                if not np.isfinite(t_val):
                    raise ValueError("El tiempo 't' debe ser un número real finito.")
            except Exception as e:
                raise ValueError(f"Valor de tiempo 't' inválido en Límite a: {e}")

        res = analizar_hamiltoniano_matricial(H, psi_0=psi_0, t_val=t_val)
        bloques = formatear_hamiltoniano(res)
        self._escribir_bloques(bloques)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraCuanticaAvanzada(root)
    root.mainloop()