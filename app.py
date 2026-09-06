import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

from agents.planner import plan
from agents.researcher import research
from agents.synthesizer import synthesize


load_dotenv()


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="ScholarAI",
    page_icon="📚",
    layout="wide"
)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    st.title("📚 ScholarAI")

    st.markdown(
        """
        ### AI Research Assistant

        ScholarAI can:

        - 🧠 Break a topic into research questions
        - 🔎 Search academic papers
        - 📚 Retrieve evidence from papers
        - 🌐 Search the web
        - ✍️ Synthesize research findings

        ---

        **Pipeline**

        `Plan → Research → Synthesize`
        """
    )

    st.info(
        "Demo mode is currently enabled while the Gemini API quota is unavailable."
    )


# -----------------------------
# Main page
# -----------------------------

st.title("📚 ScholarAI")

st.markdown(
    "### Your AI-powered research assistant"
)

st.write(
    "Enter a research topic and ScholarAI will break it down, "
    "investigate the questions, and generate a research report."
)

st.divider()


# -----------------------------
# Topic input
# -----------------------------

topic = st.text_area(
    "🔍 Research Topic",
    placeholder=(
        "Example: Recent advancements in Retrieval-Augmented Generation"
    ),
    height=120
)


# -----------------------------
# Research button
# -----------------------------

if st.button(
    "🚀 Start Research",
    type="primary",
    use_container_width=True
):

    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()


    # -------------------------
    # Research plan
    # -------------------------

    with st.status(
        "🧠 Creating research plan...",
        expanded=True
    ) as status:

        sub_questions = [
            f"What are the key concepts related to {topic}?",
            f"What are the recent advancements in {topic}?",
            f"What are the main challenges in {topic}?",
            f"What are the future directions for {topic}?"
        ]

        st.markdown("#### Research Questions")

        for i, question in enumerate(
            sub_questions,
            start=1
        ):
            st.write(f"**{i}.** {question}")

        status.update(
            label="✅ Research plan created",
            state="complete"
        )


    # -------------------------
    # Research
    # -------------------------

    with st.status(
        "🔎 Conducting research...",
        expanded=True
    ) as status:

        for i, question in enumerate(
            sub_questions,
            start=1
        ):

            st.write(
                f"**Question {i}:** {question}"
            )

            st.write(
                "Searching papers, retrieving evidence, and analyzing information..."
            )

        status.update(
            label="✅ Research completed",
            state="complete"
        )


    # -------------------------
    # Synthesis
    # -------------------------

    with st.status(
        "✍️ Synthesizing findings...",
        expanded=True
    ) as status:

        final_answer = f"""
## Overview

This is a temporary demonstration of ScholarAI for:

**{topic}**

## Key Findings

- ScholarAI decomposes the research topic into multiple sub-questions.
- Each sub-question can be independently researched.
- Academic papers and locally stored evidence can be used.
- The findings are eventually combined into a single research report.

## Detailed Analysis

The Gemini API is currently unavailable because the API rate limit
has been reached.

This demonstration allows the ScholarAI interface to be developed
without making additional API requests.

Once the API quota resets, this section will contain the real
AI-generated research synthesis.

## Sources

- Mock Academic Source — p. 1
- Mock Academic Source — p. 4
"""

        status.update(
            label="✅ Research report generated",
            state="complete"
        )


    # -------------------------
    # Final report
    # -------------------------

    st.divider()

    st.header("📄 Research Report")

    st.markdown(final_answer)