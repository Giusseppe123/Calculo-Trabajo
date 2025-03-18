import numpy as np
import matplotlib.pyplot as plt

#inicializo la clase para interpolacion de hermite
class InterpolacionHermite:
    def __init__(self, dias, temperaturas, derivadas):  
        self.dias = dias  #dias en los que se midieron las temperaturas
        self.temperaturas = temperaturas  #temperaturas registradas en cada dia
        self.derivadas = derivadas  #derivadas aproximadas de las temperaturas

    #funcion de interpolacion de hermite
    def interpolacion_hermite(self, x):
        n = len(self.dias)
        resultado = 0

        for i in range(n - 1):  #recorremos los dias hasta el penultimo (esta es la correccion que me hizo profe por esto no me corria el programa)
            dia_actual = self.dias[i]
            dia_siguiente = self.dias[i+1]
            temp_actual = self.temperaturas[i]
            temp_siguiente = self.temperaturas[i+1]
            derivada_actual = self.derivadas[i]
            derivada_siguiente = self.derivadas[i+1]
            diferencia = dia_siguiente - dia_actual  #diferencia entre dias

            #calculamos un valor t que normaliza x dentro del intervalo 
            t = (x - dia_actual) / diferencia  

            #formula usada para hermite
            # h(x) = h0(x) * f(x0) + h1(x) * f(x1) + h2(x) * f'(x0) + h3(x) * f'(x1)

            #funciones base de Hermite
            H0 = (1 + 2 * t) * (1 - t) ** 2  # h0(x)
            H1 = t * (1 - t) ** 2            # h2(x)
            H2 = t ** 2 * (3 - 2 * t)        # h1(x)
            H3 = t ** 2 * (t - 1)            # h3(x)

            if dia_actual <= x <= dia_siguiente:
                resultado += H0 * temp_actual + H2 * temp_siguiente + H1 * diferencia * derivada_actual + H3 * diferencia * derivada_siguiente

        return resultado

    # funcion para graficar la interpolacion de hermite
    def graficar(self):
        valores_x = np.linspace(1, 7, 100)  #genero los 100 valores 
        v_hermite = np.array([self.interpolacion_hermite(x) for x in valores_x])  #evaluamos la interpolacion para cada valor de x

        plt.plot(self.dias, self.temperaturas, 'o', label='Datos originales')  # graficamos los puntos en eje x y y
        plt.plot(valores_x, v_hermite, '-', label='Interpolacion de Hermite')  #graficamos los valores interpolados
        plt.xlabel('Dia')  # etiqueta para el eje x
        plt.ylabel('Temperatura (°C)')  # etiqueta para el eje y
        plt.legend()
        plt.title('Interpolacion de Hermite para Temperaturas Diarias')  #itulo
        plt.grid(True)
        plt.show()

#datos temperaturas y dias
dias = np.array([1, 2, 3, 4, 5, 6, 7])
temperaturas = np.array([16, 18, 20, 19, 21, 22, 23])

# derivadas aproximadas (esto lo calculamos de forma similar al codigo anterior)
derivadas = np.array([2, 3, 4, 3, 3, 4, 3])  # aproximacion de las derivadas en cada punto

#creo una instancia de la clase interpolacion hermite
interpolacion = InterpolacionHermite(dias, temperaturas, derivadas)

#accedemos al metodo para graficar
interpolacion.graficar()