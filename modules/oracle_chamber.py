"""
NOVARYN Oracle Chamber

RAG-powered AI assistant with:
- Conversation memory
- Semantic search
- Streaming support
- Source citations
"""

from __future__ import annotations

import streamlit as st

from core.logger import get_logger
from core.vector_store import vector_store
from core.groq_client import groq_client

from core.session_utils import (
    get,
    add_chat,
    increment_queries,
)

logger = get_logger("oracle")


# ==========================================================
# Prompt Builder
# ==========================================================

def build_prompt(question: str):

    results = vector_store.search(question)

    context = ""

    sources = []

    for item in results:

        context += item["text"] + "\n\n"

        sources.append(item["source"])

    messages = [

        {
            "role": "system",

            "content":
"""
You are Oracle Chamber.

Answer ONLY from the provided context.

If the answer is not found,
say:

'I could not find this information
inside the knowledge base.'

Do not hallucinate.
"""
        }

    ]

    history = get("chat_history")

    if history:

        messages.extend(history[-6:])

    messages.append({

        "role": "user",

        "content":
f"""
Context

{context}

Question

{question}
"""

    })

    return messages, sources


# ==========================================================
# Chat UI
# ==========================================================

def show_oracle_chamber():

    st.subheader("🔮 Oracle Chamber")

    st.caption(
        "Knowledge-powered AI Assistant"
    )

    history = get("chat_history")

    for message in history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask Oracle..."
    )

    if not prompt:

        return

    increment_queries()

    add_chat("user", prompt)

    with st.chat_message("user"):

        st.markdown(prompt)

    messages, sources = build_prompt(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        response = ""

        try:

            for chunk in groq_client.stream(messages):

                response += chunk

                placeholder.markdown(response + "▌")

            placeholder.markdown(response)

        except Exception as e:

            logger.exception(e)

            response = str(e)

            st.error(response)

    add_chat("assistant", response)

    if sources:

        st.divider()

        st.markdown("### Sources")

        unique = sorted(set(sources))

        for src in unique:

            st.caption(f"📄 {src}")

    logger.info(
        f"Oracle query completed: {prompt}"
    )


# ==========================================================
# Utilities
# ==========================================================

def clear_conversation():

    st.session_state.chat_history = []


def export_chat():

    history = get("chat_history")

    text = ""

    for item in history:

        text += (
            f"{item['role'].upper()}\n"
            f"{item['content']}\n\n"
        )

    return text