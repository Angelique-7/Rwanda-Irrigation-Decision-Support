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

method_districts = set(methods["District"].dropna())
source_districts = set(sources["District"].dropna())
districts = sorted(method_districts & source_districts)
available_seasons = sorted(set(methods["Season"].dropna()) & set(sources["Season"].dropna()))

st.markdown("## Choose a district")
st.markdown(
    "<p class='section-note'>Pick any district to see all reported irrigation and water-source data for it.</p>",
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
        help="Choose 'All seasons' to view every season reported for this district.",
    )

district_methods = methods[methods["District"] == selected_district].sort_values("Season")
district_sources = sources[sources["District"] == selected_district].sort_values("Season")

if selected_scope == "All seasons":
    method_record = district_methods
    source_record = district_sources
    scope_label = "All seasons"
else:
    method_record = district_methods[district_methods["Season"] == selected_scope]
    source_record = district_sources[district_sources["Season"] == selected_scope]
    scope_label = f"Season {selected_scope}"

season_count = district_methods["Season"].nunique()

st.markdown("## Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Selected district", selected_district)
col2.metric("Season scope", scope_label)
col3.metric("Seasons available", season_count)
col4.metric("Total districts", len(districts))

st.divider()

st.markdown("## Irrigation methods analysis")
st.markdown(
    f"<p class='section-note'>Location: <strong>{selected_district}</strong> &middot; "
    f"Scope: <strong>{scope_label}</strong></p>",
    unsafe_allow_html=True,
)

if method_record.empty:
    st.warning("No records found for this district-season scope.")
elif selected_scope == "All seasons":
    chart_col, table_col = st.columns([2, 1])

    with chart_col:
        method_long = method_record.melt(
            id_vars=["Season"],
            value_vars=method_columns,
            var_name="Irrigation method",
            value_name="Percentage",
        ).dropna(subset=["Percentage"])

        if method_long.empty:
            st.warning("No irrigation method data available for this district.")
        else:
            fig = px.bar(
                method_long,
                x="Season",
                y="Percentage",
                color="Irrigation method",
                barmode="group",
                title=f"Irrigation methods in {selected_district} by season",
                color_discrete_sequence=METHOD_COLORS,
                labels={"Percentage": "Percentage (%)"},
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#1f2d24",
                title_font_color="#14532d",
                legend_title_text="Irrigation method",
                margin=dict(t=60, l=10, r=10, b=10),
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(gridcolor="#e6efe8")
            st.plotly_chart(fig, width="stretch")

    with table_col:
        st.markdown("### Breakdown by season")
        method_table = method_record.set_index("Season")[method_columns].round(2)
        method_table.insert(
            0,
            "Dominant method",
            method_table.apply(
                lambda row: row.idxmax() if row.notna().any() else "No data",
                axis=1,
            ),
        )
        st.dataframe(method_table, width="stretch")

        overall_methods = method_record[method_columns].mean(skipna=True).dropna()
        if not overall_methods.empty:
            st.metric(
                "Dominant method (average)",
                overall_methods.idxmax(),
                f"{overall_methods.max():.2f}%",
            )
else:
    method_vals = method_record.iloc[0][method_columns].dropna()
    if method_vals.empty:
        st.warning("No irrigation method data available for this selection.")
    else:
        chart_col, table_col = st.columns([2, 1])

        with chart_col:
            fig = px.bar(
                x=method_vals.index,
                y=method_vals.values,
                labels={"x": "Irrigation method", "y": "Percentage (%)"},
                title=f"Irrigation methods in {selected_district} - Season {selected_scope}",
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

st.divider()

st.markdown("## Agricultural water sources analysis")
st.markdown(
    f"<p class='section-note'>Location: <strong>{selected_district}</strong> &middot; "
    f"Scope: <strong>{scope_label}</strong></p>",
    unsafe_allow_html=True,
)

if source_record.empty:
    st.warning("No records found for this district-season scope.")
elif selected_scope == "All seasons":
    chart_col, table_col = st.columns([2, 1])

    with chart_col:
        source_long = source_record.melt(
            id_vars=["Season"],
            value_vars=source_columns,
            var_name="Water source",
            value_name="Percentage",
        ).dropna(subset=["Percentage"])

        if source_long.empty:
            st.warning("No water source data available for this district.")
        else:
            fig = px.bar(
                source_long,
                x="Season",
                y="Percentage",
                color="Water source",
                barmode="group",
                title=f"Water sources in {selected_district} by season",
                color_discrete_sequence=SOURCE_COLORS,
                labels={"Percentage": "Percentage (%)"},
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#1f2d24",
                title_font_color="#14532d",
                legend_title_text="Water source",
                margin=dict(t=60, l=10, r=10, b=10),
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(gridcolor="#e6efe8")
            st.plotly_chart(fig, width="stretch")

    with table_col:
        st.markdown("### Breakdown by season")
        source_table = source_record.set_index("Season")[source_columns].round(2)
        source_table.insert(
            0,
            "Primary source",
            source_table.apply(
                lambda row: row.idxmax() if row.notna().any() else "No data",
                axis=1,
            ),
        )
        st.dataframe(source_table, width="stretch")

        overall_sources = source_record[source_columns].mean(skipna=True).dropna()
        if not overall_sources.empty:
            st.metric(
                "Primary source (average)",
                overall_sources.idxmax(),
                f"{overall_sources.max():.2f}%",
            )
else:
    source_vals = source_record.iloc[0][source_columns].dropna()
    if source_vals.empty:
        st.warning("No water source data available for this selection.")
    else:
        chart_col, table_col = st.columns([2, 1])

        with chart_col:
            fig = px.pie(
                values=source_vals.values,
                names=source_vals.index,
                title=f"Water sources in {selected_district} - Season {selected_scope}",
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

st.divider()

st.markdown("## Data quality and notes")
quality_notes = []
if "Data_Quality_Note" in methods.columns:
    for _, row in method_record.iterrows():
        note = row.get("Data_Quality_Note")
        if pd.notna(note) and str(note).strip():
            quality_notes.append(("Irrigation methods", row["Season"], str(note).strip()))
if "Data_Quality_Note" in sources.columns:
    for _, row in source_record.iterrows():
        note = row.get("Data_Quality_Note")
        if pd.notna(note) and str(note).strip():
            quality_notes.append(("Water sources", row["Season"], str(note).strip()))

if quality_notes:
    for dataset, season, note in quality_notes:
        st.info(f"**{dataset} (Season {season}):** {note}")
else:
    st.success("No specific data quality notes recorded for this selection.")

seasons_in_scope = set(method_record["Season"]) if selected_scope == "All seasons" else {selected_scope}
if "C" in seasons_in_scope:
    st.warning("Season C has substantial missing data. Interpret results with caution.")

render_footer()
