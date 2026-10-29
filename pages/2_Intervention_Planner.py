"""
Intervention Planner - Rwanda Irrigation Decision Support System
Smart recommendations for irrigation improvements and water storage solutions
"""

import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import pandas as pd
import streamlit as st

from ui import (
    apply_theme,
    render_footer,
    render_header,
    render_page_heading,
    svg_icon,
)

st.set_page_config(
    page_title="Intervention Planner | Rwanda Irrigation DSS",
    page_icon=":material/lightbulb:",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
render_header("Intervention Planner")
render_page_heading(
    "lightbulb",
    "Intervention Planner",
    "Smart recommendations for climate-resilient irrigation solutions",
)

OUTPUTS_DIR = PROJECT_DIR / "Outputs"
METHODS_FILE = OUTPUTS_DIR / "cleaned_irrigation_methods_by_district.csv"
SOURCES_FILE = OUTPUTS_DIR / "cleaned_irrigation_water_sources_by_district.csv"

PLANNING_MODES = [
    ":material/smart_toy: AI-powered recommendation",
    ":material/back_hand: Custom strategy builder",
]


@st.cache_data
def load_data():
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


if not METHODS_FILE.exists() or not SOURCES_FILE.exists():
    st.error("Data files not found. Please ensure cleaned CSV files are in the Outputs folder.")
    render_footer()
    st.stop()

methods, sources, method_columns, source_columns = load_data()

method_districts = set(methods["District"].dropna())
source_districts = set(sources["District"].dropna())
districts = sorted(method_districts & source_districts)
available_seasons = sorted(set(methods["Season"].dropna()) & set(sources["Season"].dropna()))

st.markdown("## Planning parameters")
st.markdown(
    "<p class='section-note'>Pick any district to build recommendations for it.</p>",
    unsafe_allow_html=True,
)
filter_col1, filter_col2 = st.columns([1.2, 1])
with filter_col1:
    selected_district = st.selectbox("Select district", districts, key="district_filter")
with filter_col2:
    scope_options = ["All seasons"] + available_seasons
    selected_scope = st.selectbox(
        "Select season scope",
        scope_options,
        key="season_scope",
        help="Choose 'All seasons' to base the plan on the district's combined averages.",
    )

district_methods = methods[methods["District"] == selected_district]
district_sources = sources[sources["District"] == selected_district]

if selected_scope == "All seasons":
    method_records = district_methods
    source_records = district_sources
    scope_label = "All seasons (combined)"
else:
    method_records = district_methods[district_methods["Season"] == selected_scope]
    source_records = district_sources[district_sources["Season"] == selected_scope]
    scope_label = f"Season {selected_scope}"

seasons_used = sorted(method_records["Season"].dropna().unique())
method_vals = (
    method_records[method_columns].mean(skipna=True).dropna()
    if not method_records.empty
    else pd.Series(dtype=float)
)
source_vals = (
    source_records[source_columns].mean(skipna=True).dropna()
    if not source_records.empty
    else pd.Series(dtype=float)
)

st.markdown("## Current situation assessment")
col1, col2 = st.columns(2, gap="medium")

with col1:
    if not method_vals.empty:
        dom_method = method_vals.idxmax()
        st.markdown(
            f"""
            <div class="panel-card">
                <span class="feature-icon">{svg_icon("droplet", 21)}</span>
                <h4>Dominant irrigation method</h4>
                <p><strong style="color:#14532d;font-size:1.05rem;">{dom_method}</strong>
                &middot; {method_vals.max():.2f}% of reported practices</p>
                <p style="margin-top:0.5rem;">Scope: {scope_label} &middot; {len(seasons_used)} season(s) assessed.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("No irrigation method data available for this selection.")

with col2:
    if not source_vals.empty:
        dom_source = source_vals.idxmax()
        st.markdown(
            f"""
            <div class="panel-card">
                <span class="feature-icon">{svg_icon("database", 21)}</span>
                <h4>Primary water source</h4>
                <p><strong style="color:#14532d;font-size:1.05rem;">{dom_source}</strong>
                &middot; {source_vals.max():.2f}% of reported sources</p>
                <p style="margin-top:0.5rem;">Scope: {scope_label} &middot; {len(seasons_used)} season(s) assessed.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("No water source data available for this selection.")

st.divider()

st.markdown("## Intervention strategy development")

planning_mode = st.radio(
    "Choose planning approach",
    PLANNING_MODES,
    horizontal=True,
)

method_to_improvement = {
    "Traditional techniques": "Improve water delivery and irrigation scheduling",
    "Surface irrigation": "Modernize surface irrigation channels and control systems",
    "Flood irrigation": "Optimize flood irrigation with better field management",
    "Drip irrigation": "Expand and optimize drip irrigation systems",
    "Sprinkler irrigation": "Enhance sprinkler irrigation efficiency",
    "Pivot irrigation": "Evaluate and optimize pivot irrigation infrastructure",
}

source_to_storage = {
    "Rainwater": "Rainwater harvesting with covered storage tanks",
    "Water catchment": "Construct farm ponds and water catchment structures",
    "Underground": "Sustainable groundwater abstraction with storage",
    "Lake / streams": "Seasonal water storage from surface sources",
    "Water treatment": "Treated water storage and distribution systems",
}

if planning_mode == PLANNING_MODES[0]:
    st.markdown("### Data-driven recommendations")

    if not method_vals.empty and not source_vals.empty:
        dom_method = method_vals.idxmax()
        dom_source = source_vals.idxmax()

        rec_irrigation = method_to_improvement.get(
            dom_method, "Assess locally suitable irrigation improvements"
        )
        rec_storage = source_to_storage.get(
            dom_source, "Develop an integrated water management approach"
        )

        rec_col1, rec_col2 = st.columns(2, gap="medium")
        with rec_col1:
            st.markdown(
                f"""
                <div class="panel-card">
                    <span class="feature-icon">{svg_icon("droplet", 21)}</span>
                    <h4>Recommended irrigation improvement</h4>
                    <p style="color:#14532d;font-weight:600;">{rec_irrigation}</p>
                    <p style="margin-top:0.5rem;">Based on the dominant irrigation method for {scope_label}.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with rec_col2:
            st.markdown(
                f"""
                <div class="panel-card">
                    <span class="feature-icon">{svg_icon("database", 21)}</span>
                    <h4>Recommended water storage solution</h4>
                    <p style="color:#14532d;font-weight:600;">{rec_storage}</p>
                    <p style="margin-top:0.5rem;">Based on the primary water source for {scope_label}.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.success(f"Recommendations generated from the reported irrigation patterns for {scope_label}.")
    else:
        st.warning("Insufficient data for automated recommendations.")

else:
    st.markdown("### Build a custom strategy")

    irrigation_options = [
        "Improve water delivery and irrigation scheduling",
        "Modernize surface irrigation channels and control systems",
        "Optimize flood irrigation with better field management",
        "Expand and optimize drip irrigation systems",
        "Enhance sprinkler irrigation efficiency",
        "Evaluate and optimize pivot irrigation infrastructure",
        "Introduce precision irrigation technologies",
    ]

    storage_options = [
        "Rainwater harvesting with covered storage tanks",
        "Construct farm ponds and water catchment structures",
        "Sustainable groundwater abstraction with storage",
        "Seasonal water storage from surface sources",
        "Treated water storage and distribution systems",
        "Multi-purpose water reservoirs",
        "Integrated water harvesting systems",
    ]

    select_col1, select_col2 = st.columns(2, gap="medium")
    with select_col1:
        selected_irrigation = st.selectbox("Select irrigation improvement", irrigation_options)
    with select_col2:
        selected_storage = st.selectbox("Select water storage solution", storage_options)

    st.markdown(
        f"""
        <div class="panel-card">
            <h4>Your custom strategy</h4>
            <p style="margin-bottom:0.4rem;"><strong>District:</strong> {selected_district}
            &nbsp;&middot;&nbsp; <strong>Scope:</strong> {scope_label}</p>
            <p style="margin-bottom:0.4rem;"><strong>Irrigation:</strong> {selected_irrigation}</p>
            <p><strong>Water storage:</strong> {selected_storage}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown("## Feasibility assessment checklist")
st.markdown(
    "<p class='section-note'>Before implementation, verify the following critical factors.</p>",
    unsafe_allow_html=True,
)

feasibility_items = [
    ("water_drop", "Water availability", "Assess dry-season water reliability and quantity"),
    ("rainy", "Climate data", "Analyze local rainfall patterns and variability"),
    ("agriculture", "Crop requirements", "Match solutions to local crops and growing cycles"),
    ("payments", "Economic viability", "Evaluate costs, financing, and farmer affordability"),
    ("build", "Technical capacity", "Assess maintenance skills and spare parts availability"),
    ("gavel", "Regulatory compliance", "Check water rights, permits, and environmental regulations"),
    ("groups", "Community acceptance", "Ensure farmer buy-in and adoption potential"),
    ("public", "Environmental impact", "Consider sustainability and ecosystem effects"),
]

for icon_name, title, description in feasibility_items:
    st.checkbox(
        f":material/{icon_name}: **{title}** - {description}",
        key=f"feasibility_{title}",
    )

st.divider()

st.markdown("## Important considerations")
st.info("""
**Planning guidelines:**
- This tool provides data-informed suggestions based on reported patterns, not absolute recommendations.
- Additional local assessment is essential before implementation.
- Consider seasonal variations and long-term climate projections.
- Engage local stakeholders and technical experts in final decision-making.
- Factor in maintenance costs and long-term sustainability.
""")

render_footer()
