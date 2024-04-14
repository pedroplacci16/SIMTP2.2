import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QMessageBox, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import random
import openpyxl
import tempfile
import os
from histograma import HistogramWindow
from uniforme import UniformWindow
from exponencial import ExponentialWindow
from normal import NormalWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar tamaño de la ventana
        self.resize(700, 500)  # Tamaño personalizado

        # Configurar layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Parte superior: Texto "RANDOM NUMBERS"
        random_numbers_label = QLabel("RANDOM NUMBERS")
        random_numbers_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        random_numbers_label.setFont(QFont("Haettenschweiler", 24))
        layout.addWidget(random_numbers_label)

        # Añadir línea negra debajo del título "RANDOM NUMBERS"
        line_top = QFrame()
        line_top.setFrameShape(QFrame.HLine)
        line_top.setFrameShadow(QFrame.Sunken)
        line_top.setStyleSheet(
            "color: black")  # Añadir un margen inferior para separar del siguiente elemento
        layout.addWidget(line_top)

        # Crear un layout horizontal para la entrada de la cantidad y los intervalos
        input_layout = QHBoxLayout()

        cantidad_label = QLabel("Cantidad:")
        input_layout.addWidget(cantidad_label)

        self.cantidad_entry = QLineEdit()
        input_layout.addWidget(self.cantidad_entry)

        k_intervalos_label = QLabel("K-Intervalos:")
        input_layout.addWidget(k_intervalos_label)

        self.k_intervalos_entry = QLineEdit()
        input_layout.addWidget(self.k_intervalos_entry)

        layout.addLayout(input_layout)

        # Botones para seleccionar la distribución
        uniform_button = QPushButton("Uniforme")
        uniform_button.clicked.connect(self.open_uniform_window)

        exponential_button = QPushButton("Exponencial")
        exponential_button.clicked.connect(self.open_exponential_window)

        normal_button = QPushButton("Normal")
        normal_button.clicked.connect(self.open_normal_window)

        button_layout = QHBoxLayout()
        button_layout.addWidget(uniform_button)
        button_layout.addWidget(exponential_button)
        button_layout.addWidget(normal_button)
        layout.addLayout(button_layout)

        self.setWindowTitle("Generador de números aleatorios")

        # Inicializar variables para almacenar los números aleatorios y los intervalos
        self.numeros_generados = []
        self.k_intervalos = 0

    def generar_numeros_aleatorios(self, cantidad):
        self.numeros_generados = []
        for _ in range(cantidad):
            numero = round(random.random(), 4)
            self.numeros_generados.append(numero)

    def guardar_excel(self):
        # Crear archivo Excel
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "Numeros Aleatorios"

        for i, numero in enumerate(self.numeros_generados, start=1):
            sheet.cell(row=i, column=1, value=numero)

        # Guardar archivo Excel como archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
            temp_filename = temp_file.name
            wb.save(temp_filename)

        # Abrir el archivo temporal en el sistema
        os.startfile(temp_filename)

    def generar_aleatorios(self):
        cantidad = self.cantidad_entry.text()
        k_intervalos = self.k_intervalos_entry.text()
        if not cantidad or not k_intervalos:
            QMessageBox.critical(self, "Error", "Por favor, complete todos los campos.")
            return
        try:
            cantidad = int(cantidad)
            self.k_intervalos = int(k_intervalos)

            if cantidad <= 0:
                QMessageBox.critical(self, "Error", "Por favor ingrese un número positivo mayor que 0.")
                return

            if self.k_intervalos not in [10, 15, 20, 25]:
                QMessageBox.critical(self, "Error",
                                     "Por favor ingrese uno de los siguientes K-intervalos: 10, 15, 20, 25.")
                return

            if cantidad > 1000000:
                QMessageBox.critical(self, "Error", "El límite máximo es de un millón de números aleatorios.")
                return

            self.generar_numeros_aleatorios(cantidad)
            self.guardar_excel()
            self.close()  # Cerrar la ventana principal
            self.open_histogram_window()  # Abrir la ventana del histograma

        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor, ingrese un número válido.")

    def open_histogram_window(self):
        self.histogram_window = HistogramWindow(self.numeros_generados, self.k_intervalos)
        self.histogram_window.show()

    def open_uniform_window(self):
        self.uniform_window = UniformWindow(parent=self)
        self.uniform_window.valuesConfirmed.connect(self.handle_uniform_values)
        self.uniform_window.show()

    def open_exponential_window(self):
        self.exponential_window = ExponentialWindow()
        self.exponential_window.show()

    def open_normal_window(self):
        self.normal_window = NormalWindow()
        self.normal_window.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()