import numpy as np
import matplotlib.pyplot as plt

class NumeroCondicionMatriz:
    def __init__(self, tamaño):
        self.tamaño = tamaño #indicara el tamaño de la matriz
        self.matriz = self.generar_matriz_aleatoria(tamaño) #creara la matriz aleatoria

    def generar_matriz_aleatoria(self, tamaño):
        return np.random.rand(tamaño, tamaño) #creara una matriz de tamaño x tamaño con numeros aleatorios

    def calcular_condicion(self):
        return np.linalg.cond(self.matriz) #calcula el numero de condicion de la matriz que indica cuan sensible es la solucion de un sistema de ecuaciones lineakes a cambios en los datos de entrada

    def mostrar_matriz(self):
        print(f"Matriz {self.tamaño}x{self.tamaño}:\n{self.matriz}\n") #imprime la matriz con su tamaño y los valores de la matriz

class AnalisisMatrices:
    def __init__(self, tamaños):
        self.tamaños = tamaños #sera una lista de tamaños de matricces q se analizaran
        self.numeros_condicion = [] #inicializa una lista vacia que alamacera los numeros de condicion de las matrices

    def ejecutar(self):
        for tamaño in self.tamaños:
            condicion_matriz = NumeroCondicionMatriz(tamaño) #creara una nueva instancia de la clase NumeroCondicionMatriz con el tamaño de la matriz
            num_condicion = condicion_matriz.calcular_condicion() #calcula el numero de condicion de la matriz
            self.numeros_condicion.append(num_condicion) # y agregara el numero de condicion dado a la lista

            condicion_matriz.mostrar_matriz()
            print(f"Numero de condicion: {num_condicion}\n")

        self.graficar_resultados()

    def graficar_resultados(self):
        plt.plot(self.tamaños, self.numeros_condicion, 'o-') #graficara los tamaños de las matrices en el eje x y los numeros de condicion en el eje y el argumento o- indica que se deben usar puntos conectados por líneas.
        plt.xlabel('Tamaño de la matriz')
        plt.ylabel('Numero de condicion')
        plt.title('Numero de condicion en funcion del tamaño de la matriz')
        plt.show()

if __name__ == "__main__":
    tamaños = range(2, 7)  #dependiendo de los numeros que se eligan  en este caso se generaran matrices de 2x2 a 6x6 
    analisis = AnalisisMatrices(tamaños)
    analisis.ejecutar()