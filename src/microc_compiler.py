"""
MicroC Pre-Compilador
Curso: Autómatas y Lenguajes - Universidad Mesoamericana 2026
Catedrático: Ing. Baudilio Boteo
"""

import tkinter as tk
from tkinter import filedialog, messagebox, font
import os


class MicroCCompiler:
    def __init__(self, root):
        self.root = root
        self.root.title("MicroC Compiler — [Sin archivo]")
        self.root.geometry("1100x680")
        self.root.minsize(800, 500)
        self.root.configure(bg="#1e1e2e")

        # Estado de la aplicación
        self.archivo_actual = None       # Ruta del archivo abierto/guardado
        self.es_nuevo = True             # True = nuevo (sin archivo físico)
        self.modificado = False          # True = hay cambios sin guardar

        self._build_ui()
        self._bind_events()

    # ─────────────────────────────────────────
    #  CONSTRUCCIÓN DE LA INTERFAZ
    # ─────────────────────────────────────────
    def _build_ui(self):
        # ── Barra de menú ──────────────────────────────────────
        menubar = tk.Menu(self.root, bg="#313244", fg="#cdd6f4",
                          activebackground="#45475a", activeforeground="#cdd6f4",
                          relief="flat", bd=0)
        self.root.config(menu=menubar)

        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0, bg="#313244", fg="#cdd6f4",
                               activebackground="#45475a", activeforeground="#cdd6f4")
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="🆕  Nuevo        Ctrl+N", command=self.nuevo)
        menu_archivo.add_command(label="📂  Abrir        Ctrl+O", command=self.abrir)
        menu_archivo.add_command(label="💾  Guardar      Ctrl+S", command=self.guardar)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="🚪  Salir        Alt+F4", command=self.salir)

        # Menú Editar
        menu_editar = tk.Menu(menubar, tearoff=0, bg="#313244", fg="#cdd6f4",
                              activebackground="#45475a", activeforeground="#cdd6f4")
        menubar.add_cascade(label="Editar", menu=menu_editar)
        menu_editar.add_command(label="✏️  Habilitar edición", command=self.habilitar_edicion)

        # Menú Compilar
        menu_compilar = tk.Menu(menubar, tearoff=0, bg="#313244", fg="#cdd6f4",
                                activebackground="#45475a", activeforeground="#cdd6f4")
        menubar.add_cascade(label="Compilar", menu=menu_compilar)
        menu_compilar.add_command(label="▶  Compilar     F5", command=self.compilar)

        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0, bg="#313244", fg="#cdd6f4",
                             activebackground="#45475a", activeforeground="#cdd6f4")
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="📖  Documentación", command=self.ayuda)

        # ── Barra de herramientas ───────────────────────────────
        toolbar = tk.Frame(self.root, bg="#181825", pady=4, padx=6)
        toolbar.pack(side="top", fill="x")

        btn_style = {
            "bg": "#313244", "fg": "#cdd6f4", "relief": "flat",
            "padx": 12, "pady": 5, "cursor": "hand2",
            "font": ("Consolas", 9, "bold"), "bd": 0,
            "activebackground": "#45475a", "activeforeground": "#a6e3a1"
        }

        tk.Button(toolbar, text="🆕 Nuevo",    command=self.nuevo,             **btn_style).pack(side="left", padx=2)
        tk.Button(toolbar, text="📂 Abrir",    command=self.abrir,             **btn_style).pack(side="left", padx=2)
        tk.Button(toolbar, text="💾 Guardar",  command=self.guardar,           **btn_style).pack(side="left", padx=2)
        tk.Button(toolbar, text="✏️ Editar",   command=self.habilitar_edicion, **btn_style).pack(side="left", padx=2)

        sep = tk.Frame(toolbar, bg="#45475a", width=2, height=28)
        sep.pack(side="left", padx=6, pady=2)

        tk.Button(toolbar, text="▶ Compilar", command=self.compilar,
                  **{**btn_style, "bg": "#1e3a2f", "fg": "#a6e3a1",
                     "activebackground": "#2d5a42"}).pack(side="left", padx=2)

        sep2 = tk.Frame(toolbar, bg="#45475a", width=2, height=28)
        sep2.pack(side="left", padx=6, pady=2)

        tk.Button(toolbar, text="❓ Ayuda",   command=self.ayuda,             **btn_style).pack(side="left", padx=2)
        tk.Button(toolbar, text="🚪 Salir",   command=self.salir,
                  **{**btn_style, "bg": "#3a1e1e", "fg": "#f38ba8",
                     "activebackground": "#5a2d2d"}).pack(side="right", padx=2)

        # ── Barra de ruta del archivo ───────────────────────────
        ruta_frame = tk.Frame(self.root, bg="#11111b", pady=2, padx=8)
        ruta_frame.pack(side="top", fill="x")

        tk.Label(ruta_frame, text="📄 Archivo:", bg="#11111b",
                 fg="#6c7086", font=("Consolas", 8)).pack(side="left")

        self.lbl_ruta = tk.Label(ruta_frame, text="[Sin archivo — Nuevo documento]",
                                 bg="#11111b", fg="#89b4fa",
                                 font=("Consolas", 8), anchor="w")
        self.lbl_ruta.pack(side="left", fill="x", expand=True)

        self.lbl_estado = tk.Label(ruta_frame, text="● Sin cambios",
                                   bg="#11111b", fg="#a6e3a1",
                                   font=("Consolas", 8))
        self.lbl_estado.pack(side="right", padx=4)

        # ── Panel principal (dos columnas) ─────────────────────
        main_pane = tk.PanedWindow(self.root, orient="horizontal",
                                   bg="#1e1e2e", sashwidth=6,
                                   sashrelief="flat", sashpad=2)
        main_pane.pack(fill="both", expand=True, padx=8, pady=6)

        # ── TextBox1: Editor de código ─────────────────────────
        editor_frame = tk.Frame(main_pane, bg="#1e1e2e")
        main_pane.add(editor_frame, minsize=300)

        hdr_editor = tk.Frame(editor_frame, bg="#181825", pady=4, padx=8)
        hdr_editor.pack(fill="x")
        tk.Label(hdr_editor, text="◈  CÓDIGO MICRO-C",
                 bg="#181825", fg="#cba6f7",
                 font=("Consolas", 9, "bold")).pack(side="left")
        self.lbl_modo = tk.Label(hdr_editor, text="[SOLO LECTURA]",
                                 bg="#181825", fg="#f38ba8",
                                 font=("Consolas", 8))
        self.lbl_modo.pack(side="right")

        # Frame con número de líneas + texto
        txt_frame = tk.Frame(editor_frame, bg="#1e1e2e")
        txt_frame.pack(fill="both", expand=True)

        self.line_numbers = tk.Text(
            txt_frame, width=4, padx=6, pady=8,
            bg="#11111b", fg="#585b70", bd=0,
            font=("Consolas", 11), state="disabled",
            selectbackground="#11111b", cursor="arrow"
        )
        self.line_numbers.pack(side="left", fill="y")

        scrollbar_y = tk.Scrollbar(txt_frame)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = tk.Scrollbar(editor_frame, orient="horizontal")
        scrollbar_x.pack(fill="x")

        self.textbox1 = tk.Text(
            txt_frame,
            bg="#1e1e2e", fg="#cdd6f4",
            insertbackground="#f5c2e7",
            selectbackground="#45475a",
            font=("Consolas", 11),
            padx=8, pady=8,
            bd=0, relief="flat",
            undo=True,
            wrap="none",
            yscrollcommand=self._sync_scroll,
            xscrollcommand=scrollbar_x.set,
            state="disabled"
        )
        self.textbox1.pack(side="left", fill="both", expand=True)

        scrollbar_y.config(command=self._scroll_both)
        scrollbar_x.config(command=self.textbox1.xview)

        # ── TextBox2: Panel de resultados ─────────────────────
        output_frame = tk.Frame(main_pane, bg="#1e1e2e")
        main_pane.add(output_frame, minsize=250)

        hdr_output = tk.Frame(output_frame, bg="#181825", pady=4, padx=8)
        hdr_output.pack(fill="x")
        tk.Label(hdr_output, text="◈  RESULTADOS / CONSOLA",
                 bg="#181825", fg="#a6e3a1",
                 font=("Consolas", 9, "bold")).pack(side="left")
        tk.Button(hdr_output, text="🗑 Limpiar",
                  command=self._limpiar_output,
                  bg="#181825", fg="#6c7086", relief="flat",
                  font=("Consolas", 8), cursor="hand2",
                  activebackground="#313244", bd=0).pack(side="right")

        scrollbar_out = tk.Scrollbar(output_frame)
        scrollbar_out.pack(side="right", fill="y")

        self.textbox2 = tk.Text(
            output_frame,
            bg="#11111b", fg="#a6e3a1",
            insertbackground="#cdd6f4",
            selectbackground="#313244",
            font=("Consolas", 10),
            padx=10, pady=8,
            bd=0, relief="flat",
            state="disabled",
            yscrollcommand=scrollbar_out.set,
            wrap="word"
        )
        self.textbox2.pack(fill="both", expand=True)
        scrollbar_out.config(command=self.textbox2.yview)

        # ── Barra de estado (pie) ──────────────────────────────
        statusbar = tk.Frame(self.root, bg="#181825", pady=3, padx=10)
        statusbar.pack(side="bottom", fill="x")

        self.lbl_pos = tk.Label(statusbar, text="Ln 1, Col 1",
                                bg="#181825", fg="#6c7086",
                                font=("Consolas", 8))
        self.lbl_pos.pack(side="right")

        tk.Label(statusbar, text="MicroC Pre-Compilador v1.0  |  Universidad Mesoamericana 2026",
                 bg="#181825", fg="#45475a",
                 font=("Consolas", 8)).pack(side="left")

        # Mensaje inicial en consola
        self._log("╔══════════════════════════════════════════════╗")
        self._log("║     MicroC Pre-Compilador — v1.0             ║")
        self._log("║     Universidad Mesoamericana 2026           ║")
        self._log("║     Autómatas y Lenguajes                    ║")
        self._log("╚══════════════════════════════════════════════╝")
        self._log("")
        self._log("▸ Listo. Use [Nuevo] para comenzar a escribir.")
        self._log("▸ Use [Abrir] para cargar un archivo .C")

    # ─────────────────────────────────────────
    #  EVENTOS Y ATAJOS
    # ─────────────────────────────────────────
    def _bind_events(self):
        self.root.bind("<Control-n>", lambda e: self.nuevo())
        self.root.bind("<Control-o>", lambda e: self.abrir())
        self.root.bind("<Control-s>", lambda e: self.guardar())
        self.root.bind("<F5>",        lambda e: self.compilar())
        self.root.protocol("WM_DELETE_WINDOW", self.salir)

        self.textbox1.bind("<KeyRelease>", self._on_key)
        self.textbox1.bind("<ButtonRelease>", self._actualizar_posicion)

    def _on_key(self, event=None):
        self.modificado = True
        self._actualizar_estado()
        self._actualizar_lineas()
        self._actualizar_posicion()

    def _actualizar_posicion(self, event=None):
        try:
            pos = self.textbox1.index("insert")
            ln, col = pos.split(".")
            self.lbl_pos.config(text=f"Ln {ln}, Col {int(col)+1}")
        except Exception:
            pass

    def _actualizar_estado(self):
        if self.modificado:
            self.lbl_estado.config(text="● Modificado", fg="#fab387")
        else:
            self.lbl_estado.config(text="● Sin cambios", fg="#a6e3a1")

    def _actualizar_titulo(self):
        if self.archivo_actual:
            nombre = os.path.basename(self.archivo_actual)
            self.root.title(f"MicroC Compiler — {self.archivo_actual}")
            self.lbl_ruta.config(text=self.archivo_actual)
        else:
            self.root.title("MicroC Compiler — [Nuevo documento]")
            self.lbl_ruta.config(text="[Sin archivo — Nuevo documento]")

    def _actualizar_lineas(self):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        total = int(self.textbox1.index("end-1c").split(".")[0])
        nums = "\n".join(str(i) for i in range(1, total + 1))
        self.line_numbers.insert("1.0", nums)
        self.line_numbers.config(state="disabled")

    def _sync_scroll(self, *args):
        self.line_numbers.yview_moveto(args[0])
        # Usamos el scrollbar a través del widget directamente
        self.textbox1.tk.call(self.textbox1._w, "yview", "moveto", args[0])

    def _scroll_both(self, *args):
        self.textbox1.yview(*args)
        self.line_numbers.yview(*args)

    # ─────────────────────────────────────────
    #  HELPERS DE OUTPUT
    # ─────────────────────────────────────────
    def _log(self, msg, color="#a6e3a1"):
        self.textbox2.config(state="normal")
        self.textbox2.insert("end", msg + "\n")
        self.textbox2.see("end")
        self.textbox2.config(state="disabled")

    def _limpiar_output(self):
        self.textbox2.config(state="normal")
        self.textbox2.delete("1.0", "end")
        self.textbox2.config(state="disabled")

    def _get_code(self):
        return self.textbox1.get("1.0", "end-1c")

    def _set_code(self, texto):
        self.textbox1.config(state="normal")
        self.textbox1.delete("1.0", "end")
        self.textbox1.insert("1.0", texto)
        self.textbox1.config(state="normal")
        self._actualizar_lineas()

    def _preguntar_guardar(self):
        """Pregunta si desea guardar antes de continuar. Retorna True si puede continuar."""
        if self.modificado:
            r = messagebox.askyesnocancel(
                "Cambios sin guardar",
                "El documento tiene cambios sin guardar.\n¿Desea guardarlo antes de continuar?")
            if r is None:     # Cancelar
                return False
            if r:             # Sí
                self.guardar()
        return True

    # ─────────────────────────────────────────
    #  ACCIONES PRINCIPALES
    # ─────────────────────────────────────────
    def nuevo(self):
        """Habilita el TextBox1 en modo edición para escribir texto nuevo."""
        if not self._preguntar_guardar():
            return
        self.archivo_actual = None
        self.es_nuevo = True
        self.modificado = False
        self._set_code("")
        self.textbox1.config(state="normal")
        self.lbl_modo.config(text="[EDICIÓN]", fg="#a6e3a1")
        self._actualizar_titulo()
        self._actualizar_estado()
        self._actualizar_lineas()
        self._log("─" * 48)
        self._log("▸ Nuevo documento creado. Listo para editar.")
        self.textbox1.focus_set()

    def abrir(self):
        """Carga un archivo .C en TextBox1 en modo solo lectura."""
        if not self._preguntar_guardar():
            return
        ruta = filedialog.askopenfilename(
            title="Abrir archivo MicroC",
            filetypes=[("Archivos C", "*.c *.C"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
            self.archivo_actual = ruta
            self.es_nuevo = False
            self.modificado = False
            self._set_code(contenido)
            self.textbox1.config(state="disabled")   # Solo lectura al abrir
            self.lbl_modo.config(text="[SOLO LECTURA]", fg="#f38ba8")
            self._actualizar_titulo()
            self._actualizar_estado()
            self._log("─" * 48)
            self._log(f"▸ Archivo abierto: {os.path.basename(ruta)}")
            self._log(f"  Ruta: {ruta}")
            self._log("  Use [Editar] para habilitar la edición.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def guardar(self):
        """Guarda el contenido de TextBox1 con extensión .C."""
        if self.es_nuevo or self.archivo_actual is None:
            # Nuevo → pedir ubicación
            ruta = filedialog.asksaveasfilename(
                title="Guardar archivo MicroC",
                defaultextension=".c",
                filetypes=[("Archivos C", "*.c *.C"), ("Todos los archivos", "*.*")]
            )
            if not ruta:
                return
            self.archivo_actual = ruta
            self.es_nuevo = False

        try:
            codigo = self._get_code()
            with open(self.archivo_actual, "w", encoding="utf-8") as f:
                f.write(codigo)
            self.modificado = False
            self._actualizar_titulo()
            self._actualizar_estado()
            self._log("─" * 48)
            self._log(f"▸ Archivo guardado: {os.path.basename(self.archivo_actual)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    def habilitar_edicion(self):
        """Habilita la edición en TextBox1 (para archivos abiertos en solo lectura)."""
        self.textbox1.config(state="normal")
        self.lbl_modo.config(text="[EDICIÓN]", fg="#a6e3a1")
        self._log("─" * 48)
        self._log("▸ Modo edición habilitado.")
        self.textbox1.focus_set()

    def compilar(self):
        """Compilación — funcionalidad pendiente para próximas entregas."""
        self._log("─" * 48)
        self._log("▸ [Compilar] — Función en desarrollo.")
        self._log("  Esta funcionalidad se implementará")
        self._log("  en próximas entregas del proyecto.")
        self._log("─" * 48)
        messagebox.showinfo("Compilar",
                            "La función de compilación se desarrollará\nen próximas entregas.\n\n[Compilación en desarrollo]")

    def ayuda(self):
        """Muestra documentación básica del proyecto."""
        self._log("─" * 48)
        self._log("▸ [Ayuda] — Documentación MicroC v1.0")
        self._log("─" * 48)

        ventana = tk.Toplevel(self.root)
        ventana.title("Ayuda — MicroC Pre-Compilador")
        ventana.geometry("520x420")
        ventana.configure(bg="#1e1e2e")
        ventana.resizable(False, False)

        tk.Label(ventana, text="MicroC Pre-Compilador — Ayuda",
                 bg="#1e1e2e", fg="#cba6f7",
                 font=("Consolas", 12, "bold")).pack(pady=(18, 4))

        tk.Label(ventana, text="Universidad Mesoamericana · Autómatas y Lenguajes 2026",
                 bg="#1e1e2e", fg="#6c7086",
                 font=("Consolas", 9)).pack(pady=(0, 12))

        txt = tk.Text(ventana, bg="#11111b", fg="#cdd6f4",
                      font=("Consolas", 9), padx=16, pady=12,
                      bd=0, relief="flat", wrap="word")
        txt.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        ayuda_texto = """\
FUNCIONES DISPONIBLES:
──────────────────────────────────────
🆕  Nuevo    → Crea un nuevo documento en blanco.
               Activa el modo edición.

📂  Abrir    → Carga un archivo .C existente.
               Se abre en modo solo lectura.

💾  Guardar  → Guarda el contenido actual.
               Si es nuevo, pide la ubicación.
               Si ya existe, sobreescribe.

✏️  Editar   → Habilita la edición de un
               archivo abierto en solo lectura.

▶  Compilar → [En desarrollo — próxima entrega]

❓  Ayuda    → Muestra esta ventana.

🚪  Salir    → Cierra la aplicación.
               Si hay cambios sin guardar,
               pregunta antes de salir.

──────────────────────────────────────
ATAJOS DE TECLADO:
  Ctrl+N  →  Nuevo
  Ctrl+O  →  Abrir
  Ctrl+S  →  Guardar
  F5      →  Compilar
──────────────────────────────────────
"""
        txt.insert("1.0", ayuda_texto)
        txt.config(state="disabled")

        tk.Button(ventana, text="Cerrar", command=ventana.destroy,
                  bg="#313244", fg="#cdd6f4", relief="flat",
                  font=("Consolas", 10), padx=20, pady=6,
                  cursor="hand2").pack(pady=(0, 12))

    def salir(self):
        """Cierra la aplicación preguntando si hay cambios sin guardar."""
        if self.modificado:
            r = messagebox.askyesnocancel(
                "Salir",
                "Hay cambios sin guardar.\n¿Desea guardar antes de salir?")
            if r is None:    # Cancelar → no salir
                return
            if r:            # Sí → guardar primero
                self.guardar()
        self.root.destroy()


# ─────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = MicroCCompiler(root)
    root.mainloop()


