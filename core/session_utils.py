"""
NOVARYN Session Manager
Centralized Streamlit session state management.
"""

from __future__ import annotations

import streamlit as st
from typing import Any


# ==========================================================
# Default Session Values
# ==========================================================

DEFAULT_STATE = {

    # Navigation
    "active_module": "Dashboard",

    # Chat
    "chat_history": [],

    # Conversation Memory
    "memory": [],

    # Uploaded Files
    "uploaded_files": [],

    # Indexed Documents
    "documents": [],

    # Search Results
    "search_results": [],

    # User Settings
    "theme": "dark",

    # Runtime
    "groq_client": None,
    "vector_store": None,
    "embedding_model": None,

    # Statistics
    "queries": 0,
    "tokens": 0,
    "files_processed": 0,

    # Status
    "initialized": False
}


# ==========================================================
# Initialize
# ==========================================================

def initialize_session():
    """
    Initialize session state with default values.
    Safe to call multiple times.
    """

    for key, value in DEFAULT_STATE.items():

        if key not in st.session_state:
            st.session_state[key] = value


# ==========================================================
# Generic Methods
# ==========================================================

def get(key: str, default: Any = None):
    """
    Get session value.
    """

    return st.session_state.get(key, default)


def set(key: str, value: Any):
    """
    Set session value.
    """

    st.session_state[key] = value


def exists(key: str) -> bool:
    """
    Check whether key exists.
    """

    return key in st.session_state


def remove(key: str):
    """
    Remove a key.
    """

    if key in st.session_state:
        del st.session_state[key]


# ==========================================================
# Chat
# ==========================================================

def add_chat(role: str, message: str):
    """
    Add chat message.

    role:
        user
        assistant
        system
    """

    st.session_state.chat_history.append(
        {
            "role": role,
            "content": message
        }
    )


def clear_chat():
    """
    Clear chat history.
    """

    st.session_state.chat_history = []


# ==========================================================
# Memory
# ==========================================================

def add_memory(text: str):

    st.session_state.memory.append(text)


def clear_memory():

    st.session_state.memory = []


# ==========================================================
# Uploaded Files
# ==========================================================

def add_uploaded_file(file):

    st.session_state.uploaded_files.append(file)


def remove_uploaded_file(filename: str):

    st.session_state.uploaded_files = [

        f for f in st.session_state.uploaded_files

        if getattr(f, "name", "") != filename

    ]


# ==========================================================
# Statistics
# ==========================================================

def increment_queries():

    st.session_state.queries += 1


def increment_tokens(count: int):

    st.session_state.tokens += count


def increment_processed_files():

    st.session_state.files_processed += 1


# ==========================================================
# Reset
# ==========================================================

def reset():

    st.session_state.clear()

    initialize_session()


# ==========================================================
# Debug
# ==========================================================

def dump():

    """
    Return current session dictionary.
    """

    return dict(st.session_state)