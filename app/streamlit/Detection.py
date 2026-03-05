# app/streamlit/Detection.py

import streamlit as st
from PIL import Image, ImageDraw
import os

from agrovision.models.yolo import WeedDetector as YoloWeedDetector

st.set_page_config(page_title="Weed Detection", page_icon="🌿")

st.title("🌿 Weed Detection")
st.write("Upload an image and detect weeds using the YOLOv8 model.")

# Ensure upload directory exists
os.makedirs("uploads", exist_ok=True)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save uploaded file
    image_path = os.path.join("uploads", uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display uploaded image
    image = Image.open(image_path)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("Running detection...")

    model_path = "weights/best.pt"

    if os.path.exists(model_path):
        detector = YoloWeedDetector(model_path)
        result = detector.detect(image_path)

        detections = result["detections"]

        # Draw bounding boxes
        draw = ImageDraw.Draw(image)
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            draw.text((x1, y1), det["class_name"], fill="red")

        st.image(image, caption="Detections", use_column_width=True)

        st.write("Raw detections:")
        st.json(detections)

    else:
        st.error(f"Model weights not found at {model_path}.")
