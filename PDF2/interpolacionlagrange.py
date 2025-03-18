import numpy as np
import matplotlib.pyplot as plt

#inicializo la primera clase
class InterpolacionLagrange:
    def __init__(self, dias, temperaturas):  #creo el constructor con los datos
        self.dias = dias  #dias en los que se midieron las temperaturas
        self.temperaturas = temperaturas  # temperaturas registradas en cada dia

    # definimos funcion de Lagrange 
    def interpolacion_lagrange(self, x):
        n = len(self.dias) #numero de puntos de datos longitud de arreglo
        resultado = 0 #variable para almacenar
        for i in range(n): #recorremos todos los puntos de datos para calcular cada término
            # Calculamos el polinomio L_i(x) para cada punto
            termino = self.temperaturas[i] # valor de la temperatura en el punto i
        #calculo del producto de los factores
            for j in range(n): #recorro todos lo puntos de datos pero solo calculo los puntos j
                if j != i:
                    termino *= (x - self.dias[j]) / (self.dias[i] - self.dias[j]) 
                    #calculo de factor (x - xj) / ( xi - xj ) para polinomio base Li(x)
            resultado += termino
        return resultado

    # funcion para la grafica de lagrange 
    def graficar(self):
        valores_x = np.linspace(1, 7, 200)  # genero los 100 valores entre 1 y 7
        v_lagrange = np.array([self.interpolacion_lagrange(x) for x in valores_x])  #evaluamos la interpolacion para cada valor de x

        plt.plot(self.dias, self.temperaturas, 'o', label='Datos originales')  # graficamos los puntos en eje x y y
        plt.plot(valores_x, v_lagrange, '-', label='Interpolacion de Lagrange') # graficamos los valores interpolados
        plt.xlabel('Dia') #etiqueta para el eje x
        plt.ylabel('Temperatura (°C)') #etiqueta para el eje y
        plt.legend()
        plt.title('Interpolacion de Lagrange para Temperaturas Diarias') #titulo
        plt.grid(True)
        plt.show()

# datos temperaturas y dias
dias = np.array([1, 2, 3, 4, 5, 6, 7])
temperaturas = np.array([16, 18, 20, 19, 21, 22, 23])

# creao una instancia de la clase 
interpolacion = InterpolacionLagrange(dias, temperaturas)

# accedemos al metodo para graficar
interpolacion.graficar()
