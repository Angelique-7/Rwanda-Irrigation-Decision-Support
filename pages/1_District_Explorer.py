"""
District Explorer - Rwanda Irrigation Decision Support System
Detailed analysis of irrigation methods and water sources by district
"""

import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import pandas as pd
import plotly.express as px
import streamlit as st

from ui import (
    apply_theme,
    render_footer,
    render_header,
    render_page_heading,
    render_sidebar_credit,
)

st.set_page_config(
    page_title="District Explorer | Rwanda Irrigation DSS",
    page_icon=":material/map:",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
render_header("District Explorer")
render_page_heading(
    "map",
    "District Explorer",
    "Comprehensive analysis of irrigation patterns by district and season",
)

OUTPUTS_DIR = PROJECT_DIR / "Outputs"
METHODS_FILE = OUTPUTS_DIR / "cleaned_irrigation_methods_by_district.csv"
SOURCES_FILE = OUTPUTS_DIR / "cleaned_irrigation_water_sources_by_district.csv"

METHOD_COLORS = ["#166534", "#15803d", "#16a34a", "#22c55e", "#4ade80", "#86efac"]
SOURCE_COLORS = ["#14532d", "#166534", "#15803d", "#22c55e", "#4ade80"]


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

st.sidebar.markdown("### :material/tune: Filter analysis")
method_districts = set(methods["District"].dropna())
source_districts = set(sources["District"].dropna())
districts = sorted(method_districts & source_districts)
available_seasons = sorted(set(methods["Season"].dropna()) & set(sources["Season"].dropna()))

selected_district = st.sidebar.selectbox("Select district", districts)
selected_season = st.sidebar.selectbox("Select agricultural season", available_seasons)
render_sidebar_credit()

method_record = methods[
    (methods["District"] == selected_district) & (methods["Season"] == selected_season)
]
source_record = sources[
    (sources["District"] == selected_district) & (sources["Season"] == selected_season)
]

st.markdown("## Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Selected district", selected_district)
col2.metric("Agricultural season", selected_season)
col3.metric("Total districts", len(districts))
col4.metric("Total seasons", len(available_seasons))

st.divider()

st.markdown("## Irrigation methods analysis")
st.markdown(
    f"<p class='section-note'>Location: <strong>{selected_district}</strong> &middot; "
    f"Season: <strong>{selected_season}</strong></p>",
    unsafe_allow_html=True,
)

if not method_record.empty:
    method_vals = method_record.iloc[0][method_columns].dropna()
    if not method_vals.empty:
        chart_col, table_col = st.columns([2, 1])

        with chart_col:
            fig = px.bar(
                x=method_vals.index,
                y=method_vals.values,
                labels={"x": "Irrigation method", "y": "Percentage (%)"},
                title=f"Irrigation methods in {selected_district} - Season {selected_season}",
                color=method_vals.values,
                color_continuous_scale="Greens",
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#1f2d24",
                title_font_color="#14532d",
                coloraxis_showscale=False,
                margin=dict(t=60, l=10, r=10, b=10),
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(gridcolor="#e6efe8")
            st.plotly_chart(fig, width="stretch")

        with table_col:
            st.markdown("### Method breakdown")
            method_df = pd.DataFrame(
                {
                    "Irrigation method": method_vals.index,
                    "Percentage": method_vals.values,
                }
            ).sort_values("Percentage", ascending=False)
            method_df["Percentage"] = method_df["Percentage"].round(2)
            st.dataframe(method_df, hide_index=True, width="stretch")

            dominant = method_vals.idxmax()
            st.metric("Dominant method", dominant, f"{method_vals.max():.2f}%")
    else:
        st.warning("No irrigation method data available for this selection.")
else:
    st.warning("No records found for this district-season combination.")

st.divider()

st.markdown("## Agricultural water sources analysis")
st.markdown(
    f"<p class='section-note'>Location: <strong>{selected_district}</strong> &middot; "
    f"Season: <strong>{selected_season}</strong></p>",
    unsafe_allow_html=True,
)

if not source_record.empty:
    source_vals = source_record.iloc[0][source_columns].dropna()
    if not source_vals.empty:
        chart_col, table_col = st.columns([2, 1])

        with chart_col:
            fig = px.pie(
                values=source_vals.values,
                names=source_vals.index,
                title=f"Water sources in {selected_district} - Season {selected_season}",
                color_discrete_sequence=SOURCE_COLORS,
                hole=0.42,
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#1f2d24",
                title_font_color="#14532d",
                legend_title_text="Water source",
                margin=dict(t=60, l=10, r=10, b=10),
            )
            st.plotly_chart(fig, width="stretch")

        with table_col:
            st.markdown("### Source breakdown")
            source_df = pd.DataFrame(
                {
                    "Water source": source_vals.index,
                    "Percentage": source_vals.values,
                }
            ).sort_values("Percentage", ascending=False)
            source_df["Percentage"] = source_df["Percentage"].round(2)
            st.dataframe(source_df, hide_index=True, width="stretch")

            dominant_src = source_vals.idxmax()
            st.metric("Primary water source", dominant_src, f"{source_vals.max():.2f}%")
    else:
        st.warning("No water source data available for this selection.")
else:
    st.warning("No records found for this district-season combination.")

st.divider()

st.markdown("## Data quality and notes")
quality_notes = []
if not method_record.empty and "Data_Quality_Note" in methods.columns:
    note = method_record.iloc[0].get("Data_Quality_Note")
    if pd.notna(note) and str(note).strip():
        quality_notes.append(("Irrigation methods", str(note).strip()))
if not source_record.empty and "Data_Quality_Note" in sources.columns:
    note = source_record.iloc[0].get("Data_Quality_Note")
    if pd.notna(note) and str(note).strip():
        quality_notes.append(("Water sources", str(note).strip()))

if quality_notes:
    for dataset, note in quality_notes:
        st.info(f"**{dataset}:** {note}")
else:
    st.success("No specific data quality notes recorded for this selection.")

if selected_season == "C":
    st.warning("Season C has substantial missing data. Interpret results with caution.")

render_footer()
