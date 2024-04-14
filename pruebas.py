import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QMessageBox, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import random
import openpyxl
import tempfile
import os
from histograma import HistogramWindow

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

        buttons_layout = QHBoxLayout()

        self.generar_button = QPushButton("Generar")
        buttons_layout.addWidget(self.generar_button)

        self.cancelar_button = QPushButton("Cancelar")
        buttons_layout.addWidget(self.cancelar_button)

        layout.addLayout(buttons_layout)

        # Conectar botón a la función de generación de números aleatorios
        self.generar_button.clicked.connect(self.generar_aleatorios)

        # Habilitar generación al presionar la tecla Enter
        self.cantidad_entry.returnPressed.connect(self.generar_aleatorios)

        self.cancelar_button.clicked.connect(self.close)

        self.setWindowTitle("Generador de números aleatorios")

        # Inicializar variables para almacenar los números aleatorios y los intervalos
        self.numeros_generados = []
        self.k_intervalos = 0

    def generar_numeros_aleatorios(self, cantidad):
        self.numeros_generados = []
        while len(self.numeros_generados) < cantidad:
            numero = round(random.uniform(0, 1), 4)
            if 0 < numero < 1:
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


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()