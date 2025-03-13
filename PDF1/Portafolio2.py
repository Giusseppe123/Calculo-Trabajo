"""Tareas: 
1. Cálculo del Número de Condición: Calcula el número de 
condición de la matriz de rigidez 𝐴. Comenta sobre la 
estabilidad del diseño basándote en este resultado.
 
2. Método de Potencia: Utiliza el Método de Potencia para 
calcular el autovalor dominante de la matriz de rigidez 𝐴. 
Interpreta el autovalor y el auto vector en términos de la rigidez 
estructural del puente. ¿En qué dirección la estructura es más 
resistente? 

3. Método de Potencia Inverso: Utiliza el Método de Potencia 
Inverso para calcular el autovalor más pequeño de la matriz. 
Comenta sobre las direcciones de mayor vulnerabilidad 
estructural. 

4. Visualización: Grafica la convergencia de los autovalores 
obtenidos en las iteraciones de los métodos de potencia y de 
potencia inverso. Explica qué tan rápido convergen estos 
métodos y cómo afecta la convergencia al análisis estructural. 

5. Datos Iniciales: Puedes utilizar una matriz de rigidez simétrica 
de ejemplo, o generar una matriz aleatoria simétrica que 
represente el modelo estructural del puente para fines de 
simulación."""

import numpy as np
import matplotlib.pyplot as plt

class MatrizRigidez:
    def __init__(self, n_puntos):
        self.matriz = self.generar_matriz_rigidez(n_puntos) #se inicializa la matriz de rigidez con la matriz generada por el metodo generar_matriz_rigidez

    def generar_matriz_rigidez(self, n):
        A = np.random.rand(n, n) #se genera una matriz de n x n con numeros aleatorios
        A = (A + A.T) / 2 #se suma la matriz con su transpuesta y se divide entre 2 para que la matriz sea simetrica
        
        # se asegura que la matriz sea definida positiva (característica de matrices de rigidez)
        A = A @ A.T + n * np.eye(n) # se multiplica la matriz por su transpuesta y se suma una matriz identidad para asegurar q sea positiva definida
        return A
    
    def mostrar_matriz(self):
        print(f"Matriz de Rigidez:\n{self.matriz}\n") #imprime la matriz de rigidez y la matriz de rigidez es una matriz cuadrada que representa la rigidez de una estructura
    
