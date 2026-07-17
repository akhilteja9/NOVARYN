"""
NOVARYN Knowledge Base
Manage manually added knowledge.
"""

from __future__ import annotations

import streamlit as st

from core.vector_store import vector_store
from core.session_utils import (
    increment_processed_files
)
from core.utils import chunk_text

from core.logger import get_logger

logger = get_logger("knowledge_base")


def show_knowledge_base():

    st.subheader("📚 Knowledge Base")

    st.caption(
        "Create, search and manage your knowledge."
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Add Knowledge",
            "Search",
            "Manage"
        ]
    )

    # =====================================================
    # Add Knowledge
    # =====================================================

    with tab1:

        st.markdown("### Add Knowledge")

        source = st.text_input(
            "Source Name",
            value="Manual Entry"
        )

        text = st.text_area(
            "Knowledge",
            height=250
        )

        chunk_size = st.slider(
            "Chunk Size",
            300,
            1200,
            800
        )

        overlap = st.slider(
            "Overlap",
            0,
            300,
            100
        )

        if st.button(
            "➕ Index Knowledge",
            use_container_width=True
        ):

            if not text.strip():

                st.warning(
                    "Enter some text."
                )

            else:

                chunks = chunk_text(
                    text,
                    chunk_size,
                    overlap
                )

                with st.spinner(
                    "Generating embeddings..."
                ):

                    indexed = vector_store.add_documents(
                        chunks,
                        source
                    )

                increment_processed_files()

                logger.info(
                    f"{indexed} chunks indexed."
                )

                st.success(
                    f"{indexed} chunks added successfully."
                )

    # =====================================================
    # Search
    # =====================================================

    with tab2:

        st.markdown("### Semantic Search")

        query = st.text_input(
            "Search Query"
        )

        top_k = st.slider(
            "Results",
            1,
            20,
            5
        )

        if st.button(
            "🔍 Search",
            use_container_width=True
        ):

            results = vector_store.search(
                query,
                top_k
            )

            if not results:

                st.info(
                    "No results found."
                )

            else:

                for i, item in enumerate(results):

                    with st.expander(
                        f"Result {i+1}"
                    ):

                        st.write(
                            item["text"]
                        )

                        st.caption(
                            f"Source : {item['source']}"
                        )

                        st.caption(
                            f"Distance : {item['score']:.4f}"
                        )

    # =====================================================
    # Manage
    # =====================================================

    with tab3:

        st.markdown(
            "### Database Statistics"
        )

        stats = vector_store.stats()

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Documents",
            stats["documents"]
        )

        c2.metric(
            "Vectors",
            stats["vectors"]
        )

        c3.metric(
            "Dimension",
            stats["dimension"]
        )

        st.divider()

        st.markdown(
            "### Stored Knowledge"
        )

        if not vector_store.metadata:

            st.info(
                "Knowledge base is empty."
            )

        else:

            for i, item in enumerate(
                vector_store.metadata
            ):

                with st.expander(
                    f"{i+1}. {item['source']}"
                ):

                    st.write(
                        item["text"]
                    )

                    st.caption(
                        item["fingerprint"][:16]
                    )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "💾 Save Database",
                use_container_width=True
            ):

                vector_store.save()

                st.success(
                    "Database saved."
                )

        with col2:

            if st.button(
                "🗑 Clear Database",
                use_container_width=True
            ):

                vector_store.delete_all()

                st.success(
                    "Knowledge base cleared."
                )

        st.divider()

        st.download_button(
            "⬇ Export Metadata",
            data=str(vector_store.metadata),
            file_name="knowledge_metadata.txt",
            mime="text/plain",
            use_container_width=True
        )