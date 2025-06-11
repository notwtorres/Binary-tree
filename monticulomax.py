import tkinter as tk
from tkinter import simpledialog, messagebox

class MonticuloMaximo:
    def __init__(self):
        self.monticulo = []

    def insertar(self, valor):
        self.monticulo.append(valor)
        self._reordenar_hacia_arriba(len(self.monticulo) - 1)

    def extraer_maximo(self):
        if not self.monticulo:
            return None
        if len(self.monticulo) == 1:
            return self.monticulo.pop()

        maximo = self.monticulo[0]
        self.monticulo[0] = self.monticulo.pop()
        self._reordenar_hacia_abajo(0)
        return maximo

    def _reordenar_hacia_arriba(self, indice):
        while indice > 0:
            padre = (indice - 1) // 2
            if self.monticulo[indice] > self.monticulo[padre]:
                self.monticulo[indice], self.monticulo[padre] = self.monticulo[padre], self.monticulo[indice]
                indice = padre
            else:
                break

    def _reordenar_hacia_abajo(self, indice):
        n = len(self.monticulo)
        while True:
            izq = 2 * indice + 1
            der = 2 * indice + 2
            mayor = indice

            if izq < n and self.monticulo[izq] > self.monticulo[mayor]:
                mayor = izq
            if der < n and self.monticulo[der] > self.monticulo[mayor]:
                mayor = der
            if mayor == indice:
                break
            self.monticulo[indice], self.monticulo[mayor] = self.monticulo[mayor], self.monticulo[indice]
            indice = mayor

    def mostrar(self):
        return self.monticulo

# --- Interfaz gráfica con Tkinter ---

class MonticuloApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Montículo Máximo Visual")
        self.monticulo = MonticuloMaximo()

        # Canvas para dibujar el árbol
        self.canvas = tk.Canvas(root, width=700, height=350, bg="white")
        self.canvas.pack(pady=10)

        # Frame para los botones y mensajes
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.boton_insertar = tk.Button(self.frame, text="Insertar valor", command=self.insertar_valor)
        self.boton_insertar.grid(row=0, column=0, padx=5, pady=5)

        self.boton_extraer = tk.Button(self.frame, text="Extraer máximo", command=self.extraer_maximo)
        self.boton_extraer.grid(row=0, column=1, padx=5, pady=5)

        self.boton_mostrar = tk.Button(self.frame, text="Mostrar montículo", command=self.mostrar_monticulo)
        self.boton_mostrar.grid(row=0, column=2, padx=5, pady=5)

        self.label_estado = tk.Label(self.frame, text="", fg="blue")
        self.label_estado.grid(row=1, column=0, columnspan=3)

        self.dibujar_monticulo()

    def insertar_valor(self):
        if len(self.monticulo.monticulo) >= 10:
            messagebox.showinfo("Límite alcanzado", "No se pueden insertar más de 10 elementos.")
            return
        valor = simpledialog.askinteger("Insertar", "Ingrese un número entero:")
        if valor is not None:
            self.monticulo.insertar(valor)
            self.label_estado.config(text=f"Valor {valor} insertado correctamente.")
            self.dibujar_monticulo()

    def extraer_maximo(self):
        maximo = self.monticulo.extraer_maximo()
        if maximo is None:
            self.label_estado.config(text="El montículo está vacío.")
        else:
            self.label_estado.config(text=f"Valor máximo extraído: {maximo}")
        self.dibujar_monticulo()

    def mostrar_monticulo(self):
        monticulo = self.monticulo.mostrar()
        self.label_estado.config(text=f"Montículo actual: {monticulo}")

    def dibujar_monticulo(self):
        self.canvas.delete("all")
        nodos = self.monticulo.monticulo
        if not nodos:
            self.canvas.create_text(350, 50, text="Montículo vacío", font=("Arial", 16), fill="gray")
            return
        # Parámetros de dibujo
        radio = 22
        nivel_y = 50
        sep_y = 60
        ancho = self.canvas.winfo_width()
        if ancho < 700: ancho = 700

        posiciones = {}

        def calcular_posicion(indice, x, y, dx):
            if indice >= len(nodos):
                return
            posiciones[indice] = (x, y)
            izq = 2 * indice + 1
            der = 2 * indice + 2
            if izq < len(nodos):
                self.canvas.create_line(x, y+radio, x-dx, y+sep_y-radio, width=2)
                calcular_posicion(izq, x-dx, y+sep_y, dx//2)
            if der < len(nodos):
                self.canvas.create_line(x, y+radio, x+dx, y+sep_y-radio, width=2)
                calcular_posicion(der, x+dx, y+sep_y, dx//2)

        # Comenzar desde la raíz
        calcular_posicion(0, ancho//2, nivel_y, 120)

        # Dibujar nodos
        for i, valor in enumerate(nodos):
            x, y = posiciones[i]
            self.canvas.create_oval(x-radio, y-radio, x+radio, y+radio, fill="#4a90e2", outline="black", width=2)
            self.canvas.create_text(x, y, text=str(valor), font=("Arial", 14), fill="white")

if __name__ == "__main__":
    root = tk.Tk()
    app = MonticuloApp(root)
    root.mainloop()