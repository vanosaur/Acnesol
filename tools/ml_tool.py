import joblib
import numpy as np

result_map = {0: "Mild", 1: "Moderate", 2: "Severe"}
bmi_map = {"Underweight": 0, "Normal": 1, "Overweight": 2, "Obese": 3}

_MODEL = None

def load_ml_model(path: str = "models/acne_model.pkl"):
    global _MODEL
    if _MODEL is None:
        import joblib
        _MODEL = joblib.load(path)
    return _MODEL

def predict_severity(model, sleep: int, stress: int, bmi: str):
    if model is None:
        model = load_ml_model()
    X = np.array([[sleep, stress, bmi_map[bmi]]])
    pred = model.predict(X)[0]
    return result_map[pred]
