"""
NOVARYN Propaganda Detector

Detects:
- Bias
- Propaganda techniques
- Logical fallacies
- Emotional manipulation
- Credibility
- Neutral rewrite
"""

from __future__ import annotations

import streamlit as st

from core.groq_client import groq_client
from core.logger import get_logger
from core.session_utils import increment_queries

logger = get_logger("propaganda_detector")


# ==========================================================
# Prompt
# ==========================================================

SYSTEM_PROMPT = """
You are an Intelligence Analyst.

Analyze the supplied text.

Return your response in Markdown.

Sections

1. Overall Risk Score (0-100)

2. Political / Ideological Bias

3. Emotional Manipulation

4. Propaganda Techniques

5. Logical Fallacies

6. Misinformation Risk

7. Credibility Assessment

8. Missing Evidence

9. Neutral Rewrite

10. Final Recommendation

Be objective.

Do not invent facts.
"""


# ==========================================================
# Analysis
# ==========================================================

def analyze(text):

    messages = [

        {

            "role":"system",

            "content":SYSTEM_PROMPT

        },

        {

            "role":"user",

            "content":text

        }

    ]

    return groq_client.chat(messages)


# ==========================================================
# UI
# ==========================================================

def show_propaganda_detector():

    st.subheader("🛡️ Propaganda Detector")

    st.caption(
        "Detect bias, manipulation and misinformation."
    )

    tab1, tab2 = st.tabs(

        [

            "Analyzer",

            "Examples"

        ]

    )

    # ======================================================
    # Analyzer
    # ======================================================

    with tab1:

        text = st.text_area(

            "Paste article, speech or social media post",

            height=300

        )

        col1, col2 = st.columns(2)

        with col1:

            detailed = st.checkbox(

                "Detailed Analysis",

                True

            )

        with col2:

            show_rewrite = st.checkbox(

                "Generate Neutral Rewrite",

                True

            )

        if st.button(

            "Analyze",

            use_container_width=True

        ):

            if not text.strip():

                st.warning(
                    "Please enter some text."
                )

                return

            increment_queries()

            with st.spinner(

                "Analyzing..."

            ):

                result = analyze(text)

            st.divider()

            st.markdown(result)

            logger.info(
                "Propaganda analysis completed."
            )

            if show_rewrite:

                rewrite_prompt = [

                    {

                        "role":"system",

                        "content":
"""
Rewrite the supplied text.

Requirements

- Neutral

- Objective

- Remove emotional language

- Preserve factual meaning

Return only rewritten text.
"""

                    },

                    {

                        "role":"user",

                        "content":text

                    }

                ]

                rewrite = groq_client.chat(

                    rewrite_prompt

                )

                st.divider()

                st.markdown(

                    "## Neutral Rewrite"

                )

                st.success(

                    rewrite

                )

    # ======================================================
    # Examples
    # ======================================================

    with tab2:

        st.markdown("""

### Detectable Techniques

- Emotional Language

- Fear Appeals

- False Dilemma

- Cherry Picking

- Bandwagon

- Ad Hominem

- Slippery Slope

- Appeal to Authority

- Whataboutism

- Loaded Language

- Confirmation Bias

- Repetition

- Oversimplification

- Misinformation Indicators

""")

        st.info(

            "The detector assists analysis and does not determine truth. Human verification is always recommended."

        )