from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Predecir el precio de vivienda según la superficie en metros cuadrados 
# Datos de entrenamiento (X) y etiquetas (y)

x = np.array([[40], [50], [60], [85], [100], [120]])
y = np.array([210000000, 300000000, 350000000, 500000000, 600000000, 700000000])

# Entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(x, y)


# # predicciones de prueba
# y_pred = model.predict(x)

# # Imprimir la información del modelo entrenado
# print("Coeficiente de regresión:", model.coef_[0])
# print("Término independiente:", model.intercept_)

# #Graficar los datos reales
# plt.scatter(x, y, color='red', label='Datos reales')

# # Graficar los datos de entrenamiento y la línea de regresión
# plt.plot(x, y_pred, color='blue', label='Datos de entrenamiento')

# plt.xlabel('Superficie (m²)')
# plt.ylabel('Precio de vivienda (COP)')
# plt.title('Regresión Lineal: Precio de vivienda vs Superficie')
# plt.legend()
# plt.grid(True)

# #Imprimir la gráfica
# plt.show()


# Guardar el artefacto del modelo entrenado en un archivo
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "linear_model.joblib"

joblib.dump(model, MODEL_PATH)