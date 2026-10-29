"""
Rwanda Irrigation Decision Support System
A professional data-driven tool for climate-resilient agricultural planning
"""

import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import pandas as pd
import streamlit as st

from ui import apply_theme, render_footer, render_header, render_hero, svg_icon

st.set_page_config(
    page_title="Rwanda Irrigation Decision Support System",
    page_icon=":material/water_drop:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_theme()
render_header("Home")
render_hero()

OUTPUTS_DIR = PROJECT_DIR / "Outputs"
METHODS_FILE = OUTPUTS_DIR / "cleaned_irrigation_methods_by_district.csv"
SOURCES_FILE = OUTPUTS_DIR / "cleaned_irrigation_water_sources_by_district.csv"


@st.cache_data
def load_data():
    """Load and preprocess irrigation data."""
    if not METHODS_FILE.exists() or not SOURCES_FILE.exists():
        return None, None, None, None

    methods = pd.read_csv(METHODS_FILE)
    sources = pd.read_csv(SOURCES_FILE)

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

    for col in method_columns:
        methods[col] = pd.to_numeric(methods[col], errors="coerce")
    for col in source_columns:
        sources[col] = pd.to_numeric(sources[col], errors="coerce")

    methods["District"] = methods["District"].astype(str).str.strip()
    sources["District"] = sources["District"].astype(str).str.strip()
    methods["Season"] = methods["Season"].astype(str).str.strip().str.upper()
    sources["Season"] = sources["Season"].astype(str).str.strip().str.upper()

    return methods, sources, method_columns, source_columns


methods, sources, method_columns, source_columns = load_data()

st.markdown("## Platform overview")

if methods is not None:
    districts = sorted(set(methods["District"].dropna()) & set(sources["District"].dropna()))
    seasons = sorted(set(methods["Season"].dropna()) & set(sources["Season"].dropna()))

    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    stat_col1.metric("Districts covered", len(districts))
    stat_col2.metric("Agricultural seasons", len(seasons))
    stat_col3.metric("Survey records", len(methods) + len(sources))
    stat_col4.metric("Datasets integrated", 2)
else:
    st.warning("Cleaned data files were not found in the Outputs folder. Add them to populate the dashboard.")

st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

mission_col, capability_col = st.columns([1, 1.15], gap="large")

with mission_col:
    st.markdown(
        """
        <div class="panel-card">
            <h4>Our mission</h4>
            <p>
                Empower agricultural planners, policymakers, and farmers with evidence-based insight
                into irrigation methods and water sources across Rwanda's districts, supporting
                climate-resilient food systems and better-targeted investment.
            </p>
            <p style="margin-top:0.9rem;">
                The platform is designed for exploration and planning support. It should be combined
                with local expertise and field validation before decisions are made.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with capability_col:
    st.markdown(
        """
        <div class="panel-card">
            <h4>What you can do</h4>
            <ul class="feature-list">
                <li>Compare irrigation methods and water-source patterns by district and season.</li>
                <li>Identify dominant practices and data-quality gaps before planning.</li>
                <li>Generate practical, rule-based intervention and water-storage options.</li>
                <li>Review methodology, limitations, and usage guidance for defensible decisions.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("## Platform capabilities")

features = [
    (
        "map",
        "District intelligence",
        "Explore irrigation and water-source profiles for every district and agricultural season.",
    ),
    (
        "lightbulb",
        "Intervention planning",
        "Translate dominant practices into targeted irrigation and water-storage improvements.",
    ),
    (
        "database",
        "Evidence and transparency",
        "Understand the data source, processing steps, limitations, and responsible use guidance.",
    ),
]

feature_cols = st.columns(3, gap="medium")
for column, (icon_name, title, description) in zip(feature_cols, features):
    with column:
        st.markdown(
            f"""
            <div class="feature-card">
                <span class="feature-icon">{svg_icon(icon_name, 21)}</span>
                <h4>{title}</h4>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("## Explore the platform")

nav_cards = [
    (
        "/District_Explorer",
        "map",
        "District Explorer",
        "Detailed irrigation method and water-source analysis with seasonal comparisons.",
    ),
    (
        "/Intervention_Planner",
        "lightbulb",
        "Intervention Planner",
        "Build a practical strategy and work through a feasibility assessment checklist.",
    ),
    (
        "/About_the_Data",
        "database",
        "About the Data",
        "Data sources, methodology, limitations, and responsible usage guidelines.",
    ),
]

nav_cols = st.columns(3, gap="medium")
for column, (href, icon_name, title, description) in zip(nav_cols, nav_cards):
    with column:
        st.markdown(
            f"""
            <a class="nav-card" href="{href}" target="_self">
                <span class="nav-card-title">{svg_icon(icon_name, 18)} {title}</span>
                <p>{description}</p>
            </a>
            """,
            unsafe_allow_html=True,
        )

render_footer()
