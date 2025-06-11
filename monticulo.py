import tkinter as tk
from tkinter import messagebox

class MonticuloMinimo:
    def __init__(self):
        self.monticulo = []

    def insertar(self, valor):
        self.monticulo.append(valor)
        self._reordenar_hacia_arriba(len(self.monticulo) - 1)

    def extraer_minimo(self):
        if not self.monticulo:
            return None
        if len(self.monticulo) == 1:
            return self.monticulo.pop()
        minimo = self.monticulo[0]
        self.monticulo[0] = self.monticulo.pop()
        self._reordenar_hacia_abajo(0)
        return minimo

    def _reordenar_hacia_arriba(self, indice):
        while indice > 0:
            padre = (indice - 1) // 2
            if self.monticulo[indice] < self.monticulo[padre]:
                self.monticulo[indice], self.monticulo[padre] = self.monticulo[padre], self.monticulo[indice]
                indice = padre
            else:
                break

    def _reordenar_hacia_abajo(self, indice):
        n = len(self.monticulo)
        while True:
            izq = 2 * indice + 1
            der = 2 * indice + 2
            menor = indice
            if izq < n and self.monticulo[izq] < self.monticulo[menor]:
                menor = izq
            if der < n and self.monticulo[der] < self.monticulo[menor]:
                menor = der
            if menor == indice:
                break
            self.monticulo[indice], self.monticulo[menor] = self.monticulo[menor], self.monticulo[indice]
            indice = menor

    def mostrar(self):
        print("Montículo actual:", self.monticulo)

# --- Interfaz gráfica con Tkinter ---

class MonticuloApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Montículo Mínimo")
        self.root.geometry("900x700")
        self.monticulo = MonticuloMinimo()

        # Canvas para graficar el montículo
        self.canvas = tk.Canvas(root, width=880, height=400, bg="white")
        self.canvas.pack(pady=10)

        # Frame para los controles
        self.controls = tk.Frame(root)
        self.controls.pack(pady=20)

        # Entrada para insertar
        tk.Label(self.controls, text="Valor a insertar:").grid(row=0, column=0, padx=5)
        self.entry_valor = tk.Entry(self.controls, width=10)
        self.entry_valor.grid(row=0, column=1, padx=5)
        self.btn_insertar = tk.Button(self.controls, text="Insertar", command=self.insertar)
        self.btn_insertar.grid(row=0, column=2, padx=5)

        # Botón extraer mínimo
        self.btn_extraer = tk.Button(self.controls, text="Extraer mínimo", command=self.extraer_minimo)
        self.btn_extraer.grid(row=0, column=3, padx=5)

        # Botón mostrar montículo (en consola)
        self.btn_mostrar = tk.Button(self.controls, text="Mostrar en consola", command=self.mostrar_consola)
        self.btn_mostrar.grid(row=0, column=4, padx=5)

        # Botón salir
        self.btn_salir = tk.Button(self.controls, text="Salir", command=root.quit)
        self.btn_salir.grid(row=0, column=5, padx=5)

        # Etiqueta para mensajes
        self.lbl_mensaje = tk.Label(root, text="", fg="blue")
        self.lbl_mensaje.pack(pady=10)

        self.dibujar_monticulo()

    def insertar(self):
        if len(self.monticulo.monticulo) >= 10:
            messagebox.showwarning("Límite alcanzado", "No se pueden insertar más de 10 elementos.")
            return
        valor = self.entry_valor.get()
        try:
            numero = int(valor)
            self.monticulo.insertar(numero)
            self.lbl_mensaje.config(text="Valor insertado correctamente.")
            self.entry_valor.delete(0, tk.END)
            self.dibujar_monticulo()
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida. Ingrese un número entero.")

    def extraer_minimo(self):
        minimo = self.monticulo.extraer_minimo()
        if minimo is None:
            self.lbl_mensaje.config(text="El montículo está vacío.")
        else:
            self.lbl_mensaje.config(text=f"Valor mínimo extraído: {minimo}")
        self.dibujar_monticulo()

    def mostrar_consola(self):
        self.monticulo.mostrar()

    def dibujar_monticulo(self):
        self.canvas.delete("all")
        if not self.monticulo.monticulo:
            self.canvas.create_text(440, 200, text="Montículo vacío", font=("Arial", 18), fill="gray")
            return
        # Llama a la función recursiva para dibujar el árbol
        self._dibujar_nodo(0, 440, 40, 200)

    def _dibujar_nodo(self, indice, x, y, dx):
        if indice >= len(self.monticulo.monticulo):
            return
        valor = self.monticulo.monticulo[indice]
        radio = 25
        # Dibuja el nodo
        self.canvas.create_oval(x-radio, y-radio, x+radio, y+radio, fill="#b3e6ff", outline="black")
        self.canvas.create_text(x, y, text=str(valor), font=("Arial", 14, "bold"))
        # Dibuja las líneas e hijos
        izq = 2 * indice + 1
        der = 2 * indice + 2
        if izq < len(self.monticulo.monticulo):
            self.canvas.create_line(x, y+radio, x-dx, y+80-radio, width=2)
            self._dibujar_nodo(izq, x-dx, y+80, dx//2)
        if der < len(self.monticulo.monticulo):
            self.canvas.create_line(x, y+radio, x+dx, y+80-radio, width=2)
            self._dibujar_nodo(der, x+dx, y+80, dx//2)

if __name__ == "__main__":
    root = tk.Tk()
    app = MonticuloApp(root)
    root.mainloop()