"""
NOVARYN Configuration
Central configuration for the entire application.
"""

import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# ----------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------

load_dotenv()

# ----------------------------------------------------
# Project Paths
# ----------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"

UPLOAD_DIR = DATA_DIR / "uploads"

FAISS_DIR = DATA_DIR / "faiss"

CACHE_DIR = DATA_DIR / "cache"

LOG_DIR = DATA_DIR / "logs"

TEMP_DIR = DATA_DIR / "temp"

ASSETS_DIR = ROOT_DIR / "assets"

THEME_DIR = ROOT_DIR / "theme"

TEST_DIR = ROOT_DIR / "tests"

# Automatically create required folders
for folder in [
    DATA_DIR,
    UPLOAD_DIR,
    FAISS_DIR,
    CACHE_DIR,
    LOG_DIR,
    TEMP_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------
# Application
# ----------------------------------------------------

APP_NAME = "NOVARYN"

APP_VERSION = "1.0.0"

APP_TAGLINE = "Global Intelligence Court"

PAGE_ICON = "⚖️"

DEFAULT_LAYOUT = "wide"

SIDEBAR_STATE = "expanded"

# ----------------------------------------------------
# Groq Configuration
# ----------------------------------------------------



GROQ_API_KEY = st.secrets["groq"]["api_key"]

GROQ_MODEL = "llama-3.3-70b-versatile"

TEMPERATURE = 0.30

MAX_TOKENS = 2048

REQUEST_TIMEOUT = 60

# ----------------------------------------------------
# Embedding Model
# ----------------------------------------------------

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

VECTOR_DISTANCE = "L2"

TOP_K_RESULTS = 5

# ----------------------------------------------------
# File Upload Settings
# ----------------------------------------------------

SUPPORTED_EXTENSIONS = [
    "pdf",
    "docx",
    "txt",
    "csv",
    "md"
]

MAX_FILE_SIZE_MB = 50

CHUNK_SIZE = 800

CHUNK_OVERLAP = 100

# ----------------------------------------------------
# Logging
# ----------------------------------------------------

LOG_LEVEL = "INFO"

LOG_FILE = LOG_DIR / "novaryn.log"

# ----------------------------------------------------
# Dashboard
# ----------------------------------------------------

MAX_RECENT_ACTIVITY = 25

# ----------------------------------------------------
# Session
# ----------------------------------------------------

SESSION_TIMEOUT_MINUTES = 60

# ----------------------------------------------------
# Theme
# ----------------------------------------------------

PRIMARY_COLOR = "#C9A44C"

BACKGROUND_COLOR = "#080808"

CARD_COLOR = "#1A1A1A"

TEXT_COLOR = "#F7F4EC"

# ----------------------------------------------------
# Agent Limits
# ----------------------------------------------------

MAX_AGENT_STEPS = 5

MAX_CONTEXT_RESULTS = 6

MAX_CHAT_HISTORY = 20

# ----------------------------------------------------
# Security
# ----------------------------------------------------

ALLOW_HTML = False

ENABLE_FILE_DELETE = True

ENABLE_EXPORT = True

ENABLE_CACHE = True

# ----------------------------------------------------
# Version Information
# ----------------------------------------------------

BUILD = "Production"

AUTHOR = "NOVARYN Team"