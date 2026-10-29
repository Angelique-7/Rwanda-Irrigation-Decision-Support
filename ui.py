"""
Shared UI components for the Rwanda Irrigation Decision Support System.
Provides a consistent header, navigation bar, page headings, and footer.
"""

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

PROJECT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = PROJECT_DIR / "assets"
HERO_IMAGE = ASSETS_DIR / "hero_irrigation.jpg"

NAV_ITEMS = [
    ("Home", "/", "home"),
    ("District Explorer", "/District_Explorer", "map"),
    ("Intervention Planner", "/Intervention_Planner", "lightbulb"),
    ("About the Data", "/About_the_Data", "database"),
]

ICONS = {
    "home": '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/>',
    "map": (
        '<path d="m9 18-6 3V6l6-3 6 3 6-3v15l-6 3-6-3Z"/>'
        '<path d="M9 3v15"/><path d="M15 6v15"/>'
    ),
    "lightbulb": (
        '<path d="M9 18h6"/><path d="M10 22h4"/>'
        '<path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2Z"/>'
    ),
    "database": (
        '<ellipse cx="12" cy="5" rx="9" ry="3"/>'
        '<path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5"/>'
        '<path d="M3 12c0 1.7 4 3 9 3s9-1.3 9-3"/>'
    ),
    "droplet": '<path d="M12 2s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/>',
    "arrow": '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
}


