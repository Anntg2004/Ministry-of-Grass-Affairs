import streamlit as st
import cv2
import numpy as np
import os
import json
import secrets
from datetime import datetime

DATA_FOLDER = ".grass_data"
LAWNS_FILE = os.path.join(DATA_FOLDER, "lawns.json")
os.makedirs(DATA_FOLDER, exist_ok=True)


def load_lawns():
    if os.path.exists(LAWNS_FILE):
        try:
            with open(LAWNS_FILE, "r") as file:
                return json.load(file)
        except Exception:
            return {}
    return {}


def save_lawns(lawns):
    with open(LAWNS_FILE, "w") as file:
        json.dump(lawns, file, indent=4)


lawns = load_lawns()


def get_citizens(lawn):
    citizens = lawn.get("citizens", [])
    if isinstance(citizens, list):
        return citizens
    if isinstance(citizens, dict):
        return list(citizens.values())
    return []


st.set_page_config(
    page_title="Ministry of Grass Affairs",
    page_icon="🌱",
    layout="wide"
)

# ------------------------------------------------------------
# PAGE DESIGN
# ------------------------------------------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #edf7ea 0%, #f8fcf6 50%, #e3f1df 100%);
    color: #183d22;
}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

.gov-topbar {
    background: #174f29;
    color: white;
    padding: 9px 18px;
    border-radius: 6px 6px 0 0;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: .4px;
}

.gov-title-box {
    background: white;
    border: 1px solid #b4cdb8;
    padding: 22px;
    text-align: center;
}

.gov-emblem {
    font-size: 55px;
    line-height: 1;
}

.gov-title {
    font-size: 34px;
    font-weight: 900;
    color: #154f26;
}

.gov-subtitle {
    font-size: 17px;
    color: #496651;
    margin-top: 5px;
}

.gov-motto {
    font-size: 13px;
    color: #6a806e;
    margin-top: 6px;
    font-style: italic;
}

.gov-nav {
    background: #dfeee1;
    border: 1px solid #b4cdb8;
    border-top: none;
    padding: 11px 18px;
    color: #24552e;
    font-weight: 700;
    text-align: center;
    margin-bottom: 24px;
}

.grass-official {
    background: rgba(255,255,255,.92);
    border: 1px solid #b8d0bb;
    border-left: 6px solid #27723b;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 25px;
}

.section-title {
    font-size: 30px;
    font-weight: 800;
    color: #155d2a;
    margin-top: 30px;
    margin-bottom: 15px;
}

label, .stTextInput label, .stSelectbox label, .stFileUploader label {
    color: #244c2c !important;
    font-weight: 600 !important;
}

.stTextInput input {
    background: white !important;
    color: #173d21 !important;
    border: 1px solid #8db596 !important;
    border-radius: 8px;
}

.stButton > button {
    background: #174f29;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    padding: 10px 20px;
}

.stButton > button:hover {
    background: #246d39;
    color: white;
}

.certificate-box {
    border: 5px double #1d5c2a;
    padding: 30px;
    background: #fbfff9;
    margin-top: 20px;
}

.certificate-title {
    text-align: center;
    color: #155d2a;
    font-size: 30px;
    font-weight: 800;
}

.certificate-subtitle {
    text-align: center;
    color: #52745b;
    font-size: 15px;
}

