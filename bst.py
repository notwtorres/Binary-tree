import tkinter as tk
from tkinter import messagebox

class NodoBST:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def insertar(self, nuevo_valor):
        if nuevo_valor < self.valor:
            if self.izquierdo is None:
                self.izquierdo = NodoBST(nuevo_valor)
            else:
                self.izquierdo.insertar(nuevo_valor)
        elif nuevo_valor > self.valor:
            if self.derecho is None:
                self.derecho = NodoBST(nuevo_valor)
            else:
                self.derecho.insertar(nuevo_valor)
        # Si es igual, no se inserta (sin duplicados)

    def calcular_posiciones(self, x, y, x_offset, posiciones):
        posiciones[self] = (x, y)
        if self.izquierdo:
            self.izquierdo.calcular_posiciones(x - x_offset, y + 80, x_offset // 2 if x_offset > 40 else 40, posiciones)
        if self.derecho:
            self.derecho.calcular_posiciones(x + x_offset, y + 80, x_offset // 2 if x_offset > 40 else 40, posiciones)

    def dibujar(self, canvas, posiciones):
        x, y = posiciones[self]
        radio = 20
        canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill="lightgreen")
        canvas.create_text(x, y, text=str(self.valor))
        if self.izquierdo:
            x_i, y_i = posiciones[self.izquierdo]
            canvas.create_line(x, y + radio, x_i, y_i - radio)
            self.izquierdo.dibujar(canvas, posiciones)
        if self.derecho:
            x_d, y_d = posiciones[self.derecho]
            canvas.create_line(x, y + radio, x_d, y_d - radio)
            self.derecho.dibujar(canvas, posiciones)

    def recorrido_preorden(self):
        resultado = [self.valor]
        if self.izquierdo:
            resultado.extend(self.izquierdo.recorrido_preorden())
        if self.derecho:
            resultado.extend(self.derecho.recorrido_preorden())
        return resultado

    def recorrido_inorden(self):
        resultado = []
        if self.izquierdo:
            resultado.extend(self.izquierdo.recorrido_inorden())
        resultado.append(self.valor)
        if self.derecho:
            resultado.extend(self.derecho.recorrido_inorden())
        return resultado

    def recorrido_postorden(self):
        resultado = []
        if self.izquierdo:
            resultado.extend(self.izquierdo.recorrido_postorden())
        if self.derecho:
            resultado.extend(self.derecho.recorrido_postorden())
        resultado.append(self.valor)
        return resultado

def actualizar_arbol():
    canvas.delete("all")
    posiciones.clear()
    if raiz:
        ancho_canvas = canvas.winfo_width()
        if ancho_canvas == 1:
            ancho_canvas = 900
        raiz.calcular_posiciones(ancho_canvas // 2, 40, 160, posiciones)
        raiz.dibujar(canvas, posiciones)

def agregar_nodo():
    global raiz
    valor = entry_valor.get()
    if not valor:
        messagebox.showwarning("Advertencia", "Ingrese un valor.")
        return
    try:
        valor_int = int(valor)
    except ValueError:
        messagebox.showerror("Error", "El valor debe ser un número entero.")
        return

    if raiz is None:
        raiz = NodoBST(valor_int)
    else:
        raiz.insertar(valor_int)

    entry_valor.delete(0, tk.END)
    actualizar_arbol()

def mostrar_preorden():
    if raiz:
        recorrido = raiz.recorrido_preorden()
        messagebox.showinfo("Recorrido Preorden", ", ".join(map(str, recorrido)))

def mostrar_inorden():
    if raiz:
        recorrido = raiz.recorrido_inorden()
        messagebox.showinfo("Recorrido Inorden", ", ".join(map(str, recorrido)))

def mostrar_postorden():
    if raiz:
        recorrido = raiz.recorrido_postorden()
        messagebox.showinfo("Recorrido Postorden", ", ".join(map(str, recorrido)))

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Árbol BST Interactivo")
canvas = tk.Canvas(ventana, width=900, height=700, bg="white")
canvas.pack()
canvas.bind("<Configure>", lambda event: actualizar_arbol())

frame = tk.Frame(ventana)
frame.pack(pady=5)

tk.Label(frame, text="Valor del nuevo nodo:").grid(row=0, column=0)
entry_valor = tk.Entry(frame, width=10)
entry_valor.grid(row=0, column=1, padx=5)

btn_agregar = tk.Button(frame, text="Agregar nodo", command=agregar_nodo)
btn_agregar.grid(row=0, column=2, padx=5)

btn_preorden = tk.Button(frame, text="Preorden", command=mostrar_preorden)
btn_preorden.grid(row=1, column=0, pady=5)

btn_inorden = tk.Button(frame, text="Inorden", command=mostrar_inorden)
btn_inorden.grid(row=1, column=1, pady=5)

btn_postorden = tk.Button(frame, text="Postorden", command=mostrar_postorden)
btn_postorden.grid(row=1, column=2, pady=5)

raiz = None
posiciones = {}

ventana.mainloop()
