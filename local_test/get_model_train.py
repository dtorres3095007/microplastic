import joblib
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

linear_model = joblib.load("data/train/models/Linear_Regression.pkl")
random_forest = joblib.load("data/train/models/Random_Forest.pkl")
neural_network = joblib.load("data/train/models/Neural_Network.pkl")

scaler = joblib.load("data/train/models/scaler.pkl")
df = pd.read_csv("data/train/dataset/microplastics.csv")

def evaluar_modelo(modelo, X_test, y_test, nombre):
    """
    Evalúa un modelo con MSE y R².
    """
    y_pred = modelo.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"📊 {nombre}:")
    print(f"   ✅ MSE: {mse:.4f}")
    print(f"   ✅ R² Score: {r2:.4f}\n")


if __name__ == "__main__":
    # Definir features y target
    columnas_features = ["NDVI", "NDWI", "NDCI", "FDI", "NDPI"]
    X = df[columnas_features]
    y = df["microplastic_concentration"]

    # Aplicar el escalado (si lo usaste en el entrenamiento)
    X_scaled = scaler.transform(X)

    # Evaluar cada modelo
    evaluar_modelo(linear_model, X_scaled, y, "Linear Regression")
    evaluar_modelo(random_forest, X_scaled, y, "Random Forest")
    evaluar_modelo(neural_network, X_scaled, y, "Neural Network")