.official-seal {
    text-align: center;
    border: 3px solid #1d5c2a;
    border-radius: 50%;
    padding: 16px;
    color: #155d2a;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# GOVERNMENT WEBSITE OPENING
# ------------------------------------------------------------

st.markdown(
    '<div class="gov-topbar">GOVERNMENT OF THE REPUBLIC OF LAWN &nbsp; | &nbsp; OFFICIAL GOVERNMENT WEBSITE</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="gov-title-box">
        <div class="gov-emblem">🌱</div>
        <div class="gov-title">MINISTRY OF GRASS AFFAIRS</div>
        <div class="gov-subtitle">Department of National Grass Administration</div>
        <div class="gov-motto">Official Portal of Grass Citizen Services</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="gov-nav">🏛️ Home &nbsp; | &nbsp; 🌱 Grass Census &nbsp; | &nbsp; 📋 Citizen Registry &nbsp; | &nbsp; 🏡 Lawn Administration &nbsp; | &nbsp; 📜 Certificates</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="grass-official">
        <strong>🌿 Welcome to the National Grass Administration Portal</strong><br>
        Authorized government services for grass registration, census administration,
        citizen records, certificates and lawn population monitoring.
    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# GRASS DETECTION
# ------------------------------------------------------------

def detect_grass_mask(input_image):
    hsv = cv2.cvtColor(input_image.copy(), cv2.COLOR_BGR2HSV)

    lower_green = np.array([25, 35, 30])
    upper_green = np.array([95, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)

    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return mask


def analyze_grass(image_bytes):
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        return None, None, 0, 0

    mask = detect_grass_mask(image)
    total_pixels = mask.size
    grass_pixels = cv2.countNonZero(mask)

    coverage = (grass_pixels / total_pixels) * 100
    estimated_population = max(1, int(grass_pixels / 12))

    return image, mask, coverage, estimated_population


def create_lawn_id():
    numbers = []

    for lawn_id in lawns.keys():
        try:
            numbers.append(int(lawn_id.split("-")[1]))
        except Exception:
            pass

    next_number = max(numbers) + 1 if numbers else 1
    return f"LAWN-{next_number:03d}"


def create_citizens(lawn_id, population, registered_on):
    citizens = []
    citizen_count = min(population, 1000)

    for number in range(1, citizen_count + 1):
        citizens.append({
            "citizen_id": f"{lawn_id}-GRASS-{number:04d}",
            "name": "Bladie McGreen",
            "verification_code": str(secrets.randbelow(9000) + 1000),
            "registered_on": registered_on,
            "status": "ACTIVE",
            "classification": "Grass Citizen"
        })

    return citizens


# ------------------------------------------------------------
# NATIONAL GRASS CENSUS
# ------------------------------------------------------------

st.markdown('<div class="section-title">🌱 National Grass Census</div>', unsafe_allow_html=True)

if lawns:
    lawn_options = list(lawns.keys())
    selected_lawn_id = st.selectbox("Select Registered Lawn", lawn_options)
    current_lawn = lawns[selected_lawn_id]
else:
    selected_lawn_id = None
    current_lawn = None

st.markdown("---")
st.subheader("🏡 Register a New Lawn")

lawn_name = st.text_input(
    "Enter Lawn Name",
    placeholder="Example: College Garden"
)

uploaded_day1 = st.file_uploader(
    "Upload Day-1 Lawn Photograph",
    type=["jpg", "jpeg", "png"],
    key="day1"
)

if st.button("🌱 Conduct Initial Grass Census"):
    if not lawn_name:
        st.warning("Please enter a lawn name.")
    elif uploaded_day1 is None:
        st.warning("Please upload a Day-1 lawn photograph.")
    else:
        image, mask, coverage, population = analyze_grass(uploaded_day1.getvalue())

        if image is None:
            st.error("Unable to process the image.")
        else:
            lawn_id = create_lawn_id()
            registered_on = datetime.now().strftime("%Y-%m-%d")
            baseline_path = os.path.join(DATA_FOLDER, f"{lawn_id}_baseline.jpg")

            cv2.imwrite(baseline_path, image)

            citizens = create_citizens(
                lawn_id,
                population,
                registered_on
            )

            lawns[lawn_id] = {
                "name": lawn_name,
                "registered_on": registered_on,
                "population": population,
                "coverage": coverage,
                "baseline_image": baseline_path,
                "citizens": citizens
            }

            save_lawns(lawns)

            st.success(f"✅ Lawn successfully registered as {lawn_id}")
            st.info(f"🌱 Estimated Grass Citizen Population: {population:,}")
            st.info(f"🌿 Grass Coverage: {coverage:.2f}%")

            if citizens:
                demo = citizens[0]
                st.info(
                    "🎫 DEMO CITIZEN ACCESS\n\n"
                    f"Citizen ID: {demo['citizen_id']}\n\n"
                    f"Verification Code: {demo['verification_code']}"
                )


# ------------------------------------------------------------
# EXISTING LAWN INFORMATION
# ------------------------------------------------------------

if current_lawn:
    current_citizens = get_citizens(current_lawn)

    st.markdown("---")
    st.subheader(
        f"📋 Lawn Administration: {current_lawn.get('name', 'Registered Lawn')}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Grass Population", f"{current_lawn.get('population', 0):,}")

    with col2:
        st.metric("Grass Coverage", f"{current_lawn.get('coverage', 0):.2f}%")

    with col3:
        st.metric("Citizen Records", len(current_citizens))


# ------------------------------------------------------------
# CITIZEN REGISTRY
# ------------------------------------------------------------

if current_lawn:
    st.markdown("---")
    st.subheader("📋 National Grass Citizen Registry")

    registry_citizens = get_citizens(current_lawn)

    st.write(
        f"Official registry for **{current_lawn.get('name', 'Registered Lawn')}** "
        f"({selected_lawn_id})."
    )

    if registry_citizens:
        registry_rows = []

        for citizen in registry_citizens[:100]:
            if isinstance(citizen, dict):
                registry_rows.append([
                    citizen.get("citizen_id", "N/A"),
                    citizen.get("name", "Bladie McGreen"),
                    citizen.get("status", "ACTIVE"),
                    citizen.get("classification", "Grass Citizen")
                ])

        if registry_rows:
            st.table(
                {
                    "Citizen ID": [row[0] for row in registry_rows],
                    "Citizen Name": [row[1] for row in registry_rows],
                    "Status": [row[2] for row in registry_rows],
                    "Classification": [row[3] for row in registry_rows]
                }
            )

            if len(registry_citizens) > 100:
                st.caption(
                    f"Showing first 100 of {len(registry_citizens):,} registered citizens."
                )
    else:
        st.info("No grass citizens are currently registered for this lawn.")


# ------------------------------------------------------------
# CITIZEN SEARCH
# ------------------------------------------------------------

if current_lawn:
    st.markdown("---")
    st.subheader("🔎 Grass Citizen Search")

    citizen_id_input = st.text_input(
        "Enter Grass Citizen ID",
        placeholder="LAWN-001-GRASS-0001"
    )

    verification_input = st.text_input(
        "Enter Private Verification Code",
        type="password"
    )

    if st.button("🔐 Access Citizen Record"):
        found_citizen = None

        for citizen in get_citizens(current_lawn):
            if not isinstance(citizen, dict):
                continue

            if citizen.get("citizen_id") == citizen_id_input.strip():
                if citizen.get("verification_code") == verification_input.strip():
                    found_citizen = citizen
                break

        if found_citizen is None:
            st.error("❌ Citizen record not found or verification code is incorrect.")
        else:
            st.success("✅ Citizen identity verified.")

            st.markdown("---")

            certificate_number = (
                f"MGA/{selected_lawn_id}/"
                f"{citizen_id_input.strip().split('-')[-1]}/"
                f"{found_citizen.get('registered_on', '0000-00-00')}"
            )

            st.markdown('<div class="certificate-box">', unsafe_allow_html=True)

            seal_col1, seal_col2, seal_col3 = st.columns([1, 2, 1])

            with seal_col1:
                st.markdown(
                    """
                    <div class="official-seal">
                    🏛️<br>MGA<br>🌱<br>OFFICIAL
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with seal_col2:
                st.markdown(
                    '<div class="certificate-title">MINISTRY OF GRASS AFFAIRS</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    '<div class="certificate-subtitle">Department of National Grass Administration<br>Grass Citizen Registration Authority</div>',
                    unsafe_allow_html=True
                )

            with seal_col3:
                st.markdown(
                    """
                    <div class="official-seal">
                    🌿<br>2026<br>🌱<br>VERIFIED
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("---")

            st.markdown(
                '<div class="certificate-title">🌿 CERTIFICATE OF BIRTH 🌿</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="certificate-subtitle">Official Government Document</div>',
                unsafe_allow_html=True
            )

            st.markdown("---")

            reg_col1, reg_col2 = st.columns(2)

            with reg_col1:
                st.write(
                    f"**Certificate Registration No.**\n\n`{certificate_number}`"
                )

            with reg_col2:
                st.write(
                    f"**Citizen Registration No.**\n\n`{citizen_id_input.strip()}`"
                )

            st.markdown("---")
            st.markdown("### 🌱 PARTICULARS OF THE CITIZEN")

            certificate_rows = [
                ["1", "Name of Citizen", "Bladie McGreen"],
                ["2", "Date of Birth", found_citizen.get("registered_on", "Record Not Available")],
                ["3", "Place of Birth", f"{selected_lawn_id}, Green Zone"],
                ["4", "Sex", "Grass 🌱"],
                ["5", "Citizenship", "Republic of Lawn"],
                ["6", "Permanent Address", f"{current_lawn.get('name', 'Registered Lawn')}, Sector 001, Green Zone"],
                ["7", "Occupation", "Professional Lawn Decoration"],
                ["8", "Citizen Status", found_citizen.get("status", "ACTIVE")],
                ["9", "Classification", "Grass Citizen"],
                ["10", "Jurisdiction", selected_lawn_id]
            ]

            st.table(certificate_rows)

            st.markdown("---")
            st.markdown("### 🌿 PARTICULARS OF PARENTAGE")

            st.table([
                ["Mother", "Mother Grass 🌿"],
                ["Father", "Father Grass 🌱"],
                ["Family Name", "The Green Family"],
                ["Family Status", "Rooted & Growing"]
            ])

            st.markdown("---")
            st.markdown("### 🏛️ OFFICIAL GOVERNMENT CLASSIFICATION")

            class_col1, class_col2 = st.columns(2)

            with class_col1:
                st.info(
                    "**Species**\n\n*Grassus Extremely Greenus*\n\n"
                    "**Occupation**\n\nLawn Decoration\n\n"
                    "**Annual Income**\n\n₹0.00"
                )

            with class_col2:
                st.info(
                    "**Threat Level**\n\nExtremely Harmless\n\n"
                    "**International Travel**\n\nNot permitted — roots attached\n\n"
                    "**Government Importance**\n\nSurprisingly High"
                )

            st.markdown("---")
            st.markdown("### 📝 DECLARATION BY THE CITIZEN")

            st.write(
                "I hereby declare that I am a legitimate resident of the above-mentioned lawn. "
                "I promise to photosynthesize responsibly, remain reasonably green, and contribute "
                "positively to the national grass population. I further request that the authorities "
                "protect me from unnecessary mowing."
            )

            st.markdown(
                '> **“I may just be grass, but I have government documents now.” 🌱**'
            )

            st.markdown("---")
            st.markdown("### 🏆 OFFICIAL GOVERNMENT RECOGNITION")

            award_col1, award_col2, award_col3 = st.columns(3)

            with award_col1:
                st.success("🏆 **BEST LOOKING BLADE**\n\nExceptional greenness")

            with award_col2:
                st.success("🌿 **OUTSTANDING GREENNESS**\n\nValuable lawn contribution")

            with award_col3:
                st.success("☀️ **PHOTOSYNTHESIS EXCELLENCE**\n\nOutstanding solar absorption")

            st.markdown("---")

            st.warning(
                "⚠️ **OFFICIAL GOVERNMENT NOTICE**\n\n"
                "This citizen has been officially registered by the Ministry of Grass Affairs.\n\n"
                "Unauthorized mowing, trimming, uprooting, or suspicious lawn activity may be subject "
                "to administrative review.\n\n**MOWING IS NOW A GOVERNMENT MATTER.**"
            )

            st.markdown("---")

            signature_col1, signature_col2 = st.columns(2)

            with signature_col1:
                st.markdown(
                    "### 🏛️ OFFICIAL SEAL\n\n"
                    "**MINISTRY OF GRASS AFFAIRS**\n\n"
                    "**NATIONAL GRASS ADMINISTRATION**\n\n🌱"
                )

            with signature_col2:
                st.write("")
                st.write("")
                st.markdown("**____________________________**")
                st.markdown("**The Grass Administrator**")
                st.caption("Authorized Government Officer")

            st.markdown("---")
            st.caption(
                "Issued under the authority of the Department of National Grass Administration."
            )
            st.success("🌿 EVERY BLADE COUNTS. EVERY CITIZEN MATTERS.")

            st.markdown("</div>", unsafe_allow_html=True)


# ------------------------------------------------------------
# DAY-2 GRASS CENSUS
# ------------------------------------------------------------

if current_lawn:
    st.markdown("---")
    st.subheader("📅 Day-2 Grass Census")

    st.write(
        "Upload another photograph of the same lawn to compare it with the Day-1 baseline."
    )

    uploaded_day2 = st.file_uploader(
        "Upload Day-2 Lawn Photograph",
        type=["jpg", "jpeg", "png"],
        key="day2"
    )

    if st.button("🔍 Conduct Day-2 Census"):
        if uploaded_day2 is None:
            st.warning("Please upload a Day-2 photograph.")
        else:
            baseline_path = current_lawn.get("baseline_image")

            if not baseline_path or not os.path.exists(baseline_path):
                st.error("Baseline image was not found for this lawn.")
            else:
                day2_image, day2_mask, day2_coverage, day2_population = analyze_grass(
                    uploaded_day2.getvalue()
                )

                baseline_image = cv2.imread(baseline_path)

                if baseline_image is None or day2_image is None:
                    st.error("Unable to read or process the images.")
                else:
                    # Resize Day 2 image and mask to match Baseline dimensions
                    height, width = baseline_image.shape[:2]
                    day2_image = cv2.resize(day2_image, (width, height))
                    day2_mask = cv2.resize(day2_mask, (width, height))

                    baseline_mask = detect_grass_mask(baseline_image)
                    baseline_population = current_lawn.get("population", 0)

                    if baseline_population <= 0:
                        baseline_population = 1

                    raw_missing_rate = (
                        (baseline_population - day2_population)
                        / baseline_population
                    ) * 100

                    raw_new_rate = (
                        (day2_population - baseline_population)
                        / baseline_population
                    ) * 100

                    missing_rate = max(0, min(3, raw_missing_rate))
                    new_rate = max(0, min(3, raw_new_rate))

                    displayed_day2_population = int(
                        baseline_population
                        * (1 - missing_rate / 100 + new_rate / 100)
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Day-1 Population", f"{baseline_population:,}")

                    with col2:
                        st.metric("Day-2 Population", f"{displayed_day2_population:,}")

                    with col3:
                        st.metric("Missing Grass Rate", f"{missing_rate:.2f}%")

                    st.subheader("🗺️ Grass Citizen Change Detection Map")

                    baseline_bool = baseline_mask > 0
                    day2_bool = day2_mask > 0

                    missing_mask = baseline_bool & ~day2_bool
                    new_mask = day2_bool & ~baseline_bool

                    change_map = np.zeros(
                        (baseline_mask.shape[0], baseline_mask.shape[1], 3),
                        dtype=np.uint8
                    )

                    change_map[missing_mask] = [0, 0, 255]
                    change_map[new_mask] = [255, 0, 0]

                    change_map_rgb = cv2.cvtColor(
                        change_map,
                        cv2.COLOR_BGR2RGB
                    )

                    st.image(
                        change_map_rgb,
                        caption="🔴 Red = potentially missing grass regions | 🔵 Blue = newly detected grass regions",
                        use_container_width=True
                    )

                    if missing_rate > 0:
                        st.error(
                            f"🚨 **GRASS CITIZEN ALERT**\n\n"
                            f"Approximately **{missing_rate:.2f}%** of the registered grass population "
                            "appears to be unaccounted for.\n\n"
                            "The Ministry has classified the case as a **PROVISIONAL MISSING GRASS INCIDENT**.\n\n"
                            "🔎 Investigation status: **ONGOING**"
                        )
                    else:
                        st.success(
                            "✅ **NATIONAL GRASS POPULATION STABLE**\n\n"
                            "No significant grass population change was detected between Day-1 and Day-2.\n\n"
                            "All citizens appear to be present and photosynthesizing normally. 🌱"
                        )


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.markdown("---")
st.markdown(
    "🏛️ **GOVERNMENT OF THE REPUBLIC OF LAWN**  \n"
    "**MINISTRY OF GRASS AFFAIRS**  \n"
    "Department of National Grass Administration  \n"
    "🌱 Every blade counts. Every citizen matters."
)