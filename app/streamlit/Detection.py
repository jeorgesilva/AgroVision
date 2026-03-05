# app/streamlit/Detection.py
import streamlit as st
from PIL import Image
import os
from agrovision.core.detection import WeedDetector
from agrovision.utils.file_utils import create_dir_if_not_exists

st.set_page_config(page_title="Weed Detection", page_icon="🌿")

st.title("🌿 Weed Detection")

st.write("Upload an image and the YOLOv8 model will detect weeds.")

# Create directories if they don't exist
create_dir_if_not_exists("uploads")
create_dir_if_not_exists("weights")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save the uploaded file
    image_path = os.path.join("uploads", uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    st.write("")
    st.write("Detecting weeds...")

    # Perform detection
    model_path = "weights/best.pt"  # Make sure this path is correct
    if os.path.exists(model_path):
        detector = WeedDetector(model_path)
        detections = detector.detect(image_path)

        # For demonstration, we'll just print the detections
        st.write(detections)

        # Here you would typically draw the bounding boxes on the image
        # and display it. That requires a bit more code with OpenCV or PIL.
    else:
        st.error(f"Model weights not found at {model_path}. Please make sure the weights file exists.")
