import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QApplication, QLabel, \
    QHBoxLayout, QPushButton, QMessageBox
import numpy as np
from scipy.stats import chi2, expon


class ChiExpWindow(QWidget):
    def __init__(self, numeros, k_intervalos, lambdae, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Test de Chi-cuadrado")
        self.setGeometry(700, 100, 1300, 1200)
        self.numeros = numeros
        self.k_intervalos = k_intervalos
        self.lambdae = lambdae
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

    def calcular_chi_cuadrado(self, numeros, k_intervalos):
        # Calcular los límites de los intervalos
        min_value = min(numeros)
        max_value = max(numeros)
        interval_length = (max_value - min_value) / k_intervalos
        limites_inferiores = [min_value + i * interval_length for i in range(k_intervalos)]
        limites_superiores = [limite_inf + interval_length for limite_inf in limites_inferiores]

        # Calcular las frecuencias observadas
        frecuencias_observadas, _ = np.histogram(numeros, bins=k_intervalos, range=(min_value, max_value))

        # Calcular las frecuencias esperadas
        frecuencias_esperadas = []
        for i in range(k_intervalos):
            frecuencia_inf = expon.cdf(limites_inferiores[i], scale=1 / self.lambdae)
            frecuencia_sup = expon.cdf(limites_superiores[i], scale=1 / self.lambdae)
            frecuencia_esperada = (frecuencia_sup - frecuencia_inf) * len(numeros)
            frecuencias_esperadas.append(frecuencia_esperada)

        # Preparar los datos para mostrar en una tabla
        datos_tabla = []
        for i in range(k_intervalos):
            datos_tabla.append([i+1, limites_inferiores[i], limites_superiores[i], frecuencias_observadas[i],
                                frecuencias_esperadas[i], ((frecuencias_observadas[i] - frecuencias_esperadas[i])
                                                           ** 2) / frecuencias_esperadas[i]])

        return datos_tabla

    def agrupar_intervalos(self, datos_tabla_original):
        datos_tabla_agrupada = []
        frecuencias_esp_acumulada = 0
        frecuencias_obs_acumulada = 0
        intervalo_agrupado = None

        for fila in datos_tabla_original:
            intervalo, limite_inferior, limite_superior, frecuencia_obs, frecuencia_esp, chi_cuadrado = fila

            if frecuencia_esp < 5:
                if intervalo_agrupado is None:
                    intervalo_agrupado = intervalo

                frecuencias_obs_acumulada += frecuencia_obs
                frecuencias_esp_acumulada += frecuencia_esp
            else:
                if intervalo_agrupado is not None:
                    chi_cuadrado_calculado = ((frecuencias_obs_acumulada - frecuencias_esp_acumulada) ** 2) / frecuencias_esp_acumulada
                    datos_tabla_agrupada.append([f"{intervalo_agrupado}-{intervalo}",
                                                 frecuencias_obs_acumulada, frecuencias_esp_acumulada, chi_cuadrado_calculado])
                    intervalo_agrupado = None
                    frecuencias_esp_acumulada = 0
                    frecuencias_obs_acumulada = 0

                # Calcular el chi cuadrado para el intervalo no agrupado
                chi_cuadrado_calculado = ((frecuencia_obs - frecuencia_esp) ** 2) / frecuencia_esp
                datos_tabla_agrupada.append([intervalo, frecuencia_obs, frecuencia_esp, chi_cuadrado_calculado])

        # Si quedan intervalos agrupados al final, agregarlos
        if intervalo_agrupado is not None:
            # Calcular el chi cuadrado para el intervalo agrupado final
            chi_cuadrado_calculado = ((frecuencias_obs_acumulada - frecuencias_esp_acumulada) ** 2) / frecuencias_esp_acumulada
            datos_tabla_agrupada.append([f"{intervalo_agrupado}-{intervalo}",
                                         frecuencias_obs_acumulada, frecuencias_esp_acumulada, chi_cuadrado_calculado])


        return datos_tabla_agrupada

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

    def mostrar_tabla_agrupada(self):
        # Crear y mostrar la ventana de ChiExpWindow para la tabla agrupada
        self.agrupada_window = ChiExpWindowAgrupada(self.agrupar_intervalos(self.datos_tabla))
        self.agrupada_window.show()

class ChiExpWindowAgrupada(QWidget):
    def __init__(self, datos_tabla_agrupada, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Test de Chi-cuadrado (Tabla Agrupada)")
        self.setGeometry(100, 100, 1300, 1200)

        layout = QVBoxLayout(self)

        # Crear la tabla para mostrar los datos agrupados
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Mostrar los resultados en la tabla agrupada
        self.mostrar_resultados_en_tabla(datos_tabla_agrupada)


        k_intervalos = len(datos_tabla_agrupada)

        # Calcular la suma de la columna de Chi cuadrado
        chi_cuadrado_suma = sum(row[3] for row in datos_tabla_agrupada)

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

    def mostrar_resultados_en_tabla(self, datos_tabla):
        self.table.setRowCount(len(datos_tabla))
        self.table.setColumnCount(len(datos_tabla[0]))
        self.table.setHorizontalHeaderLabels(["Intervalos", "Fr. Observada", "Fr. Esperada", "Chi^2"])

        for i, row in enumerate(datos_tabla):
            for j, value in enumerate(row):
                # Formatear los números con cuatro decimales
                formatted_value = "{:.4f}".format(value) if isinstance(value, float) else str(value)
                item = QTableWidgetItem(formatted_value)
                self.table.setItem(i, j, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChiExpWindow([0.1, 0.2, 0.3, 0.4, 0.5], 5, 5)
    window.show()
    sys.exit(app.exec_())
