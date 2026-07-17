"""
NOVARYN Exception Handling
Centralized exception definitions and decorators.
"""

from functools import wraps
from typing import Callable, Any

from core.logger import get_logger

logger = get_logger("exceptions")


# ====================================================
# Base Exception
# ====================================================

class NovarynError(Exception):
    """Base class for all NOVARYN exceptions."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# ====================================================
# Configuration
# ====================================================

class ConfigurationError(NovarynError):
    """Invalid or missing configuration."""


# ====================================================
# API
# ====================================================

class APIError(NovarynError):
    """External API failure."""


class AuthenticationError(APIError):
    """API authentication failed."""


class RateLimitError(APIError):
    """API rate limit exceeded."""


# ====================================================
# Vector Store
# ====================================================

class VectorStoreError(NovarynError):
    """Vector database operation failed."""


class EmbeddingError(VectorStoreError):
    """Embedding generation failed."""


# ====================================================
# Files
# ====================================================

class FileProcessingError(NovarynError):
    """Unable to process uploaded file."""


class UnsupportedFileType(FileProcessingError):
    """Unsupported file format."""


class FileTooLarge(FileProcessingError):
    """Uploaded file exceeds allowed size."""


# ====================================================
# Knowledge Base
# ====================================================

class KnowledgeBaseError(NovarynError):
    """Knowledge base operation failed."""


# ====================================================
# Agent
# ====================================================

class AgentExecutionError(NovarynError):
    """Agent execution failed."""


# ====================================================
# Decorator
# ====================================================

def handle_exceptions(default_return=None):
    """
    Decorator for consistent exception handling.

    Example:

    @handle_exceptions([])
    def search():
        ...
    """

    def decorator(func: Callable):

        @wraps(func)
        def wrapper(*args, **kwargs):

            try:
                return func(*args, **kwargs)

            except NovarynError as e:
                logger.error(f"{func.__name__}: {e}")
                return default_return

            except Exception as e:
                logger.exception(
                    f"Unhandled exception in {func.__name__}: {e}"
                )
                return default_return

        return wrapper

    return decorator


# ====================================================
# Utility
# ====================================================

def raise_if(condition: bool, exception: Exception):
    """
    Raise an exception if condition is True.

    Example:
        raise_if(api_key == "", ConfigurationError("Missing API Key"))
    """

    if condition:
        raise exception