import streamlit as st
import numpy as np
from PIL import Image
import os

CLASSES = [
    "Healthy",
    "Bacterial Spot",
    "Early Blight",
    "Late Blight",
    "Leaf Mold",
]

SOLUTIONS = {
    "Healthy":        "✅ Your plant is healthy! Continue regular watering and monitoring.",
    "Bacterial Spot": "🔴 Use copper-based fungicide. Remove and destroy infected leaves immediately.",
    "Early Blight":   "🟠 Spray Mancozeb or Chlorothalonil every 7–10 days. Remove lower infected leaves.",
    "Late Blight":    "🔴 Apply Copper fungicide. Avoid overhead irrigation. Destroy infected plants.",
    "Leaf Mold":      "🟡 Improve air circulation. Apply sulfur-based fungicide. Reduce humidity.",
}

def _load_model():
    model_path = "models/plant_disease_model.h5"
    if not os.path.exists(model_path):
        return None
    try:
        import tensorflow as tf
        return tf.keras.models.load_model(model_path)
    except Exception:
        return None

def run():
    st.markdown("### 🍃 Plant Disease Scanner")
    st.markdown("Upload a leaf photo and get instant AI diagnosis.")

    uploaded = st.file_uploader(
        "Upload leaf image", type=["jpg", "jpeg", "png"],
        help="Take a clear photo of the affected leaf"
    )

    if uploaded:
        img = Image.open(uploaded).convert("RGB")
        st.image(img, caption="Uploaded Leaf", use_container_width=True)

        if st.button("🔍 Diagnose Disease", use_container_width=True):
            model = _load_model()

            if model is None:
                # Demo mode — rule-based on pixel brightness
                st.info("🔬 Model file not found — running visual demo analysis.")
                arr = np.array(img.resize((64, 64))) / 255.0
                r_mean = arr[:,:,0].mean()
                g_mean = arr[:,:,1].mean()

                if g_mean > 0.42:
                    result = "Healthy"
                elif r_mean > 0.45:
                    result = "Early Blight"
                elif g_mean < 0.28:
                    result = "Late Blight"
                elif r_mean > g_mean * 1.2:
                    result = "Bacterial Spot"
                else:
                    result = "Leaf Mold"
            else:
                with st.spinner("Analyzing..."):
                    arr = np.array(img.resize((64, 64))) / 255.0
                    arr = np.expand_dims(arr, axis=0)
                    pred = model.predict(arr)
                    result = CLASSES[np.argmax(pred)]

            tag_color = "green" if result == "Healthy" else "red"
            st.markdown(f"**Diagnosis:** :{tag_color}[**{result}**]")
            st.info(SOLUTIONS[result])

            if result != "Healthy":
                st.markdown("#### 📋 Treatment Steps")
                steps = {
                    "Bacterial Spot": ["Remove infected leaves", "Apply copper fungicide", "Avoid overhead watering", "Monitor weekly"],
                    "Early Blight":   ["Remove lower infected leaves", "Spray Mancozeb/Chlorothalonil", "Water at base only", "Repeat every 7–10 days"],
                    "Late Blight":    ["Isolate infected plants", "Apply copper fungicide", "Destroy infected material", "Do not compost"],
                    "Leaf Mold":      ["Improve ventilation", "Reduce humidity", "Apply sulfur fungicide", "Prune crowded branches"],
                }
                for i, step in enumerate(steps.get(result, []), 1):
                    st.markdown(f"{i}. {step}")
