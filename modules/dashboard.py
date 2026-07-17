"""
NOVARYN Dashboard
System overview and quick access.
"""

from __future__ import annotations

import streamlit as st
from datetime import datetime

from core.vector_store import vector_store
from core.session_utils import get
from core.groq_client import groq_client

from theme.styles import (
    card,
    metric
)


def show_dashboard():

    st.subheader("🏠 Dashboard")

    st.caption("Welcome to NOVARYN Intelligence Platform")

    stats = vector_store.stats()

    # ===================================================
    # Top Metrics
    # ===================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric(
            "Documents",
            stats["documents"]
        )

    with col2:
        metric(
            "Vectors",
            stats["vectors"]
        )

    with col3:
        metric(
            "Queries",
            get("queries")
        )

    with col4:
        metric(
            "Files",
            get("files_processed")
        )

    st.divider()

    # ===================================================
    # System Information
    # ===================================================

    left, right = st.columns([2, 1])

    with left:

        st.markdown("### System Information")

        st.info(f"""
Application : NOVARYN

Embedding Model :
{stats["embedding_model"]}

LLM :
{groq_client.get_model()}

Current Time :
{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
""")

    with right:

        st.markdown("### Health")

        if groq_client.health():

            st.success("Groq API Connected")

        else:

            st.error("Groq API Offline")

        if stats["vectors"] > 0:

            st.success("Knowledge Base Ready")

        else:

            st.warning("Knowledge Base Empty")

    st.divider()

    # ===================================================
    # Quick Actions
    # ===================================================

    st.markdown("### Quick Actions")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        if st.button(
            "📂 Upload Files",
            use_container_width=True
        ):

            st.session_state.active_module = \
                "File Intelligence"

            st.rerun()

    with c2:

        if st.button(
            "🧠 Open Oracle",
            use_container_width=True
        ):

            st.session_state.active_module = \
                "Oracle Chamber"

            st.rerun()

    with c3:

        if st.button(
            "⚖ Genius Court",
            use_container_width=True
        ):

            st.session_state.active_module = \
                "Genius Court"

            st.rerun()

    with c4:

        if st.button(
            "🤖 Agent Mode",
            use_container_width=True
        ):

            st.session_state.active_module = \
                "Agent Mode"

            st.rerun()

    st.divider()

    # ===================================================
    # Recent Chat
    # ===================================================

    st.markdown("### Recent Conversation")

    history = get("chat_history")

    if not history:

        st.info(
            "No conversations yet."
        )

    else:

        for msg in history[-5:]:

            if msg["role"] == "user":

                st.chat_message(
                    "user"
                ).write(msg["content"])

            else:

                st.chat_message(
                    "assistant"
                ).write(msg["content"])

    st.divider()

    # ===================================================
    # Recent Files
    # ===================================================

    st.markdown("### Recent Files")

    files = get("uploaded_files")

    if not files:

        st.info(
            "No uploaded files."
        )

    else:

        for file in files[-10:]:

            st.write(
                "📄",
                file.name
            )

    st.divider()

    # ===================================================
    # Storage Statistics
    # ===================================================

    st.markdown("### Storage")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Knowledge Entries",
            stats["documents"]
        )

    with col2:

        st.metric(
            "Vector Count",
            stats["vectors"]
        )

    st.divider()

    # ===================================================
    # About
    # ===================================================

    card(
        """
### NOVARYN

Global Intelligence Court

Modules Included

- Dashboard
- Knowledge Base
- File Intelligence
- Oracle Chamber
- Perspective Engine
- Genius Court
- Propaganda Detector
- Agent Mode

Version : 1.0
"""
    )