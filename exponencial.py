import math
import os
import sys
import tempfile

import openpyxl

from test_chi2_exponencial import ChiExpWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QMessageBox, QApplication


class ExponentialWindow(QWidget):
    valuesConfirmed = pyqtSignal(float, list)

    def __init__(self, numeros, k_intervalos, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Distribución Exponencial")
        self.numeros = numeros
        self.k_intervalos = k_intervalos
        self.test_chi_cuadrado = None

        layout = QVBoxLayout()

        self.lambda_label = QLabel("Ingrese el valor de lambda:")
        layout.addWidget(self.lambda_label)

        self.lambda_entry = QLineEdit()
        layout.addWidget(self.lambda_entry)

        self.confirm_button = QPushButton("Confirmar")
        self.confirm_button.clicked.connect(self.confirm_lambda)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def redondear_a_4_decimales(self, numero):
        return round(numero, 4)

    def confirm_lambda(self):
        lambda_value = self.lambda_entry.text().strip()
        lambda_value = int(lambda_value)
        if lambda_value <= 0:
            QMessageBox.critical(self, "Error", "El valor de lambda debe ser mayor que 0.")
        else:
            QMessageBox.information(self, "Éxito", f"Valor de lambda aceptado: {lambda_value}")

        numeros_exponenciales = [self.redondear_a_4_decimales(-(1/lambda_value) * math.log(1 - rnd)) for rnd in self.numeros]

        self.guardar_excel(numeros_exponenciales)

        # Emitir la señal con los valores de lambda y los números exponenciales
        self.valuesConfirmed.emit(lambda_value, numeros_exponenciales)

        # Crear y mostrar la ventana de ChiExpWindow
        self.test_chi_cuadrado = ChiExpWindow(numeros_exponenciales, self.k_intervalos, lambda_value)
        self.test_chi_cuadrado.show()

    def guardar_excel(self, numeros):
        # Crear archivo Excel
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "Numeros Aleatorios"

        for i, numero in enumerate(numeros, start=1):
            sheet.cell(row=i, column=1, value=numero)

        # Guardar archivo Excel como archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
            temp_filename = temp_file.name
            wb.save(temp_filename)

        # Abrir el archivo temporal en el sistema
        os.startfile(temp_filename)

if __name__ == "__main__":
    # Datos de ejemplo
    numeros = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    k_intervalos = 4

    app = QApplication(sys.argv)
    window = ExponentialWindow(numeros, k_intervalos)
    window.show()
    sys.exit(app.exec_())
