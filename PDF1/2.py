import numpy as np
import matplotlib.pyplot as plt

class MetodoDePotencia:
    def __init__(self, matriz, max_iteraciones=1000, tolerancia=1e-6): #Se utiliza un numero maximo de iteraciones de 1000 porque es el por defecto y la tolerancia es de 1e-6 porque es el valor por defecto
        self.matriz = matriz
        self.max_iteraciones = max_iteraciones
        self.tolerancia = tolerancia

    def calcular_autovalor_y_autovector(self):
        n = self.matriz.shape[0] #se obtiene el tamaño de la matriz numero de filas o columnas ya q es cuadrada
        v = np.random.rand(n) #se genera un vector aleatorio de tamaño n
        v = v / np.linalg.norm(v)  # se normaliza el vector para que tenga una longitud de 1
        autovalores = []
        autovectores = []

        for _ in range(self.max_iteraciones): # se inicia el blucle para q se ejecute hasta el numero maximo de iteraciones que habran
            v_nuevo = np.dot(self.matriz, v) # se multplica la matriz por el vector "v" para que se obtenga un nuevo vector q seria v_nuevo
            autovalor = np.linalg.norm(v_nuevo)#calculara el autovalor como la norma del nuevo vector v_nuevo
            autovalores.append(autovalor) #se añade el autovalor a la lista de autovalores
            v_nuevo = v_nuevo / autovalor #se normaliza el nuevo vector dividiendolo por el autovalor
            autovectores.append(v_nuevo) #se añade el nuevo vector a la lista de autovectores

            # Comprobar la convergencia
            if np.linalg.norm(v_nuevo - v) < self.tolerancia: #Esto permite comprobar si la diferencia entre el nuevo vector y el vector anterior es menor que la tolerancia. si esto es asi se considera que el algoritmo ha convergido y se sale del bucle
                break
            v = v_nuevo #se actualiza el vector "v" con el nuevo vector "v_nuevo" para que se pueda seguir con la iteracion

        return autovalor, v, autovalores, autovectores

class Grafica:
    def __init__(self, autovalores, autovectores):
        self.autovalores = autovalores 
        self.autovectores = autovectores
        #la lista de los autovalores calculados y autovectores calculados

    def visualizar_convergencia(self):
        iteraciones = range(len(self.autovalores)) # creara un rango de iteraciones basado en la longitud de la lista de autovalores

        # Visualizar el autovalor
        plt.figure(figsize=(12, 6)) #se crea una figura con un tamaño de 12x6
        plt.subplot(1, 2, 1) #se crea un subplot con 1 fila y 2 columnas y se selecciona la primera columna
        plt.plot(iteraciones, self.autovalores, marker='o') #graficara los autovalores en funcion de las iteraciones
        plt.title('Convergencia del Autovalor Dominante')
        plt.xlabel('Iteraciones')
        plt.ylabel('Autovalor')
        plt.grid()

        # Visualizar el autovector
        plt.subplot(1, 2, 2) #se selecciona la segunda columna
        for i in range(len(self.autovectores[0])):
            plt.plot(iteraciones, [v[i] for v in self.autovectores], marker='o', label=f'Componente {i+1}') # graficara cada componente del autovector en funcion de las iteraciones
        plt.title('Convergencia del Autovector')
        plt.xlabel('Iteraciones')
        plt.ylabel('Valor del Autovector')
        plt.legend()
        plt.grid()

        plt.tight_layout()
        plt.show()

class AnalisisPotencia:
    def __init__(self):
        # Definir una matriz 3x3 por ejemplo
        self.matriz = np.array([[48, 15, 43],
                                 [65, 33, 0],
                                 [78, 43, 0]])

    def ejecutar(self):
        metodo_potencia = MetodoDePotencia(self.matriz)
        autovalor, autovector, autovalores, autovectores = metodo_potencia.calcular_autovalor_y_autovector()

        print(f"Autovalor Dominante: {autovalor}")
        print(f"Autovector: {autovector}")
        
        grafica = Grafica(autovalores, autovectores)
        grafica.visualizar_convergencia()

if __name__ == "__main__":
    analisis = AnalisisPotencia()
    analisis.ejecutar()