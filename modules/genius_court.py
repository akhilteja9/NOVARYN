"""
NOVARYN Genius Court

Multi-Agent Debate Engine

Roles
-----
1. Prosecutor
2. Defender
3. Expert Analyst
4. Judge

Each agent receives the same evidence from the
knowledge base before debating.
"""

from __future__ import annotations

import streamlit as st

from core.groq_client import groq_client
from core.vector_store import vector_store
from core.logger import get_logger
from core.session_utils import increment_queries

logger = get_logger("genius_court")


# ==========================================================
# Agents
# ==========================================================

AGENTS = {

    "Prosecutor":
"""
You are the Prosecutor.

Challenge every assumption.

Find weaknesses.

Point out flaws.

Use evidence only.
""",

    "Defender":
"""
You are the Defender.

Support the proposal.

Highlight strengths.

Use only provided evidence.
""",

    "Expert":
"""
You are an independent expert.

Remain unbiased.

Provide factual analysis only.
""",

    "Judge":
"""
You are the Judge.

Read every argument.

Determine

• strongest evidence

• weakest argument

• final verdict

• confidence score

Remain neutral.
"""
}


# ==========================================================
# Context
# ==========================================================

def retrieve_context(question):

    docs = vector_store.search(question)

    context = "\n\n".join(
        d["text"]
        for d in docs
    )

    return context, docs


# ==========================================================
# Agent
# ==========================================================

def run_agent(role, question, context):

    messages = [

        {

            "role":"system",

            "content":AGENTS[role]

        },

        {

            "role":"user",

            "content":
f"""
Evidence

{context}

Question

{question}
"""

        }

    ]

    return groq_client.chat(messages)


# ==========================================================
# Judge
# ==========================================================

def judge(question,
          prosecutor,
          defender,
          expert):

    prompt = [

        {

            "role":"system",

            "content":AGENTS["Judge"]

        },

        {

            "role":"user",

            "content":
f"""
Question

{question}

------------------

Prosecutor

{prosecutor}

------------------

Defender

{defender}

------------------

Expert

{expert}
"""

        }

    ]

    return groq_client.chat(prompt)


# ==========================================================
# UI
# ==========================================================

def show_genius_court():

    st.subheader("⚖️ Genius Court")

    st.caption(
        "Multi-Agent Debate Engine"
    )

    question = st.text_area(

        "Case",

        height=120,

        placeholder="Should facial recognition be banned?"

    )

    if st.button(

        "Start Trial",

        use_container_width=True

    ):

        if not question:

            st.warning(
                "Enter a case."
            )

            return

        increment_queries()

        context, docs = retrieve_context(
            question
        )

        progress = st.progress(0)

        with st.spinner(
            "Prosecutor..."
        ):

            prosecutor = run_agent(
                "Prosecutor",
                question,
                context
            )

        progress.progress(25)

        with st.spinner(
            "Defender..."
        ):

            defender = run_agent(
                "Defender",
                question,
                context
            )

        progress.progress(50)

        with st.spinner(
            "Expert..."
        ):

            expert = run_agent(
                "Expert",
                question,
                context
            )

        progress.progress(75)

        with st.spinner(
            "Judge..."
        ):

            verdict = judge(

                question,

                prosecutor,

                defender,

                expert

            )

        progress.progress(100)

        st.divider()

        with st.expander(
            "🟥 Prosecutor",
            expanded=True
        ):

            st.markdown(
                prosecutor
            )

        with st.expander(
            "🟩 Defender",
            expanded=True
        ):

            st.markdown(
                defender
            )

        with st.expander(
            "🟦 Expert",
            expanded=True
        ):

            st.markdown(
                expert
            )

        st.divider()

        st.markdown(
            "## 👨‍⚖️ Judge Verdict"
        )

        st.success(
            verdict
        )

        st.divider()

        st.markdown(
            "### Evidence Used"
        )

        if docs:

            for doc in docs:

                st.caption(
                    f"📄 {doc['source']}"
                )

        else:

            st.info(
                "No evidence found."
            )

        logger.info(
            "Genius Court trial completed."
        )