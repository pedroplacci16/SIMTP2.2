import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QApplication, QLabel, \
    QHBoxLayout
import numpy as np
from scipy.stats import chi2


class ChiSquareWindow(QWidget):
    def __init__(self, numeros, k_intervalos, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Test de Chi-cuadrado")
        self.setGeometry(700, 100, 1300, 1200)
        self.numeros = numeros
        self.k_intervalos = k_intervalos

        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Calcular el test de chi-cuadrado y mostrar los resultados en la tabla
        datos_tabla = self.calcular_chi_cuadrado(numeros, k_intervalos)
        self.mostrar_resultados_en_tabla(datos_tabla)

        # Mostrar la suma de la columna de Chi cuadrado y el Chi tabulado
        chi_cuadrado_suma = sum(row[5] for row in datos_tabla)
        chi_tabulado = chi2.ppf(0.1, self.k_intervalos - 1)

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

        # Calcular el estadístico de chi-cuadrado
        frecuencias_esperadas = [len(numeros) / k_intervalos] * k_intervalos

        # Preparar los datos para mostrar en una tabla
        datos_tabla = []
        for i in range(k_intervalos):
            datos_tabla.append([i+1, limites_inferiores[i], limites_superiores[i], frecuencias_observadas[i],
                                frecuencias_esperadas[i], ((frecuencias_observadas[i] - frecuencias_esperadas[i])
                                                           ** 2) / frecuencias_esperadas[i]])

        return datos_tabla

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChiSquareWindow([0.1, 0.2, 0.3, 0.4, 0.5], 5)
    window.show()
    sys.exit(app.exec_())
