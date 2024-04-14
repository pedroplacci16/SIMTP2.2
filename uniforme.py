import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QMainWindow, QApplication
from PyQt5.QtCore import pyqtSignal
from test_chi2_uniforme import ChiSquareWindow

class UniformWindow(QMainWindow):
    valuesConfirmed = pyqtSignal(float, float, list)

    def __init__(self, numeros, k_intervalos, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Distribución Uniforme")
        self.setGeometry(800, 50, 500, 200)
        self.numeros = numeros
        self.k_intervalos = k_intervalos
        self.test_chi_cuadrado = None

        # Creamos un widget central y un layout vertical
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Etiquetas y campos de entrada para A y B
        label_a = QLabel("Valor de A:")
        self.input_a = QLineEdit()
        layout.addWidget(label_a)
        layout.addWidget(self.input_a)

        label_b = QLabel("Valor de B:")
        self.input_b = QLineEdit()
        layout.addWidget(label_b)
        layout.addWidget(self.input_b)

        # Botón para confirmar valores
        confirm_button = QPushButton("Confirmar")
        confirm_button.clicked.connect(self.confirm_values)
        layout.addWidget(confirm_button)

    def confirm_values(self):
        a = self.input_a.text()
        b = self.input_b.text()

        try:
            a = float(a)
            b = float(b)

            if b <= a:
                raise ValueError("El valor de B debe ser mayor que el valor de A.")

            # Utilizar los números generados previamente en la fórmula A + RND(B - A)
            numeros_uniformes = [a + numero * (b - a) for numero in self.numeros]

            # Emitir la señal con los valores de A y B
            self.valuesConfirmed.emit(a, b, numeros_uniformes)

            # Crear y mostrar la ventana de ChiSquareWindow
            self.test_chi_cuadrado = ChiSquareWindow(numeros_uniformes, self.k_intervalos)
            self.test_chi_cuadrado.show()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            print("Error:", e)  # Mensaje de depuración para imprimir la excepción

if __name__ == "__main__":
    # Datos de ejemplo
    numeros = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    k_intervalos = 4

    app = QApplication(sys.argv)
    window = UniformWindow(numeros, k_intervalos)
    window.show()
    sys.exit(app.exec_())