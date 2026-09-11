import joblib
from pathlib import Path
import numpy as np
from sklearn.linear_model import LinearRegression

x = np.array([[40], [50], [60], [90], [100], [120]])
y = np.array([210000000, 300000000, 350000000, 500000000, 600000000, 700000000])

model = LinearRegression()
model.fit(x, y)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models/linear_model.joblib"
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(model, MODEL_PATH)
