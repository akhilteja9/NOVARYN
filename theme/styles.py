"""
NOVARYN Premium Theme
Reusable CSS and UI helpers.
"""

import streamlit as st

# -------------------------------------------------------
# Color Palette
# -------------------------------------------------------

PRIMARY = "#C9A44C"
SECONDARY = "#D6B55B"

BACKGROUND = "#0B0B0B"
CARD = "#171717"

TEXT = "#F5F5F5"
MUTED = "#A5A5A5"

SUCCESS = "#4CAF50"
WARNING = "#F9A825"
ERROR = "#E53935"

# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

def configure_page():

    st.set_page_config(
        page_title="NOVARYN",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )


# -------------------------------------------------------
# CSS
# -------------------------------------------------------

def load_css():

    st.markdown(f"""

<style>

/* Background */

.stApp {{
    background:{BACKGROUND};
    color:{TEXT};
}}

/* Sidebar */

[data-testid="stSidebar"] {{
    background:#111111;
    border-right:1px solid #2C2C2C;
}}

/* Buttons */

.stButton>button {{

    width:100%;

    background:{PRIMARY};

    color:black;

    border:none;

    border-radius:10px;

    font-weight:bold;

    padding:10px;

}}

.stButton>button:hover {{

    background:{SECONDARY};

}}

/* Cards */

.card {{

    background:{CARD};

    border-radius:14px;

    padding:20px;

    margin-bottom:15px;

    border:1px solid #2C2C2C;

}}

/* Titles */

.title {{

    font-size:32px;

    font-weight:bold;

    color:{PRIMARY};

}}

.subtitle {{

    color:{MUTED};

    font-size:16px;

}}

/* Metrics */

.metric {{

    background:#1B1B1B;

    border-left:5px solid {PRIMARY};

    padding:15px;

    border-radius:12px;

    margin-bottom:10px;

}}

.metric-title {{

    color:{MUTED};

    font-size:14px;

}}

.metric-value {{

    font-size:28px;

    font-weight:bold;

    color:white;

}}

/* Chat */

.user-msg {{

    background:#222;

    padding:12px;

    border-radius:10px;

}}

.bot-msg {{

    background:#1A1A1A;

    border-left:4px solid {PRIMARY};

    padding:12px;

    border-radius:10px;

}}

/* Footer */

.footer {{

    text-align:center;

    color:gray;

    margin-top:30px;

}}

</style>

""", unsafe_allow_html=True)


# -------------------------------------------------------
# Components
# -------------------------------------------------------

def title(text, subtitle=""):

    st.markdown(
        f"""
<div class='title'>{text}</div>
<div class='subtitle'>{subtitle}</div>
<br>
""",
        unsafe_allow_html=True
    )


def card(content):

    st.markdown(
        f"""
<div class='card'>
{content}
</div>
""",
        unsafe_allow_html=True
    )


def metric(title, value):

    st.markdown(
        f"""
<div class='metric'>
<div class='metric-title'>{title}</div>
<div class='metric-value'>{value}</div>
</div>
""",
        unsafe_allow_html=True
    )


def footer():

    st.markdown(
        """
<div class='footer'>
NOVARYN • Global Intelligence Court • Version 1.0
</div>
""",
        unsafe_allow_html=True
    )