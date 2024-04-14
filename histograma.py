import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel, QPushButton, \
    QHBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from uniforme import UniformWindow
from exponencial import ExponentialWindow
from normal import NormalWindow

class HistogramWindow(QWidget):
    def __init__(self, numeros, k_intervalos):
        super().__init__()
        self.setWindowTitle("Histograma y Distribuciones")
        self.setGeometry(800, 50, 1000, 1200)

        self.numeros = numeros
        self.k_intervalos = k_intervalos

        layout = QVBoxLayout(self)

        # Crear el canvas para el histograma
        self.figure_hist = Figure(figsize=(10, 6))
        self.canvas_hist = FigureCanvas(self.figure_hist)
        layout.addWidget(self.canvas_hist)

        # Agregar un título debajo del histograma
        title_label = QLabel("¿Cuál será la distribución de probabilidad más apropiada?")
        layout.addWidget(title_label)

        # Plot de la distribución uniforme
        self.figure_uniform = Figure()
        self.canvas_uniform = FigureCanvas(self.figure_uniform)
        layout.addWidget(self.canvas_uniform)

        # Plot de la distribución exponencial
        self.figure_exponential = Figure()
        self.canvas_exponential = FigureCanvas(self.figure_exponential)
        layout.addWidget(self.canvas_exponential)

        # Plot de la distribución normal
        self.figure_normal = Figure()
        self.canvas_normal = FigureCanvas(self.figure_normal)
        layout.addWidget(self.canvas_normal)

        # Agregar un espaciador al final del layout
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

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

        # Actualizar los gráficos
        self.update_plots()

    def update_plots(self):
        self.plot_histogram()
        self.plot_uniform_distribution()
        self.plot_exponential_distribution()
        self.plot_normal_distribution()

    def plot_histogram(self):
        ax = self.figure_hist.add_subplot(111)
        ax.hist(self.numeros, bins=self.k_intervalos, color='skyblue', edgecolor='black')
        ax.set_xlabel('Valor')
        ax.set_ylabel('Frecuencia')
        ax.set_title('Histograma de Números Aleatorios')
        ax.grid(True)
        self.canvas_hist.draw()

    def plot_uniform_distribution(self):
        ax = self.figure_uniform.add_subplot(111)
        x = np.linspace(0, 1, 100)
        y = np.ones_like(x)
        ax.plot(x, y, color='green')
        ax.set_xlabel('Valor')
        ax.set_ylabel('Densidad de probabilidad')
        ax.set_title('Distribución Uniforme')
        ax.grid(True)
        self.canvas_uniform.draw()

    def plot_exponential_distribution(self):
        ax = self.figure_exponential.add_subplot(111)
        x = np.linspace(0, 5, 100)
        y = np.exp(-x)
        ax.plot(x, y, color='orange')
        ax.set_xlabel('Valor')
        ax.set_ylabel('Densidad de probabilidad')
        ax.set_title('Distribución Exponencial')
        ax.grid(True)
        self.canvas_exponential.draw()

    def plot_normal_distribution(self):
        ax = self.figure_normal.add_subplot(111)
        x = np.linspace(-3, 3, 100)
        y = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x ** 2)
        ax.plot(x, y, color='purple')
        ax.set_xlabel('Valor')
        ax.set_ylabel('Densidad de probabilidad')
        ax.set_title('Distribución Normal')
        ax.grid(True)
        self.canvas_normal.draw()

    def close_histogram_window(self):
        self.close()

    def open_uniform_window(self):
        self.close_histogram_window()
        self.uniform_window = UniformWindow(self.numeros, self.k_intervalos, parent=self)
        self.uniform_window.valuesConfirmed.connect(self.handle_uniform_values)
        self.uniform_window.show()

    def open_exponential_window(self):
        try:
            self.close_histogram_window()
            self.exponential_window = ExponentialWindow(self.numeros, self.k_intervalos)
            self.exponential_window.show()
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Ha ocurrido un error al abrir la ventana exponencial: {str(e)}")

    def open_normal_window(self):
        self.close_histogram_window()
        self.normal_window = NormalWindow(self.numeros, self.k_intervalos)
        self.normal_window.show()

    def handle_uniform_values(self, a, b):
        # Aquí puedes utilizar los valores de A y B para realizar las pruebas de bondad de ajuste
        QMessageBox.information(self, "Valores de Uniforme", f"A: {a}, B: {b}")

    def handle_exponential_values(self, lambda_value):
        try:
            QMessageBox.information(self, "Valores Exponenciales",
                                    f"Valor de lambda: {lambda_value}")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Ha ocurrido un error al manejar los valores exponenciales: {str(e)}")


def main():
    try:
        app = QApplication(sys.argv)
        window = HistogramWindow([0.1, 0.2, 0.3, 0.4, 0.5], 5)
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Ha ocurrido un error: {str(e)}")

if __name__ == "__main__":
    main()
