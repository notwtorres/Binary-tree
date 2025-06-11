import tkinter as tk
from tkinter import simpledialog, messagebox

class NodoEnario:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, nodo_hijo):
        self.hijos.append(nodo_hijo)

    def calcular_posiciones(self, x, y, x_offset, posiciones):
        posiciones[self] = (x, y)
        if not self.hijos:
            return x
        ancho_total = x_offset * (len(self.hijos) - 1)
        x_inicio = x - ancho_total // 2
        for i, hijo in enumerate(self.hijos):
            hijo_x = x_inicio + i * x_offset
            hijo.calcular_posiciones(hijo_x, y + 80, x_offset // 2 if x_offset > 40 else 40, posiciones)
        return x

    def dibujar(self, canvas, posiciones, callback=None):
        x, y = posiciones[self]
        radio = 20
        # Dibuja el nodo y lo asocia a un tag único
        tag = f"nodo_{id(self)}"
        canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill="lightblue", tags=tag)
        canvas.create_text(x, y, text=str(self.valor), tags=tag)
        if callback:
            canvas.tag_bind(tag, "<Button-1>", lambda e, nodo=self: callback(nodo))
        for hijo in self.hijos:
            x_h, y_h = posiciones[hijo]
            canvas.create_line(x, y + radio, x_h, y_h - radio)
            hijo.dibujar(canvas, posiciones, callback)

def actualizar_arbol():
    canvas.delete("all")
    posiciones.clear()
    # Obtener el tamaño actual del canvas
    ancho_canvas = canvas.winfo_width()
    if ancho_canvas == 1:  # Si aún no se ha renderizado, usar el ancho inicial
        ancho_canvas = 900
    raiz.calcular_posiciones(ancho_canvas // 2, 40, 160, posiciones)
    raiz.dibujar(canvas, posiciones, seleccionar_nodo)

def seleccionar_nodo(nodo):
    global nodo_seleccionado
    nodo_seleccionado = nodo
    entry_padre.config(state="normal")
    entry_padre.delete(0, tk.END)
    entry_padre.insert(0, str(nodo.valor))
    entry_padre.config(state="readonly")

def agregar_nodo():
    valor = entry_valor.get()
    if not valor:
        messagebox.showwarning("Advertencia", "Ingrese un valor para el nodo.")
        return
    if nodo_seleccionado is None:
        messagebox.showwarning("Advertencia", "Seleccione un nodo padre haciendo clic en el árbol.")
        return
    nuevo_nodo = NodoEnario(valor)
    nodo_seleccionado.agregar_hijo(nuevo_nodo)
    entry_valor.delete(0, tk.END)
    actualizar_arbol()

# Crear ventana y canvas de tkinter
ventana = tk.Tk()
ventana.title("Árbol N-ario Interactivo")
canvas = tk.Canvas(ventana, width=900, height=700, bg="white")
canvas.pack()
canvas.bind("<Configure>", lambda event: actualizar_arbol())
# Configurar el canvas para que se ajuste al tamaño de la ventana

# Widgets para agregar nodos
frame = tk.Frame(ventana)
frame.pack(pady=5)

tk.Label(frame, text="Nodo padre seleccionado:").grid(row=0, column=0)
entry_padre = tk.Entry(frame, width=10, state="readonly")
entry_padre.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Valor del nuevo nodo:").grid(row=0, column=2)
entry_valor = tk.Entry(frame, width=10)
entry_valor.grid(row=0, column=3, padx=5)

btn_agregar = tk.Button(frame, text="Agregar nodo", command=agregar_nodo)
btn_agregar.grid(row=0, column=4, padx=5)

# Inicializar árbol con solo la raíz
raiz = NodoEnario("A")
nodo_seleccionado = raiz
posiciones = {}

actualizar_arbol()

ventana.mainloop()