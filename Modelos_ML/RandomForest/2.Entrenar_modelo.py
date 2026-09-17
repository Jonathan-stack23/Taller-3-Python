import pandas as pd
from sklearn.model_selection import train_test_split # pip install scikit-learn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib #pip install joblib
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

os.system("cls" if os.name == "nt" else "clear")

def log(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "dataset_medico_ampliado.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODELO_PATH = os.path.join(MODELS_DIR, "modelo_random_forest_ampliado.pkl")

try:
    # =========================
    # 1. CARGA DEL DATASET AMPLIADO
    # =========================
    log("1. CARGA DEL DATASET AMPLIADO")
    df = pd.read_csv(DATA_PATH)
    print(f"✔ Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
    
    # =========================
    # 2. SEPARAR FEATURES Y TARGET
    # =========================
    log("2. PREPARACIÓN DE DATOS")
    X = df.drop("diagnostico", axis=1)
    y = df["diagnostico"]
    
    print(f"🔢 Features utilizadas ({len(X.columns)}):")
    for i, col in enumerate(X.columns, 1):
        print(f"   {i}. {col}")
    print(f"\n🎯 Clases objetivo: {y.unique()}")
    
    # =========================
    # 3. DIVISIÓN TRAIN/TEST
    # =========================
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    print(f"\n📊 Split: Train {X_train.shape[0]} | Test {X_test.shape[0]}")
    
    # =========================
    # 4. ENTRENAMIENTO
    # =========================
    log("3. ENTRENAMIENTO DEL MODELO")
    model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    print("✔ Modelo entrenado")
    
    # =========================
    # 5. EVALUACIÓN
    # =========================
    log("4. EVALUACIÓN")
    y_pred = model.predict(X_test)
    accuracy = model.score(X_test, y_test)
    print(f"🎯 Accuracy(Exactitud): {accuracy:.4f} ({accuracy*100:.2f}%)\n")
    print("📋 Classification Report:")
    print(classification_report(y_test, y_pred))
    print("📊 Matriz de confusión:")
    print(confusion_matrix(y_test, y_pred))
    
    # =========================
    # 6. IMPORTANCIA DE VARIABLES
    # =========================
    log("5. IMPORTANCIA DE VARIABLES")
    imp_df = pd.DataFrame({
        "Feature": X.columns,
        "Importancia (%)": (model.feature_importances_ * 100).round(2)
    }).sort_values("Importancia (%)", ascending=False)
    print(imp_df.head(15).to_string(index=False))
    
    # =========================
    # 7. GUARDAR MODELO
    # =========================
    log("6. GUARDANDO MODELO")
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(model, MODELO_PATH)
    print(f"💾 Modelo guardado en: {MODELO_PATH}")
    
except FileNotFoundError:
    log("ERROR")
    print(f"❌ No se encontró '{DATA_PATH}'")
    print("👉 Ejecuta primero '1.Crear_dataset.py'")
    exit(1)