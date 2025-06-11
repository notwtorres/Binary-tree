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
        print("Montículo actual:", self.monticulo)


def app_consola():
    monticulo = MonticuloMaximo()
    print("=== Montículo Máximo ===")

    while True:
        print("\nMenú:")
        print("1. Insertar valor")
        print("2. Extraer valor máximo")
        print("3. Mostrar montículo")
        print("4. Salir")

        opcion = input("Seleccione una opción (1-4): ")

        if opcion == "1":
            if len(monticulo.monticulo) >= 10:
                print("No se pueden insertar más de 10 elementos.")
                continue
            valor = input("Ingrese un número entero: ")
            try:
                numero = int(valor)
                monticulo.insertar(numero)
                print("Valor insertado correctamente.")
            except ValueError:
                print("Entrada inválida. Intente de nuevo.")
        elif opcion == "2":
            maximo = monticulo.extraer_maximo()
            if maximo is None:
                print("El montículo está vacío.")
            else:
                print(f"Valor máximo extraído: {maximo}")
        elif opcion == "3":
            monticulo.mostrar()
        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Ingrese un número del 1 al 4.")

app_consola()