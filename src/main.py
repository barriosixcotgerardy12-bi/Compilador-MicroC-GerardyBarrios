import tkinter as tk
from tkinter import filedialog, messagebox

class MicroCPreCompilador:

    def __init__(self, root):
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

        # -------- TextBox2 (Consola) --------
        self.text_consola = tk.Text(self.root, height=8, bg="black", fg="lime")
        self.text_consola.pack(fill=tk.BOTH)
        self.text_consola.config(state=tk.DISABLED)

    # -------- FUNCIONES VACÍAS POR AHORA --------
    def nuevo(self):
        pass

    def abrir(self):
        pass

    def guardar(self):
        pass

    def editar(self):
        pass

    def compilar(self):
        pass

    def ayuda(self):
        pass

    def salir(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = MicroCPreCompilador(root)
    root.mainloop()

