"""
NOVARYN File Intelligence

Upload, analyze, chunk, embed and index files.
Supports:
- PDF
- DOCX
- TXT
- CSV
- MD
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
from pathlib import Path
from pypdf import PdfReader
from docx import Document

from config.settings import (
    UPLOAD_DIR,
    SUPPORTED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

from core.logger import get_logger
from core.utils import (
    chunk_text,
    validate_extension,
    file_extension,
    file_size_mb,
)

from core.vector_store import vector_store
from core.session_utils import (
    add_uploaded_file,
    increment_processed_files,
)

logger = get_logger("file_intelligence")


# ==========================================================
# Readers
# ==========================================================

def read_pdf(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def read_docx(path):

    doc = Document(path)

    return "\n".join(
        p.text
        for p in doc.paragraphs
    )


def read_txt(path):

    with open(
        path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:

        return f.read()


def read_md(path):

    return read_txt(path)


def read_csv(path):

    df = pd.read_csv(path)

    return df.to_string()


# ==========================================================
# Extract
# ==========================================================

def extract_text(path):

    ext = file_extension(path)

    if ext == "pdf":
        return read_pdf(path)

    if ext == "docx":
        return read_docx(path)

    if ext == "txt":
        return read_txt(path)

    if ext == "md":
        return read_md(path)

    if ext == "csv":
        return read_csv(path)

    return ""


# ==========================================================
# UI
# ==========================================================

def show_file_intelligence():

    st.subheader("📂 File Intelligence")

    st.caption(
        "Upload files into the knowledge base."
    )

    uploaded = st.file_uploader(

        "Choose files",

        type=SUPPORTED_EXTENSIONS,

        accept_multiple_files=True

    )

    if uploaded:

        for file in uploaded:

            save_path = UPLOAD_DIR / file.name

            with open(save_path, "wb") as f:
                f.write(file.getbuffer())

            add_uploaded_file(file)

        st.success(
            f"{len(uploaded)} file(s) uploaded."
        )

    st.divider()

    files = sorted(
        UPLOAD_DIR.glob("*")
    )

    if not files:

        st.info(
            "No uploaded files."
        )

        return

    st.markdown("## Uploaded Files")

    for file in files:

        with st.expander(file.name):

            size = file_size_mb(file)

            st.write(
                f"Extension : {file_extension(file.name)}"
            )

            st.write(
                f"Size : {size:.2f} MB"
            )

            if not validate_extension(
                file.name,
                SUPPORTED_EXTENSIONS
            ):

                st.error(
                    "Unsupported file."
                )

                continue

            col1, col2, col3 = st.columns(3)

            with col1:

                if st.button(
                    f"Preview##{file.name}"
                ):

                    text = extract_text(file)

                    st.text_area(

                        "Preview",

                        text[:5000],

                        height=250

                    )

            with col2:

                if st.button(
                    f"Index##{file.name}"
                ):

                    text = extract_text(file)

                    chunks = chunk_text(

                        text,

                        CHUNK_SIZE,

                        CHUNK_OVERLAP

                    )

                    with st.spinner(
                        "Generating embeddings..."
                    ):

                        count = vector_store.add_documents(

                            chunks,

                            file.name

                        )

                    increment_processed_files()

                    st.success(
                        f"{count} chunks indexed."
                    )

                    logger.info(
                        f"{file.name} indexed."
                    )

            with col3:

                if st.button(
                    f"Delete##{file.name}"
                ):

                    Path(file).unlink(
                        missing_ok=True
                    )

                    st.success(
                        "Deleted."
                    )

                    st.rerun()

    st.divider()

    st.markdown("## Database")

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
        "Embedding",
        stats["embedding_model"]
    )

    st.divider()

    if st.button(
        "Index All Files",
        use_container_width=True
    ):

        total = 0

        progress = st.progress(0)

        for i, file in enumerate(files):

            text = extract_text(file)

            chunks = chunk_text(

                text,

                CHUNK_SIZE,

                CHUNK_OVERLAP

            )

            total += vector_store.add_documents(

                chunks,

                file.name

            )

            progress.progress(
                (i + 1) / len(files)
            )

        st.success(
            f"{total} chunks indexed successfully."
        )

        logger.info(
            "Bulk indexing completed."
        )