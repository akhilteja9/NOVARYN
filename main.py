"""
NOVARYN
Main Application
"""

import streamlit as st

# -------------------------------------------------------
# Theme
# -------------------------------------------------------

from theme.styles import (
    configure_page,
    load_css,
    title,
    footer
)

# -------------------------------------------------------
# Core
# -------------------------------------------------------

from core.session_utils import (
    initialize_session,
    get,
    set
)

from core.logger import get_logger
from core.vector_store import vector_store
from core.groq_client import groq_client

# -------------------------------------------------------
# Modules
# -------------------------------------------------------

from modules.dashboard import show_dashboard
from modules.knowledge_base import show_knowledge_base
from modules.file_intelligence import show_file_intelligence
from modules.oracle_chamber import show_oracle_chamber
from modules.perspective_engine import show_perspective_engine
from modules.genius_court import show_genius_court
from modules.propaganda_detector import show_propaganda_detector
from modules.agent_mode import show_agent_mode

logger = get_logger("app")

# -------------------------------------------------------
# Initialize
# -------------------------------------------------------

configure_page()
load_css()
initialize_session()

if not get("initialized"):

    set("vector_store", vector_store)
    set("groq_client", groq_client)

    set("initialized", True)

    logger.info("NOVARYN initialized successfully.")

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:

    st.image(
        "assets/logo.png",
        use_container_width=True
    )

    st.markdown("## NOVARYN")

    st.caption("Global Intelligence Court")

    st.divider()

    module = st.radio(

        "Navigation",

        [

            "Dashboard",

            "Knowledge Base",

            "File Intelligence",

            "Oracle Chamber",

            "Perspective Engine",

            "Genius Court",

            "Propaganda Detector",

            "Agent Mode"

        ]

    )

    set("active_module", module)

    st.divider()

    stats = vector_store.stats()

    st.markdown("### System Status")

    st.success("System Online")

    st.write(f"Documents : {stats['documents']}")
    st.write(f"Vectors : {stats['vectors']}")
    st.write(f"Embedding : {stats['embedding_model']}")
    st.write(f"Model : {groq_client.get_model()}")

    st.divider()

    if st.button("Clear Chat"):

        set("chat_history", [])

        st.success("Chat history cleared.")

    if st.button("Clear Knowledge Base"):

        vector_store.delete_all()

        st.success("Knowledge base cleared.")

# -------------------------------------------------------
# Header
# -------------------------------------------------------

title(

    "NOVARYN",

    "AI-Powered Global Intelligence Court"

)

# -------------------------------------------------------
# Routing
# -------------------------------------------------------

if module == "Dashboard":

    show_dashboard()

elif module == "Knowledge Base":

    show_knowledge_base()

elif module == "File Intelligence":

    show_file_intelligence()

elif module == "Oracle Chamber":

    show_oracle_chamber()

elif module == "Perspective Engine":

    show_perspective_engine()

elif module == "Genius Court":

    show_genius_court()

elif module == "Propaganda Detector":

    show_propaganda_detector()

elif module == "Agent Mode":

    show_agent_mode()

# -------------------------------------------------------
# Footer
# -------------------------------------------------------

footer()