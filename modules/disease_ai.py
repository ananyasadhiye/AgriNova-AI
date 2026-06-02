import tensorflow as tf
import numpy as np
from PIL import Image

model=tf.keras.models.load_model("models/plant_disease_model.h5")

classes = [
    "Healthy",
    "Bacterial Spot",
    "Early Blight",
    "Late Blight",
    "Leaf Mold"
]
solutions = {
    "Healthy": "Your plant is healthy. Continue regular watering and monitoring.",
    "Bacterial Spot": "Use copper-based fungicide and remove infected leaves.",
    "Early Blight": "Spray Mancozeb or Chlorothalonil every 7–10 days.",
    "Late Blight": "Apply Copper fungicide and avoid overhead irrigation.",
    "Leaf Mold": "Improve air circulation and apply sulfur fungicide."
}

def detect_disease(img_file):

    img = Image.open(img_file).convert("RGB")   # IMPORTANT FIX

    img = img.resize((224,224))

    img = np.array(img)

    img = img / 255.0

    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)

    result = classes[np.argmax(pred)]

    return result, solutions[result]