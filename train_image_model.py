import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.utils.class_weight import compute_class_weight

# --- CONFIGURATION ---
DATASET_DIR = "/Users/vanirudra/Downloads/AcneDataset"
TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VALID_DIR = os.path.join(DATASET_DIR, "valid")
TEST_DIR = os.path.join(DATASET_DIR, "test")

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
MODELS_DIR = "models"
os.makedirs(MODELS_DIR, exist_ok=True)

# --- 1. DATA GENERATORS & AUGMENTATION ---
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2]
)

valid_test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

valid_generator = valid_test_datagen.flow_from_directory(
    VALID_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

test_generator = valid_test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

# Save class mapping
class_indices = train_generator.class_indices
class_mapping = {v: k for k, v in class_indices.items()}
with open(os.path.join(MODELS_DIR, "class_indices.json"), "w") as f:
    json.dump(class_mapping, f, indent=4)
print(f"Saved class mapping: {class_mapping}")

num_classes = len(class_indices)

# --- 2. CLASS WEIGHTS ---
labels = train_generator.classes
class_weights_arr = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(labels),
    y=labels
)
class_weights = dict(enumerate(class_weights_arr))
print(f"Computed class weights: {class_weights}")

# --- 3. MODEL ARCHITECTURE ---
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Phase 1: Freeze all base model layers
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.4)(x)
predictions = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# --- 4. CALLBACKS ---
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.3,
    patience=2,
    min_lr=1e-7,
    verbose=1
)

model_checkpoint = ModelCheckpoint(
    filepath=os.path.join(MODELS_DIR, "acne_image_model_best.h5"),
    monitor='val_loss',
    save_best_only=True,
    verbose=1
)

callbacks = [early_stopping, reduce_lr, model_checkpoint]

# --- 5. PHASE 1: FEATURE EXTRACTION ---
print("\n--- PHASE 1: Training Classification Head ---")
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history_phase1 = model.fit(
    train_generator,
    validation_data=valid_generator,
    epochs=10,
    class_weight=class_weights,
    callbacks=callbacks
)

# --- 6. PHASE 2: FINE-TUNING ---
print("\n--- PHASE 2: Fine-Tuning Last 25 Layers ---")
# Unfreeze the base model
base_model.trainable = True

# Freeze all layers except the last 25
for layer in base_model.layers[:-25]:
    layer.trainable = False

# Recompile with a very low learning rate
model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-5), 
    loss='categorical_crossentropy', 
    metrics=['accuracy']
)

history_phase2 = model.fit(
    train_generator,
    validation_data=valid_generator,
    epochs=10,
    class_weight=class_weights,
    callbacks=callbacks
)

# --- 7. SAVE FINAL MODEL AND EVALUATE ---
final_model_path = os.path.join(MODELS_DIR, "acne_image_model_final.h5")
model.save(final_model_path)
print(f"\nSaved final model to {final_model_path}")

print("\n--- EVALUATION ON TEST DATASET ---")
# Evaluate the best model (since EarlyStopping with restore_best_weights=True restores the best weights)
test_loss, test_acc = model.evaluate(test_generator)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_acc:.4f}")

print("\nTraining Pipeline Complete!")
