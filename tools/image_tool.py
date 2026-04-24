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

def load_cnn_model(path: str = "models/final_model.keras"):
    global _MODEL
    if _MODEL is None:
        import tensorflow as tf
        from tensorflow.keras.layers import InputLayer, BatchNormalization
        
        # Monkeypatch to handle Keras 2/3 and version-specific mismatches
        # This strips out 'renorm' and other keywords that cause deserialization errors
        def patch_layer(layer_cls):
            old_init = layer_cls.__init__
            def new_init(self, *args, **kwargs):
                # Keywords that frequently cause "Unrecognized keyword argument" errors
                forbidden = ['batch_shape', 'optional', 'renorm', 'renorm_clipping', 'renorm_momentum', 'synchronized']
                for key in forbidden:
                    kwargs.pop(key, None)
                return old_init(self, *args, **kwargs)
            layer_cls.__init__ = new_init

        patch_layer(InputLayer)
        patch_layer(BatchNormalization)

        print("Importing TensorFlow with resilient layer patches...")
        # Use compile=False for faster inference-only loading
        _MODEL = tf.keras.models.load_model(path, compile=False)
        print("Model loaded successfully!")
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
