import streamlit as st
import cv2
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Ministry of Grass Affairs",
    page_icon="🌱",
    layout="wide"
)

# Ministry Header
st.title("🏛️ MINISTRY OF GRASS AFFAIRS")
st.subheader("Department of National Grass Administration")

st.write(
    "Official Government Portal for the Registration, "
    "Enumeration and Administration of Grass Citizens."
)

st.divider()

# Grass Census Section
st.header("🌱 National Grass Census")

st.write(
    "Submit a lawn image for official population enumeration."
)

st.info(
    "📋 All grass citizens detected during this census "
    "will be considered temporarily registered with the Ministry."
)

# Image Upload
st.subheader("📋 Census Submission")

uploaded_file = st.file_uploader(
    "Upload official lawn photograph",
    type=["jpg", "jpeg", "png"]
)

st.caption(
    "Accepted formats: JPG, JPEG, PNG • "
    "Photograph will be processed by the Department of Grass Enumeration."
)

# Process uploaded image
if uploaded_file:

    # Read uploaded image
    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    # Display submitted image
    st.image(
        image,
        channels="BGR",
        caption="Submitted for Official Grass Census"
    )

    # Convert image to HSV
    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    # Define green colour range
    lower_green = (25, 40, 40)
    upper_green = (95, 255, 255)

    # Create grass mask
    mask = cv2.inRange(
        hsv,
        lower_green,
        upper_green
    )

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

    # Estimated population
    count = len(grass_regions)

    # Census result
    st.divider()

    st.subheader("📊 Official Census Result")

    st.success(
        "✅ Grass Census successfully completed."
    )

    st.metric(
        "🌱 Estimated Grass Population",
        count
    )

    st.caption(
        "Population figure represents AI-assisted detection "
        "of grass-like regions in the submitted photograph."
    )