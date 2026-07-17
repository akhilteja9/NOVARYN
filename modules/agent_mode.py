"""
NOVARYN Agent Mode

Autonomous AI Orchestrator

This module intelligently decides which
NOVARYN components to invoke.

Workflow

Question
      │
      ▼
Retrieve Knowledge
      │
      ▼
Need Multiple Perspectives?
      │
      ├── Yes → Perspective Engine
      │
      ▼
Need Debate?
      │
      ├── Yes → Genius Court
      │
      ▼
Need Propaganda Analysis?
      │
      ├── Yes → Propaganda Detector
      │
      ▼
Generate Final Report
"""

from __future__ import annotations

import streamlit as st

from core.groq_client import groq_client
from core.vector_store import vector_store
from core.logger import get_logger
from core.session_utils import increment_queries

logger = get_logger("agent_mode")


# ==========================================================
# Planner
# ==========================================================

PLANNER = """
You are NOVARYN Planner.

Read the user's request.

Return ONLY JSON.

{
 "retrieve": true,
 "perspective": true/false,
 "debate": true/false,
 "propaganda": true/false,
 "reason":"..."
}

Rules

Simple factual question
→ retrieve only

Decision making
→ perspective

Controversial topic
→ debate

Political article / speech /
media article

→ propaganda

Multiple conditions may be true.
"""


# ==========================================================
# Planning
# ==========================================================

def plan(question):

    response = groq_client.chat(

        [

            {

                "role":"system",

                "content":PLANNER

            },

            {

                "role":"user",

                "content":question

            }

        ]

    )

    return response


# ==========================================================
# Retrieve
# ==========================================================

def retrieve(question):

    docs = vector_store.search(question)

    context = "\n\n".join(

        d["text"]

        for d in docs

    )

    return context, docs


# ==========================================================
# Final Synthesis
# ==========================================================

def final_answer(

    question,

    context,

    planner,

    perspective="",

    debate="",

    propaganda=""

):

    prompt = [

        {

            "role":"system",

            "content":
"""
You are NOVARYN.

Combine every analysis.

Produce

1. Executive Summary

2. Detailed Analysis

3. Risks

4. Recommendations

5. Final Answer

Mention uncertainty where appropriate.

Use Markdown.
"""

        },

        {

            "role":"user",

            "content":
f"""
Question

{question}

--------------------------------

Planner

{planner}

--------------------------------

Knowledge

{context}

--------------------------------

Perspective

{perspective}

--------------------------------

Debate

{debate}

--------------------------------

Propaganda

{propaganda}
"""

        }

    ]

    return groq_client.chat(prompt)


# ==========================================================
# UI
# ==========================================================

def show_agent_mode():

    st.subheader("🤖 Agent Mode")

    st.caption(
        "Autonomous Intelligence Workflow"
    )

    question = st.text_area(

        "Mission",

        height=140,

        placeholder="Example: Should governments regulate AI generated news?"

    )

    if st.button(

        "Execute",

        use_container_width=True

    ):

        if not question:

            st.warning(
                "Enter a mission."
            )

            return

        increment_queries()

        progress = st.progress(0)

        # ------------------------

        with st.spinner("Planning..."):

            planner = plan(question)

        progress.progress(20)

        # ------------------------

        with st.spinner("Retrieving knowledge..."):

            context, docs = retrieve(question)

        progress.progress(40)

        # ------------------------

        # Placeholder integrations
        # These will call other modules in V2

        perspective = ""

        debate = ""

        propaganda = ""

        if "perspective" in planner.lower():

            perspective = "Perspective analysis executed."

        progress.progress(60)

        if "debate" in planner.lower():

            debate = "Debate executed."

        progress.progress(80)

        if "propaganda" in planner.lower():

            propaganda = "Propaganda analysis executed."

        with st.spinner(

            "Generating report..."

        ):

            report = final_answer(

                question,

                context,

                planner,

                perspective,

                debate,

                propaganda

            )

        progress.progress(100)

        st.divider()

        st.markdown("## Planner")

        st.code(

            planner,

            language="json"

        )

        st.divider()

        st.markdown("## Final Report")

        st.markdown(report)

        if docs:

            st.divider()

            st.markdown("## Sources")

            for d in docs:

                st.caption(
                    f"📄 {d['source']}"
                )

        logger.info(
            "Agent Mode completed."
        )