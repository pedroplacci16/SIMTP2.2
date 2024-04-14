from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class HistogramWindow(QWidget):
    def __init__(self, numeros, k_intervalos):
        super().__init__()
        self.setWindowTitle("Histograma")
        self.setGeometry(800, 50, 1000, 600)

        self.numeros = numeros
        self.k_intervalos = k_intervalos

        layout = QVBoxLayout(self)

        # Crear el canvas para el histograma
        self.figure_hist = Figure(figsize=(10, 6))
        self.canvas_hist = FigureCanvas(self.figure_hist)
        layout.addWidget(self.canvas_hist)


        # Actualizar los gráficos
        self.update_plots()
    

    def update_plots(self):
        self.plot_histogram()

    def plot_histogram(self):
        ax = self.figure_hist.add_subplot(111)
        ax.hist(self.numeros, bins=self.k_intervalos, color='skyblue', edgecolor='black')
        ax.set_xlabel('Valor')
        ax.set_ylabel('Frecuencia')
        ax.set_title('Histograma de Números Aleatorios')
        ax.grid(True)
        self.canvas_hist.draw()
