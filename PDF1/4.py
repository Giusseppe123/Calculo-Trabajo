import numpy as np
import matplotlib.pyplot as plt

class MetodoPotenciaInverso:
    def __init__(self, matriz, tolerancia=1e-6, max_iter=1000):
        self.matriz = matriz
        self.tolerancia = tolerancia
        self.max_iter = max_iter
        self.autovalor_menor = None
        self.autovector_menor = None
        self.convergencia_autovalores = []

    def normalizar(self, vector):
        return vector / np.linalg.norm(vector)

    def calcular_autovalor_menor(self):
        n = self.matriz.shape[0] #se obtiene el tamaño de la matriz
        v = np.random.rand(n)
        v = self.normalizar(v)

        # es necesario invertir la matriz para aplicar el método de la potencia inversa
        matriz_inversa = np.linalg.inv(self.matriz) #se calcula la matriz inversa de la matriz original para poder aplicar el metodo de potencia inverso el np.linalg.inv calcula la inversa de la matriz

        for _ in range(self.max_iter): #se inicia el bucle para que se ejecute hasta el numero maximo de iteraciones
            v_nuevo = np.dot(matriz_inversa, v) # se multiplica la matriz inversa por el vector v para que se obtenga un nuevo vector v_nuevo
            autovalor = np.dot(v_nuevo, v) #se calcula el autovalor como el producto punto entre el nuevo vector y el vector "v"
            v_nuevo = self.normalizar(v_nuevo) #se normaliza el nuevo vector dividiendolo por su norma

            # guardar la convergencia
            self.convergencia_autovalores.append(1 / autovalor)  # se guarda el inverso del autovalor ya q se busca el autovalor mas pequeño y el autovalor es el inverso del autovalor mas pequeño

            # se verifica
            if np.linalg.norm(v_nuevo - v) < self.tolerancia:
                break

            v = v_nuevo

        self.autovalor_menor = 1 / autovalor  # se guarda el autovalor más pequeño
        self.autovector_menor = v #se guarda el autovector menor

    def resultados(self):
        return self.autovalor_menor, self.autovector_menor #se devuelven el autovalor y autovector menor

    def graficar_convergencia(self):
        plt.figure(figsize=(8, 5)) #se crea una figura con un tamaño de 8x5
        plt.plot(self.convergencia_autovalores, marker='o') #se graficara la convergencia de los autovalores
        plt.title('Convergencia del Autovalor Más Pequeño')
        plt.xlabel('Iteración')
        plt.ylabel('Autovalor')
        plt.grid()
        plt.show()

if __name__ == "__main__":
    # matriz de ejemplo
    matriz = np.array([[20, 14, 26],
                       [10, 90, 0],
                       [54, 12, 55]])

    metodo_potencia_inverso = MetodoPotenciaInverso(matriz)
    metodo_potencia_inverso.calcular_autovalor_menor()
    autovalor, autovector = metodo_potencia_inverso.resultados()

    print("El autovalor menor es:", autovalor)
    print("El autovector correspondiente es:", autovector)
    metodo_potencia_inverso.graficar_convergencia()