import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
from src.shared.constants import STATUS_BAD_REQUEST, STATUS_OK

class Models:
    def __init__(self, csv_path):
        """
        Initialize the class with dataset path and set common variables.
        :param csv_path: Path to the CSV dataset.
        """
        self.csv_path = csv_path
        self.features = ["NDVI", "NDWI", "NDCI", "FDI", "NDPI"]
        self.target = "microplastic_concentration"
        self.scaler = StandardScaler()
        self.models = {}  # Dictionary to store trained models

    def load_data(self):
        """
        Load and clean the dataset (removing NaN values).
        :return: (STATUS, Response Message)
        """
        try:
            df = pd.read_csv(self.csv_path)
            df = df.dropna()  # Remove missing values
            return STATUS_OK, df
        except Exception as e:
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def split_data(self, df):
        """
        Split the dataset into training and testing sets (80% train, 20% test).
        :param df: Processed DataFrame.
        :return: (STATUS, Response Message or Data)
        """
        try:
            X = df[self.features]
            y = df[self.target]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Normalize features using StandardScaler
            self.scaler.fit(X_train)
            X_train_scaled = self.scaler.transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)

            return STATUS_OK, (X_train_scaled, X_test_scaled, y_train, y_test)
        except Exception as e:
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def train_models(self, X_train, y_train):
        """
        Train three models: Linear Regression, Random Forest, and Neural Network.
        :param X_train: Scaled training features.
        :param y_train: Target values for training.
        :return: (STATUS, Response Message)
        """
        try:
            self.models["Linear Regression"] = LinearRegression()
            self.models["Linear Regression"].fit(X_train, y_train)

            self.models["Random Forest"] = RandomForestRegressor(n_estimators=100, random_state=42)
            self.models["Random Forest"].fit(X_train, y_train)

            self.models["Neural Network"] = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42)
            self.models["Neural Network"].fit(X_train, y_train)

            return STATUS_OK, {"message": "Models trained."}
        except Exception as e:
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def evaluate_models(self, X_test, y_test):
        """
        Evaluate all trained models using MSE and R² score.
        :param X_test: Scaled test features.
        :param y_test: True target values.
        :return: (STATUS, Response Message or Evaluation Results)
        """
        try:
            results = {}
            for name, model in self.models.items():
                y_pred = model.predict(X_test)
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                results[name] = {"mse": mse, "r2": r2}

            return STATUS_OK, results
        except Exception as e:
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def save_models(self, path="models/"):
        """
        Save trained models to disk.
        :param path: Directory to save models.
        :return: (STATUS, Response Message)
        """
        try:
            for name, model in self.models.items():
                joblib.dump(model, f"{path}/{name.replace(' ', '_')}.pkl")
            joblib.dump(self.scaler, f"{path}/scaler.pkl")
            return STATUS_OK, {"message": "Models saved successfully."}
        except Exception as e:
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def load_models(self, path="models/"):
        """
        Load trained models from disk.
        :param path: Directory to load models.
        :return: (STATUS, Response Message)
        """
        try:
            self.models["Linear Regression"] = joblib.load(f"{path}/Linear_Regression.pkl")
            self.models["Random Forest"] = joblib.load(f"{path}/Random_Forest.pkl")
            self.models["Neural Network"] = joblib.load(f"{path}/Neural_Network.pkl")
            self.scaler = joblib.load(f"{path}/scaler.pkl")
            return STATUS_OK, {"message": "Models loaded successfully."}
        except Exception as e:
            return STATUS_BAD_REQUEST, {"message": str(e)}
