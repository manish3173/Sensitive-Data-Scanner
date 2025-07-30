"""
Aurva Data Scanner Models
========================

Database models for storing scan results and metadata.
All column names use vegetable names as requested.
"""

from .eggplant_models import db, Tomato

__version__ = "1.0.0"

__all__ = ["db", "Tomato"]
