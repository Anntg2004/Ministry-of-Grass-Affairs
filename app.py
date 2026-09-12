import streamlit as st
import cv2
import numpy as np

st.title("🌱 Ministry of Grass Affairs")
st.write("National Grass Population Census")

uploaded_file = st.file_uploader(
    "Upload a lawn image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    # Read uploaded image
    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    st.image(image, channels="BGR", caption="Submitted for Grass Census")

    # Detect green areas
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_green = (25, 40, 40)
    upper_green = (95, 255, 255)

    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find grass regions
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    grass_regions = []

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 50:
            grass_regions.append(contour)

    count = len(grass_regions)

    st.success("Grass Census completed!")

    st.metric(
        "🌱 Estimated Grass Population",
        count
    )