def svg_icon(name: str, size: int = 18) -> str:
    """Return an inline, theme-aware SVG icon."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
    )


def apply_theme() -> None:
    """Inject the application-wide professional theme."""
    st.markdown(
        """
        <style>
            :root {
                --green-950: #052e16;
                --green-900: #14532d;
                --green-800: #166534;
                --green-700: #15803d;
                --green-600: #16a34a;
                --green-100: #dcfce7;
                --green-50: #f0fdf4;
                --ink: #1f2d24;
                --muted: #5b6b60;
                --line: #e0e9e1;
                --surface: #ffffff;
                --page: #f4f7f3;
            }

            html, body, [class*="css"] {
                font-family: "Segoe UI", "Inter", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif;
            }

            .stApp {
                background:
                    radial-gradient(1200px 500px at 85% -10%, #e3f5e7 0%, rgba(227, 245, 231, 0) 60%),
                    var(--page);
                color: var(--ink);
            }

            [data-testid="stHeader"],
            [data-testid="stToolbar"],
            #MainMenu,
            footer:not(.app-footer) {
                display: none !important;
            }

            .block-container,
            [data-testid="stMainBlockContainer"] {
                max-width: 1240px;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                padding-top: 1.25rem;
                padding-bottom: 2rem;
            }

            h1, h2, h3, h4 {
                color: var(--green-900);
                letter-spacing: -0.01em;
            }

            .stApp p, .stApp li, .stApp label {
                color: var(--ink);
            }

            /* ---------- Header / navigation ---------- */
            .app-header {
                position: sticky;
                top: 0.6rem;
                z-index: 999;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                flex-wrap: wrap;
                padding: 0.75rem 1.1rem;
                margin-bottom: 1.6rem;
                background: rgba(255, 255, 255, 0.94);
                backdrop-filter: blur(12px);
                border: 1px solid var(--line);
                border-radius: 16px;
                box-shadow: 0 8px 28px rgba(20, 83, 45, 0.07);
            }

            .brand {
                display: flex;
                align-items: center;
                gap: 0.7rem;
                text-decoration: none !important;
                flex-shrink: 0;
            }

            .brand-mark {
                width: 42px;
                height: 42px;
                border-radius: 12px;
                display: grid;
                place-items: center;
                color: #ffffff;
                background: linear-gradient(135deg, var(--green-800) 0%, var(--green-600) 100%);
                box-shadow: 0 6px 14px rgba(22, 101, 52, 0.28);
            }

            .brand-name {
                display: block;
                font-size: 1rem;
                font-weight: 700;
                line-height: 1.15;
                color: var(--green-900) !important;
            }

            .brand-sub {
                display: block;
                font-size: 0.66rem;
                font-weight: 600;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: #6b7f72 !important;
            }

            .top-nav {
                display: flex;
                align-items: center;
                gap: 0.25rem;
                flex-wrap: wrap;
            }

            .top-nav a {
                display: inline-flex;
                align-items: center;
                gap: 0.42rem;
                padding: 0.5rem 0.85rem;
                border-radius: 9px;
                font-size: 0.88rem;
                font-weight: 600;
                color: #475569 !important;
                text-decoration: none !important;
                border: 1px solid transparent;
                transition: all 0.18s ease;
            }

            .top-nav a:hover {
                color: var(--green-800) !important;
                background: var(--green-50);
                border-color: var(--green-100);
            }

            .top-nav a.active {
                color: #ffffff !important;
                background: linear-gradient(135deg, var(--green-800), var(--green-700));
                box-shadow: 0 4px 12px rgba(22, 101, 52, 0.25);
            }

            /* ---------- Hero ---------- */
            .hero {
                position: relative;
                display: flex;
                align-items: center;
                min-height: 430px;
                margin-bottom: 1.75rem;
                border-radius: 22px;
                overflow: hidden;
                background-size: cover;
                background-position: center 55%;
                box-shadow: 0 24px 60px rgba(20, 83, 45, 0.2);
            }

            .hero::before {
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(
                    90deg,
                    rgba(5, 46, 22, 0.92) 0%,
                    rgba(5, 46, 22, 0.78) 42%,
                    rgba(5, 46, 22, 0.18) 100%
                );
            }

            .hero-inner {
                position: relative;
                z-index: 1;
                max-width: 640px;
                padding: 3rem;
            }

            .hero-eyebrow {
                display: inline-flex;
                align-items: center;
                padding: 0.35rem 0.8rem;
                border-radius: 999px;
                font-size: 0.68rem;
                font-weight: 700;
                letter-spacing: 0.09em;
                text-transform: uppercase;
                color: #bbf7d0 !important;
                background: rgba(22, 101, 52, 0.45);
                border: 1px solid rgba(187, 247, 208, 0.35);
            }

            .hero h1 {
                margin: 0.95rem 0 0.8rem;
                padding: 0;
                border: none;
                font-size: 2.65rem;
                line-height: 1.1;
                font-weight: 800;
                letter-spacing: -0.025em;
                color: #ffffff !important;
            }

            .hero p {
                margin: 0 0 1.5rem;
                font-size: 1.02rem;
                line-height: 1.65;
                color: #e2f2e5 !important;
            }

            .hero-actions {
                display: flex;
                gap: 0.7rem;
                flex-wrap: wrap;
            }

            .hero-btn {
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                padding: 0.68rem 1.15rem;
                border-radius: 10px;
                font-size: 0.9rem;
                font-weight: 700;
                text-decoration: none !important;
                transition: all 0.2s ease;
            }

            .hero-btn.primary {
                color: #052e16 !important;
                background: #4ade80;
                box-shadow: 0 8px 22px rgba(74, 222, 128, 0.32);
            }

            .hero-btn.primary:hover {
                background: #86efac;
                transform: translateY(-2px);
            }

            .hero-btn.secondary {
                color: #ffffff !important;
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.45);
            }

            .hero-btn.secondary:hover {
                background: rgba(255, 255, 255, 0.22);
                transform: translateY(-2px);
            }

            .hero-credit {
                position: absolute;
                right: 1rem;
                bottom: 0.7rem;
                z-index: 1;
                font-size: 0.63rem;
                letter-spacing: 0.02em;
                color: rgba(255, 255, 255, 0.72) !important;
            }

            /* ---------- Page heading ---------- */
            .page-heading {
                display: flex;
                align-items: flex-start;
                gap: 0.9rem;
                margin-bottom: 1.5rem;
                padding-bottom: 1.1rem;
                border-bottom: 1px solid var(--line);
            }

            .page-heading-icon {
                display: grid;
                place-items: center;
                width: 46px;
                height: 46px;
                flex-shrink: 0;
                border-radius: 13px;
                color: var(--green-700);
                background: var(--green-50);
                border: 1px solid var(--green-100);
            }

            .page-heading h1 {
                margin: 0;
                padding: 0;
                border: none;
                font-size: 1.75rem;
                font-weight: 750;
                line-height: 1.2;
            }

            .page-heading p {
                margin: 0.3rem 0 0;
                font-size: 0.95rem;
                color: var(--muted) !important;
            }

            /* ---------- Cards ---------- */
            .feature-card,
            .nav-card,
            .panel-card {
                height: 100%;
                padding: 1.3rem;
                background: var(--surface);
                border: 1px solid var(--line);
                border-radius: 16px;
                box-shadow: 0 4px 16px rgba(20, 83, 45, 0.045);
            }

            .feature-icon {
                display: grid;
                place-items: center;
                width: 42px;
                height: 42px;
                margin-bottom: 0.9rem;
                border-radius: 12px;
                color: var(--green-700);
                background: var(--green-50);
                border: 1px solid var(--green-100);
            }

            .feature-card h4,
            .panel-card h4 {
                margin: 0 0 0.4rem;
                font-size: 1rem;
                font-weight: 700;
                color: var(--green-900);
            }

            .feature-card p,
            .nav-card p,
            .panel-card p {
                margin: 0;
                font-size: 0.88rem;
                line-height: 1.55;
                color: var(--muted) !important;
            }

            .panel-card p + p {
                margin-top: 0.5rem;
            }

            .nav-card {
                display: block;
                text-decoration: none !important;
                transition: all 0.2s ease;
            }

            .nav-card:hover {
                transform: translateY(-3px);
                border-color: #86efac;
                box-shadow: 0 14px 30px rgba(20, 83, 45, 0.11);
            }

            .nav-card-title {
                display: flex;
                align-items: center;
                gap: 0.55rem;
                margin-bottom: 0.45rem;
                font-size: 0.98rem;
                font-weight: 700;
                color: var(--green-900) !important;
            }

            .nav-card-title svg {
                color: var(--green-600);
            }

            .panel-card {
                height: auto;
            }

            /* ---------- Metrics ---------- */
            [data-testid="stMetric"] {
                padding: 1.05rem 1.15rem;
                background: var(--surface);
                border: 1px solid var(--line);
                border-radius: 14px;
                box-shadow: 0 4px 16px rgba(20, 83, 45, 0.045);
            }

            [data-testid="stMetricLabel"] {
                color: var(--muted) !important;
                font-size: 0.78rem !important;
                font-weight: 600 !important;
                letter-spacing: 0.03em;
                text-transform: uppercase;
            }

            [data-testid="stMetricValue"] {
                color: var(--green-900) !important;
                font-size: 1.85rem !important;
                font-weight: 750 !important;
            }

            [data-testid="stMetricDelta"] {
                color: var(--green-700) !important;
            }

            /* ---------- Sidebar ---------- */
            [data-testid="stSidebar"] {
                background: #f1f7f2;
                border-right: 1px solid #dbe7dd;
            }

            [data-testid="stSidebarNav"] {
                display: none !important;
            }

            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] h4 {
                color: var(--green-900) !important;
                font-size: 0.82rem;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }

            [data-testid="stSidebar"] .stMarkdown p,
            [data-testid="stSidebar"] label {
                color: var(--ink) !important;
            }

            /* ---------- Widgets ---------- */
            .stButton > button {
                border: none;
                border-radius: 9px;
                padding: 0.55rem 1.25rem;
                font-weight: 650;
                color: #ffffff;
                background: linear-gradient(135deg, var(--green-800), var(--green-700));
                transition: all 0.2s ease;
            }

            .stButton > button:hover {
                color: #ffffff;
                background: linear-gradient(135deg, var(--green-900), var(--green-800));
                box-shadow: 0 6px 16px rgba(22, 101, 52, 0.3);
                transform: translateY(-1px);
            }

            .stDownloadButton > button {
                border-radius: 9px;
                font-weight: 650;
            }

            .stSelectbox [data-baseweb="select"] > div,
            .stTextInput input,
            .stNumberInput input {
                border-radius: 9px;
                border-color: #cfe0d2;
                background: #ffffff;
                color: var(--ink);
            }

            .stRadio > label,
            .stCheckbox > label {
                color: var(--ink) !important;
            }

            .stAlert {
                border-radius: 12px;
                border-left-width: 4px;
            }

            [data-testid="stDataFrame"] {
                overflow: hidden;
                border: 1px solid var(--line);
                border-radius: 12px;
            }

            hr {
                border-color: var(--line);
                margin: 2rem 0;
            }

            .section-note {
                margin: -0.4rem 0 1.1rem;
                font-size: 0.9rem;
                color: var(--muted) !important;
            }

            .text-block h4 {
                margin: 0 0 0.5rem;
                font-size: 1rem;
                color: var(--green-900);
            }

            .text-block ul {
                margin: 0;
                padding-left: 1.15rem;
            }

            .text-block li {
                margin-bottom: 0.45rem;
                font-size: 0.9rem;
                line-height: 1.5;
                color: var(--muted);
            }

            .text-block ol {
                margin: 0;
                padding-left: 1.15rem;
            }

            .feature-list {
                margin: 0.2rem 0 0;
                padding-left: 1.1rem;
            }

            .feature-list li {
                margin-bottom: 0.55rem;
                font-size: 0.9rem;
                line-height: 1.55;
                color: var(--muted);
            }

            .feature-list li::marker {
                color: var(--green-600);
            }

            .sidebar-credit {
                margin-top: 1.5rem;
                padding-top: 1rem;
                border-top: 1px solid #dbe7dd;
                font-size: 0.72rem;
                line-height: 1.5;
                color: #6b7f72 !important;
            }

            /* ---------- Footer ---------- */
            .app-footer {
                margin-top: 3rem;
                padding: 2.25rem 2rem 1.25rem;
                border-radius: 20px;
                background: linear-gradient(150deg, #0b2e1b 0%, #052e16 100%);
                color: #cfe3d4;
                box-shadow: 0 20px 44px rgba(5, 46, 22, 0.22);
            }

            .footer-grid {
                display: grid;
                grid-template-columns: 2.2fr 1fr 1fr;
                gap: 2rem;
            }

            .footer-brand {
                display: flex;
                align-items: flex-start;
                gap: 0.8rem;
            }

            .footer-brand .brand-mark {
                box-shadow: none;
                background: rgba(74, 222, 128, 0.16);
                color: #86efac;
            }

            .footer-title {
                margin: 0 0 0.35rem;
                font-size: 1rem;
                font-weight: 700;
                color: #ffffff !important;
            }

            .footer-copy {
                margin: 0;
                max-width: 340px;
                font-size: 0.82rem;
                line-height: 1.6;
                color: #a9c6b2 !important;
            }

            .footer-heading {
                margin: 0 0 0.7rem;
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                color: #86efac !important;
            }

            .footer-links {
                display: flex;
                flex-direction: column;
                gap: 0.45rem;
            }

            .footer-links a,
            .footer-links span {
                font-size: 0.84rem;
                color: #cfe3d4 !important;
                text-decoration: none !important;
            }

            .footer-links a:hover {
                color: #ffffff !important;
            }

            .footer-bottom {
                display: flex;
                justify-content: space-between;
                gap: 1rem;
                flex-wrap: wrap;
                margin-top: 1.75rem;
                padding-top: 1rem;
                border-top: 1px solid rgba(255, 255, 255, 0.12);
                font-size: 0.73rem;
                color: #9fb9a7 !important;
            }

            .footer-bottom span {
                color: #9fb9a7 !important;
            }

            /* ---------- Responsive ---------- */
            @media (max-width: 900px) {
                .footer-grid {
                    grid-template-columns: 1fr 1fr;
                }
                .hero-inner {
                    padding: 2.25rem;
                }
                .hero h1 {
                    font-size: 2.15rem;
                }
            }

            @media (max-width: 640px) {
                .app-header {
                    justify-content: center;
                }
                .top-nav {
                    justify-content: center;
                }
                .hero {
                    min-height: 380px;
                }
                .hero-inner {
                    padding: 1.6rem;
                }
                .hero h1 {
                    font-size: 1.8rem;
                }
                .footer-grid {
                    grid-template-columns: 1fr;
                    gap: 1.5rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(active: str = "Home") -> None:
    """Render the shared brand header and top navigation bar."""
    links = []
    for label, href, icon in NAV_ITEMS:
        active_class = " active" if label == active else ""
        links.append(
            f'<a class="nav-link{active_class}" href="{href}" target="_self">'
            f"{svg_icon(icon, 16)}<span>{label}</span></a>"
        )

    st.markdown(
        f"""
        <header class="app-header">
            <a class="brand" href="/" target="_self">
                <span class="brand-mark">{svg_icon("droplet", 22)}</span>
                <span>
                    <span class="brand-name">Rwanda Irrigation</span>
                    <span class="brand-sub">Decision Support System</span>
                </span>
            </a>
            <nav class="top-nav" aria-label="Main navigation">
                {''.join(links)}
            </nav>
        </header>
        """,
        unsafe_allow_html=True,
    )


def render_page_heading(icon: str, title: str, subtitle: str) -> None:
    """Render a consistent page title block with an icon."""
    st.markdown(
        f"""
        <div class="page-heading">
            <span class="page-heading-icon">{svg_icon(icon, 23)}</span>
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def _hero_data_uri() -> str:
    if not HERO_IMAGE.exists():
        return ""
    encoded = base64.b64encode(HERO_IMAGE.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def render_hero() -> None:
    """Render the agriculture-themed landing hero with the survey photo."""
    image_uri = _hero_data_uri()
    background = f"background-image: url('{image_uri}');" if image_uri else ""

    st.markdown(
        f"""
        <section class="hero" style="{background}">
            <div class="hero-inner">
                <span class="hero-eyebrow">NISR Big Data Hackathon 2026 &middot; Agricultural Productivity</span>
                <h1>Climate-resilient irrigation planning for Rwanda</h1>
                <p>
                    Turn seasonal agricultural survey data into district-level insight on irrigation
                    methods and water sources, so planners can target investments where they matter most.
                </p>
                <div class="hero-actions">
                    <a class="hero-btn primary" href="/District_Explorer" target="_self">
                        {svg_icon("map", 16)} Explore District Data
                    </a>
                    <a class="hero-btn secondary" href="/Intervention_Planner" target="_self">
                        {svg_icon("lightbulb", 16)} Build an Intervention Plan
                    </a>
                </div>
            </div>
            <span class="hero-credit">Photo: Bernd Dittrich / Unsplash</span>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render the shared professional footer."""
    st.markdown(
        f"""
        <footer class="app-footer">
            <div class="footer-grid">
                <div class="footer-brand">
                    <span class="brand-mark">{svg_icon("droplet", 22)}</span>
                    <div>
                        <p class="footer-title">Rwanda Irrigation DSS</p>
                        <p class="footer-copy">
                            Evidence-based decision support for climate-resilient irrigation and
                            agricultural water management across Rwanda's districts.
                        </p>
                    </div>
                </div>
                <div>
                    <p class="footer-heading">Platform</p>
                    <div class="footer-links">
                        <a href="/" target="_self">Home</a>
                        <a href="/District_Explorer" target="_self">District Explorer</a>
                        <a href="/Intervention_Planner" target="_self">Intervention Planner</a>
                        <a href="/About_the_Data" target="_self">About the Data</a>
                    </div>
                </div>
                <div>
                    <p class="footer-heading">Data &amp; Credits</p>
                    <div class="footer-links">
                        <span>NISR Seasonal Agricultural Survey 2025</span>
                        <span>Streamlit &amp; Plotly</span>
                        <span>Hero photo: Bernd Dittrich / Unsplash</span>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <span>&copy; 2026 Rwanda Irrigation Decision Support System</span>
                <span>NISR Big Data Hackathon 2026 &middot; Agricultural Productivity Track</span>
            </div>
        </footer>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_credit() -> None:
    """Render a small data credit block at the bottom of the sidebar."""
    st.sidebar.markdown(
        """
        <div class="sidebar-credit">
            <strong>Data source</strong><br>
            NISR Seasonal Agricultural Survey 2025
        </div>
        """,
        unsafe_allow_html=True,
    )
