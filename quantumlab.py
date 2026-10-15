try:
    import _pylong
except ImportError:
    pass

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sympy as sp
import numpy as np

from quantumlab_i18n import get_i18n, t
from quantumlab_engine import (
    QuantumLabError,
    MathParseError,
    ParseSecurityError,
    ScientificValidationError,
    AsyncCalculationManager,
    SafeASTParser,
    parse_parameters,
    parse_matrix,
    parse_state_vector,
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

    def __init__(self, root):
        self.root = root
        self.i18n = get_i18n()

        self.root.title(t("app.title"))
        self.root.configure(bg=self.C["background"])

        # Responsive initial sizing adapted to screen resolution
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

        # Tracking state
        self._modo_actual = 0
        self._ultimo_resultado = None
        self._ultimo_modo = None
        self.historial_calculos = []  # DEF-03: Multi-step calculation history
        self.calc_manager = AsyncCalculationManager(self.root)  # DEF-09: Responsive execution watchdog

        # Persistent inputs per mode so clicking modes does not erase user inputs
        self._inputs_por_modo = {
            i: {
                "psi": t(f"preset.{i}.psi"),
                "potencial": t(f"preset.{i}.pot"),
                "lim_a": t(f"preset.{i}.lim_a"),
                "lim_b": t(f"preset.{i}.lim_b"),
                "params": t(f"preset.{i}.params"),
            }
            for i in range(6)
        }

        self._configurar_estilos()
        self._construir_layout_dividido()
        self._cargar_modo(0, forzar_preset=True)
        self._actualizar_visual_modo()

        # Keyboard shortcuts
        self.root.bind("<Control-Return>", lambda event: self.resolver_ecuacion())
        self.root.bind("<Control-s>", lambda event: self.exportar_hoja())
        self.root.bind("<Control-l>", lambda event: self.limpiar_hoja())

    @property
    def NOMBRES(self):
        return [t(f"module.{i}.name") for i in range(6)]

    @property
    def SUBTITULOS(self):
        return [t(f"module.{i}.sub") for i in range(6)]

    @property
    def DESCRIPCIONES(self):
        return [t(f"module.{i}.desc") for i in range(6)]

    @property
    def PRESETS(self):
        return [
            {
                "psi": t(f"preset.{i}.psi"),
                "potencial": t(f"preset.{i}.pot"),
                "lim_a": t(f"preset.{i}.lim_a"),
                "lim_b": t(f"preset.{i}.lim_b"),
                "params": t(f"preset.{i}.params"),
            }
            for i in range(6)
        ]

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
        self.header_sub = self._texto(brand, t("header.brand_sub"), 8, "muted", "bold")
        self.header_sub.pack(anchor="w")

        right = tk.Frame(inner, bg=self.C["header"])
        right.pack(side="right", fill="y")

        # Language Selector (Permanently visible in header across all modules)
        # Requirement: Label must be permanently 'Language' (never translated)
        # Options must be 'English' and 'Spanish'
        lang_frame = tk.Frame(right, bg=self.C["header"])
        lang_frame.pack(side="right", padx=(16, 0), pady=6)

        self.lbl_language = tk.Label(
            lang_frame, text="🌐 Language", font=("Segoe UI", 9, "bold"),
            bg=self.C["header"], fg=self.C["accent"]
        )
        self.lbl_language.pack(side="left", padx=(0, 6))

        self.combo_lang = ttk.Combobox(
            lang_frame, values=["English", "Spanish"], state="readonly",
            style="Quantum.TCombobox", width=9, takefocus=True
        )
        current_lang = self.i18n.current_language
        self.combo_lang.set("English" if current_lang == "en" else "Spanish")
        self.combo_lang.pack(side="left")
        self.combo_lang.bind("<<ComboboxSelected>>", self._on_cambiar_idioma_combo)

        # Verified Engine Info
        info_frame = tk.Frame(right, bg=self.C["header"])
        info_frame.pack(side="left", padx=(0, 10))
        self.header_verified = self._texto(info_frame, t("header.engine_verified"), 9, "success", "bold")
        self.header_verified.pack(anchor="e", pady=(2, 3))
        self.header_libs = self._texto(info_frame, t("header.engine_libs"), 9, "secondary")
        self.header_libs.pack(anchor="e")

        self._linea(self.root).pack(fill="x")

    def _on_cambiar_idioma_combo(self, event=None):
        val = self.combo_lang.get()
        new_lang = "en" if val == "English" else "es"
        self._cambiar_idioma(new_lang)

    def _es_preset(self, modo: int, campo: str, valor: str) -> bool:
        """
        DEF-02: Determines whether a field contains an application-generated preset in any language.
        Separates scientific math data from localized descriptive text to prevent overwriting user work.
        """
        if not valor:
            return True
        v = valor.strip()
        val_es = t(f"preset.{modo}.{campo}", lang="es").strip()
        val_en = t(f"preset.{modo}.{campo}", lang="en").strip()
        return v in (val_es, val_en)

    def _cambiar_idioma(self, new_lang: str):
        if self.i18n.current_language == new_lang:
            return

        # Save current user inputs before switching
        self._guardar_entradas_actuales()

        self.i18n.set_language(new_lang)
        self.combo_lang.set("English" if new_lang == "en" else "Spanish")

        # DEF-02: Update descriptive presets across all modules without touching user-custom entries
        for m in range(6):
            if m in self._inputs_por_modo:
                for campo in ("psi", "potencial", "lim_a", "lim_b", "params"):
                    val = self._inputs_por_modo[m][campo]
                    if self._es_preset(m, campo, val):
                        self._inputs_por_modo[m][campo] = t(f"preset.{m}.{campo}", lang=new_lang)

        # Update currently active mode entries if they contain unmodified presets
        active_data = self._inputs_por_modo[self._modo_actual]
        if self._es_preset(self._modo_actual, "psi", self.entry_psi.get()):
            self.entry_psi.delete(0, tk.END)
            self.entry_psi.insert(0, active_data["psi"])
        if self._es_preset(self._modo_actual, "potencial", self.entry_potencial.get()):
            self.entry_potencial.delete(0, tk.END)
            self.entry_potencial.insert(0, active_data["potencial"])
        if self._es_preset(self._modo_actual, "lim_a", self.entry_lim_a.get()):
            self.entry_lim_a.delete(0, tk.END)
            self.entry_lim_a.insert(0, active_data["lim_a"])
        if self._es_preset(self._modo_actual, "lim_b", self.entry_lim_b.get()):
            self.entry_lim_b.delete(0, tk.END)
            self.entry_lim_b.insert(0, active_data["lim_b"])
        if self._es_preset(self._modo_actual, "params", self.entry_params.get()):
            self.entry_params.delete(0, tk.END)
            self.entry_params.insert(0, active_data["params"])

        self._actualizar_textos_ui()

    def _actualizar_textos_ui(self):
        """
        Dynamically updates all UI texts to the currently active language.
        Preserves user inputs, current mode, window layout, and re-renders calculation history.
        """
        # Window & header
        self.root.title(t("app.title"))
        self.header_sub.config(text=t("header.brand_sub"))
        self.header_verified.config(text=t("header.engine_verified"))
        self.header_libs.config(text=t("header.engine_libs"))
        # (self.lbl_language intentionally stays 'Language')

        # Sidebar
        self.sidebar_ws_title.config(text=t("sidebar.workspace_title"))
        self.sidebar_mod_title.config(text=t("sidebar.modules_title"))
        self.sidebar_mod_sub.config(text=t("sidebar.modules_sub"))

        self.modos = [t(f"module.{i}.combo") for i in range(6)]
        self.combo_modo.config(values=self.modos)
        self.combo_modo.current(self._modo_actual)

        for i, widgets in enumerate(self.nav_filas):
            fila, barra, numero, contenido, title, sub = widgets
            title.config(text=t(f"module.{i}.name"))
            sub.config(text=t(f"module.{i}.sub"))

        self.lbl_shortcuts_title.config(text=t("sidebar.shortcuts_title"))
        self.lbl_shortcut_calc.config(text=t("sidebar.shortcut_calc"))
        self.lbl_shortcut_export.config(text=t("sidebar.shortcut_export"))
        self.lbl_shortcut_clear.config(text=t("sidebar.shortcut_clear"))

        # Editor
        self.editor_contador.config(text=t("editor.step_counter", current=self._modo_actual + 1, total=6))
        self.editor_titulo.config(text=t(f"module.{self._modo_actual}.name"))
        self.editor_descripcion.config(text=t(f"module.{self._modo_actual}.desc"))

        self.lbl_rotulo_psi.config(text=t("editor.label_psi"))
        self.lbl_rotulo_pot.config(text=t("editor.label_pot"))
        self.lbl_rotulo_limits.config(text=t("editor.label_limits"))
        self.lbl_lim_a_desc.config(text=t("editor.label_lim_a"))
        self.lbl_lim_b_desc.config(text=t("editor.label_lim_b"))
        self.lbl_rotulo_params.config(text=t("editor.label_params"))

        self.lbl_kbd_title.config(text=t("editor.keyboard_title"))
        self.lbl_kbd_hint.config(text=t("editor.keyboard_hint"))

        self.btn_solve.config(text=t("editor.btn_solve"))
        self.btn_clear.config(text=t("editor.btn_clear"))
        self.btn_reset.config(text=t("editor.btn_reset"))
        self.btn_export.config(text=t("editor.btn_export"))

        # Refresh hints for active mode
        self._actualizar_visual_modo()

        # Results console
        self.lbl_res_console.config(text=t("results.console_title"))
        self.lbl_res_sheet.config(text=t("results.sheet_title"))
        self.lbl_res_step.config(text=t("results.step_by_step"))
        self.lbl_empty_title.config(text=t("results.empty_title"))
        self.lbl_empty_desc.config(text=t("results.empty_desc"))
        self.lbl_res_footer.config(text=t("results.footer_info"))

        # Footer
        self.lbl_footer_brand.config(text=t("footer.brand"))
        self.lbl_footer_security.config(text=t("footer.security"))

        # DEF-03: Re-render entire calculation history in the active language without losing multi-step records
        new_lang = self.i18n.current_language
        if self.historial_calculos:
            self.hoja.delete("1.0", tk.END)
            self.estado_vacio.place_forget()
            for item in self.historial_calculos:
                modo = item["modo"]
                res = item["resultado"]
                if modo == 0:
                    bloques = formatear_analisis_onda(res, lang=new_lang)
                elif modo == 1:
                    bloques = formatear_schrodinger(res, lang=new_lang)
                elif modo == 2:
                    bloques = formatear_pozo_infinito(res, lang=new_lang)
                elif modo == 3:
                    bloques = formatear_oscilador(res, lang=new_lang)
                elif modo == 4:
                    bloques = formatear_tunel(res, lang=new_lang)
                elif modo == 5:
                    bloques = formatear_hamiltoniano(res, lang=new_lang)
                else:
                    bloques = []

                self._escribir_bloques(bloques)
                self._escribir("═" * 68, "separador")
            self.etiqueta_estado.config(text=t("status.available"), fg=self.C["success"])
        elif self._ultimo_resultado is not None and self._ultimo_modo is not None:
            self.hoja.delete("1.0", tk.END)
            self.estado_vacio.place_forget()
            modo = self._ultimo_modo
            res = self._ultimo_resultado
            if modo == 0:
                bloques = formatear_analisis_onda(res, lang=new_lang)
            elif modo == 1:
                bloques = formatear_schrodinger(res, lang=new_lang)
            elif modo == 2:
                bloques = formatear_pozo_infinito(res, lang=new_lang)
            elif modo == 3:
                bloques = formatear_oscilador(res, lang=new_lang)
            elif modo == 4:
                bloques = formatear_tunel(res, lang=new_lang)
            elif modo == 5:
                bloques = formatear_hamiltoniano(res, lang=new_lang)
            else:
                bloques = []

            self._escribir_bloques(bloques)
            self._escribir("═" * 68, "separador")
            self.etiqueta_estado.config(text=t("status.available"), fg=self.C["success"])
        else:
            self.etiqueta_estado.config(text=t("status.no_results"), fg=self.C["muted"])

    def _construir_sidebar(self):
        sidebar = tk.Frame(
            self.main_grid, bg=self.C["surface"], width=225,
            highlightbackground=self.C["border"], highlightthickness=1
        )
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 11))
        sidebar.grid_propagate(False)

        self.sidebar_ws_title = self._texto(sidebar, t("sidebar.workspace_title"), 9, "muted", "bold")
        self.sidebar_ws_title.pack(anchor="w", padx=18, pady=(20, 6))

        self.sidebar_mod_title = self._texto(sidebar, t("sidebar.modules_title"), 12, "text", "bold")
        self.sidebar_mod_title.pack(anchor="w", padx=18)

        self.sidebar_mod_sub = self._texto(sidebar, t("sidebar.modules_sub"), 9, "secondary")
        self.sidebar_mod_sub.pack(anchor="w", padx=18, pady=(3, 14))

        self._linea(sidebar).pack(fill="x", padx=17, pady=(0, 12))

        self.modos = [t(f"module.{i}.combo") for i in range(6)]

        self.combo_modo = ttk.Combobox(sidebar, values=self.modos, state="readonly", style="Quantum.TCombobox")
        self.combo_modo.current(0)
        self.combo_modo.pack(fill="x", padx=14, pady=(0, 10))
        self.combo_modo.bind("<<ComboboxSelected>>", lambda e: self._seleccionar_modo(self.combo_modo.current()))

        self.nav_filas = []
        for i in range(6):
            fila = tk.Frame(sidebar, bg=self.C["surface"], cursor="hand2", height=54)
            fila.pack(fill="x", padx=8, pady=2)
            fila.pack_propagate(False)
            barra = tk.Frame(fila, bg=self.C["surface"], width=3)
            barra.pack(side="left", fill="y")
            numero = self._texto(fila, f"{i+1:02}", 10, "muted", "bold")
            numero.pack(side="left", padx=(8, 8))
            contenido = tk.Frame(fila, bg=self.C["surface"])
            contenido.pack(side="left", fill="both", expand=True)
            title = self._texto(contenido, t(f"module.{i}.name"), 10, "text", "bold", anchor="w")
            title.pack(fill="x", pady=(6, 1))
            sub = self._texto(contenido, t(f"module.{i}.sub"), 8, "muted", anchor="w")
            sub.pack(fill="x")
            widgets = (fila, barra, numero, contenido, title, sub)
            for widget in widgets:
                widget.bind("<Button-1>", lambda e, idx=i: self._seleccionar_modo(idx))
                widget.bind("<Enter>", lambda e, idx=i: self._pintar_navegacion(idx))
                widget.bind("<Leave>", lambda e: self._pintar_navegacion())
            self.nav_filas.append((fila, barra, numero, contenido, title, sub))

        tk.Frame(sidebar, bg=self.C["surface"]).pack(fill="both", expand=True)
        self._linea(sidebar).pack(fill="x", padx=17, pady=(5, 12))

        self.lbl_shortcuts_title = self._texto(sidebar, t("sidebar.shortcuts_title"), 8, "muted", "bold")
        self.lbl_shortcuts_title.pack(anchor="w", padx=18)

        self.lbl_shortcut_calc = self._texto(sidebar, t("sidebar.shortcut_calc"), 9, "secondary")
        self.lbl_shortcut_calc.pack(anchor="w", padx=18, pady=(7, 2))

        self.lbl_shortcut_export = self._texto(sidebar, t("sidebar.shortcut_export"), 9, "secondary")
        self.lbl_shortcut_export.pack(anchor="w", padx=18, pady=2)

        self.lbl_shortcut_clear = self._texto(sidebar, t("sidebar.shortcut_clear"), 9, "secondary")
        self.lbl_shortcut_clear.pack(anchor="w", padx=18, pady=(2, 16))

    def _guardar_entradas_actuales(self):
        """Saves current entry contents to avoid losing work when switching modes."""
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

        if forzar_preset or idx not in self._inputs_por_modo:
            data = {
                "psi": t(f"preset.{idx}.psi"),
                "potencial": t(f"preset.{idx}.pot"),
                "lim_a": t(f"preset.{idx}.lim_a"),
                "lim_b": t(f"preset.{idx}.lim_b"),
                "params": t(f"preset.{idx}.params"),
            }
        else:
            data = self._inputs_por_modo.get(idx, self.PRESETS[idx])

        self.entry_psi.insert(0, data["psi"])
        self.entry_potencial.insert(0, data["potencial"])
        self.entry_lim_a.insert(0, data["lim_a"])
        self.entry_lim_b.insert(0, data["lim_b"])
        self.entry_params.insert(0, data["params"])

    def _seleccionar_modo(self, idx):
        if idx == self._modo_actual:
            return

        self._guardar_entradas_actuales()
        self._modo_actual = idx
        self.combo_modo.current(idx)
        self._cargar_modo(idx, forzar_preset=False)
        self._actualizar_visual_modo()
        self.canvas_entrada.yview_moveto(0)

    def restablecer_preset_actual(self, mostrar_dialogo: bool = True):
        """Explicitly reloads the default preset for the current mode."""
        self._cargar_modo(self._modo_actual, forzar_preset=True)
        self._guardar_entradas_actuales()
        if mostrar_dialogo:
            messagebox.showinfo(
                t("dialog.preset_restored_title"),
                t("dialog.preset_restored_msg", name=t(f"module.{self._modo_actual}.name")),
            )

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
        self.editor_contador.config(text=t("editor.step_counter", current=idx + 1, total=6))
        self.editor_titulo.config(text=t(f"module.{idx}.name"))
        self.editor_descripcion.config(text=t(f"module.{idx}.desc"))

        self.lbl_hint_psi.config(text=t(f"hint.{idx}.psi"))
        self.lbl_hint_pot.config(text=t(f"hint.{idx}.pot"))
        self.lbl_hint_params.config(text=t(f"hint.{idx}.params"))

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

        self.editor_contador = self._texto(title_area, t("editor.step_counter", current=1, total=6), 9, "accent", "bold")
        self.editor_contador.pack(anchor="w", padx=23, pady=(16, 3))

        self.editor_titulo = self._texto(title_area, t("module.0.name"), 18, "text", "bold")
        self.editor_titulo.pack(anchor="w", padx=23)

        self.editor_descripcion = self._texto(
            title_area, t("module.0.desc"), 9, "secondary", anchor="w", justify="left", wraplength=340
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

        self.lbl_rotulo_psi = self._rotulo(form, "01", t("editor.label_psi"))
        self.entry_psi = self._entrada(form, accent=True)
        self.lbl_hint_psi = self._texto(form, t("hint.0.psi"), 8, "muted")
        self.lbl_hint_psi.pack(anchor="w", pady=(3, 10))

        self.lbl_rotulo_pot = self._rotulo(form, "02", t("editor.label_pot"))
        self.entry_potencial = self._entrada(form)
        self.lbl_hint_pot = self._texto(form, t("hint.0.pot"), 8, "muted")
        self.lbl_hint_pot.pack(anchor="w", pady=(3, 10))

        self.lbl_rotulo_limits = self._rotulo(form, "03", t("editor.label_limits"))
        limites = tk.Frame(form, bg=self.C["surface"])
        limites.pack(fill="x", pady=(4, 10))
        limites.grid_columnconfigure(0, weight=1, uniform="limits")
        limites.grid_columnconfigure(1, weight=1, uniform="limits")

        self.lbl_lim_a_desc = self._texto(limites, t("editor.label_lim_a"), 9, "secondary")
        self.lbl_lim_a_desc.grid(row=0, column=0, sticky="w")
        self.lbl_lim_b_desc = self._texto(limites, t("editor.label_lim_b"), 9, "secondary")
        self.lbl_lim_b_desc.grid(row=0, column=1, sticky="w", padx=(8, 0))

        self.entry_lim_a = self._entrada(limites, use_grid=True, column=0, padx=(0, 8))
        self.entry_lim_b = self._entrada(limites, use_grid=True, column=1, padx=(8, 0))

        self.lbl_rotulo_params = self._rotulo(form, "04", t("editor.label_params"))
        self.entry_params = self._entrada(form)
        self.lbl_hint_params = self._texto(form, t("hint.0.params"), 8, "muted", wraplength=350, justify="left")
        self.lbl_hint_params.pack(anchor="w", pady=(3, 14))

        self._linea(form).pack(fill="x", pady=(0, 12))
        ptitle = tk.Frame(form, bg=self.C["surface"])
        ptitle.pack(fill="x", pady=(0, 9))
        self.lbl_kbd_title = self._texto(ptitle, t("editor.keyboard_title"), 10, "text", "bold")
        self.lbl_kbd_title.pack(side="left")
        self.lbl_kbd_hint = self._texto(ptitle, t("editor.keyboard_hint"), 8, "muted")
        self.lbl_kbd_hint.pack(side="right")

        pad = tk.Frame(form, bg=self.C["surface"])
        pad.pack(fill="x")
        for i in range(4):
            pad.grid_columnconfigure(i, weight=1, uniform="keys")

        botones_simbolos = [
            ("sin(x)", "sin(x)"), ("cos(x)", "cos(x)"), ("exp(-x²)", "exp(-x**2)"), ("sqrt()", "sqrt()"),
            ("π (pi)", "pi"), ("ℏ (hbar)", "hbar"), ("∞ (oo)", "oo"), ("-∞ (-oo)", "-oo"),
            ("x²", "x**2"), ("L", "L"), ("ω", "w"), ("m", "m"),
            ("ψ₁", "sqrt(2/L)*sin(pi*x/L)"), ("exp(-x²/2)", "exp(-x**2/2)"),
            ("Armónico", "x*exp(-x**2/2)"), ("H Pauli-X", "0, 1; 1, 0")
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

        self.btn_solve = self._boton(
            buttons, t("editor.btn_solve"), self.resolver_ecuacion,
            "accent", "accent_dark", fuente=11, alto=9
        )
        self.btn_solve.config(activebackground="#90FFF1", activeforeground=self.C["accent_dark"])
        self.btn_solve.pack(fill="x", pady=(0, 7))

        row = tk.Frame(buttons, bg=self.C["surface"])
        row.pack(fill="x")
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=1)
        row.grid_columnconfigure(2, weight=1)

        self.btn_clear = self._boton(
            row, t("editor.btn_clear"), self.limpiar_hoja,
            "surface_alt", "secondary", alto=7
        )
        self.btn_clear.grid(row=0, column=0, sticky="ew", padx=(0, 3))

        self.btn_reset = self._boton(
            row, t("editor.btn_reset"), self.restablecer_preset_actual,
            "surface_alt", "secondary", alto=7
        )
        self.btn_reset.grid(row=0, column=1, sticky="ew", padx=3)

        self.btn_export = self._boton(
            row, t("editor.btn_export"), self.exportar_hoja,
            "surface_alt", "secondary", alto=7
        )
        self.btn_export.grid(row=0, column=2, sticky="ew", padx=(3, 0))

    def _rotulo(self, parent, indice, texto):
        linea = tk.Frame(parent, bg=self.C["surface"])
        linea.pack(fill="x", pady=(0, 5))
        self._texto(linea, indice, 9, "accent", "bold").pack(side="left", padx=(0, 8))
        lbl = self._texto(linea, texto, 9, "secondary", "bold")
        lbl.pack(side="left")
        return lbl

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

        self.lbl_res_console = self._texto(head, t("results.console_title"), 9, "violet", "bold")
        self.lbl_res_console.pack(anchor="w", padx=22, pady=(16, 3))

        self.lbl_res_sheet = self._texto(head, t("results.sheet_title"), 18, "text", "bold")
        self.lbl_res_sheet.pack(anchor="w", padx=22)

        bottom = tk.Frame(head, bg=self.C["surface"])
        bottom.pack(fill="x", padx=22, pady=(2, 0))

        self.lbl_res_step = self._texto(bottom, t("results.step_by_step"), 9, "secondary")
        self.lbl_res_step.pack(side="left")

        # Fixed width and right anchor eliminates Windows GDI pixel ghosting artifacts
        self.etiqueta_estado = tk.Label(
            bottom, text=t("status.no_results"), font=("Segoe UI", 8, "bold"),
            bg=self.C["surface"], fg=self.C["muted"], width=26, anchor="e"
        )
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
        self.lbl_empty_title = self._texto(self.estado_vacio, t("results.empty_title"), 15, "text", "bold")
        self.lbl_empty_title.pack()
        self.lbl_empty_desc = self._texto(
            self.estado_vacio,
            t("results.empty_desc"),
            10, "secondary", justify="center"
        )
        self.lbl_empty_desc.pack(pady=(8, 0))
        self.estado_vacio.place(relx=0.5, rely=0.45, anchor="center")

        footer = tk.Frame(self.panel_der, bg=self.C["surface"])
        footer.grid(row=2, column=0, sticky="ew")
        self._linea(footer).pack(fill="x")
        self.lbl_res_footer = self._texto(
            footer, t("results.footer_info"),
            8, "muted", "bold"
        )
        self.lbl_res_footer.pack(anchor="w", padx=22, pady=12)

    def _construir_pie(self):
        footer = tk.Frame(self.root, bg=self.C["background"])
        footer.pack(fill="x", side="bottom", padx=23, pady=(0, 9))
        self.lbl_footer_brand = self._texto(footer, t("footer.brand"), 8, "muted", "bold")
        self.lbl_footer_brand.pack(side="left")
        self.lbl_footer_security = self._texto(footer, t("footer.security"), 8, "muted")
        self.lbl_footer_security.pack(side="right")

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
        self.historial_calculos.clear()
        self._ultimo_resultado = None
        self._ultimo_modo = None
        self.estado_vacio.place(relx=0.5, rely=0.45, anchor="center")
        self.etiqueta_estado.config(text=t("status.no_results"), fg=self.C["muted"])

    def exportar_hoja(self):
        """Robust file export with localized dialog messages and exception handling."""
        contenido = self.hoja.get("1.0", tk.END).strip()
        if not contenido:
            messagebox.showwarning(t("dialog.export_empty_title"), t("dialog.export_empty_msg"))
            return

        ruta = filedialog.asksaveasfilename(
            title=t("dialog.export_title"),
            defaultextension=".txt",
            filetypes=[("Text File (*.txt)", "*.txt"), ("All Files (*.*)", "*.*")]
        )
        if not ruta:
            return

        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)
            messagebox.showinfo(
                t("dialog.export_success_title"),
                t("dialog.export_success_msg", path=ruta)
            )
        except OSError as e:
            messagebox.showerror(
                t("dialog.export_error_title"),
                t("dialog.export_error_msg", error=str(e))
            )

    def _parsear_expresion(self, texto):
        """Safe AST parser replacing sp.sympify()."""
        return SafeASTParser.parse(texto)

    # =========================================================
    # MOTOR DE RESOLUCIÓN Y DESPACHO
    # =========================================================
    def _registrar_calculo(self, modo: int, res: Any, bloques: list):
        """
        DEF-03: Registers a structured calculation in history for non-destructive re-rendering.
        """
        import time
        self._ultimo_resultado = res
        self._ultimo_modo = modo
        self.historial_calculos.append({
            "modo": modo,
            "resultado": res,
            "timestamp": time.strftime("%H:%M:%S")
        })
        self._escribir_bloques(bloques)

    def resolver_ecuacion(self):
        """Handles calculation with accurate status updates and localized error handling."""
        modo = self.combo_modo.current()
        self.etiqueta_estado.config(text=t("status.calculating"), fg=self.C["warning"])
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
            self.etiqueta_estado.config(text=t("status.available"), fg=self.C["success"])

        except Exception as e:
            self._manejar_error_calculo(e)

    def _manejar_error_calculo(self, e: Exception):
        """DEF-01: Centralized error handler displaying 100% localized messages in the active language."""
        curr_lang = self.i18n.current_language
        if isinstance(e, QuantumLabError):
            msg = e.to_localized(curr_lang)
            if isinstance(e, (ParseSecurityError, MathParseError)):
                self.etiqueta_estado.config(text=t("status.syntax_error"), fg=self.C["warning"])
                messagebox.showerror(t("dialog.error_syntax_title"), msg)
            elif isinstance(e, ScientificValidationError):
                self.etiqueta_estado.config(text=t("status.param_error"), fg=self.C["warning"])
                messagebox.showerror(t("dialog.error_param_title"), msg)
            else:
                self.etiqueta_estado.config(text=t("status.calc_error"), fg=self.C["warning"])
                messagebox.showerror(t("dialog.error_calc_title"), msg)
        elif isinstance(e, ValueError):
            self.etiqueta_estado.config(text=t("status.param_error"), fg=self.C["warning"])
            messagebox.showerror(t("dialog.error_param_title"), str(e))
        else:
            self.etiqueta_estado.config(text=t("status.calc_error"), fg=self.C["warning"])
            messagebox.showerror(t("dialog.error_calc_title"), f"{t('dialog.error_calc_prefix')} {e}")

    # =========================================================
    # RESOLUTORES POR MODALIDAD
    # =========================================================
    def _resolver_analisis_onda(self):
        psi_raw = self._parsear_expresion(self.entry_psi.get())
        a = self._parsear_expresion(self.entry_lim_a.get())
        b = self._parsear_expresion(self.entry_lim_b.get())

        res = analizar_funcion_onda(psi_raw, a, b)
        bloques = formatear_analisis_onda(res, lang=self.i18n.current_language)
        self._registrar_calculo(0, res, bloques)
        return res

    def _resolver_schrodinger_simbolico(self):
        psi = self._parsear_expresion(self.entry_psi.get())
        V = self._parsear_expresion(self.entry_potencial.get())

        a_str = self.entry_lim_a.get().strip()
        b_str = self.entry_lim_b.get().strip()
        a = self._parsear_expresion(a_str) if a_str else None
        b = self._parsear_expresion(b_str) if b_str else None

        res = analizar_schrodinger_1d(psi, V, a=a, b=b)
        bloques = formatear_schrodinger(res, lang=self.i18n.current_language)
        self._registrar_calculo(1, res, bloques)
        return res

    def _resolver_pozo_infinito(self):
        a = self._parsear_expresion(self.entry_lim_a.get())
        b = self._parsear_expresion(self.entry_lim_b.get())

        params = parse_parameters(self.entry_params.get())
        n_val = params.get("n", 1)
        L_val = params.get("L", None)

        res = analizar_pozo_infinito(a, b, n_val=n_val, L_val=L_val)
        bloques = formatear_pozo_infinito(res, lang=self.i18n.current_language)
        self._registrar_calculo(2, res, bloques)
        return res

    def _resolver_oscilador_armonico(self):
        params = parse_parameters(self.entry_params.get())
        n_val = params.get("n", 0)

        res = analizar_oscilador_armonico(n_val=n_val)
        bloques = formatear_oscilador(res, lang=self.i18n.current_language)
        self._registrar_calculo(3, res, bloques)
        return res

    def _resolver_efecto_tunel(self):
        params = parse_parameters(self.entry_params.get())
        E_ev = float(params.get("E", 3.2))
        V0_ev = float(params.get("V0", 5.0))
        ancho_nm = float(params.get("a", 0.5))

        res = analizar_efecto_tunel(E_ev=E_ev, V0_ev=V0_ev, ancho_nm=ancho_nm)
        bloques = formatear_tunel(res, lang=self.i18n.current_language)
        self._registrar_calculo(4, res, bloques)
        return res

    def _resolver_hamiltoniano_matricial(self):
        raw_matrix = self.entry_params.get().strip()
        H = parse_matrix(raw_matrix)

        raw_psi = self.entry_psi.get().strip()
        psi_0 = None
        preset_psi_es = t("preset.5.psi", lang="es").strip()
        preset_psi_en = t("preset.5.psi", lang="en").strip()
        if raw_psi:
            if (raw_psi == preset_psi_es or raw_psi == preset_psi_en) and H.shape[0] != 2:
                psi_0 = None
            else:
                try:
                    psi_0 = parse_state_vector(raw_psi, expected_dim=H.shape[0])
                except Exception as e:
                    raise ScientificValidationError("error.state_vector_invalid", detail=str(e))

        t_val = 0.0
        t_str = self.entry_lim_a.get().strip()
        if t_str:
            try:
                t_sym = self._parsear_expresion(t_str)
                t_val = float(t_sym.evalf())
                if not np.isfinite(t_val):
                    raise ScientificValidationError("error.time_must_be_finite")
            except Exception as e:
                raise ScientificValidationError("error.time_invalid", detail=str(e))

        res = analizar_hamiltoniano_matricial(H, psi_0=psi_0, t_val=t_val)
        bloques = formatear_hamiltoniano(res, lang=self.i18n.current_language)
        self._registrar_calculo(5, res, bloques)
        return res


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraCuanticaAvanzada(root)
    root.mainloop()