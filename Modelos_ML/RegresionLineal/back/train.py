import joblib
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Predecir precios de viviendas según la superficie en m2

# Datos de entrenamiento (X) y etiquetas (y)
x = np.array([[40], [50], [60], [90], [100], [120]])
y = np.array([210000000, 300000000, 350000000, 500000000, 600000000, 700000000])

# Entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(x, y)

# # predicciones de prueba
# y_pred = model.predict(x)

# #imprimir la información del modelo entrenado
# print("Coeficiente de regresión:", model.coef_[0])
# print("Término independiente:", model.intercept_)

# #Graficar datos reales
# plt.scatter(x, y, color='red', label='Datos de entrenamiento')

# #Graficar la línea de regresión
# plt.plot(x, y_pred, color='blue', label='Línea de regresión')

# plt.xlabel('Superficie (m2)')
# plt.ylabel('Precio (COP)')
# plt.title('Regresión Lineal: Precio de Viviendas según Superficie (m2)')
# plt.legend()
# plt.grid(True)

# # imprimir la gráfica
# plt.show()

# Guardar el artefacto del modelo entrenado en un archivo
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models/linear_model.joblib"

joblib.dump(model, MODEL_PATH)
