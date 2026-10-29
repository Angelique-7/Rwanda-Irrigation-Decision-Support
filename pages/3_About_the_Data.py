"""
About the Data - Rwanda Irrigation Decision Support System
Data sources, methodology, and usage guidelines
"""

import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import pandas as pd
import streamlit as st

from ui import apply_theme, render_footer, render_header, render_page_heading, svg_icon

st.set_page_config(
    page_title="About the Data | Rwanda Irrigation DSS",
    page_icon=":material/info:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_theme()
render_header("About the Data")
render_page_heading(
    "database",
    "About the Data",
    "Data sources, methodology, limitations, and usage guidelines",
)

OUTPUTS_DIR = PROJECT_DIR / "Outputs"
METHODS_FILE = OUTPUTS_DIR / "cleaned_irrigation_methods_by_district.csv"
SOURCES_FILE = OUTPUTS_DIR / "cleaned_irrigation_water_sources_by_district.csv"


@st.cache_data
def load_data_summary():
    try:
        methods = pd.read_csv(METHODS_FILE)
        sources = pd.read_csv(SOURCES_FILE)
        return methods, sources
    except Exception:
        return None, None


methods, sources = load_data_summary()

st.markdown("## Data overview")

overview_col1, overview_col2 = st.columns(2, gap="medium")

with overview_col1:
    method_stats = ""
    if methods is not None:
        method_stats = (
            f"<p><strong>Records:</strong> {len(methods)}</p>"
            f"<p><strong>Districts:</strong> {methods['District'].nunique()}</p>"
            f"<p><strong>Seasons:</strong> {methods['Season'].nunique()}</p>"
        )
    st.markdown(
        f"""
        <div class="panel-card">
            <span class="feature-icon">{svg_icon("droplet", 21)}</span>
            <h4>Irrigation methods dataset</h4>
            {method_stats}
            <p><strong>Methods covered:</strong> Surface, flood, drip, sprinkler, pivot,
            and traditional techniques.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with overview_col2:
    source_stats = ""
    if sources is not None:
        source_stats = (
            f"<p><strong>Records:</strong> {len(sources)}</p>"
            f"<p><strong>Districts:</strong> {sources['District'].nunique()}</p>"
            f"<p><strong>Seasons:</strong> {sources['Season'].nunique()}</p>"
        )
    st.markdown(
        f"""
        <div class="panel-card">
            <span class="feature-icon">{svg_icon("database", 21)}</span>
            <h4>Water sources dataset</h4>
            {source_stats}
            <p><strong>Sources covered:</strong> Rainwater, water treatment, underground,
            lake and streams, and water catchment.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown("## Data source")
st.markdown(
    """
    <div class="panel-card">
        <p><strong>Source:</strong> National Institute of Statistics of Rwanda (NISR) -
        Seasonal Agricultural Survey (SAS) 2025</p>
        <p style="margin-top:0.5rem;"><strong>Survey type:</strong> Annual agricultural survey tables</p>
        <p style="margin-top:0.5rem;"><strong>Focus:</strong> Agricultural productivity, irrigation
        practices, and water resource utilization</p>
        <p style="margin-top:0.5rem;"><strong>Coverage:</strong> National level with district-level
        disaggregation</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

st.markdown("## Methodology")
method_col1, method_col2 = st.columns(2, gap="large")

with method_col1:
    st.markdown(
        """
        <div class="text-block">
            <h4>Data processing</h4>
            <ol>
                <li><strong>Data extraction</strong> - Relevant tables were extracted from the SAS 2025 annual tables.</li>
                <li><strong>Data cleaning</strong> - District names and season labels were standardized.</li>
                <li><strong>Data validation</strong> - Records were cross-referenced and checked for consistency.</li>
                <li><strong>Missing values</strong> - Missing values were preserved as NaN, not treated as zero.</li>
                <li><strong>Quality assessment</strong> - Data quality notes were documented where applicable.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

with method_col2:
    st.markdown(
        """
        <div class="text-block">
            <h4>Analysis approach</h4>
            <ol>
                <li><strong>Descriptive analysis</strong> - District and season-level patterns.</li>
                <li><strong>Comparative assessment</strong> - Cross-district and cross-season comparisons.</li>
                <li><strong>Pattern recognition</strong> - Identification of dominant methods and sources.</li>
                <li><strong>Decision support</strong> - Rule-based recommendations linking patterns to interventions.</li>
                <li><strong>Uncertainty awareness</strong> - Clear communication of limitations.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown("## Limitations and important notes")
st.warning("""
**Critical limitations:**
- **Not a measure of need:** Reported percentages show existing practices, not water stress or irrigation demand.
- **Data completeness:** Some district-season combinations may have missing data, especially Season C.
- **Static snapshot:** Data represents a specific survey period, not temporal trends.
- **No performance metrics:** Crop yields, water efficiency, and intervention effectiveness are not included.
- **Context missing:** Local soil, topography, and socio-economic factors are not captured.
""")

st.info("""
**Usage guidelines:**
- Use this as an exploratory and planning support tool, not a definitive recommendation system.
- Always validate findings with local expertise and additional data.
- Consider the feasibility checklist before implementing any intervention.
- Account for seasonal variations and climate change projections.
- Engage farmers and local authorities in decision-making processes.
""")

st.divider()

st.markdown("## Technical information")
st.markdown(
    """
    <div class="panel-card">
        <p><strong>Application:</strong> Rwanda Irrigation Decision Support System (DSS)</p>
        <p style="margin-top:0.5rem;"><strong>Framework:</strong> Streamlit (Python)</p>
        <p style="margin-top:0.5rem;"><strong>Data format:</strong> CSV files with district, season,
        and percentage values</p>
        <p style="margin-top:0.5rem;"><strong>Visualization:</strong> Interactive charts and tables</p>
        <p style="margin-top:0.5rem;"><strong>Deployment:</strong> Local or cloud-compatible Streamlit application</p>
        <p style="margin-top:0.5rem;"><strong>Version:</strong> 1.0 - NISR Big Data Hackathon 2026</p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_footer()
