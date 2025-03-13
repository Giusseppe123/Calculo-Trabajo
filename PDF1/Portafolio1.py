"""Tareas: 
1. Cálculo del Número de Condición: Calcula el número de 
condición de la matriz de covarianza 𝐶. Si el número de 
condición es alto, sugiere posibles problemas de estabilidad o 
concentración del riesgo en pocos activos.
 
2. Método de Potencia: Implementa el Método de Potencia para 
calcular el autovalor dominante y el auto vector asociado, 
interpretando los resultados como la dirección de mayor 
volatilidad en el portafolio. ¿Qué combinación de activos está 
causando el mayor riesgo? 

3. Método de Potencia Inverso: Implementa el Método de 
Potencia Inverso para encontrar el autovalor más pequeño y su 
auto vector asociado, lo cual te ayudará a identificar 
combinaciones de activos que podrían disminuir el riesgo a 
través de la diversificación. 

4. Visualización: Grafica la convergencia de los autovalores a lo 
largo de las iteraciones de los métodos de potencia y potencia 
inverso, e interpreta el comportamiento de la convergencia en 
el contexto del análisis de riesgo. 

5. Datos Iniciales: La matriz de covarianza puede ser simulada o 
calculada a partir de datos reales de retornos de activos, si se 
dispone de ellos. Para este ejercicio, puedes generar una 
matriz de covarianza aleatoria y asegurarte de que sea 
simétrica y positiva definida. """


import numpy as np
import matplotlib.pyplot as plt

class MatrizCovarianza:
    def __init__(self, n_activos):
        self.matriz = self.generar_matriz_covarianza(n_activos) #se inicializa la matriz de covarianza con la matriz generada por el metodo generar_matriz_covarianza

    def generar_matriz_covarianza(self, n):
        A = np.random.rand(n, n) #se genera una matriz de n x n con numeros aleatorios
        A = (A + A.T) / 2 #se suma la matriz con su transpuesta y se divide entre 2 para que la matriz sea simetrica
        return A @ A.T # se multiplica la matriz por su transpuesta para asegurar q sea positiva definida
    
    def mostrar_matriz(self):
        print(f"Matriz de Covarianza:\n{self.matriz}\n" ) #imprime la matriz de covarianza y la matriz de covarianza es una matriz simetrica
    
