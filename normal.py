from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QMessageBox
import numpy as np
from histogramador import HistogramWindow
from tablaNormal2 import NormWindow
from PyQt5.QtWidgets import QApplication
import sys
import pandas as pd
import os

class NormalWindow(QWidget):
    def __init__(self, numeros, k_intervalos):
        super().__init__()
        self.numeros = numeros
        self.k_intervalos = k_intervalos

        self.setWindowTitle("Distribución Normal")

        layout = QVBoxLayout()

        self.mean_label = QLabel("Ingrese el valor de la media:")
        layout.addWidget(self.mean_label)

        self.mean_entry = QLineEdit()
        layout.addWidget(self.mean_entry)

        self.variance_label = QLabel("Ingrese el valor de la varianza:")
        layout.addWidget(self.variance_label)

        self.variance_entry = QLineEdit()
        layout.addWidget(self.variance_entry)

        self.confirm_button = QPushButton("Confirmar")
        self.confirm_button.clicked.connect(self.confirm_parameters)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def box_muller_transform(self, u, mu, sigma):
        # Inicializa un vector vacío para almacenar los números generados
        z = np.empty(len(u))

        for i in range(0, len(u), 2):
            # Aplica la transformación de Box-Muller a cada par de elementos
            R = np.sqrt(-2.0 * np.log(u[i]))
            theta = 2.0 * np.pi * u[i+1] if i+1 < len(u) else 2.0 * np.pi * np.random.uniform(0, 1)
            z[i] = R * np.cos(theta)
            if i+1 < len(u):
                z[i+1] = R * np.sin(theta)

        # Ajusta los números generados a la media y la varianza deseadas
        z = mu + z*sigma


        return z
    
    def box_muller_transform2(self, u, mu, sigma):
        # Inicializa un vector vacío para almacenar los números generados, pero comprueba
        # que el tamaño del vector sea par, ya que necesitamos siempre dos numeros para generar
        # otros dos, por lo tanto si sobra un numero se lo desprecia
        longitud = len(u)
        if longitud % 2 == 0: 
            z = np.empty(longitud)
        else:
            z = np.empty(longitud-1)

        #Usamos un for que vaya de 2 en 2 para tomar de a dos numeros en el vector, por eso es el 2 del final del range
        # Tambien usamos la longitud del vector vacio z, ya que debe ser par
        for i in range(0, len(z), 2):
            # Aplica la transformación de Box-Muller a cada par de elementos
            # Tenemos que aplicar la formula para convertir el vector de numeros random
            # Con la funcion max nos aseguramos que nunca aparezca un 0 que haga fallar al programa
            z[i] = round((np.sqrt((-2)*np.log(max(u[i], 0.0001)))*np.cos(2*np.pi*u[i+1]))*sigma+mu, 4)
            z[i+1] = round((np.sqrt((-2)*np.log(max(u[i], 0.0001)))*np.sin(2*np.pi*u[i+1]))*sigma+mu, 4)
        
        # Esto lo imprime por consola para verificar si no tomamos el ultimo valor en caso de ser impar
        print(len(u), len(z))
        return z
    
    def crear_excel(self, vector):
        # Crear un DataFrame con el vector
        df = pd.DataFrame(vector, columns=['Numeros Aleatorios Normales'])
    
        # Crear un archivo Excel temporal
        df.to_excel('temporal.xlsx', index=False)

        os.system('start temporal.xlsx')


    def confirm_parameters(self):
        mean_value = self.mean_entry.text()
        variance_value = self.variance_entry.text()
        try:
            mean_value = float(mean_value)
            variance_value = float(variance_value)
            if variance_value <= 0:
                QMessageBox.critical(self, "Error", "La varianza debe ser mayor que 0.")
            elif mean_value < 0:
                QMessageBox.critical(self, "Error", "La media debe ser mayor o igual que 0.")
            else:
                QMessageBox.information(self, "Éxito", f"Valores aceptados: Media={mean_value}, Varianza={variance_value}")
                # Aquí puedes realizar cualquier acción adicional que desees con la media y la varianza
                normales = self.box_muller_transform2(self.numeros, mean_value, variance_value)
                print(normales)
                if np.isinf(normales).any():
                    print("El vector contiene al menos un valor infinito")
                else:
                    print("El vector no contiene valores infinitos")
                # Create an instance of App (the class that contains the table)
                self.table_window = NormWindow(normales, self.k_intervalos, mean_value, variance_value)

                # Show the App window
                self.table_window.show()

                self.crear_excel(normales)

        except ValueError as e:
            QMessageBox.critical(self, "Error", "Por favor, ingrese valores numéricos para la media y la varianza.")
            print(e)