class AnalisisEstructural:
    def __init__(self, matriz_rig):
        self.matriz_rig = matriz_rig
        self.autovalor_dominante = None
        self.autovector_dominante = None
        self.autovalor_menor = None
        self.autovector_menor = None
        self.convergencia_autovalores = []
        self.convergencia_autovectores = []

    def calcularcondicion(self):
        return np.linalg.cond(self.matriz_rig) #calcula el numero de condicion de la matriz de rigidez
    
    def metodoPotencia(self):
        n = self.matriz_rig.shape[0] #se obtiene el tamaño de la matriz de rigidez
        v = np.random.rand(n) #se genera un vector aleatorio de tamaño n
        v = v / np.linalg.norm(v) #se normaliza el vector para que tenga una longitud de 1

        self.convergencia_autovalores = [] # se reinicia la lista para este método
        self.convergencia_autovectores = []

        for _ in range(1000): #se inicia el bucle para que se ejecute hasta el numero maximo de iteraciones
            v_nuevo = np.dot(self.matriz_rig, v) #se multiplica la matriz de rigidez por el vector "v" para que se obtenga un nuevo vector q seria v_nuevo
            autovalor = np.linalg.norm(v_nuevo) #calculara el autovalor como la norma del nuevo vector v_nuevo
            self.convergencia_autovalores.append(autovalor) 
            v_nuevo = v_nuevo / autovalor #se normaliza el nuevo vector dividiendolo por el autovalor
            self.convergencia_autovectores.append(v_nuevo)

            if np.linalg.norm(v_nuevo - v) < 1e-6: #esto permite comprobar si la diferencia entre el nuevo vector y el vector anterior es menor que la tolerancia. si esto es asi se considera que el algoritmo ha convergido y se sale del bucle
                break

            v = v_nuevo #se actualiza el vector "v" con el nuevo vector "v_nuevo" para que se pueda seguir con la iteracion

        self.autovalor_dominante = autovalor #se guarda el autovalor dominante
        self.autovector_dominante = v #se guarda el autovector dominante

    def metodoPotenciaInverso(self):
        n = self.matriz_rig.shape[0]
        v = np.random.rand(n)
        v = v / np.linalg.norm(v)

        matriz_inversa = np.linalg.inv(self.matriz_rig) #se calcula la matriz inversa de la matriz de rigidez

        self.convergencia_autovalores_inv = [] # Lista separada para el método inverso
        self.convergencia_autovectores_inv = []

        for _ in range(1000):
            v_nuevo = np.dot(matriz_inversa, v)
            autovalor = np.dot(v_nuevo, v) #se calcula el autovalor como el producto punto entre el nuevo vector y el vector "v"
            self.convergencia_autovalores_inv.append(1 / autovalor) #se guarda el inverso del autovalor ya q se busca el autovalor mas pequeño
            v_nuevo = v_nuevo / np.linalg.norm(v_nuevo) #se normaliza el nuevo vector
            self.convergencia_autovectores_inv.append(v_nuevo)

            if np.linalg.norm(v_nuevo - v) < 1e-6:
                break

            v = v_nuevo
        self.autovalor_menor = 1 / autovalor #se divide ya que se busca el autovalor mas pequeño
        self.autovector_menor = v #se guarda el autovector menor

    def grafica(self):
        plt.figure(figsize=(12, 10))

        # se haran 4 graficas para que se pueda observar detalladamente la convergencia de los metodos

        #primer se grafica la convergencia del autovalor dominante
        plt.subplot(2, 2, 1) #se crea un subplot con 2 filas y 2 columnas y se selecciona la primera posicion
        plt.plot(self.convergencia_autovalores, marker='o')
        plt.title('Convergencia del Autovalor Dominante')
        plt.xlabel('Iteración')
        plt.ylabel('Autovalor')
        plt.grid()

        # luego se grafica la convergencia del autovalor menor usando el metodo de potencia inverso
        plt.subplot(2, 2, 2) #se selecciona la segunda posicion
        plt.plot(self.convergencia_autovalores_inv, marker='o', color='r') 
        plt.title('Convergencia del Autovalor Menor')
        plt.xlabel('Iteración')
        plt.ylabel('Autovalor')
        plt.grid()

        #luego se grafica la convergencia del autovector dominante
        plt.subplot(2, 2, 3) #se selecciona la tercera posicion
        for i in range(len(self.convergencia_autovectores[0])): #se crea un bucle para que se ejecute por cada componente del autovector
            plt.plot([vec[i] for vec in self.convergencia_autovectores], marker='o', label=f'Punto {i+1}') #se graficara cada componente del autovector en funcion de las iteraciones el plt.plot se encarga de graficar los puntos 
        plt.title('Convergencia del Autovector Dominante')
        plt.xlabel('Iteración')
        plt.ylabel('Valor del componente')
        plt.legend()
        plt.grid()

        #y por ultimo se grafica la convergencia del autovector menor aplicando el metodo de potencia inverso
        plt.subplot(2, 2, 4) #se selecciona la cuarta posicion
        for i in range(len(self.convergencia_autovectores_inv[0])): #se crea un bucle para que se ejecute por cada componente del autovector inverso
            plt.plot([vec[i] for vec in self.convergencia_autovectores_inv], marker='o', label=f'Punto {i+1}', color=f'C{i}') #se graficara cada componente del autovector inverso en funcion de las iteraciones
        plt.title('Convergencia del Autovector Menor')
        plt.xlabel('Iteración')
        plt.ylabel('Valor del componente')
        plt.legend()
        plt.grid()

        plt.tight_layout()
        plt.show()
    
    def interpretar_resultados(self):
        print("\nINTERPRETACION DE RESULTADOS\n")
        
        # punto numero 1. numero de condicion
        print("1. Numero de Condicion:")
        numero_condicion = self.calcularcondicion()
        print(f"   Valor: {numero_condicion:.2f}")
        
        if numero_condicion > 1000:
            print("   el numero de condicion es muy alto por lo que no es bueno para nuestro puente.")
            print("   esto significa que pequeños cambios en las fuerzas aplicadas podrian causar")
            print("   grandes deformaciones en la estructura se deberia revisar el diseño porque")
            print("   podria ser inestable bajo ciertas condiciones de carga.")
        elif numero_condicion > 100:
            print("   el numero de condicion es algo elevado no es critico pero indica que")
            print("   la estructura podria ser sensible a ciertas cargas asi q seria bueno revisar")
            print("   los puntos mas debiles del diseño para mejorar la estabilidad general.")
        else:
            print("   el numero de condicion es aceptable esto sugiere que la estructura del puente")
            print("   es bastante estable y deberia responder bien a las cargas normales sin")
            print("   deformaciones excesivas.")
        
        # punto numero 2. autovalor dominante y su autovector mayor usando el metodo de potencia
        print("\n2. Autovalor Dominante y su Autovector:")
        print(f"   Autovalor Dominante: {self.autovalor_dominante:.4f}")
        print("   este valor representa la maxima rigidez de la estructura del puente.")
        print("   canto mayor sea este valor mas resistente sera el puente en cierta direccion.")
        
        print("\n   Autovector Dominante (direccion de maxima rigidez):")
        for i, componente in enumerate(self.autovector_dominante):
            print(f"   Punto {i+1}: {componente:.4f}")
        
        # identificar el punto con mayor rigidez
        indice_max_rigidez = np.argmax(np.abs(self.autovector_dominante)) #se obtiene el indice del punto con mayor rigidez
        print(f"\n   vemos que el Punto {indice_max_rigidez + 1} contribuye mas a la rigidez")
        print(f"   con un valor de {np.abs(self.autovector_dominante[indice_max_rigidez]):.4f}.")
        print("   esto significa que este punto del puente es el mas resistente a las deformaciones.")
        print("   pdriamos aprovechar esta caracteristica para distribuir mejor las cargas.")
        
        # punto numero 3 direcciones de mayor vulnerabilidad usando el metodo de potencia inverso
        print("\n3. Autovalor Menor y su Autovector:")
        print(f"   Autovalor Menor: {self.autovalor_menor:.4f}")
        print("   este valor representa la minima rigidez de la estructura.")
        print("   es super importante porque nos muestra donde el puente podria fallar primero.")
        
        print("\n   Autovector Menor (direccion de minima rigidez):")
        for i, componente in enumerate(self.autovector_menor):
            print(f"   Punto {i+1}: {componente:.4f}")
        
        # identificar el punto con menor rigidez
        indice_min_rigidez = np.argmax(np.abs(self.autovector_menor)) #se obtiene el indice del punto con menor rigidez
        print(f"\n   El Punto {indice_min_rigidez + 1} es el que mas contribuye a la vulnerabilidad")
        print(f"   con un valor de {np.abs(self.autovector_menor[indice_min_rigidez]):.4f}.")
        print("   este punto es donde el puente es mas susceptible a deformarse bajo carga.")
        print("   Deberiamos reforzar esta area para mejorar la estabilidad general del puente.")
        
        # punto numero 4. interpretacion de la convergencia
        print("\n4. Sobre la Convergencia:")
        print("   Si miramos las graficas, podemos ver que tan rapido convergen los metodos.")
        
        # verificar la velocidad de convergencia del metodo de potencia
        if len(self.convergencia_autovalores) < 10:
            print("   el metodo de potencia convergio muy rapido lo que indica que el autovalor")
            print("   dominante esta bien separado de los demas esto es bueno porque significa")
            print("   que hay una direccion clara de maxima rigidez en la estructura.")
        else:
            print("   el metodo de potencia tardo en converger lo que podria indicar que hay")
            print("   varios autovalores cercanos al dominante esto significa que la estructura")
            print("   tiene rigidez similar en varias direcciones.")
            
        # verificar la velocidad de convergencia del metodo de potencia inverso
        if len(self.convergencia_autovalores_inv) < 10:
            print("   el metodo de potencia inverso convergio rapido lo que indica que el autovalor")
            print("   mas pequeño esta bien separado essto significa que hay una direccion clara")
            print("   de minima rigidez que debemos atender.")
        else:
            print("   el metodo de potencia inverso tardo en converger lo que podria indicar")
            print("   que hay varios puntos debiles con rigidez similar dberiamos revisar")
            print("   multiples areas de la estructura para mejorar su estabilidad general.")
        
        # final
        print("\n5. En resumen:")
        ratio_rigidez = self.autovalor_dominante / self.autovalor_menor #se calcula la relacion entre la maxima y minima rigidez para ver si la estructura es equilibrada
        print(f"   La relacion entre la maxima y minima rigidez es de {ratio_rigidez:.2f}.")
        
        if ratio_rigidez > 1000:
            print("   esta relacion es demasiado alta por lo que indica un diseño muy")
            print("   desequilibrado el puente es muy rigido en algunas direcciones pero")
            print("   muy debil en otras eto podria llevar a fallos estructurales bajo")
            print("   ciertas condiciones de carga recomendaria rediseñar la estructura.")
        elif ratio_rigidez > 100:
            print("   esta relacion es bastante alta aunque el puente podria funcionar")
            print("   en condiciones normales eria recomendable reforzar los puntos debiles")
            print("   para mejorar su comportamiento bajo cargas extremas o inesperadas.")
        else:
            print("   esta relacion es razonable para un puente la estructura parece")
            print("   tener una buena distribucion de rigidez aunque siempre se pueden")
            print("   hacer mejoras en los puntos identificados como mas vulnerables.")

if __name__ == "__main__":
    n_puntos = 5 #se define el numero de puntos clave en la estructura del puente
    matriz_rig = MatrizRigidez(n_puntos) #se crea la matriz de rigidez
    analisis = AnalisisEstructural(matriz_rig.matriz) #se crea el objeto analisis estructural

    matriz_rig.mostrar_matriz() #se muestra la matriz de rigidez

    numero_condicion = analisis.calcularcondicion()
    print(f"Numero de condicion: {numero_condicion}")

    analisis.metodoPotencia()
    print(f"Autovalor Dominante: {analisis.autovalor_dominante}")
    print(f"Autovector Dominante: {analisis.autovector_dominante}")

    analisis.metodoPotenciaInverso()
    print(f"Autovalor Menor: {analisis.autovalor_menor}")
    print(f"Autovector Menor: {analisis.autovector_menor}")
    analisis.interpretar_resultados()
    analisis.grafica()
    