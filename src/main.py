import tkinter as tk
from tkinter import filedialog, messagebox

class MicroCPreCompilador:

    def __init__(self, root):
        self.palabras_reservadas = [
        "begin",
        "end",
        "read",
        "write",
        "int",
        "float",
        "char"
    ]
        self.root = root
        self.root.title("MicroC - Pre Compilador")
        self.root.geometry("1000x600")

        self.archivo_actual = None
        self.archivo_guardado = True

        self.crear_componentes()

    def crear_componentes(self):

        # -------- Frame Botones --------
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(fill=tk.X)

        tk.Button(frame_botones, text="Nuevo", command=self.nuevo).pack(side=tk.LEFT)
        tk.Button(frame_botones, text="Abrir", command=self.abrir).pack(side=tk.LEFT)
        tk.Button(frame_botones, text="Guardar", command=self.guardar).pack(side=tk.LEFT)
        tk.Button(frame_botones, text="Editar", command=self.editar).pack(side=tk.LEFT)
        tk.Button(frame_botones, text="Compilar", command=self.compilar).pack(side=tk.LEFT)
        tk.Button(frame_botones, text="Ayuda", command=self.ayuda).pack(side=tk.LEFT)
        tk.Button(frame_botones, text="Salir", command=self.salir).pack(side=tk.RIGHT)

        # -------- Nombre Archivo --------
        self.label_archivo = tk.Label(self.root, text="Ningún archivo abierto", anchor="w")
        self.label_archivo.pack(fill=tk.X)

        # -------- TextBox1 (Editor) --------
        self.text_editor = tk.Text(self.root, height=15)
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        self.text_editor.bind("<<Modified>>", self.marcar_no_guardado)
        self.text_editor.bind("<Return>", self.auto_indent)
        self.text_editor.bind("<KeyRelease>", self.resaltar_sintaxis)

        # -------- TextBox2 (Consola) --------
        self.text_consola = tk.Text(self.root, height=8, bg="black", fg="lime")
        self.text_consola.pack(fill=tk.BOTH)
        self.text_consola.config(state=tk.DISABLED)

    # -------- FUNCIONES --------
    def nuevo(self):
       if not self.archivo_guardado:
        respuesta = messagebox.askyesnocancel(
            "Guardar",
            "Hay cambios sin guardar. ¿Desea guardar antes de continuar?"
        )

        if respuesta:  # Sí
            self.guardar()
        elif respuesta is None:  # Cancelar
            return

        self.text_editor.config(state=tk.NORMAL)
        self.text_editor.delete("1.0", tk.END)

        self.archivo_actual = None
        self.archivo_guardado = True

        self.label_archivo.config(text="Nuevo archivo sin guardar")

        self.text_consola.config(state=tk.NORMAL)
        self.text_consola.insert(tk.END, "Nuevo archivo creado.\n")
        self.text_consola.config(state=tk.DISABLED)

    def marcar_no_guardado(self, event=None):
        self.archivo_guardado = False
        self.text_editor.edit_modified(False)

    def abrir(self):
        ruta = filedialog.askopenfilename(
        filetypes=[("Archivos C", "*.c")]
        )

        if not ruta:
            return

        with open(ruta, "r") as archivo:
            contenido = archivo.read()

        self.text_editor.config(state=tk.NORMAL)
        self.text_editor.delete("1.0", tk.END)
        self.text_editor.insert(tk.END, contenido)

        self.text_editor.config(state=tk.DISABLED)

        self.archivo_actual = ruta
        self.archivo_guardado = True

        self.label_archivo.config(text=ruta)

        self.text_consola.config(state=tk.NORMAL)
        self.text_consola.insert(tk.END, "Archivo abierto en modo lectura.\n")
        self.text_consola.config(state=tk.DISABLED)
        
    def guardar(self):
            if self.archivo_actual is None:
                ruta = filedialog.asksaveasfilename(
                    defaultextension=".c",
                    filetypes=[("Archivos C", "*.c")]
                )
                if not ruta:
                    return
                self.archivo_actual = ruta
            else:
                ruta = self.archivo_actual

            with open(ruta, "w") as archivo:
                contenido = self.text_editor.get("1.0", tk.END)
                archivo.write(contenido)

            self.archivo_guardado = True
            self.label_archivo.config(text=ruta)

            self.text_consola.config(state=tk.NORMAL)
            self.text_consola.insert(tk.END, "Archivo guardado correctamente.\n")
            self.text_consola.config(state=tk.DISABLED)

    def editar(self):
        self.text_editor.config(state=tk.NORMAL)

        self.text_consola.config(state=tk.NORMAL)
        self.text_consola.insert(tk.END, "Modo edición activado.\n")
        self.text_consola.config(state=tk.DISABLED)

    def compilar(self):
        self.text_consola.config(state=tk.NORMAL)
        self.text_consola.delete("1.0", tk.END)

        codigo = self.text_editor.get("1.0", tk.END)

        errores = []

        # Verificar begin y end
        if "begin" not in codigo:
            errores.append("Error: Falta 'begin'.")

        if "end" not in codigo:
            errores.append("Error: Falta 'end'.")

        # Verificar punto y coma
        lineas = codigo.split("\n")
        for i, linea in enumerate(lineas, start=1):
            linea = linea.strip()

            if linea and not linea.startswith("begin") and not linea.startswith("end"):
                if not linea.endswith(";"):
                    errores.append(f"Error en línea {i}: Falta ';'")

        # Mostrar resultados
        if errores:
            for error in errores:
                self.text_consola.insert(tk.END, error + "\n")
        else:
            self.text_consola.insert(tk.END, "Compilación exitosa.\n")

        self.text_consola.config(state=tk.DISABLED)

    def ayuda(self):
        mensaje = """
    MicroC - Pre Compilador

    Comandos soportados:

    begin           -> Inicio del programa
    end             -> Fin del programa
    :=              -> Asignación
    read(a,b)       -> Lectura
    write(a,b)      -> Escritura

    Reglas:
    - Cada instrucción debe terminar en ;
    - El programa debe contener begin y end
    - Las variables deben usarse correctamente

    Proyecto desarrollado por Gerardy Barrios
    """

        messagebox.showinfo("Ayuda - MicroC", mensaje)

    def salir(self):
        if not self.archivo_guardado:
            respuesta = messagebox.askyesnocancel(
                "Salir",
                "Hay cambios sin guardar. ¿Desea guardar antes de salir?"
            )

            if respuesta:  # Sí
                self.guardar()
                self.root.destroy()
            elif respuesta is False:  # No
                self.root.destroy()
            else:
                return
        else:
            self.root.destroy()

    def auto_indent(self, event):
        linea_actual = self.text_editor.get("insert linestart", "insert")
        indentacion = ""

        # Copiar indentación anterior
        for char in linea_actual:
            if char in (" ", "\t"):
                indentacion += char
            else:
                break

        # Si la línea tiene begin, aumentar indentación
        if linea_actual.strip().endswith("begin"):
            indentacion += "    "

        self.text_editor.insert("insert", "\n" + indentacion)
        return "break"
    
    def resaltar_sintaxis(self, event=None):
        contenido = self.text_editor.get("1.0", tk.END)

        # limpiar colores anteriores
        for tag in self.text_editor.tag_names():
            self.text_editor.tag_delete(tag)

        for palabra in self.palabras_reservadas:
            start = "1.0"
            while True:
                pos = self.text_editor.search(palabra, start, stopindex=tk.END)

                if not pos:
                    break

                end = f"{pos}+{len(palabra)}c"
                self.text_editor.tag_add(palabra, pos, end)
                self.text_editor.tag_config(palabra, foreground="blue")

                start = end
    def analizar_codigo(self):
        codigo = self.text_editor.get("1.0", tk.END)

        tokens = []
        palabras = codigo.replace(";", " ; ").replace("(", " ( ").replace(")", " ) ").split()

        for palabra in palabras:
            if palabra in self.palabras_reservadas:
                tokens.append(("RESERVADA", palabra))
            elif palabra.isidentifier():
                tokens.append(("IDENTIFICADOR", palabra))
            elif palabra.isnumeric():
                tokens.append(("NUMERO", palabra))
            elif palabra == ";":
                tokens.append(("FIN_INSTRUCCION", palabra))
            else:
                tokens.append(("DESCONOCIDO", palabra))

        resultado = "TOKENS ENCONTRADOS:\n\n"

        for token in tokens:
            resultado += f"{token[0]} → {token[1]}\n"

        messagebox.showinfo("Analizador Léxico", resultado)

if __name__ == "__main__":
    root = tk.Tk()
    app = MicroCPreCompilador(root)
    root.mainloop()
    