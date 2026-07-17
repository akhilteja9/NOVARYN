"""
NOVARYN Utility Functions
Shared helper functions used across the project.
"""

from __future__ import annotations

import hashlib
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List


# =====================================================
# Time
# =====================================================

def current_timestamp() -> str:
    """Return current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def unix_time() -> int:
    """Return Unix timestamp."""
    return int(time.time())


# =====================================================
# File Helpers
# =====================================================

def file_extension(filename: str) -> str:
    """Return lowercase extension."""
    return Path(filename).suffix.lower().replace(".", "")


def file_size_mb(file_path: str | Path) -> float:
    """Return file size in MB."""
    size = os.path.getsize(file_path)
    return round(size / (1024 * 1024), 2)


def ensure_directory(path: str | Path):
    """Create directory if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)


# =====================================================
# Validation
# =====================================================

def validate_extension(filename: str, allowed: List[str]) -> bool:
    """Check whether file extension is allowed."""
    return file_extension(filename) in allowed


# =====================================================
# Text Chunking
# =====================================================

def chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 100,
) -> List[str]:
    """
    Split long text into overlapping chunks.
    """

    text = text.strip()

    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


# =====================================================
# Hashing
# =====================================================

def md5(text: str) -> str:
    return hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()


def sha256(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


# =====================================================
# Duplicate Detection
# =====================================================

def text_fingerprint(text: str) -> str:
    """
    Stable fingerprint used to detect duplicate
    knowledge base entries.
    """
    return sha256(text.strip().lower())


# =====================================================
# Formatting
# =====================================================

def truncate(text: str, length: int = 250) -> str:
    """Short preview."""
    if len(text) <= length:
        return text

    return text[:length].rstrip() + "..."


def format_number(number: int) -> str:
    """Thousands separator."""
    return f"{number:,}"


# =====================================================
# Search Helpers
# =====================================================

def unique_results(results: list) -> list:
    """
    Remove duplicate search results.
    """

    seen = set()

    cleaned = []

    for item in results:

        key = item.get("text", "")

        if key not in seen:
            cleaned.append(item)
            seen.add(key)

    return cleaned


# =====================================================
# Health Check
# =====================================================

def system_health() -> dict:
    """
    Basic application health information.
    """

    return {
        "status": "healthy",
        "timestamp": current_timestamp(),
        "platform": os.name,
        "python": os.sys.version.split()[0],
    }