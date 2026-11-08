"""Shared look for both portals: flat, square, green and gold (University of Alberta colours).
Edit the colours in the :root line below. Everything else follows."""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@700&family=Roboto:wght@400;500;700&display=swap');

:root {
    --green: #275D38; --green-dark: #1D4529; --gold: #F2CD00;
    --line: #D0D0D0; --text: #222222; --muted: #5A5A5A;
}

.stApp, .stApp p, .stApp label, .stApp input, .stApp textarea, .stApp button, .stApp li {
    font-family: 'Roboto', 'Helvetica Neue', Arial, sans-serif;
}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    font-family: 'Roboto Condensed', 'Arial Narrow', Arial, sans-serif;
    font-weight: 700; color: var(--green); letter-spacing: 0.01em;
}

/* ---------- Top bar: full-width green with a gold edge ---------- */
header[data-testid="stHeader"] {
    background: var(--green); height: 4rem; border-bottom: 4px solid var(--gold);
}
header[data-testid="stHeader"]::before {
    content: "RESIDENCE SAFETY   |   LISTER CENTRE";
    position: absolute; left: 1.5rem; top: 50%; transform: translateY(-50%);
    color: #FFFFFF; font-family: 'Roboto Condensed', Arial, sans-serif;
    font-weight: 700; font-size: 1.15rem; letter-spacing: 0.12em;
}
[data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer { visibility: hidden; }

.block-container { padding-top: 6.5rem !important; max-width: __MAXW__; }

/* ---------- Page title ---------- */
.page-title { margin-bottom: 1.2rem; }
.stApp .page-title h1 {
    display: inline-block; font-size: 2rem; margin: 0; padding: 0 0 0.35rem 0;
    border-bottom: 4px solid var(--gold);
}
.page-title p { color: var(--muted); margin: 0.7rem 0 0 0; font-size: 1.05rem; }

/* ---------- Cards (any container whose key starts with "card") ---------- */
[class*="st-key-card"] {
    background: #FFFFFF; border: 1px solid var(--line); border-top: 4px solid var(--green);
    padding: 1.25rem 1.25rem 1rem 1.25rem; margin-bottom: 1rem;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
}

/* ---------- Form controls: square, flat ---------- */
.stApp [data-baseweb="select"] > div,
.stApp [data-baseweb="input"],
.stApp [data-baseweb="base-input"],
.stApp [data-baseweb="textarea"] { border-radius: 0 !important; }
.stApp [data-testid="stAlert"] { border-radius: 0; }

.stApp button[kind], .stApp [data-testid^="stBaseButton"] { border-radius: 0 !important; }
.stApp button[kind="primary"], .stApp [data-testid="stBaseButton-primary"] {
    background-color: var(--green); border: 1px solid var(--green); color: #FFFFFF;
    font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; padding: 0.6rem 1.2rem;
}
.stApp button[kind="primary"]:hover, .stApp [data-testid="stBaseButton-primary"]:hover {
    background-color: var(--green-dark); border-color: var(--green-dark); color: #FFFFFF;
}
.stApp button[kind="secondary"], .stApp [data-testid="stBaseButton-secondary"] {
    background: #FFFFFF; border: 1px solid var(--green); color: var(--green);
    font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;
}
.st-key-submit_btn button, .st-key-login_btn button, .st-key-again_btn button { width: 100%; }

/* ---------- Notice, steps, badges, metrics ---------- */
.notice {
    border-left: 6px solid var(--gold); background: #FFF9D6; color: var(--text);
    padding: 0.8rem 1rem; margin-bottom: 1rem; font-size: 0.95rem;
}
.steps { display: flex; margin: 0.6rem 0 1rem 0; }
.step {
    flex: 1; text-align: center; padding: 0.9rem 0.4rem; background: #FFFFFF;
    border: 1px solid var(--line); color: var(--muted); font-size: 0.9rem;
}
.step b { display: block; font-family: 'Roboto Condensed', Arial, sans-serif; font-size: 1.5rem; }
.step.done { background: var(--green); border-color: var(--green); color: #FFFFFF; }

.badge {
    display: inline-block; padding: 0.15rem 0.6rem; margin-right: 0.5rem;
    font-family: 'Roboto Condensed', Arial, sans-serif; font-weight: 700;
    letter-spacing: 0.1em; font-size: 0.8rem;
}
.badge.high { background: #B71C1C; color: #FFFFFF; }
.badge.medium { background: var(--gold); color: #222222; }
.badge.low { background: #6B6B6B; color: #FFFFFF; }
.badge.done { background: #E8F0EA; color: var(--green); border: 1px solid var(--green); }

.badge.overdue { background: #FFFFFF; color: #B71C1C; border: 1px solid #B71C1C; }
.alert-bar {
    border-left: 6px solid #B71C1C; background: #FDECEC; color: var(--text);
    padding: 0.8rem 1rem; margin-bottom: 1rem; font-weight: 500;
}
[class*="st-key-card_incident_overdue"] { border-left: 6px solid #B71C1C; }

.legend span { display: inline-block; margin-right: 1.2rem; font-size: 0.9rem; color: var(--muted); }
.legend i { display: inline-block; width: 0.8rem; height: 0.8rem; margin-right: 0.35rem; vertical-align: -1px; }

.stApp [data-testid="stMetric"] {
    background: #FFFFFF; border: 1px solid var(--line); border-top: 4px solid var(--gold);
    border-radius: 0; padding: 0.8rem 1rem;
}
.stApp [data-testid="stMetricValue"] { color: var(--green); font-family: 'Roboto Condensed', Arial, sans-serif; }

.site-footer {
    margin-top: 2.5rem; padding: 1rem 0; border-top: 4px solid var(--green);
    color: var(--muted); font-size: 0.85rem;
}

/* ---------- Phones ---------- */
@media (max-width: 600px) {
    header[data-testid="stHeader"]::before { font-size: 0.85rem; letter-spacing: 0.06em; left: 1rem; }
    .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
    .stApp .page-title h1 { font-size: 1.6rem; }
}
</style>
"""


def apply_theme(max_width="760px"):
    """Call once, right after st.set_page_config."""
    st.markdown(CSS.replace("__MAXW__", max_width), unsafe_allow_html=True)


def page_title(title, subtitle=""):
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f'<div class="page-title"><h1>{title}</h1>{sub}</div>', unsafe_allow_html=True)


def notice(text_html):
    st.markdown(f'<div class="notice">{text_html}</div>', unsafe_allow_html=True)


def site_footer():
    st.markdown(
        '<div class="site-footer">Student prototype built at natHacks 2026. '
        "Not an official University of Alberta service. "
        "In an emergency, call 911.</div>",
        unsafe_allow_html=True,
    )