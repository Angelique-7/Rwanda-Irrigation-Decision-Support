
from pathlib import Path

import pandas as pd
import streamlit as st



# Page configuration must run before other Streamlit commands.
st.set_page_config(
    page_title="Rwanda Irrigation Planning Assistant",
    page_icon="🌱",
    layout="wide",
)

# Custom theme: Chocolate background and white text
st.markdown("""
<style>
/* Main application background */
.stApp {
    background-color: #4B2E2B;
    color: #FFFFFF;
}

/* Main text */
.stApp p,
.stApp label,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp li,
.stApp span {
    color: #FFFFFF;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #36201E;
}

/* Buttons */
.stButton > button {
    background-color: #F28C28;
    color: #FFFFFF;
    border: 1px solid #F28C28;
    border-radius: 8px;
    font-weight: bold;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #63413B;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #8B655B;
}

/* Data tables */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background-color: #FFFFFF;
    border-radius: 8px;
}

/* Form controls */
.stSelectbox [data-baseweb="select"] > div,
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: #FFFFFF;
    color: #36201E;
    border-radius: 8px;
}

/* Radio buttons and checkboxes */
.stRadio label,
.stCheckbox label {
    color: #FFFFFF;
}

/* Links */
.stApp a {
    color: #FFB347;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.title("🌱 Rwanda Irrigation Planning Assistant")

st.write(
    """
    This application explores irrigation methods and agricultural
    water sources across Rwanda's districts and agricultural seasons.

    It helps users examine reported patterns and explore possible
    combinations of irrigation improvements and water-storage options.
    """
)

st.info(
    "Planning support only: the reported data does not directly measure "
    "water stress, crop yields, or the effectiveness of an intervention. "
    "Recommendations must be checked against local conditions."
)


# ============================================================
# 2. FILE PATHS
# ============================================================

# Locate the main project folder automatically.
PROJECT_DIR = Path(__file__).resolve().parent.parent

OUTPUTS_DIR = PROJECT_DIR / "outputs"

METHODS_FILE = (
    OUTPUTS_DIR / "cleaned_irrigation_methods_by_district.csv"
)

SOURCES_FILE = (
    OUTPUTS_DIR / "cleaned_irrigation_water_sources_by_district.csv"
)


# ============================================================
# 3. LOAD THE CLEANED DATA
# ============================================================

@st.cache_data
def load_data():
    """Load the cleaned irrigation and water-source datasets."""

    methods = pd.read_csv(METHODS_FILE)
    sources = pd.read_csv(SOURCES_FILE)

    # Convert reported irrigation values to numeric values.
    # Missing or invalid values remain missing (NaN), not zero.
    method_columns = [
        "Surface irrigation",
        "Flood irrigation",
        "Drip irrigation",
        "Sprinkler irrigation",
        "Pivot irrigation",
        "Traditional techniques",
    ]

    source_columns = [
        "Rainwater",
        "Water treatment",
        "Underground",
        "Lake / streams",
        "Water catchment",
    ]

    for column in method_columns:
        methods[column] = pd.to_numeric(
            methods[column], errors="coerce"
        )

    for column in source_columns:
        sources[column] = pd.to_numeric(
            sources[column], errors="coerce"
        )

    # Standardize district names and season labels.
    methods["District"] = methods["District"].astype("string").str.strip()
    sources["District"] = sources["District"].astype("string").str.strip()

    methods["Season"] = methods["Season"].astype("string").str.strip().str.upper()
    sources["Season"] = sources["Season"].astype("string").str.strip().str.upper()

    return methods, sources, method_columns, source_columns


# ============================================================
# 4. CHECK FILES AND LOAD DATA
# ============================================================

missing_files = []

if not METHODS_FILE.exists():
    missing_files.append(str(METHODS_FILE))

if not SOURCES_FILE.exists():
    missing_files.append(str(SOURCES_FILE))

if missing_files:
    st.error(
        "The application could not find the following required file(s):"
    )

    for file_path in missing_files:
        st.code(file_path)

    st.write(
        "Check that both cleaned CSV files are saved in your project's "
        "`outputs` folder."
    )

    st.stop()


try:
    (
        methods,
        sources,
        method_columns,
        source_columns,
    ) = load_data()

except Exception as error:
    st.error("The data files could not be loaded successfully.")
    st.exception(error)
    st.stop()


# ============================================================
# 5. DISTRICT AND SEASON SELECTION
# ============================================================

st.header("📍 Explore a district")

method_districts = set(methods["District"].dropna())
source_districts = set(sources["District"].dropna())

districts = sorted(method_districts & source_districts)

if not districts:
    st.error(
        "No matching district names were found in the two datasets. "
        "Check the District columns in both CSV files."
    )
    st.stop()

available_seasons = sorted(
    set(methods["Season"].dropna())
    & set(sources["Season"].dropna())
)

if not available_seasons:
    st.error("No matching agricultural seasons were found.")
    st.stop()

# High-level overview: these counts describe records in the files,
# not the number of farmers or the severity of water stress.
district_season_count = methods[["District", "Season"]].dropna().drop_duplicates().shape[0]
method_record_count = methods[["District", "Season"]].dropna().shape[0]
source_record_count = sources[["District", "Season"]].dropna().shape[0]

st.subheader("📊 Dataset overview")
overview1, overview2, overview3 = st.columns(3)
overview1.metric("Districts represented", f"{len(districts)}")
overview2.metric("District–season combinations", f"{district_season_count}")
overview3.metric("Method / source records", f"{method_record_count} / {source_record_count}")
st.caption(
    "Counts describe records available in the cleaned files. They do not measure "
    "the number of farmers, water availability, or water-stress severity."
)

col1, col2 = st.columns(2)

with col1:
    selected_district = st.selectbox(
        "Choose a district",
        districts,
    )

with col2:
    selected_season = st.selectbox(
        "Choose an agricultural season",
        available_seasons,
    )


# Get the selected district's records for the chosen season.
method_record = methods[
    (methods["District"] == selected_district)
    & (methods["Season"] == selected_season)
]

source_record = sources[
    (sources["District"] == selected_district)
    & (sources["Season"] == selected_season)
]


# ============================================================
# 6. HELPER FUNCTION FOR SELECTED VALUES
# ============================================================

def get_reported_values(record, columns):
    """
    Return the available numeric values from one district-season record.

    Missing values are excluded rather than treated as zero.
    """

    if record.empty:
        return pd.Series(dtype="float64")

    values = record.iloc[0][columns]
    values = pd.to_numeric(values, errors="coerce")
    values = values.dropna()

    return values


method_values = get_reported_values(
    method_record,
    method_columns,
)

source_values = get_reported_values(
    source_record,
    source_columns,
)


# ============================================================
# 7. IRRIGATION METHODS
# ============================================================

st.divider()
st.header("💧 Irrigation methods")

st.write(
    f"Reported irrigation-method information for "
    f"**{selected_district}**, Season **{selected_season}**."
)

if not method_values.empty:

    method_chart = method_values.sort_values(ascending=False)

    st.bar_chart(method_chart)

    method_table = (
        method_chart
        .rename_axis("Irrigation method")
        .rename("Reported percentage")
        .reset_index()
    )

    st.dataframe(
        method_table,
        use_container_width=True,
        hide_index=True,
    )

    dominant_method = method_values.idxmax()
    dominant_method_value = method_values.max()

    st.metric(
        label="Highest reported irrigation-method value",
        value=f"{dominant_method_value:.2f}%",
        help=(
            "This is the largest available value in the selected "
            "district and season. It does not necessarily mean "
            "that the method is the most effective."
        ),
    )

    st.write(f"**Highest reported method:** {dominant_method}")

else:
    st.warning(
        "No usable irrigation-method values are available for "
        "this district and season."
    )


# ============================================================
# 8. AGRICULTURAL WATER SOURCES
# ============================================================

st.divider()
st.header("🚰 Agricultural water sources")

st.write(
    f"Reported water-source information for "
    f"**{selected_district}**, Season **{selected_season}**."
)

if not source_values.empty:

    source_chart = source_values.sort_values(ascending=False)

    st.bar_chart(source_chart)

    source_table = (
        source_chart
        .rename_axis("Water source")
        .rename("Reported percentage")
        .reset_index()
    )

    st.dataframe(
        source_table,
        use_container_width=True,
        hide_index=True,
    )

    dominant_source = source_values.idxmax()
    dominant_source_value = source_values.max()

    st.metric(
        label="Highest reported water-source value",
        value=f"{dominant_source_value:.2f}%",
        help=(
            "This is the largest available reported value. "
            "It does not establish whether the source is reliable "
            "throughout the dry season."
        ),
    )

    st.write(f"**Highest reported water source:** {dominant_source}")

else:
    st.warning(
        "No usable water-source values are available for "
        "this district and season."
    )


# ============================================================
# 9. DATA QUALITY INFORMATION
# ============================================================

st.divider()
st.header("🔎 Data quality and limitations")

quality_notes = []

if not method_record.empty and "Data_Quality_Note" in methods.columns:
    method_note = method_record.iloc[0]["Data_Quality_Note"]

    if pd.notna(method_note) and str(method_note).strip():
        quality_notes.append(
            ("Irrigation methods", str(method_note).strip())
        )

if not source_record.empty and "Data_Quality_Note" in sources.columns:
    source_note = source_record.iloc[0]["Data_Quality_Note"]

    if pd.notna(source_note) and str(source_note).strip():
        quality_notes.append(
            ("Water sources", str(source_note).strip())
        )

if selected_season == "C":
    st.warning(
        "The irrigation-method dataset has substantial missing "
        "information for Season C. Interpret comparisons involving "
        "this season with caution."
    )

if quality_notes:
    for dataset_name, note in quality_notes:
        st.markdown(f"**{dataset_name}:** {note}")
else:
    st.write(
        "No additional data-quality note was recorded for the "
        "selected district and season. This does not guarantee "
        "that the data is complete."
    )

st.caption(
    "Missing values are kept separate from zero values. A missing "
    "entry means the value is unavailable, not necessarily that "
    "the method or source is absent."
)


# ============================================================
# 10. INITIAL PLANNING INSIGHTS
# ============================================================

st.divider()
st.header("🌾 Planning insights and possible interventions")

st.write(
    "The following suggestions are preliminary options for further "
    "investigation. They are based on the highest reported values, "
    "not on a direct measurement of water shortages."
)

if not method_values.empty:

    st.subheader("Irrigation considerations")

    irrigation_insights = {
        "Traditional techniques": (
            "Assess affordable improvements to water delivery, "
            "irrigation scheduling, and field-level practices."
        ),
        "Surface irrigation": (
            "Investigate channel maintenance and controlled "
            "water delivery where technically suitable."
        ),
        "Flood irrigation": (
            "Assess field levelling and practical ways to control "
            "water application and reduce avoidable losses."
        ),
        "Drip irrigation": (
            "Assess the affordability, maintenance, and suitability "
            "of drip systems for the crops grown locally."
        ),
        "Sprinkler irrigation": (
            "Assess energy costs, wind conditions, evaporation, "
            "and equipment maintenance before expansion."
        ),
        "Pivot irrigation": (
            "Assess infrastructure, energy, land, and maintenance "
            "requirements before considering expansion."
        ),
    }

    st.write(
        irrigation_insights.get(
            method_values.idxmax(),
            "Investigate locally suitable irrigation improvements."
        )
    )

if not source_values.empty:

    st.subheader("Water-source considerations")

    water_insights = {
        "Rainwater": (
            "Investigate rainwater harvesting and covered storage "
            "based on local rainfall and crop-water requirements."
        ),
        "Water catchment": (
            "Assess suitable farm ponds or small reservoirs, "
            "including construction, safety, and environmental costs."
        ),
        "Underground": (
            "Investigate sustainable groundwater availability, "
            "access permissions, pumping costs, and recharge."
        ),
        "Lake / streams": (
            "Assess seasonal availability, legal access, and the "
            "feasibility of storing water when it is available."
        ),
        "Water treatment": (
            "Investigate supply reliability, water suitability, "
            "and costs before considering this source for irrigation."
        ),
    }

    st.write(
        water_insights.get(
            source_values.idxmax(),
            "Investigate reliable and locally suitable water sources."
        )
    )


# ============================================================
# 11. INTERACTIVE IRRIGATION AND WATER-STORAGE PLANNER
# ============================================================

st.divider()
st.header("🌱 Interactive Intervention Planner")

st.write(
    """
    Explore potential combinations of irrigation improvements
    and water-storage options for the selected district and season.

    You can use an automatic preliminary suggestion based on the
    reported data or manually select the interventions you want
    to investigate.
    """
)

st.info(
    "These are preliminary planning suggestions, not verified "
    "recommendations. The reported data does not directly measure "
    "water stress, water reliability, crop yields, or intervention "
    "effectiveness."
)


# ------------------------------------------------------------
# 11.1 DEFINE AVAILABLE INTERVENTIONS
# ------------------------------------------------------------

irrigation_options = {
    "Improve water delivery and scheduling": (
        "Investigate affordable ways to improve water delivery, "
        "schedule irrigation according to crop needs, and reduce "
        "avoidable water losses."
    ),
    "Improve surface irrigation channels": (
        "Assess channel maintenance, controlled water distribution, "
        "and field-level improvements where technically suitable."
    ),
    "Improve flood irrigation management": (
        "Investigate field levelling and practical ways to control "
        "water application and reduce avoidable losses."
    ),
    "Introduce or improve drip irrigation": (
        "Assess drip irrigation for suitable crops, including "
        "installation costs, maintenance, filtration, and affordability."
    ),
    "Improve sprinkler irrigation": (
        "Assess wind conditions, evaporation, pumping energy, "
        "equipment costs, and maintenance requirements."
    ),
    "Assess centre-pivot irrigation": (
        "Investigate whether land size, infrastructure, energy "
        "requirements, and maintenance costs make this option feasible."
    ),
    "Assess locally suitable irrigation methods": (
        "Collect additional information about local crops, water "
        "availability, terrain, existing equipment, and farmer needs "
        "before selecting an irrigation improvement."
    ),
}

storage_options = {
    "Rainwater harvesting and covered storage": (
        "Investigate collecting rainfall and storing it in suitable "
        "covered tanks or other safe structures. Assess rainfall "
        "patterns, storage capacity, construction costs, and crop needs."
    ),
    "Small farm ponds or reservoirs": (
        "Assess whether a farm pond or small reservoir is technically "
        "and environmentally suitable. Check land availability, "
        "evaporation, safety, construction costs, and water permissions."
    ),
    "Sustainable groundwater supply and storage": (
        "Investigate groundwater availability, recharge, abstraction "
        "permissions, pumping costs, and whether storage would be "
        "practical for the intended farming system."
    ),
    "Seasonal surface-water collection and storage": (
        "Investigate the seasonal availability of lake or stream water, "
        "legal access, abstraction requirements, and the feasibility "
        "of storing water when supplies are available."
    ),
    "Assess treated-water supply and storage": (
        "Investigate supply reliability, water suitability, costs, "
        "and whether using treated water for irrigation is appropriate."
    ),
    "Assess locally suitable water-management options": (
        "Collect local rainfall, water-availability, crop-demand, "
        "cost, and environmental information before choosing a "
        "water-storage or supply intervention."
    ),
}


# ------------------------------------------------------------
# 11.2 CONNECT REPORTED PATTERNS TO PRELIMINARY SUGGESTIONS
# ------------------------------------------------------------

# These mappings provide a starting point for investigation.
# They do not prove that a particular intervention is necessary.

method_to_improvement = {
    "Traditional techniques":
        "Improve water delivery and scheduling",

    "Surface irrigation":
        "Improve surface irrigation channels",

    "Flood irrigation":
        "Improve flood irrigation management",

    "Drip irrigation":
        "Introduce or improve drip irrigation",

    "Sprinkler irrigation":
        "Improve sprinkler irrigation",

    "Pivot irrigation":
        "Assess centre-pivot irrigation",
}

source_to_storage = {
    "Rainwater":
        "Rainwater harvesting and covered storage",

    "Water catchment":
        "Small farm ponds or reservoirs",

    "Underground":
        "Sustainable groundwater supply and storage",

    "Lake / streams":
        "Seasonal surface-water collection and storage",

    "Water treatment":
        "Assess treated-water supply and storage",
}


# ------------------------------------------------------------
# 11.3 CHOOSE PLANNING MODE
# ------------------------------------------------------------

planning_mode = st.radio(
    "How would you like to develop a strategy?",
    [
        "Automatic preliminary suggestion",
        "Manual intervention selection",
    ],
    horizontal=False,
    key="planning_mode",
)


# ------------------------------------------------------------
# 11.4 PREPARE AUTOMATIC SUGGESTIONS
# ------------------------------------------------------------

dominant_method = None
dominant_source = None

if not method_values.empty:
    dominant_method = method_values.idxmax()

if not source_values.empty:
    dominant_source = source_values.idxmax()


automatic_irrigation = method_to_improvement.get(
    dominant_method,
    "Assess locally suitable irrigation methods",
)

automatic_storage = source_to_storage.get(
    dominant_source,
    "Assess locally suitable water-management options",
)


# ------------------------------------------------------------
# 11.5 AUTOMATIC OR MANUAL SELECTION
# ------------------------------------------------------------

if planning_mode == "Automatic preliminary suggestion":

    st.subheader("🤖 Preliminary data-informed suggestion")

    if dominant_method is not None:
        st.write(
            f"**Highest reported irrigation-method value:** "
            f"{dominant_method}"
        )
    else:
        st.warning(
            "No usable irrigation-method values are available "
            "for the selected district and season."
        )

    if dominant_source is not None:
        st.write(
            f"**Highest reported water-source value:** "
            f"{dominant_source}"
        )
    else:
        st.warning(
            "No usable water-source values are available "
            "for the selected district and season."
        )

    selected_improvement = automatic_irrigation
    selected_storage = automatic_storage

    st.caption(
        "The automatic suggestion uses the largest available "
        "reported values as a starting point. It does not establish "
        "that the selected method or source is causing water stress."
    )

else:

    st.subheader("🛠️ Build your own intervention combination")

    st.write(
        "Choose the interventions you would like to investigate. "
        "Your choices do not change the original reported data."
    )

    selected_improvement = st.selectbox(
        "Choose an irrigation improvement",
        options=list(irrigation_options.keys()),
        index=list(irrigation_options.keys()).index(
            automatic_irrigation
        ),
        key="manual_irrigation_choice",
    )

    selected_storage = st.selectbox(
        "Choose a water-storage or supply option",
        options=list(storage_options.keys()),
        index=list(storage_options.keys()).index(
            automatic_storage
        ),
        key="manual_storage_choice",
    )


# ------------------------------------------------------------
# 11.6 DISPLAY THE COMBINED PLANNING SUMMARY
# ------------------------------------------------------------

st.divider()
st.subheader("📋 Your combined intervention strategy")

st.write(
    f"**Planning area:** {selected_district}"
)

st.write(
    f"**Agricultural season:** {selected_season}"
)

st.markdown("### 1. Irrigation improvement")

st.markdown(f"**{selected_improvement}**")

st.write(
    irrigation_options[selected_improvement]
)

st.markdown("### 2. Water-storage or supply option")

st.markdown(f"**{selected_storage}**")

st.write(
    storage_options[selected_storage]
)


# ------------------------------------------------------------
# 11.7 FEASIBILITY CHECKS
# ------------------------------------------------------------

st.markdown("### 3. Checks before implementation")

st.write(
    "Before recommending or implementing this combination, "
    "investigate the following local conditions:"
)

feasibility_checks = [
    "Dry-season water availability and reliability",
    "Local rainfall patterns and potential storage capacity",
    "Crop types, crop-water requirements, and growing seasons",
    "Installation, construction, pumping, and maintenance costs",
    "Farmer affordability and access to technical support",
    "Environmental impacts, water permissions, and safety",
]

for check in feasibility_checks:
    st.checkbox(
        check,
        key=f"planner_check_{check}",
    )

st.caption(
    "These checkboxes are a planning checklist, not evidence "
    "that a condition has been verified. Selecting an item "
    "does not mean that the intervention is feasible."
)


# ------------------------------------------------------------
# 11.8 INTERPRETATION AND LIMITATIONS
# ------------------------------------------------------------

st.markdown("### 4. How to interpret this strategy")

if planning_mode == "Automatic preliminary suggestion":

    st.write(
        "This combination was generated from the largest available "
        "reported irrigation-method and water-source values for "
        "the selected district and season. The largest reported "
        "value is not necessarily the most suitable intervention."
    )

else:

    st.write(
        "This combination reflects the options you selected. "
        "It is a proposed scenario for investigation, not a "
        "prediction of its performance or a confirmed local need."
    )

st.warning(
    "The current dataset does not directly measure water stress, "
    "dry-season source reliability, crop yields, intervention costs, "
    "or the effectiveness of proposed solutions. Additional local "
    "evidence is required before ranking or implementing strategies."
)


# ============================================================
# 12. ADDITIONAL DATA NEEDED FOR BETTER DECISIONS
# ============================================================

st.divider()
st.header("📌 What should be considered next?")

st.write(
    """
    To make stronger and more reliable irrigation-planning decisions,
    the application should eventually incorporate additional evidence:
    """
)

st.markdown(
    """
    - **Rainfall data:** How much rain does the district receive, and when?
    - **Dry-season water availability:** Are rivers, reservoirs, and
      groundwater sources reliable when crops need water?
    - **Crop requirements:** Which crops are grown, and how much water
      do they need at different growth stages?
    - **Storage feasibility:** Can water be collected and stored safely
      and economically?
    - **Affordability:** What are the installation, energy, and
      maintenance costs for farmers?
    - **Local conditions:** Are the proposed interventions suitable
      for local terrain, environmental requirements, and farming systems?
    """
)

st.warning(
    "The current dataset supports exploration of reported irrigation "
    "methods and water sources. It is not yet sufficient to rank "
    "districts by actual water-stress severity."
)


# ============================================================
# 13. FOOTER
# ============================================================

st.divider()

st.caption(
    "NISR Big Data Hackathon 2026 | Agricultural Productivity Track"
)

st.caption(
    "Data-driven exploration for climate-resilient agricultural planning in Rwanda."
)
