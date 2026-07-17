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
        initial_sidebar_state="collapsed"
    )


# -------------------------------------------------------
# CSS
# -------------------------------------------------------

def load_css():

    st.markdown(f"""

<style>

/* ===============================
   GLOBAL
================================ */

.stApp {{

    background:
    radial-gradient(
        circle at top right,
        #211b0d 0%,
        transparent 35%
    ),
    {BACKGROUND};

    color:{TEXT};

    font-family:
    "Inter",
    "Segoe UI",
    sans-serif;

}}


.main {{
    padding-top:20px;
}}


/* ===============================
   SIDEBAR
================================ */


[data-testid="stSidebar"] {{

    background:
    linear-gradient(
        180deg,
        #111111,
        #0B0B0B
    );

    border-right:
    1px solid rgba(201,164,76,0.18);

}}


[data-testid="stSidebar"] * {{

    color:#E8E8E8;

}}



/* ===============================
   LOGO
================================ */


.logo img {{

    width:90px;

    display:block;

    margin:
    10px auto 20px auto;

}}




/* ===============================
   BUTTONS
================================ */


.stButton > button {{

    width:100%;

    background:
    linear-gradient(
        135deg,
        {PRIMARY},
        {SECONDARY}
    );


    color:#090909;

    border:none;

    border-radius:12px;

    padding:
    11px 18px;


    font-weight:700;

    letter-spacing:.3px;

    transition:.25s;

}}



.stButton > button:hover {{

    transform:
    translateY(-2px);


    box-shadow:
    0 8px 25px
    rgba(201,164,76,.25);

}}



/* ===============================
   RADIO BUTTONS
================================ */


div[role="radiogroup"] {{

    background:#131313;

    padding:12px;

    border-radius:16px;

    border:
    1px solid rgba(255,255,255,.08);

}}



div[role="radiogroup"] label {{

    background:#1B1B1B;

    padding:
    10px 14px;

    border-radius:12px;

    margin-bottom:8px;

    border:
    1px solid transparent;

    transition:.2s;

}}



div[role="radiogroup"] label:hover {{

    background:#222;

    border-color:{PRIMARY};

}}



div[role="radiogroup"] label:has(input:checked) {{

    background:
    rgba(201,164,76,.15);

    border:
    1px solid {PRIMARY};

}}



div[role="radiogroup"] input {{

    accent-color:{PRIMARY};

}}




/* ===============================
   CARDS
================================ */


.card {{

    background:

    linear-gradient(
        145deg,
        #191919,
        #121212
    );


    border-radius:18px;


    padding:22px;


    margin-bottom:18px;


    border:
    1px solid rgba(255,255,255,.07);


    box-shadow:

    0 10px 30px
    rgba(0,0,0,.3);

}}




/* ===============================
   TITLES
================================ */


.title {{

    font-size:34px;

    font-weight:750;

    letter-spacing:-1px;

    color:{PRIMARY};

}}



.subtitle {{

    color:{MUTED};

    font-size:15px;

    margin-top:6px;

}}




/* ===============================
   METRICS
================================ */


.metric {{

    background:#151515;

    padding:18px;

    border-radius:16px;

    border-left:
    4px solid {PRIMARY};

}}



.metric-title {{

    color:#999;

    font-size:13px;

    text-transform:
    uppercase;

    letter-spacing:1px;

}}



.metric-value {{

    margin-top:5px;

    font-size:30px;

    font-weight:700;

    color:white;

}}




/* ===============================
   INPUTS
================================ */


.stTextInput input,
.stTextArea textarea,
.stSelectbox div {{

    background:#151515 !important;

    color:white !important;

    border-radius:12px !important;

}}



.stTextInput input:focus,
.stTextArea textarea:focus {{

    border:
    1px solid {PRIMARY} !important;

    box-shadow:
    0 0 0 2px
    rgba(201,164,76,.15);

}}




/* ===============================
   CHAT
================================ */


.user-msg {{

    background:#242424;

    padding:14px;

    border-radius:14px;

    margin-bottom:10px;

}}



.bot-msg {{

    background:#161616;

    padding:14px;

    border-radius:14px;

    border-left:
    4px solid {PRIMARY};

}}




/* ===============================
   DIVIDER
================================ */


hr {{

    border-color:
    rgba(255,255,255,.08);

}}




/* ===============================
   FOOTER
================================ */


.footer {{

    text-align:center;

    color:#777;

    font-size:13px;

    margin-top:40px;

}}


</style>

""", unsafe_allow_html=True)



# -------------------------------------------------------
# Components
# -------------------------------------------------------


def logo(path="logo.png"):

    st.markdown(
        "<div class='logo'>",
        unsafe_allow_html=True
    )

    st.image(
        path,
        width=90
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )



def title(text, subtitle=""):

    st.markdown(
        f"""
<div class='title'>
{text}
</div>

<div class='subtitle'>
{subtitle}
</div>

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

<div class='metric-title'>
{title}
</div>

<div class='metric-value'>
{value}
</div>

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
