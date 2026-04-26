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

def build_model(num_classes: int = 5):
    import tensorflow as tf
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
    from tensorflow.keras.models import Model

    base_model = MobileNetV2(weights=None, include_top=False, input_shape=(224, 224, 3))
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.4)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    return Model(inputs=base_model.input, outputs=predictions)

def load_cnn_model(path: str = "models/model_weights.h5"):
    global _MODEL
    if _MODEL is None:
        print("Rebuilding model architecture...")
        _MODEL = build_model(num_classes=len(class_labels))
        print(f"Loading weights from {path}...")
        _MODEL.load_weights(path)
        print("Model loaded successfully via weights!")
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

    if confidence < 0.35:
        label = "Clear"
        severity = "Healthy"
    elif confidence < 0.6:
        severity = "Uncertain"
    else:
        severity = severity_map[label]

    return label, severity, confidence
