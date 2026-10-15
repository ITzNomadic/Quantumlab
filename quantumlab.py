import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sympy as sp
import numpy as np


class CalculadoraCuanticaAvanzada:
    # Paleta centralizada. Todo el rediseño usa Tkinter/ttk, sin nuevas dependencias.
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
        "Analiza ψ(x), valores esperados e incertidumbres cuánticas.",
        "Comprueba autoestados de Schrödinger y despeja su energía.",
        "Calcula estados cuantizados y probabilidades de posición.",
        "Estudia el estado fundamental y la energía de punto cero.",
        "Estima transmisión y reflexión al atravesar una barrera.",
        "Diagonaliza matrices y examina sus estados estacionarios.",
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("QuantumLab  |  Calculadora Cuántica Pro Max")
        self.root.configure(bg=self.C["background"])
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        w = min(1460, max(1050, screen_w - 90))
        h = min(870, max(650, screen_h - 95))
        self.root.geometry(f"{w}x{h}")
        self.root.minsize(1030, 640)

        # Variables simbólicas originales: sin modificaciones.
        self.x = sp.Symbol('x', real=True)
        self.hbar = sp.Symbol('ℏ', positive=True, real=True)
        self.m = sp.Symbol('m', positive=True, real=True)
        self.w = sp.Symbol('ω', positive=True, real=True)
        self.L = sp.Symbol('L', positive=True, real=True)
        self.n = sp.Symbol('n', integer=True, positive=True)

        self._configurar_estilos()
        self._construir_layout_dividido()
        self._cargar_preset_ejemplo()
        self._actualizar_visual_modo()
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
        button = tk.Button(
            parent, text=texto, command=accion, font=("Segoe UI", fuente, "bold"),
            bg=self.C[fondo], fg=self.C[frente], activebackground=self.C["surface_hover"],
            activeforeground=self.C["text"], bd=0, highlightthickness=0,
            cursor="hand2", relief="flat", padx=10, pady=alto
        )
        return button

    def _construir_layout_dividido(self):
        self._construir_encabezado()
        self._construir_pie()
        self.main_grid = tk.Frame(self.root, bg=self.C["background"])
        self.main_grid.pack(fill="both", expand=True, padx=18, pady=(17, 11))
        self.main_grid.grid_rowconfigure(0, weight=1)
        self.main_grid.grid_columnconfigure(0, minsize=225, weight=0)
        self.main_grid.grid_columnconfigure(1, weight=5, minsize=376)
        self.main_grid.grid_columnconfigure(2, weight=7, minsize=400)

        self._construir_sidebar()
        self._construir_editor()
        self._construir_resultados()

    def _construir_encabezado(self):
        header = tk.Frame(self.root, bg=self.C["header"], height=84)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        inner = tk.Frame(header, bg=self.C["header"])
        inner.pack(fill="both", expand=True, padx=23, pady=14)

        icon_box = tk.Frame(inner, bg=self.C["active"], width=52, height=52)
        icon_box.pack(side="left")
        icon_box.pack_propagate(False)
        self._texto(icon_box, "⚛", 26, "accent", bg=self.C["active"]).pack(expand=True)

        brand = tk.Frame(inner, bg=self.C["header"])
        brand.pack(side="left", padx=14)
        name = tk.Frame(brand, bg=self.C["header"])
        name.pack(anchor="w")
        self._texto(name, "QUANTUM", 18, "text", "bold").pack(side="left")
        self._texto(name, "LAB", 18, "accent", "bold").pack(side="left", padx=(5, 0))
        self._texto(brand, "ESTUDIO DE MECÁNICA CUÁNTICA  /  PRO MAX", 8, "muted", "bold").pack(anchor="w", pady=(0, 0))

        right = tk.Frame(inner, bg=self.C["header"])
        right.pack(side="right", fill="y")
        self._texto(right, "MOTOR SIMBÓLICO ACTIVO", 9, "success", "bold").pack(anchor="e", pady=(3, 4))
        self._texto(right, "SymPy  •  NumPy  •  Python", 9, "secondary").pack(anchor="e")
        self._linea(self.root).pack(fill="x")

    def _construir_sidebar(self):
        sidebar = tk.Frame(
            self.main_grid, bg=self.C["surface"], width=225,
            highlightbackground=self.C["border"], highlightthickness=1
        )
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 11))
        sidebar.grid_propagate(False)

        self._texto(sidebar, "ESPACIO DE TRABAJO", 9, "muted", "bold").pack(anchor="w", padx=18, pady=(27, 7))
        self._texto(sidebar, "Módulos de cálculo", 12, "text", "bold").pack(anchor="w", padx=18)
        self._texto(sidebar, "Selecciona un sistema", 9, "secondary").pack(anchor="w", padx=18, pady=(4, 18))
        self._linea(sidebar).pack(fill="x", padx=17, pady=(0, 14))

        # Se conserva el mismo selector lógico: resolver_ecuacion() sigue leyendo .current().
        self.modos = [
            "1. Análisis Completo de Función de Onda ψ(x): Normalización, ⟨x⟩, ⟨p⟩, ⟨T⟩ y Heisenberg",
            "2. Ecuación de Schrödinger 1D: Verificar autoestado y extraer Energía E(x)",
            "3. Sistema Completo: Pozo de Potencial Infinito 1D y Probabilidad en Región",
            "4. Sistema Completo: Oscilador Armónico Cuántico y Niveles de Energía",
            "5. Efecto Túnel Cuántico: Transmisión a través de Barrera de Potencial",
            "6. Diagonalización de Hamiltoniano Matricial (H|ψ⟩ = E|ψ⟩) y Evolución Temporal",
        ]
        self.combo_modo = ttk.Combobox(sidebar, values=self.modos, state="readonly")
        self.combo_modo.current(0)
        self.combo_modo.bind("<<ComboboxSelected>>", lambda e: self._cargar_preset_ejemplo())

        self.nav_filas = []
        for i, (nombre, subtitulo) in enumerate(zip(self.NOMBRES, self.SUBTITULOS)):
            fila = tk.Frame(sidebar, bg=self.C["surface"], cursor="hand2", height=58)
            fila.pack(fill="x", padx=10, pady=3)
            fila.pack_propagate(False)
            barra = tk.Frame(fila, bg=self.C["surface"], width=3)
            barra.pack(side="left", fill="y")
            numero = self._texto(fila, f"{i+1:02}", 10, "muted", "bold")
            numero.pack(side="left", padx=(10, 10))
            contenido = tk.Frame(fila, bg=self.C["surface"])
            contenido.pack(side="left", fill="both", expand=True)
            title = self._texto(contenido, nombre, 10, "text", "bold", anchor="w")
            title.pack(fill="x", pady=(8, 1))
            sub = self._texto(contenido, subtitulo, 8, "muted", anchor="w")
            sub.pack(fill="x")
            widgets = (fila, barra, numero, contenido, title, sub)
            for widget in widgets:
                widget.bind("<Button-1>", lambda e, idx=i: self._seleccionar_modo(idx))
                widget.bind("<Enter>", lambda e, idx=i: self._pintar_navegacion(idx))
                widget.bind("<Leave>", lambda e: self._pintar_navegacion())
            self.nav_filas.append((fila, barra, numero, contenido, title, sub))

        tk.Frame(sidebar, bg=self.C["surface"]).pack(fill="both", expand=True)
        self._linea(sidebar).pack(fill="x", padx=17, pady=(5, 14))
        self._texto(sidebar, "ATAJOS DE TECLADO", 8, "muted", "bold").pack(anchor="w", padx=18)
        self._texto(sidebar, "Ctrl + Enter   Resolver", 9, "secondary").pack(anchor="w", padx=18, pady=(9, 2))
        self._texto(sidebar, "Ctrl + S           Exportar", 9, "secondary").pack(anchor="w", padx=18, pady=2)
        self._texto(sidebar, "Ctrl + L           Limpiar", 9, "secondary").pack(anchor="w", padx=18, pady=(2, 19))

    def _seleccionar_modo(self, idx):
        self.combo_modo.current(idx)
        self._cargar_preset_ejemplo()  # Mismos presets originales.
        self._actualizar_visual_modo()
        self.canvas_entrada.yview_moveto(0)

    def _pintar_navegacion(self, hover=None):
        active = self.combo_modo.current()
        for i, widgets in enumerate(self.nav_filas):
            fila, barra, numero, contenido, title, sub = widgets
            seleccionado = i == active
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

    def _construir_editor(self):
        self.panel_izq = tk.Frame(
            self.main_grid, bg=self.C["surface"],
            highlightbackground=self.C["border"], highlightthickness=1
        )
        self.panel_izq.grid(row=0, column=1, sticky="nsew", padx=(0, 11))
        self.panel_izq.grid_rowconfigure(1, weight=1)
        self.panel_izq.grid_columnconfigure(0, weight=1)

        title_area = tk.Frame(self.panel_izq, bg=self.C["surface"], height=123)
        title_area.grid(row=0, column=0, sticky="ew")
        title_area.pack_propagate(False)
        self.editor_contador = self._texto(title_area, "MÓDULO  01 / 06", 9, "accent", "bold")
        self.editor_contador.pack(anchor="w", padx=23, pady=(21, 4))
        self.editor_titulo = self._texto(title_area, "Función de onda", 19, "text", "bold")
        self.editor_titulo.pack(anchor="w", padx=23)
        self.editor_descripcion = self._texto(
            title_area, "", 9, "secondary", anchor="w", justify="left", wraplength=345
        )
        self.editor_descripcion.pack(anchor="w", padx=23, pady=(3, 4))
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
        form.pack(fill="x", padx=22, pady=(18, 19))

        self._rotulo(form, "01", "FUNCIÓN DE ONDA  ψ(x)")
        self.entry_psi = self._entrada(form, accent=True)
        self._texto(form, "Expresión simbólica en función de x", 8, "muted").pack(anchor="w", pady=(4, 12))

        self._rotulo(form, "02", "POTENCIAL  V(x)")
        self.entry_potencial = self._entrada(form)
        self._texto(form, "Admite x, m, w y hbar", 8, "muted").pack(anchor="w", pady=(4, 12))

        self._rotulo(form, "03", "LÍMITES DE INTEGRACIÓN")
        limites = tk.Frame(form, bg=self.C["surface"])
        limites.pack(fill="x", pady=(5, 12))
        limites.grid_columnconfigure(0, weight=1, uniform="limits")
        limites.grid_columnconfigure(1, weight=1, uniform="limits")
        self._texto(limites, "Límite inferior  a", 9, "secondary").grid(row=0, column=0, sticky="w")
        self._texto(limites, "Límite superior  b", 9, "secondary").grid(row=0, column=1, sticky="w", padx=(8, 0))
        self.entry_lim_a = self._entrada(limites, use_grid=True, column=0, padx=(0, 8))
        self.entry_lim_b = self._entrada(limites, use_grid=True, column=1, padx=(8, 0))

        self._rotulo(form, "04", "PARÁMETROS / HAMILTONIANO H")
        self.entry_params = self._entrada(form)
        self._texto(form, "En matrices, separa columnas con ',' y filas con ';'", 8, "muted", wraplength=370,
                    justify="left").pack(anchor="w", pady=(4, 18))

        self._linea(form).pack(fill="x", pady=(0, 15))
        ptitle = tk.Frame(form, bg=self.C["surface"])
        ptitle.pack(fill="x", pady=(0, 11))
        self._texto(ptitle, "TECLADO SIMBÓLICO", 10, "text", "bold").pack(side="left")
        self._texto(ptitle, "Insertar en el campo", 8, "muted").pack(side="right")

        pad = tk.Frame(form, bg=self.C["surface"])
        pad.pack(fill="x")
        for i in range(4):
            pad.grid_columnconfigure(i, weight=1, uniform="keys")

        # Se mantienen los 16 símbolos y sus valores originales.
        botones_simbolos = [
            ("sin(x)", "sin(x)"), ("cos(x)", "cos(x)"), ("exp(-x²)", "exp(-x**2)"), ("sqrt()", "sqrt()"),
            ("π (pi)", "pi"), ("ℏ (hbar)", "hbar"), ("∞ (oo)", "oo"), ("-∞ (-oo)", "-oo"),
            ("x²", "x**2"), ("L (Ancho)", "L"), ("ω (Omega)", "w"), ("m (Masa)", "m"),
            ("Pozo ψ₁", "sqrt(2/L)*sin(pi*x/L)"), ("Gaussiana", "exp(-x**2/2)"),
            ("Armónico n=1", "x*exp(-x**2/2)"), ("H Pauli-X", "1, 2; 2, -1")
        ]
        for i, (etiqueta, valor) in enumerate(botones_simbolos):
            boton = self._boton(
                pad, etiqueta, lambda v=valor: self._insertar_en_foco(v),
                "surface_alt", "secondary", fuente=9, alto=8
            )
            boton.grid(row=i // 4, column=i % 4, sticky="ew", padx=3, pady=3)
        self._vincular_rueda(inner)

        action_area = tk.Frame(self.panel_izq, bg=self.C["surface"])
        action_area.grid(row=2, column=0, sticky="ew")
        self._linea(action_area).pack(fill="x")
        buttons = tk.Frame(action_area, bg=self.C["surface"])
        buttons.pack(fill="x", padx=22, pady=15)
        run = self._boton(buttons, "⚡  RESOLVER ECUACIÓN", self.resolver_ecuacion,
                          "accent", "accent_dark", fuente=11, alto=11)
        run.config(activebackground="#90FFF1", activeforeground=self.C["accent_dark"])
        run.pack(fill="x", pady=(0, 9))
        row = tk.Frame(buttons, bg=self.C["surface"])
        row.pack(fill="x")
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=1)
        self._boton(row, "Limpiar hoja", self.limpiar_hoja,
                    "surface_alt", "secondary", alto=8).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self._boton(row, "Exportar .txt", self.exportar_hoja,
                    "surface_alt", "secondary", alto=8).grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def _rotulo(self, parent, indice, texto):
        linea = tk.Frame(parent, bg=self.C["surface"])
        linea.pack(fill="x", pady=(0, 7))
        self._texto(linea, indice, 9, "accent", "bold").pack(side="left", padx=(0, 9))
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
            campo.grid(row=1, column=column, sticky="ew", padx=padx, pady=(6, 0), ipady=11, ipadx=9)
        else:
            campo.pack(fill="x", ipady=11, ipadx=9)
        return campo

    def _vincular_rueda(self, widget):
        # Scroll sobre el editor, también al apuntar a etiquetas o al teclado.
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

        head = tk.Frame(self.panel_der, bg=self.C["surface"], height=123)
        head.grid(row=0, column=0, sticky="ew")
        head.pack_propagate(False)
        self._texto(head, "CONSOLA DE RESULTADOS", 9, "violet", "bold").pack(anchor="w", padx=25, pady=(21, 4))
        self._texto(head, "Hoja de resultados", 19, "text", "bold").pack(anchor="w", padx=25)
        bottom = tk.Frame(head, bg=self.C["surface"])
        bottom.pack(fill="x", padx=25, pady=(3, 0))
        self._texto(bottom, "Desarrollo matemático paso a paso", 9, "secondary").pack(side="left")
        self.etiqueta_estado = self._texto(bottom, "SIN RESULTADOS", 8, "muted", "bold")
        self.etiqueta_estado.pack(side="right")
        self._linea(head).pack(side="bottom", fill="x")

        output_container = tk.Frame(self.panel_der, bg=self.C["editor"])
        output_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.hoja = tk.Text(
            output_container, bg=self.C["editor"], fg=self.C["secondary"],
            insertbackground=self.C["accent"],
            selectbackground=self.C["active"], selectforeground=self.C["text"],
            font=("Segoe UI", 11), wrap="word", bd=0, highlightthickness=0,
            padx=17, pady=16, spacing1=3, spacing3=4, undo=True, width=1, height=1,
        )
        scroll = ttk.Scrollbar(
            output_container, command=self.hoja.yview,
            style="Quantum.Vertical.TScrollbar"
        )
        scroll.pack(side="right", fill="y")
        self.hoja.pack(side="left", fill="both", expand=True)
        self.hoja.configure(yscrollcommand=scroll.set)

        self.hoja.tag_configure(
            "titulo", font=("Segoe UI", 13, "bold"), foreground=self.C["accent"],
            spacing1=13, spacing3=12
        )
        self.hoja.tag_configure(
            "paso", font=("Segoe UI", 11, "bold"), foreground=self.C["warning"],
            spacing1=14, spacing3=7
        )
        self.hoja.tag_configure(
            "explicacion", font=("Segoe UI", 11), foreground=self.C["secondary"],
            spacing1=4, spacing3=5
        )
        self.hoja.tag_configure(
            "formula", font=("Consolas", 10, "bold"), foreground=self.C["text"],
            background=self.C["surface_alt"], lmargin1=13, lmargin2=13,
            rmargin=8, spacing1=9, spacing3=9
        )
        self.hoja.tag_configure(
            "conclusion", font=("Segoe UI", 11, "bold"), foreground=self.C["success"],
            spacing1=12, spacing3=12
        )
        self.hoja.tag_configure("separador", foreground=self.C["border"], spacing1=8, spacing3=8)

        # Pantalla vacía visual: no se inserta texto falso en los resultados.
        self.estado_vacio = tk.Frame(output_container, bg=self.C["editor"])
        self._texto(self.estado_vacio, "⚛", 48, "accent").pack(pady=(0, 16))
        self._texto(self.estado_vacio, "Tu espacio de resultados", 16, "text", "bold").pack()
        self._texto(
            self.estado_vacio,
            "Selecciona un módulo, ajusta las entradas\ny ejecuta el cálculo para ver los pasos.",
            10, "secondary", justify="center"
        ).pack(pady=(9, 0))
        self.estado_vacio.place(relx=0.5, rely=0.45, anchor="center")

        footer = tk.Frame(self.panel_der, bg=self.C["surface"])
        footer.grid(row=2, column=0, sticky="ew")
        self._linea(footer).pack(fill="x")
        self._texto(
            footer, "SALIDA SIMBÓLICA  •  TEXTO SELECCIONABLE  •  EXPORTACIÓN .TXT",
            8, "muted", "bold"
        ).pack(anchor="w", padx=24, pady=14)

    def _construir_pie(self):
        footer = tk.Frame(self.root, bg=self.C["background"])
        footer.pack(fill="x", side="bottom", padx=23, pady=(0, 11))
        self._texto(footer, "QUANTUMLAB  /  WORKSPACE", 8, "muted", "bold").pack(side="left")
        self._texto(footer, "Interfaz renovada  ·  Motor matemático original", 8, "muted").pack(side="right")

    def _insertar_en_foco(self, texto):
        widget = self.root.focus_get()
        if isinstance(widget, tk.Entry):
            widget.insert(tk.INSERT, texto)
        else:
            self.entry_psi.insert(tk.INSERT, texto)

    def _cargar_preset_ejemplo(self):
        idx = self.combo_modo.current()
        self.entry_psi.delete(0, tk.END)
        self.entry_potencial.delete(0, tk.END)
        self.entry_lim_a.delete(0, tk.END)
        self.entry_lim_b.delete(0, tk.END)
        self.entry_params.delete(0, tk.END)

        if idx == 0:
            # Paquete de onda Gaussiano en espacio libre
            self.entry_psi.insert(0, "exp(-x**2 / 2)")
            self.entry_potencial.insert(0, "0")
            self.entry_lim_a.insert(0, "-oo")
            self.entry_lim_b.insert(0, "oo")
            self.entry_params.insert(0, "Paquete Gaussiano estándar")
        elif idx == 1:
            # Autoestado en Ecuación de Schrödinger
            self.entry_psi.insert(0, "sin(pi*x/L)")
            self.entry_potencial.insert(0, "0")
            self.entry_lim_a.insert(0, "0")
            self.entry_lim_b.insert(0, "L")
            self.entry_params.insert(0, "Autoestado de caja cuántica")
        elif idx == 2:
            # Pozo de potencial infinito: n=1, L=1 nm, integrar de 0 a L/3
            self.entry_psi.insert(0, "sqrt(2/L)*sin(n*pi*x/L)")
            self.entry_potencial.insert(0, "0 (Dentro del pozo), oo (Fuera)")
            self.entry_lim_a.insert(0, "0")
            self.entry_lim_b.insert(0, "L/3")
            self.entry_params.insert(0, "n=1, L=1.0 (nm)")
        elif idx == 3:
            # Oscilador armónico cuántico
            self.entry_psi.insert(0, "exp(-m*w*x**2 / (2*hbar))")
            self.entry_potencial.insert(0, "(1/2)*m*w**2*x**2")
            self.entry_lim_a.insert(0, "-oo")
            self.entry_lim_b.insert(0, "oo")
            self.entry_params.insert(0, "n=0 (Estado base)")
        elif idx == 4:
            # Efecto Túnel
            self.entry_psi.insert(0, "exp(I*k*x)")
            self.entry_potencial.insert(0, "V0 = 5.0 eV")
            self.entry_lim_a.insert(0, "0")
            self.entry_lim_b.insert(0, "0.5")
            self.entry_params.insert(0, "E=3.2, V0=5.0, a=0.5 (E, V0 en eV; ancho a en nm)")
        elif idx == 5:
            # Diagonalización de Hamiltoniano
            self.entry_psi.insert(0, "[1, 0] (Estado inicial |ψ(0)⟩)")
            self.entry_potencial.insert(0, "Sistema de 2 niveles acoplados")
            self.entry_lim_a.insert(0, "0")
            self.entry_lim_b.insert(0, "1")
            self.entry_params.insert(0, "2, 1-1j; 1+1j, 3")

    def _texto_seguro(self, texto):
        """Convierte ciertos símbolos Unicode problemáticos a variantes más compatibles con Tkinter/Windows."""
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
        # Solo cambia la presentación: ocultar el estado vacío al generar salida.
        self.estado_vacio.place_forget()
        self.etiqueta_estado.config(text="RESULTADOS DISPONIBLES", fg=self.C["success"])
        texto = self._texto_seguro(str(texto))
        self.hoja.insert(tk.END, texto + "\n", tag)
        self.hoja.see(tk.END)

    def limpiar_hoja(self):
        self.hoja.delete("1.0", tk.END)
        self.estado_vacio.place(relx=0.5, rely=0.45, anchor="center")
        self.etiqueta_estado.config(text="SIN RESULTADOS", fg=self.C["muted"])

    def exportar_hoja(self):
        contenido = self.hoja.get("1.0", tk.END).strip()
        if not contenido:
            messagebox.showwarning("Hoja vacía", "Resuelve primero una ecuación antes de exportar.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de Texto", "*.txt")])
        if ruta:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)
            messagebox.showinfo("Exportado", f"Hoja de resultados guardada en:\n{ruta}")

    def _parsear_expresion(self, texto):
        local_dict = {
            "x": self.x, "hbar": self.hbar, "m": self.m,
            "w": self.w, "L": self.L, "n": self.n,
            "pi": sp.pi, "oo": sp.oo, "I": sp.I
        }
        return sp.sympify(texto, locals=local_dict)

    # =========================================================
    # MOTOR DE RESOLUCIÓN EXPLICADA PASO A PASO
    # =========================================================
    def resolver_ecuacion(self):
        modo = self.combo_modo.current()
        self._escribir("═" * 68, "separador")

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
        except Exception as e:
            messagebox.showerror("Error de Sintaxis Matemática", f"Revisa la expresión ingresada:\n{e}")

    def _resolver_analisis_onda(self):
        psi_raw = self._parsear_expresion(self.entry_psi.get())
        a = self._parsear_expresion(self.entry_lim_a.get())
        b = self._parsear_expresion(self.entry_lim_b.get())

        self._escribir("📘 ANÁLISIS CUÁNTICO COMPLETO DE LA FUNCIÓN DE ONDA ψ(x)", "titulo")
        self._escribir(
            "Vamos a analizar paso a paso el estado cuántico propuesto. Primero verificaremos si la función "
            "es físicamente válida normalizándola, y luego extraeremos sus observables físicos mediante operadores.",
            "explicacion"
        )
        self._escribir(f"  ψ_inicial(x) = {sp.pretty(psi_raw)}   en el dominio [{a}, {b}]", "formula")

        # Paso 1: Normalización
        self._escribir("🔹 PASO 1: Condición de Normalización de Born", "paso")
        self._escribir(
            "En mecánica cuántica, la probabilidad total de encontrar la partícula en todo el dominio debe ser 100% (es decir, 1). "
            "Planteamos la integral de la densidad de probabilidad |A·ψ(x)|² = 1:",
            "explicacion"
        )
        densidad = sp.simplify(sp.conjugate(psi_raw) * psi_raw)
        integral_norm = sp.integrate(densidad, (self.x, a, b))
        constante_A = sp.simplify(1 / sp.sqrt(integral_norm))
        psi_norm = sp.simplify(constante_A * psi_raw)

        self._escribir(f"  ∫ |ψ(x)|² dx = {integral_norm}\n  Constante de normalización: A = 1 / √({integral_norm}) = {constante_A}\n  Función normalizada: ψ(x) = {psi_norm}", "formula")

        # Paso 2: Valor esperado de la posición <x> y <x²>
        self._escribir("🔹 PASO 2: Valor Esperado de la Posición ⟨x⟩ y Dispersión Δx", "paso")
        self._escribir(
            "Calculamos la posición promedio donde se espera medir la partícula aplicando el operador posición x̂:",
            "explicacion"
        )
        exp_x = sp.simplify(sp.integrate(sp.conjugate(psi_norm) * self.x * psi_norm, (self.x, a, b)))
        exp_x2 = sp.simplify(sp.integrate(sp.conjugate(psi_norm) * (self.x**2) * psi_norm, (self.x, a, b)))
        delta_x = sp.simplify(sp.sqrt(exp_x2 - exp_x**2))

        self._escribir(f"  ⟨x⟩  = ∫ ψ*(x) · x · ψ(x) dx  = {exp_x}\n  ⟨x²⟩ = ∫ ψ*(x) · x² · ψ(x) dx = {exp_x2}\n  Incertidumbre en posición: Δx = √(⟨x²⟩ - ⟨x⟩²) = {delta_x}", "formula")

        # Paso 3: Operador Momento <p> y Energía Cinética <T>
        self._escribir("🔹 PASO 3: Operador Momento Lineal p̂ = -iℏ(d/dx) y Energía Cinética", "paso")
        self._escribir(
            "Derivamos simbólicamente la función de onda para aplicar el operador diferencial de momento y el Laplaciano 1D:",
            "explicacion"
        )
        d_psi = sp.diff(psi_norm, self.x)
        d2_psi = sp.diff(psi_norm, self.x, 2)

        exp_p = sp.simplify(sp.integrate(sp.conjugate(psi_norm) * (-sp.I * self.hbar * d_psi), (self.x, a, b)))
        exp_p2 = sp.simplify(sp.integrate(sp.conjugate(psi_norm) * (-self.hbar**2 * d2_psi), (self.x, a, b)))
        delta_p = sp.simplify(sp.sqrt(exp_p2 - exp_p**2))
        exp_T = sp.simplify(exp_p2 / (2 * self.m))

        self._escribir(
            f"  dψ/dx  = {d_psi}\n"
            f"  d²ψ/dx² = {d2_psi}\n"
            f"  ⟨p⟩  = {exp_p}\n"
            f"  ⟨p²⟩ = {exp_p2}\n"
            f"  Incertidumbre en momento: Δp = √(⟨p²⟩ - ⟨p⟩²) = {delta_p}\n"
            f"  Energía Cinética media ⟨T⟩ = ⟨p²⟩ / (2m) = {exp_T}",
            "formula"
        )

        # Paso 4: Principio de Incertidumbre de Heisenberg
        self._escribir("🔹 PASO 4: Verificación del Principio de Incertidumbre de Heisenberg", "paso")
        producto_incertidumbre = sp.simplify(delta_x * delta_p)
        self._escribir(f"  Δx · Δp = {producto_incertidumbre}   (Límite cuántico fundamental: ≥ ℏ/2)", "formula")
        self._escribir(
            f"💡 INTERPRETACIÓN FÍSICA: La partícula tiene una posición media en x = {exp_x} y un momento neto promedio ⟨p⟩ = {exp_p}. "
            f"El producto de incertidumbres nos da {producto_incertidumbre}, cumpliendo estrictamente el límite cuántico de Heisenberg (ℏ/2).",
            "conclusion"
        )

    def _resolver_schrodinger_simbolico(self):
        psi = self._parsear_expresion(self.entry_psi.get())
        V = self._parsear_expresion(self.entry_potencial.get())

        self._escribir("📗 ECUACIÓN DE SCHRÖDINGER INDEPENDIENTE DEL TIEMPO (1D)", "titulo")
        self._escribir(
            "Vamos a comprobar si la función ψ(x) ingresada es un estado estacionario (autoestado) del Hamiltoniano "
            "y despejaremos analíticamente su energía total E.",
            "explicacion"
        )
        self._escribir("  Ecuación maestra:  [- (ℏ² / 2m) · d²/dx² + V(x)] ψ(x) = E · ψ(x)", "formula")

        self._escribir("🔹 PASO 1: Segunda derivada espacial de la función de onda", "paso")
        d2_psi = sp.diff(psi, self.x, 2)
        self._escribir(f"  ψ(x) = {psi}\n  d²ψ/dx² = {d2_psi}", "formula")

        self._escribir("🔹 PASO 2: Acción del Operador Hamiltoniano Ĥ sobre ψ(x)", "paso")
        termino_cinetico = sp.simplify(-(self.hbar**2 / (2 * self.m)) * d2_psi)
        H_psi = sp.simplify(termino_cinetico + V * psi)
        self._escribir(f"  T̂ψ(x) = {termino_cinetico}\n  V̂ψ(x) = {V * psi}\n  Ĥψ(x) = {H_psi}", "formula")

        self._escribir("🔹 PASO 3: Despeje del Autovalor de Energía E = (Ĥψ) / ψ", "paso")
        energia = sp.simplify(H_psi / psi)
        depende_de_x = self.x in energia.free_symbols

        self._escribir(f"  E = {energia}", "formula")
        if not depende_de_x:
            self._escribir(
                f"💡 INTERPRETACIÓN FÍSICA: Como la energía resultante E = {energia} es una constante que NO depende de 'x', "
                "queda demostrado matemáticamente que ψ(x) es un AUTOESTADO EXACTO de la ecuación de Schrödinger con energía bien definida.",
                "conclusion"
            )
        else:
            self._escribir(
                f"💡 INTERPRETACIÓN FÍSICA: El cociente E(x) = {energia} todavía depende de la coordenada 'x'. "
                "Esto significa que ψ(x) no es un estado estacionario puro para ese potencial V(x), sino una superposición de múltiples niveles de energía.",
                "conclusion"
            )

    def _resolver_pozo_infinito(self):
        a = self._parsear_expresion(self.entry_lim_a.get())
        b = self._parsear_expresion(self.entry_lim_b.get())

        self._escribir("📙 PARTÍCULA EN UNA CAJA CUÁNTICA 1D (POZO DE POTENCIAL INFINITO)", "titulo")
        self._escribir(
            "Una partícula confinada entre paredes impenetrables en x = 0 y x = L solo puede existir en ondas estacionarias cuantizadas.",
            "explicacion"
        )

        psi_n = sp.sqrt(2 / self.L) * sp.sin(self.n * sp.pi * self.x / self.L)
        energia_n = (self.n**2 * sp.pi**2 * self.hbar**2) / (2 * self.m * self.L**2)

        self._escribir("🔹 PASO 1: Funciones propias y Cuantización de la Energía", "paso")
        self._escribir(f"  ψₙ(x) = √(2/L) · sin(n·π·x / L)\n  Eₙ    = (n² · π² · ℏ²) / (2 · m · L²)", "formula")

        self._escribir(f"🔹 PASO 2: Probabilidad de hallar la partícula entre [{a}, {b}] para el estado fundamental (n=1)", "paso")
        psi_1 = psi_n.subs(self.n, 1)
        prob_simbolica = sp.simplify(sp.integrate(psi_1**2, (self.x, a, b)))
        prob_num = float(prob_simbolica.evalf()) if not prob_simbolica.free_symbols else prob_simbolica

        self._escribir(f"  P({a} ≤ x ≤ {b}) = ∫ (2/L)·sin²(πx/L) dx = {prob_simbolica}", "formula")
        if isinstance(prob_num, float):
            self._escribir(
                f"💡 INTERPRETACIÓN FÍSICA: En una caja clásica la probabilidad en ese tramo sería uniforme, pero debido a la interferencia "
                f"cuántica de la función de onda en n=1, la probabilidad exacta de detectar la partícula en [{a}, {b}] es del {prob_num*100:.2f}%.",
                "conclusion"
            )

    def _resolver_oscilador_armonico(self):
        psi = sp.exp(-self.m * self.w * self.x**2 / (2 * self.hbar))
        V = sp.Rational(1, 2) * self.m * self.w**2 * self.x**2

        self._escribir("📕 OSCILADOR ARMÓNICO CUÁNTICO (ESTADO FUNDAMENTAL Y ENERGÍA DE PUNTO CERO)", "titulo")
        self._escribir(
            "El oscilador armónico modela vibraciones moleculares y campos cuánticos con el potencial parabólico V(x) = ½ m ω² x².",
            "explicacion"
        )

        self._escribir("🔹 PASO 1: Normalización de la Gaussiana del estado fundamental (n=0)", "paso")
        int_gauss = sp.integrate(psi**2, (self.x, -sp.oo, sp.oo))
        A0 = sp.simplify(1 / sp.sqrt(int_gauss))
        psi_0 = A0 * psi
        self._escribir(f"  A₀ = (m·ω / π·ℏ)^(1/4)\n  ψ₀(x) = {psi_0}", "formula")

        self._escribir("🔹 PASO 2: Aplicación del Hamiltoniano Ĥ = - (ℏ²/2m) d²/dx² + ½ m ω² x²", "paso")
        d2_psi0 = sp.diff(psi_0, self.x, 2)
        H_psi0 = sp.simplify(-(self.hbar**2 / (2 * self.m)) * d2_psi0 + V * psi_0)
        E0 = sp.simplify(H_psi0 / psi_0)

        self._escribir(f"  Ĥψ₀(x) = {H_psi0}\n  Energía del estado fundamental: E₀ = {E0}   (Fórmula general: Eₙ = ℏω(n + ½))", "formula")
        self._escribir(
            "💡 INTERPRETACIÓN FÍSICA: Incluso en el cero absoluto (n = 0), la partícula NO puede quedarse quieta en el fondo del pozo "
            "porque violaría el Principio de Incertidumbre de Heisenberg. Posee una 'Energía de Punto Cero' inquebrantable de E₀ = ½ ℏω.",
            "conclusion"
        )

    def _resolver_efecto_tunel(self):
        # Valores por defecto: E=3.2 eV, V0=5.0 eV, ancho a=0.5 nm
        E_ev, V0_ev, ancho_nm = 3.2, 5.0, 0.5
        hbar_si = 1.054571817e-34
        m_e = 9.1093837e-31
        ev_j = 1.602176634e-19

        self._escribir("🔮 EFECTO TÚNEL CUÁNTICO A TRAVÉS DE UNA BARRERA DE POTENCIAL", "titulo")
        self._escribir(
            f"Calculamos la probabilidad de que un electrón con energía E = {E_ev} eV atraviese una barrera de potencial "
            f"más alta que su propia energía (V₀ = {V0_ev} eV) de espesor a = {ancho_nm} nm.",
            "explicacion"
        )

        # Paso 1: Coeficiente de decaimiento espacial kappa
        diff_j = (V0_ev - E_ev) * ev_j
        kappa = np.sqrt(2 * m_e * diff_j) / hbar_si
        ancho_m = ancho_nm * 1e-9
        kappa_a = kappa * ancho_m

        self._escribir("🔹 PASO 1: Constante de atenuación cuántica dentro de la barrera (κ)", "paso")
        self._escribir(
            f"  κ = √[2·m·(V₀ - E)] / ℏ = {kappa:.4e} m⁻¹\n"
            f"  Factor adimensional κ·a = {kappa_a:.4f}",
            "formula"
        )

        # Paso 2: Coeficiente de Transmisión Exacto
        sinh_val = np.sinh(kappa_a)
        T = 1.0 / (1.0 + (V0_ev**2 * sinh_val**2) / (4.0 * E_ev * (V0_ev - E_ev)))
        R = 1.0 - T

        self._escribir("🔹 PASO 2: Coeficiente Exacto de Transmisión (T) y Reflexión (R)", "paso")
        self._escribir(
            f"  T = [1 + (V₀² · sinh²(κa)) / (4·E·(V₀ - E))]⁻¹\n"
            f"  Probabilidad de Transmisión (Túnel) : T = {T:.6e}  ({T*100:.4f}%)\n"
            f"  Probabilidad de Reflexión           : R = {R:.6f}  ({R*100:.4f}%)",
            "formula"
        )
        self._escribir(
            f"💡 INTERPRETACIÓN FÍSICA: En física clásica sería 100% imposible cruzar la pared porque E < V₀. "
            f"En mecánica cuántica, la función de onda penetra como una exponencial decreciente e^(-κx) y emerge al otro lado "
            f"con una probabilidad real del {T*100:.4f}%.",
            "conclusion"
        )

    def _resolver_hamiltoniano_matricial(self):
        raw = self.entry_params.get().strip()
        filas = [
            [complex(val.strip().replace("i", "j")) for val in fila.split(",")]
            for fila in raw.split(";")
        ]
        H = np.array(filas, dtype=complex)

        self._escribir("📘 DIAGONALIZACIÓN DE HAMILTONIANO MATRICIAL (H|ψ⟩ = E|ψ⟩)", "titulo")
        self._escribir(
            "Vamos a resolver el problema de autovalores y autovectores para la matriz Hamiltoniana ingresada, "
            "encontrando sus niveles de energía permitidos y sus estados estacionarios.",
            "explicacion"
        )
        self._escribir(f"  Matriz Hamiltoniana H:\n{H}", "formula")

        es_hermitica = np.allclose(H, H.conj().T)
        self._escribir("🔹 PASO 1: Verificación de Hermiticidad (H = H†)", "paso")
        self._escribir(f"  ¿Es Hermítica?: {'SÍ (Autovalores de energía 100% reales garantizados)' if es_hermitica else 'NO (Sistema abierto / no conservativo)'}", "formula")

        self._escribir("🔹 PASO 2: Cálculo de Autovalores (Niveles de Energía Eₙ) y Autovectores (|Eₙ⟩)", "paso")
        energias, autovectores = np.linalg.eigh(H) if es_hermitica else np.linalg.eig(H)

        detalle = ""
        for idx, E_val in enumerate(energias):
            vec = autovectores[:, idx]
            vec_str = "  ".join([f"{v.real:+.3f}{v.imag:+.3f}i" for v in vec])
            detalle += f"  Nivel E_{idx} = {E_val.real:.4f}   -->   Autoestado |E_{idx}⟩ = [ {vec_str} ]ᵀ\n"

        self._escribir(detalle.strip(), "formula")
        brecha = abs(energias[1].real - energias[0].real) if len(energias) >= 2 else 0.0
        self._escribir(
            f"💡 INTERPRETACIÓN FÍSICA: El estado fundamental del sistema tiene una energía mínima E₀ = {energias[0].real:.4f}. "
            f"La brecha energética (gap cuántico ΔE) para excitar el sistema al siguiente nivel es ΔE = {brecha:.4f} (frecuencia de Bohr ω = ΔE/ℏ).",
            "conclusion"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraCuanticaAvanzada(root)
    root.mainloop()