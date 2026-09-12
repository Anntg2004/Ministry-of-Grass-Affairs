import streamlit as st
import cv2
import numpy as np


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Ministry of Grass Affairs",
    page_icon="🌱",
    layout="wide"
)


# =========================================================
# GOVERNMENT STYLE
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #eef8ee, #dff2df);
}

.stApp p,
.stApp label,
.stApp span,
.stApp div {
    color: #1f2937;
}

h1, h2, h3 {
    color: #14532d !important;
}

[data-testid="stMetric"] {
    background-color: rgba(255, 255, 255, 0.85);
    border: 1px solid #b7d7b7;
    padding: 20px;
    border-radius: 16px;
}

[data-testid="stFileUploader"] {
    background-color: rgba(255, 255, 255, 0.85);
    border: 2px dashed #4d7c4d;
    border-radius: 14px;
    padding: 15px;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #f8fff8 !important;
    border: 2px dashed #4d7c4d !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background-color: #e8f5e8 !important;
    color: #14532d !important;
    border: 1px solid #4d7c4d !important;
}

[data-testid="stFileUploaderDropzone"] button:hover {
    background-color: #d5ecd5 !important;
    color: #14532d !important;
}

header[data-testid="stHeader"] {
    background-color: transparent !important;
}

[data-testid="stToolbar"] {
    background-color: transparent !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# MINISTRY HEADER
# =========================================================

st.title("🏛️ MINISTRY OF GRASS AFFAIRS")

st.subheader("Department of National Grass Administration")

st.write(
    "Official Government Portal for the Registration, "
    "Enumeration and Administration of Grass Citizens."
)

st.divider()


# =========================================================
# NATIONAL GRASS CENSUS
# =========================================================

st.header("🌱 National Grass Census")

st.write(
    "Submit a lawn image for official population enumeration."
)

st.info(
    "📋 All grass citizens detected during this census "
    "will be considered temporarily registered with the Ministry."
)


# =========================================================
# IMAGE UPLOAD
# =========================================================

st.subheader("📋 Census Submission")

uploaded_file = st.file_uploader(
    "Upload official lawn photograph",
    type=["jpg", "jpeg", "png"]
)

st.caption(
    "Accepted formats: JPG, JPEG, PNG • "
    "Photograph will be processed by the Department "
    "of Grass Enumeration."
)


# =========================================================
# PROCESS IMAGE
# =========================================================

if uploaded_file:

    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    if image is None:

        st.error(
            "❌ The Ministry could not process this photograph."
        )

    else:

        # =================================================
        # SUBMITTED IMAGE
        # =================================================

        st.subheader("📷 Submitted Lawn Photograph")

        image_rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        st.image(
            image_rgb,
            caption="Official Census Photograph",
            use_container_width=True
        )


        # =================================================
        # COMPUTER VISION PROCESSING
        # =================================================

        st.subheader("🔬 Department of Grass Enumeration")

        st.write(
            "The Department is analysing the photograph "
            "to identify grass-like regions."
        )

        # Convert image to HSV
        hsv = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2HSV
        )

        # Green colour range
        lower_green = np.array(
            [25, 40, 40]
        )

        upper_green = np.array(
            [95, 255, 255]
        )

        # Create green mask
        mask = cv2.inRange(
            hsv,
            lower_green,
            upper_green
        )

        # Find green regions
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # Keep meaningful regions
        grass_regions = []

        for contour in contours:

            area = cv2.contourArea(contour)

            if area > 50:

                grass_regions.append(contour)

        # Estimated grass population
        count = len(grass_regions)
        # =================================================
# CREATE CENSUS VERIFICATION IMAGE
# =================================================

verification_image = image.copy()

for contour in grass_regions:
    cv2.drawContours(
        verification_image,
        [contour],
        -1,
        (0, 255, 0),
        2
    )

verification_image_rgb = cv2.cvtColor(
    verification_image,
    cv2.COLOR_BGR2RGB
)


        # =================================================
        # CREATE GRASS CITIZEN IDs
        # =================================================

        grass_citizens = []

        for i in range(count):

            citizen_id = f"GRASS-{i + 1:04d}"

            grass_citizens.append(citizen_id)


        # =================================================
        # OFFICIAL CENSUS RESULT
        # =================================================

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
            "Population figure represents AI-assisted "
            "detection of grass-like regions in the "
            "submitted photograph."
        )


        # =================================================
        # OFFICIAL GRASS CITIZEN REGISTRY
        # =================================================

        st.divider()

        st.subheader(
            "📋 Official Grass Citizen Registry"
        )

        st.write(
            "The following citizens have been temporarily "
            "registered by the Ministry:"
        )

        # Create registry
        registry = []

        for citizen_id in grass_citizens:

            registry.append({
                "Citizen ID": citizen_id,
                "Status": "ACTIVE",
                "Department": "Grass Affairs"
            })


        # =================================================
        # REGISTRY TABLE
        # =================================================

        table = "| Citizen ID | Status | Department |\n"
        table += "|---|---|---|\n"

        for citizen in registry:

            table += (
                f"| {citizen['Citizen ID']} "
                f"| {citizen['Status']} "
                f"| {citizen['Department']} |\n"
            )

        st.markdown(table)


        # =================================================
        # MINISTRY RESTRICTIONS
        # =================================================

        st.divider()

        st.header("🔎 Grass Citizen Search")

        st.warning(
            "🔒 SEARCH FACILITY CURRENTLY RESTRICTED"
        )

        st.write(
            "The Ministry has temporarily suspended access "
            "to the Grass Citizen Search Database."
        )

        st.text_input(
            "Search Grass Citizen ID",
            placeholder="e.g. GRASS-0001",
            disabled=True
        )

        st.caption(
            "Reason: Citizen records are undergoing "
            "unnecessary administrative verification."
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Ministry of Grass Affairs • "
    "Department of National Grass Administration"
)

st.caption(
    "Every Blade. Every Citizen. Every Census."
)