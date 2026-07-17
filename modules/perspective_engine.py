"""
NOVARYN Perspective Engine

Generates multiple expert perspectives using
the same knowledge base.
"""

from __future__ import annotations

import streamlit as st

from core.vector_store import vector_store
from core.groq_client import groq_client
from core.logger import get_logger
from core.session_utils import increment_queries

logger = get_logger("perspective_engine")


# ==========================================================
# Expert Personas
# ==========================================================

PERSPECTIVES = {

    "Technical":
        "Analyze technically. Explain architecture, implementation, risks and engineering considerations.",

    "Business":
        "Analyze from a business perspective including ROI, cost, market opportunity and feasibility.",

    "Security":
        "Analyze security risks, attack vectors, privacy concerns and mitigations.",

    "Legal":
        "Analyze legal, regulatory and compliance implications.",

    "Ethical":
        "Analyze ethical concerns, fairness, transparency and societal impact."
}


# ==========================================================
# Prompt Builder
# ==========================================================

def build_prompt(question, role):

    docs = vector_store.search(question)

    context = "\n\n".join(
        d["text"] for d in docs
    )

    return [

        {

            "role": "system",

            "content":
f"""
You are an expert.

Perspective

{role}

Instruction

{PERSPECTIVES[role]}

Only use the supplied context.

If insufficient context exists,
clearly state that.
"""
        },

        {

            "role": "user",

            "content":
f"""
Context

{context}

Question

{question}
"""

        }

    ]


# ==========================================================
# Analysis
# ==========================================================

def analyze(question, role):

    messages = build_prompt(
        question,
        role
    )

    return groq_client.chat(messages)


# ==========================================================
# UI
# ==========================================================

def show_perspective_engine():

    st.subheader("🌍 Perspective Engine")

    st.caption(
        "Analyze one topic from multiple expert viewpoints."
    )

    question = st.text_area(

        "Question",

        height=120,

        placeholder="Example: Should governments regulate AI?"

    )

    selected = st.multiselect(

        "Choose Perspectives",

        list(PERSPECTIVES.keys()),

        default=[
            "Technical",
            "Business",
            "Security"
        ]

    )

    if st.button(

        "Generate Analysis",

        use_container_width=True

    ):

        if not question:

            st.warning(
                "Enter a question."
            )

            return

        increment_queries()

        progress = st.progress(0)

        answers = {}

        for i, role in enumerate(selected):

            with st.spinner(
                f"Generating {role}..."
            ):

                try:

                    answers[role] = analyze(
                        question,
                        role
                    )

                except Exception as e:

                    logger.exception(e)

                    answers[role] = str(e)

            progress.progress(
                (i + 1) / len(selected)
            )

        st.divider()

        for role in selected:

            with st.expander(
                f"{role} Perspective",
                expanded=True
            ):

                st.markdown(
                    answers[role]
                )

        st.divider()

        st.markdown("## Executive Summary")

        summary_prompt = [

            {

                "role":"system",

                "content":
"""
You are an executive analyst.

Compare all expert opinions.

Provide:

1. Agreements
2. Disagreements
3. Risks
4. Final Recommendation
"""

            },

            {

                "role":"user",

                "content":str(answers)

            }

        ]

        summary = groq_client.chat(
            summary_prompt
        )

        st.success(summary)

        logger.info(
            "Perspective analysis completed."
        )