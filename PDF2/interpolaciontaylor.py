import numpy as np
import matplotlib.pyplot as plt

#inicializo la primera clase
class InterpolacionTaylor:
    def __init__(self, dias, temperaturas, temp, h):  # creo el constructor y doy los datos
        self.dias = dias #dias en los que se midieron las temperaturas
        self.temperaturas = temperaturas #temperaturas registradas en cada dia
        self.temp = temp  #dia en el que se centra la interpolacion (3)
        self.h = h  #paso de la interpolacion por dias (1)
        self.temp_centro = self.temperaturas[2]  # T(temp)
        self.temp_antes = (self.temperaturas[3] - self.temperaturas[1]) / (2 * self.h)  # Aproximacion de T'(a) (temp)
        self.temp_despues = (self.temperaturas[3] - 2 * self.temperaturas[2] + self.temperaturas[1]) / (self.h**2)  # Aproximacion de T''(a) (temp)

    # definimos funcion de taylor    
    def interpolacion_taylor(self, x):
        return self.temp_centro + (x - self.temp) * self.temp_antes + ((x - self.temp)**2 / 2) * self.temp_despues
                 #T(x)= T(a) + (x−a) * T'(a) + ((x-a)**2 / 2) * T''(a)

    # funcion para la grafica de taylor 
    def graficar(self):
        valores_x = np.linspace(1, 7, 100) #generar valores 
        v_taylor = self.interpolacion_taylor(valores_x) #calculamos los valores interpolados en cada uno de los 100 valores generados
        
        plt.plot(self.dias, self.temperaturas, 'o', label='Datos originales') #grafico los valores en eje x y y
        plt.plot(valores_x, v_taylor, '-', label='Interpolacion de Taylor') #grafico los valores interpolados
        plt.xlabel('Dia') # etiqueta para el eje x
        plt.ylabel('Temperatura (°C)') # etiqueta para el eje y
        plt.legend()
        plt.grid(True)
        plt.title('Interpolacion de Taylor para Temperaturas Diarias') # agrego el titulo 
        plt.show()

# datos temperatura y dias
dias = np.array([1, 2, 3, 4, 5, 6, 7])
temperaturas = np.array([16, 18, 20, 19, 21, 22, 23])

# punto de interpolacion
temp = 3  #punto centro (dia 3)
h = 1  #distancia entre puntos(dias)

# crear una instancia de la clase
interpolacion = InterpolacionTaylor(dias, temperaturas, temp, h)

# accedemos al metodo para graficar
interpolacion.graficar()