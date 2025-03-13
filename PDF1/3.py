import numpy as np
import matplotlib.pyplot as plt

class MetodoPotenciaSimetrico:
    def __init__(self, matriz, tolerancia=1e-6, max_iter=1000):
        self.matriz = matriz
        self.tolerancia = tolerancia
        self.max_iter = max_iter
        self.autovalor_dominante = None #se inicializa el autovalor dominante en None
        self.autovector_dominante = None #se inicializa el autovector dominante en None
        self.convergencia_autovalores = [] #se inicializa la lista de convergencia de autovalores en vacio
        self.convergencia_autovectores = [] #se inicializa la lista de convergencia de autovectores en vacio

    def normalizar(self, vector):
        return vector / np.linalg.norm(vector) #se normaliza el vector dividiendolo por su norma esto se hace porque el metodo de potencia necesita que el vector tenga una longitud de 1

    def calcular_autovalor_dominante(self):
        n = self.matriz.shape[0] # se obtiene el tamaño de la matriz
        v = np.random.rand(n) # con np.random.rand se genera un vector aleatorio de tamaño n
        v = self.normalizar(v) # y se normaliza el vector

        # Se inicia el bucle para que se ejecute hasta el numero maximo de iteraciones
        for _ in range(self.max_iter):
            # Multiplicar la matriz por el vector
            v_nuevo = np.dot(self.matriz, v) #se multiplica la matriz por el vector "v" para que se obtenga un nuevo vector q seria v_nuevo
            autovalor = np.dot(v_nuevo, v) #se calcula el autovalor como el producto punto entre el nuevo vector y el vector "v"
            v_nuevo = self.normalizar(v_nuevo) #se normaliza el nuevo vector dividiendolo por su norma

            #se guarda la convergencia
            self.convergencia_autovalores.append(autovalor)
            self.convergencia_autovectores.append(v_nuevo)

            # se verifica
            if np.linalg.norm(v_nuevo - v) < self.tolerancia: #se verifica si la diferencia entre el nuevo vector y el vector anterior es menor que la tolerancia
                break #si esto es asi se considera que el algoritmo ha convergido y se sale del bucle

            v = v_nuevo #se actualiza el vector "v" con el nuevo vector "v_nuevo" para que se pueda seguir con la iteracion

        self.autovalor_dominante = autovalor
        self.autovector_dominante = v
        # y se guardaran los datos del autovalor y autovector dominante

    def obtener_resultados(self):
        return self.autovalor_dominante, self.autovector_dominante #se devuelven el autovalor y autovector dominante

    def graficar_convergencia(self):
        plt.figure(figsize=(12, 6)) #se crea una figura con un tamaño de 12x6

        # Graficar la convergencia de los autovalores
        plt.subplot(1, 2, 1) #como en el ejercio 2 se crea un subplot con 1 fila y 2 columnas y se selecciona la primera columna
        plt.plot(self.convergencia_autovalores, marker='o') #se graficara la convergencia de los autovalores
        plt.title('Convergencia de Autovalores')
        plt.xlabel('Iteración')
        plt.ylabel('Autovalor')
        plt.grid()

        # Graficar la convergencia del autovector dominante
        plt.subplot(1, 2, 2) #se selecciona la segunda columna
        for i in range(len(self.convergencia_autovectores[0])): #se crea un bucle para que se ejecute por cada componente del autovector
            plt.plot([vec[i] for vec in self.convergencia_autovectores], marker='o', label=f'Componente {i+1}') #se graficara cada componente del autovector en funcion de las iteraciones
        plt.title('Convergencia del Autovector Dominante')
        plt.xlabel('Iteración')
        plt.ylabel('Valor del Componente')
        plt.legend()
        plt.grid()

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # ejemplo definir una matriz simétrica
    matriz = np.array([[48, 19, 21],
                       [11, 76, 0],
                       [28, 0, 54]])

    metodo_potencia_simetrico = MetodoPotenciaSimetrico(matriz)
    metodo_potencia_simetrico.calcular_autovalor_dominante()
    autovalor, autovector = metodo_potencia_simetrico.obtener_resultados()

    print("El autovalor dominante es:", autovalor)
    print("El autovector dominante es:", autovector)
    metodo_potencia_simetrico.graficar_convergencia()