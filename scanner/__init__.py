"""
Aurva Data Scanner Module
========================

This module contains the core data scanning functionality for identifying
PII, PHI, and PCI data in uploaded files.
"""

from .broccoli_scanner import DataScanner

__version__ = "1.0.0"
__author__ = "Aurva Development Team"

__all__ = ["DataScanner"]
