import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QApplication, QLabel, \
    QHBoxLayout, QPushButton, QMessageBox
import numpy as np
from histogramador import HistogramWindow
from scipy.stats import chi2, norm


class NormWindow(QWidget):
    def __init__(self, numeros, k_intervalos, media, sigma, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Test de Chi-cuadrado")
        self.setGeometry(700, 100, 1300, 1200)
        self.random_numbers = numeros
        self.k_intervalos = k_intervalos
        self.media = media
        self.sigma = sigma
        self.agrupada_window = None

        layout = QVBoxLayout(self)

        # Crear la primera tabla
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Calcular el test de chi-cuadrado y mostrar los resultados en las tablas
        self.datos_tabla = self.calcular_chi_cuadrado(numeros, k_intervalos)
        self.mostrar_resultados_en_tabla(self.datos_tabla)

        # Crear el botón para mostrar la tabla agrupada
        self.agrupada_button = QPushButton("Mostrar Tabla Agrupada")
        self.agrupada_button.clicked.connect(self.mostrar_tabla_agrupada)
        layout.addWidget(self.agrupada_button)

        layout.addWidget(self.agrupada_button)

        # Mostrar la suma de la columna de Chi cuadrado y el Chi tabulado
        chi_cuadrado_suma = sum(row[5] for row in self.datos_tabla)
        chi_tabulado = chi2.isf(0.1, self.k_intervalos - 1)

        input_layout = QHBoxLayout()

        # Formatear los valores de Chi calculado y Chi tabulado para que tengan 4 decimales
        chi_cuadrado_suma_formatted = "{:.4f}".format(chi_cuadrado_suma)
        chi_tabulado_formatted = "{:.4f}".format(chi_tabulado)

        # Crear un QLabel para mostrar los valores formateados
        chi_calculado_label = QLabel("Chi calculado: " + chi_cuadrado_suma_formatted)
        input_layout.addWidget(chi_calculado_label)
        chi_calculado_label.setFont(QFont("Arial", 14))
        layout.addWidget(chi_calculado_label)

        chi_tabulado_label = QLabel("Chi tabulado: " + chi_tabulado_formatted)
        input_layout.addWidget(chi_tabulado_label)
        chi_tabulado_label.setFont(QFont("Arial", 14))
        layout.addWidget(chi_tabulado_label)

        # Calcular la condición de aceptación de la hipótesis nula
        aceptada = "La Hipótesis nula se ACEPTA" if chi_cuadrado_suma < chi_tabulado else "La Hipótesis nula se RECHAZA"

        # Crear un QLabel para mostrar el resultado
        aceptada_label = QLabel("Resultado de la prueba: " + aceptada)
        input_layout.addWidget(aceptada_label)
        aceptada_label.setFont(QFont("Arial", 14))
        layout.addWidget(aceptada_label)

    def calcular_chi_cuadrado(self, random_numbers, k_intervalos):
        # Calcular los límites de los intervalos
        min_value = min(random_numbers)
        max_value = max(random_numbers)
        interval_length = (max_value - min_value) / k_intervalos
        limites_inferiores = [min_value + i * interval_length for i in range(k_intervalos)]
        limites_superiores = [limite_inf + interval_length for limite_inf in limites_inferiores]

        # Calcular las frecuencias observadas
        frecuencias_observadas, _ = np.histogram(random_numbers, bins=k_intervalos, range=(min_value, max_value))
        # Calculamos la media y la desviación estándar de los números aleatorios
        mu, sigma = np.mean(random_numbers), np.std(random_numbers)
        
        
        # Calculamos la frecuencia esperada para una distribución normal
        frecuencias_esperadas = [len(random_numbers) * (norm.cdf(limites_superiores[i], mu, sigma) - norm.cdf(limites_inferiores[i], mu, sigma)) for i in range(k_intervalos)]
        # Calcular las frecuencias esperadas

        # Preparar los datos para mostrar en una tabla
        datos_tabla = []
        for i in range(k_intervalos):
            datos_tabla.append([i+1, limites_inferiores[i], limites_superiores[i], frecuencias_observadas[i],
                                frecuencias_esperadas[i], ((frecuencias_observadas[i] - frecuencias_esperadas[i])
                                                           ** 2) / frecuencias_esperadas[i]])

        return datos_tabla
    
    def agrupar_intervalos3(self, datos_tabla):
        # Inicializar el vector de resultados
        datos_tabla_agrupados = []
        
        # Inicializar variables para almacenar los datos del intervalo actual
        intervalo_actual = None
        frecuencia_observada_actual = 0
        frecuencia_esperada_actual = 0
        
        # Recorrer cada fila en los datos de la tabla
        for fila in datos_tabla:
            # Si la frecuencia esperada del intervalo actual es mayor a 5 o si es el primer intervalo
            if frecuencia_esperada_actual > 5 or intervalo_actual is None:
                # Agregar el intervalo actual al vector de resultados
                if intervalo_actual is not None:
                    datos_tabla_agrupados.append([intervalo_actual, limite_inferior_actual, limite_superior_actual, 
                                                frecuencia_observada_actual, frecuencia_esperada_actual, 
                                                ((frecuencia_observada_actual - frecuencia_esperada_actual) ** 2) / frecuencia_esperada_actual])
                
                # Iniciar un nuevo intervalo con los datos de la fila actual
                intervalo_actual, limite_inferior_actual, limite_superior_actual, frecuencia_observada_actual, frecuencia_esperada_actual = fila[0], fila[1], fila[2], fila[3], fila[4]
            else:
                # Si la frecuencia esperada del intervalo actual es menor o igual a 5, agregar los datos de la fila actual al intervalo actual
                intervalo_actual = f"{intervalo_actual}-{fila[0]}"
                limite_superior_actual = fila[2]
                frecuencia_observada_actual += fila[3]
                frecuencia_esperada_actual += fila[4]
        
        # Si la frecuencia esperada del último intervalo es menor o igual a 5
        if frecuencia_esperada_actual <= 5 and len(datos_tabla_agrupados) > 0:
            # Agregar los datos del último intervalo al penúltimo intervalo
            datos_tabla_agrupados[-1][0] = f"{datos_tabla_agrupados[-1][0]}-{intervalo_actual}"
            datos_tabla_agrupados[-1][2] = limite_superior_actual
            datos_tabla_agrupados[-1][3] += frecuencia_observada_actual
            datos_tabla_agrupados[-1][4] += frecuencia_esperada_actual
            datos_tabla_agrupados[-1][5] = ((datos_tabla_agrupados[-1][3] - datos_tabla_agrupados[-1][4]) ** 2) / datos_tabla_agrupados[-1][4]
        else:
            # Agregar el último intervalo al vector de resultados
            datos_tabla_agrupados.append([intervalo_actual, limite_inferior_actual, limite_superior_actual, 
                                        frecuencia_observada_actual, frecuencia_esperada_actual, 
                                        ((frecuencia_observada_actual - frecuencia_esperada_actual) ** 2) / frecuencia_esperada_actual])
        
        # Devolver el vector de resultados
        return datos_tabla_agrupados


                    

                



    def mostrar_resultados_en_tabla(self, datos_tabla):
        self.table.setRowCount(len(datos_tabla))
        self.table.setColumnCount(len(datos_tabla[0]))
        self.table.setHorizontalHeaderLabels(["Intervalos", "Límite Inferior", "Límite Superior",
                                              "Fr. Observada", "Fr. Esperada", "Chi^2"])
        for i, row in enumerate(datos_tabla):
            for j, value in enumerate(row):
                # Formatear los números con cuatro decimales
                formatted_value = "{:.4f}".format(value) if isinstance(value, float) else str(value)
                item = QTableWidgetItem(formatted_value)
                self.table.setItem(i, j, item)
        self.histogram_window = HistogramWindow(self.random_numbers, self.k_intervalos)
        # Mostrar el HistogramWindow
        self.histogram_window.show()

    def mostrar_tabla_agrupada(self):
        # Crear y mostrar la ventana de ChiExpWindow para la tabla agrupada
        self.agrupada_window = NormWindowAgrupada(self.agrupar_intervalos3(self.datos_tabla))
        self.agrupada_window.show()
        

class NormWindowAgrupada(QWidget):
    def __init__(self, datos_tabla_agrupada, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Test de Chi-cuadrado (Tabla Agrupada)")
        self.setGeometry(100, 100, 1300, 1200)

        layout = QVBoxLayout(self)

        # Crear la tabla para mostrar los datos agrupados
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Mostrar los resultados en la tabla agrupada
        self.mostrar_resultados_en_tabla2(datos_tabla_agrupada)


        k_intervalos = len(datos_tabla_agrupada)

        # Calcular la suma de la columna de Chi cuadrado
        chi_cuadrado_suma = sum(row[5] for row in datos_tabla_agrupada)

        # Calcular el valor crítico de chi-cuadrado
        chi_tabulado = chi2.isf(0.1, k_intervalos - 1)

        # df.count(axis=1) --> df es la tabla de dónde sacamos los datos, axis es la columna
        # De esta manera, logro contar las filas de la tabla agrupada lo cuál serían los k_intervalos

        input_layout = QHBoxLayout()

        # Formatear los valores de Chi calculado y Chi tabulado para que tengan 4 decimales
        chi_cuadrado_suma_formatted = "{:.4f}".format(chi_cuadrado_suma)
        chi_tabulado_formatted = "{:.4f}".format(chi_tabulado)

        # Crear un QLabel para mostrar los valores formateados
        chi_calculado_label = QLabel("Chi calculado: " + chi_cuadrado_suma_formatted)
        input_layout.addWidget(chi_calculado_label)
        chi_calculado_label.setFont(QFont("Arial", 14))
        layout.addWidget(chi_calculado_label)

        chi_tabulado_label = QLabel("Chi tabulado: " + chi_tabulado_formatted)
        input_layout.addWidget(chi_tabulado_label)
        chi_tabulado_label.setFont(QFont("Arial", 14))
        layout.addWidget(chi_tabulado_label)

        # Calcular la condición de aceptación de la hipótesis nula
        aceptada = "La Hipótesis nula se ACEPTA" if chi_cuadrado_suma < chi_tabulado else "La Hipótesis nula se RECHAZA"

        # Crear un QLabel para mostrar el resultado
        aceptada_label = QLabel("Resultado de la prueba: " + aceptada)
        input_layout.addWidget(aceptada_label)
        aceptada_label.setFont(QFont("Arial", 14))
        layout.addWidget(aceptada_label)

    def contador_intervalos_agrupada(self, datos_tabla_agrupada):
        contador = 0

        for i in datos_tabla_agrupada:
            contador += datos_tabla_agrupada[i]

        return contador
    
    def mostrar_resultados_en_tabla2(self, datos_tabla):
        self.table.setRowCount(len(datos_tabla))
        self.table.setColumnCount(len(datos_tabla[0]))
        self.table.setHorizontalHeaderLabels(["Intervalos", "Límite Inferior", "Límite Superior",
                                              "Fr. Observada", "Fr. Esperada", "Chi^2"])
        for i, row in enumerate(datos_tabla):
            for j, value in enumerate(row):
                # Formatear los números con cuatro decimales
                formatted_value = "{:.4f}".format(value) if isinstance(value, float) else str(value)
                item = QTableWidgetItem(formatted_value)
                self.table.setItem(i, j, item)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NormWindow([0.1, 0.2, 0.3, 0.4, 0.5], 5, 5)
    window.show()
    sys.exit(app.exec_())
