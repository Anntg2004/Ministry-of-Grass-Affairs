import streamlit as st
import cv2
import numpy as np

st.set_page_config(
    page_title="Ministry of Grass Affairs",
    page_icon="🌱",
    layout="wide"
)

# --------------------------------------------------
# GOVERNMENT STYLE
# --------------------------------------------------

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

header[data-testid="stHeader"] {
    background-color: transparent !important;
}

[data-testid="stToolbar"] {
    background-color: transparent !important;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# MINISTRY HEADER
# --------------------------------------------------

st.title("🏛️ MINISTRY OF GRASS AFFAIRS")

st.subheader(
    "Department of National Grass Administration"
)

st.write(
    "Official Government Portal for the Registration, "
    "Enumeration and Administration of Grass Citizens."
)

st.divider()


# --------------------------------------------------
# NATIONAL GRASS CENSUS
# --------------------------------------------------

st.header("🌱 National Grass Census")

st.write(
    "Submit a lawn image for official population estimation."
)

st.info(
    "📋 All grass citizens detected during this census "
    "will be considered temporarily registered with the Ministry."
)


# --------------------------------------------------
# CENSUS SUBMISSION
# --------------------------------------------------

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

        # --------------------------------------------------
        # SUBMITTED IMAGE
        # --------------------------------------------------

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


        # --------------------------------------------------
        # GRASS DETECTION
        # --------------------------------------------------

        st.subheader(
            "🔬 Department of Grass Enumeration"
        )

        st.write(
            "The Department is analysing the photograph "
            "to identify grass-like regions in the lawn "
            "and estimate the grass citizen population."
        )

        height, width = image.shape[:2]

        # Analyse lower 60% of photograph
        lawn_start = int(height * 0.40)

        lawn_area = image[
            lawn_start:height,
            :
        ]

        # Convert image to HSV
        hsv = cv2.cvtColor(
            lawn_area,
            cv2.COLOR_BGR2HSV
        )

        # Green colour range
        lower_green = np.array([
            25,
            35,
            30
        ])

        upper_green = np.array([
            95,
            255,
            255
        ])

        # Create grass mask
        mask = cv2.inRange(
            hsv,
            lower_green,
            upper_green
        )

        # Remove small noise
        kernel = np.ones(
            (5, 5),
            np.uint8
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            kernel
        )


        # --------------------------------------------------
        # GRASS COVERAGE
        # --------------------------------------------------

        grass_pixels = cv2.countNonZero(
            mask
        )

        lawn_pixels = (
            lawn_area.shape[0]
            *
            lawn_area.shape[1]
        )

        if lawn_pixels > 0:

            grass_percentage = (
                grass_pixels
                /
                lawn_pixels
            ) * 100

        else:

            grass_percentage = 0


        # --------------------------------------------------
        # POPULATION ESTIMATION
        # --------------------------------------------------

        count = int(
            grass_percentage * 100
        )

        count = max(
            1,
            min(count, 10000)
        )


        # --------------------------------------------------
        # FULL IMAGE MASK
        # --------------------------------------------------

        full_mask = np.zeros(
            (height, width),
            dtype=np.uint8
        )

        full_mask[
            lawn_start:height,
            :
        ] = mask


        # --------------------------------------------------
        # VERIFICATION IMAGE
        # --------------------------------------------------

        verification_image = image.copy()

        green_overlay = image.copy()

        green_overlay[
            full_mask > 0
        ] = (0, 255, 0)

        verification_image = cv2.addWeighted(
            image,
            0.65,
            green_overlay,
            0.35,
            0
        )


        # --------------------------------------------------
        # DRAW DETECTED REGIONS
        # --------------------------------------------------

        contours, _ = cv2.findContours(
            full_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:

            area = cv2.contourArea(
                contour
            )

            if area > 80:

                cv2.drawContours(
                    verification_image,
                    [contour],
                    -1,
                    (0, 255, 0),
                    3
                )


        verification_image_rgb = cv2.cvtColor(
            verification_image,
            cv2.COLOR_BGR2RGB
        )


        # --------------------------------------------------
        # OFFICIAL CENSUS RESULT
        # --------------------------------------------------

        st.divider()

        st.subheader(
            "📊 Official Census Result"
        )

        st.success(
            "✅ Grass Census successfully completed."
        )

        st.metric(
            "🌱 Estimated Grass Citizen Population",
            f"{count:,}"
        )

        st.caption(
            "Population figure represents an AI-assisted "
            "estimation based on detected grass coverage "
            "within the analysed lawn area."
        )

        st.metric(
            "🌿 Detected Grass Coverage",
            f"{grass_percentage:.1f}%"
        )


        # --------------------------------------------------
        # VERIFICATION MAP
        # --------------------------------------------------

        st.subheader(
            "🔬 Census Verification Map"
        )

        st.write(
            "Green highlighting indicates the areas "
            "identified as grass by the computer vision system."
        )

        st.image(
            verification_image_rgb,
            caption="Detected Grass Regions",
            use_container_width=True
        )


        # --------------------------------------------------
        # GRASS CITIZEN REGISTRY
        # --------------------------------------------------

        st.divider()

        st.subheader(
            "📋 Official Grass Citizen Registry"
        )

        st.write(
            "The following citizens have been temporarily "
            "registered by the Ministry:"
        )

        grass_citizens = []

        for i in range(count):

            citizen_id = (
                f"GRASS-{i + 1:04d}"
            )

            grass_citizens.append(
                citizen_id
            )


        # Registry table
        table = (
            "| Citizen ID | Status | Department |\n"
        )

        table += (
            "|---|---|---|\n"
        )

        for citizen_id in grass_citizens[:100]:

            table += (
                f"| {citizen_id} "
                f"| ACTIVE "
                f"| Grass Affairs |\n"
            )

        st.markdown(table)


        if count > 100:

            st.caption(
                f"Showing first 100 citizens out of "
                f"{count:,} registered citizens."
            )


        # --------------------------------------------------
        # GRASS CITIZEN SEARCH
        # --------------------------------------------------

        st.divider()

        st.header(
            "🔎 Grass Citizen Search"
        )

        st.write(
            "Enter a Grass Citizen ID to access the "
            "National Grass Citizen Database."
        )


        # Search box
        search_id = st.text_input(
            "Grass Citizen ID",
            placeholder="e.g. GRASS-0001"
        )

        search_button = st.button(
            "🔎 Search Citizen"
        )


        if search_button:

            st.error(
                "🔒 ACCESS DENIED"
            )

            st.warning(
                "Grass citizens have privacy rights."
            )

            st.info(
                "📋 Search privileges have been suspended "
                "under Ministry administrative regulations."
            )

            st.caption(
                "Reason: Unauthorized searching of grass "
                "citizen records is currently prohibited."
            )

        else:

            st.caption(
                "⚠️ Official notice: Citizen search access "
                "is subject to Ministry regulations."
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Ministry of Grass Affairs • "
    "Department of National Grass Administration"
)

st.caption(
    "Every Blade. Every Citizen. Every Census."
)