class AnalisisdeRiesgo:
    def __init__(self, matriz_cov):
        self.matriz_cov = matriz_cov
        self.autovalor_dominante = None
        self.autovector_dominante = None
        self.autovalor_menor = None
        self.autovector_menor = None
        self.convergencia_autovalores = []
        self.convergencia_autovectores = []
        self.convergencia_autovalores_inv = []  
        self.convergencia_autovectores_inv = []  # lista separada para el método inverso

    def calcularcondicion(self):
        return np.linalg.cond(self.matriz_cov) #se calcula el numero de condicion de la matriz de covarianza
    
    def metodoPotencia(self):
        n = self.matriz_cov.shape[0] #se obtiene el tamaño de la matriz de covarianza
        v = np.random.rand(n) #se genera un vector aleatorio de tamaño n
        v = v / np.linalg.norm(v) #se normaliza el vector para que tenga una longitud de 1

        self.convergencia_autovalores = []  # Reiniciamos la lista para este método
        self.convergencia_autovectores = []

        for _ in range(1000): #se inicia el bucle para que se ejecute hasta el numero maximo de iteraciones
            v_nuevo = np.dot(self.matriz_cov, v) #se multiplica la matriz de covarianza por el vector "v" para que se obtenga un nuevo vector q seria v_nuevo
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
        n = self.matriz_cov.shape[0]
        v = np.random.rand(n)
        v = v / np.linalg.norm(v)

        matriz_inversa = np.linalg.inv(self.matriz_cov) #se calcula la matriz inversa de la matriz de covarianza

        self.convergencia_autovalores_inv = []  # Lista separada para el método inverso
        self.convergencia_autovectores_inv = []  # Lista separada para el método inverso

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

        # Grafica de convergencia de los autovalores (dominante y menor)
        plt.subplot(2, 1, 1) #se crea un subplot con 2 filas y 1 columna y se selecciona la primera fila
        plt.plot(self.convergencia_autovalores, marker='o', label='Autovalor Dominante')  #en la grafica la y es el autovalor y la x es la iteracion
        plt.plot(self.convergencia_autovalores_inv, marker='x', color='r', label='Autovalor Menor')
        plt.title('Convergencia de Autovalores')
        plt.xlabel('Iteración')
        plt.ylabel('Autovalor')
        plt.legend()
        plt.grid()

        # Grafica de convergencia de los autovectores
        plt.subplot(2, 1, 2) #se selecciona la segunda fila
        
        # Graficar componentes del autovector dominante
        for i in range(len(self.convergencia_autovectores[0])): #se crea un bucle para que se ejecute por cada componente del autovector
            plt.plot([vec[i] for vec in self.convergencia_autovectores], marker='o',  #se graficara cada componente del autovector en funcion de las iteraciones
                    label=f'Activo {i+1} (Dominante)')
        
        # Graficar componentes del autovector menor con líneas punteadas
        for i in range(len(self.convergencia_autovectores_inv[0])): 
            plt.plot([vec[i] for vec in self.convergencia_autovectores_inv], marker='x', linestyle='--', #en la grafica se observara con lineas separadas para que se pueda diferenciar con el autovector dominante
                    label=f'Activo {i+1} (Menor)')
            
        plt.title('Convergencia de Autovectores')
        plt.xlabel('Iteración')
        plt.ylabel('Valor del componente')
        plt.legend() 
        plt.grid() 

        plt.tight_layout() 
        plt.show()
    
    def interpretar_resultados(self):
        
        print("\nINTERPRETACION DE RESULTADOS\n")
        
        # putno numero 1. sobre el numero de condicion
        print("1. Numero de Condicion:")
        numero_condicion = self.calcularcondicion()
        print(f"   Valor: {numero_condicion:.2f}")
        
        if numero_condicion > 100:
            print("   el numero de condicion es bastante alto lo que significa que")
            print("   nuestro portafolio no esta muy estable asi que que tenemos mucho riesgo")
            print("   concentrado en pocos activos asi que seria buena idea diversificar mas.")
        elif numero_condicion > 30:
            print("   el numero de condicion es algo alto por lo que que hay cierta")
            print("   concentracion de riesgo se podria mejorar un poco la diversificacion.")
        else:
            print("   el numero de condicion es bajo por lo que es bueno significa que el")
            print("   portafolio esta bien balanceado y el riesgo esta distribuido entre los activos.")
        
        # punto numero 2. sobre el autovalor dominante y su autovector
        print("\n2. Autovalor Dominante y su Autovector:")
        print(f"   Autovalor Dominante: {self.autovalor_dominante:.4f}")
        print("   este numero nos dice cual es la maxima volatilidad que podria tener nuestro portafolio.")
        
        print("\n   Autovector Dominante (direccion de maxima volatilidad):")
        for i, componente in enumerate(self.autovector_dominante): #se recorre el autovector dominante para mostrar cada componente del autovector dominante
            print(f"   Activo {i+1}: {componente:.4f}") 
        
        # se identifica el activo con mayor contribucion al riesgo
        indice_max_riesgo = np.argmax(np.abs(self.autovector_dominante)) #se busca el indice del autovector dominante con mayor valor absoluto y  np.argmax se encarga de devolver el indice del primer valor maximo
        print(f"\n   se ve que el Activo {indice_max_riesgo + 1} es el que mas contribuye al riesgo")
        print(f"   con un valor de {np.abs(self.autovector_dominante[indice_max_riesgo]):.4f}.")
        print("   este activo es el que mas volatilidad esta causando.")
        print("   si queremos reducir el riesgo podriamos considerar bajar nuestra inversion en este activo.")
        
        # punto numero 3. sobre el autovalor menor y su autovector
        print("\n3. Autovalor Menor y su Autovector:")
        print(f"   Autovalor Menor: {self.autovalor_menor:.4f}")
        print("   Este valor nos muestra la minima volatilidad posible en el portafolio.")
        
        print("\n   Autovector Menor (direccion de minima volatilidad):")
        for i, componente in enumerate(self.autovector_menor): #se recorre el autovector menor para mostrar cada componente del autovector menor
            print(f"   Activo {i+1}: {componente:.4f}")
        
        # se identifica el activo con mayor contribucion a la estabilidad
        indice_min_riesgo = np.argmax(np.abs(self.autovector_menor)) #se busca el indice del autovector menor con mayor valor absoluto np.argmax devuelve el indice del primer valor maximo
        print(f"\n   el Activo {indice_min_riesgo + 1} es el que mas contribuye a la estabilidad")
        print(f"   con un valor de {np.abs(self.autovector_menor[indice_min_riesgo]):.4f}.")
        print("   ese activo nos ayuda a reducir la volatilidad general.")
        print("   podriamos considerar aumentar nuestra inversion en este activo para mejorar la diversificacion.")
        
        # punto numero 4. sobre la convergencia interpretacion del comportamiento de la convergencia
        print("\n4. Sobre la Convergencia:")
        print("   Si miramos las graficas, podemos ver que tan rapido convergen los metodos.")
        
        # Verificar la velocidad de convergencia
        if len(self.convergencia_autovalores) < 10:
            print("   el metodo de potencia convergio rapido lo que indica que hay un factor de riesgo")
            print("   dominante muy claro en el portafolioasi que esto significa que hay una direccion")
            print("   especifica de volatilidad que es mucho mas importante que las demas.")
        else:
            print("   el metodo de potencia tardo en converger lo que podria indicar que hay")
            print("   varios factores de riesgo con importancia similar asi q Esto hace que sea mas")
            print("   dificil identificar una unica fuente principal de volatilidad.")
            
        if len(self.convergencia_autovalores_inv) < 10:
            print("   el metodo de potencia inverso convergio rapido lo que indica que hay una")
            print("   direccion clara de minima volatilidad que podriamos aprovechar para diversificar.")
        else:
            print("   el metodo de potencia inverso tardo en converger lo q sugiere que hay")
            print("   varias combinaciones de activos con volatilidad similar tenemos multiples")
            print("   opciones para diversificar el portafolio.")
        
        # final
        print("\n5. resumen:")
        ratio_riesgo = self.autovalor_dominante / self.autovalor_menor #se calcula la relacion entre el mayor y menor riesgo para ver si hay una gran diferencia entre la direccion de maximo y minimo riesgo
        print(f"   La relacion entre el mayor y menor riesgo es de {ratio_riesgo:.2f}.")
        
        if ratio_riesgo > 10:
            print("   hay una gran diferencia entre la direccion de maximo y minimo riesgo.")
            print("   nos dice que tenemos buenas oportunidades para diversificar mejor el portafolio.")
            print("   podriamos reducir significativamente el riesgo moviendo capital del Activo")
            print(f"   {indice_max_riesgo + 1} al Activo {indice_min_riesgo + 1}.")
        else:
            print("   la diferencia entre la direccion de maximo y minimo riesgo no es muy grande.")
            print("   esto sugiere que nuestro portafolio ya esta bastante diversificado,")
            print("   aunque podria ser dificil reducir mas el riesgo sin afectar el rendimiento esperado.")
            print("   quizas deberiamos considerar incluir nuevos tipos de activos en el portafolio.")

if __name__ == "__main__":
    n_activos = 5 #se define el numero de activos que se tendran en el portafolio
    matriz_cov = MatrizCovarianza(n_activos) #se crea la matriz de covarianza
    analisis = AnalisisdeRiesgo(matriz_cov.matriz) #se crea el objeto analisis de riesgo

    matriz_cov.mostrar_matriz()

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
    
