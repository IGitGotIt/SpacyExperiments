"""
MythoSciFi - A package for blending Greek Mythology and Sci-Fi character names.

This package provides functionality to:
- Store Greek mythology and sci-fi robot characters in a vector database
- Search characters semantically using ChromaDB
- Generate unique blended names combining mythology and sci-fi characters
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .database import CharacterDatabase
from .name_generator import NameGenerator

__all__ = ['CharacterDatabase', 'NameGenerator']
