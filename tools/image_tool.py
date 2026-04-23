import numpy as np
from PIL import Image

class_labels = ['Blackheads', 'Cyst', 'Papules', 'Pustules', 'Whiteheads']
severity_map = {
    "Blackheads": "Mild",
    "Whiteheads": "Mild",
    "Papules": "Moderate",
    "Pustules": "Moderate",
    "Cyst": "Severe"
}

_MODEL = None

def load_cnn_model(path: str = "models/acne_image_model.h5"):
    global _MODEL
    if _MODEL is None:
        import tensorflow as tf
        print("Imported TensorFlow successfully")
        _MODEL = tf.keras.models.load_model(path)
    return _MODEL

def predict_acne_type(model, pil_image: Image.Image):
    # If model is passed as None, try to load default
    if model is None:
        model = load_cnn_model()
    
    img = pil_image.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    
    pred_img = model.predict(img)[0]
    class_index = np.argmax(pred_img)
    confidence = float(pred_img[class_index])

    label = class_labels[class_index]

    if confidence < 0.6:
        severity = "Uncertain"
    else:
        severity = severity_map[label]

    return label, severity, confidence
