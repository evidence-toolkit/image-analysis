"""
Image Evidence Analyzer

AI-powered forensic image analysis for legal evidence processing.
Specializes in UK employment law violations and workplace safety documentation.
"""

from .core_analyzer import (
    LegalEvidenceAnalyzer,
    EvidenceOrganizer,
    LegalEvidence,
    LegalEvidenceWithPath,
    SeverityLevel,
    EvidenceType
)

__version__ = "0.1.0"
__author__ = "Evidence Toolkit Contributors"

__all__ = [
    "LegalEvidenceAnalyzer",
    "EvidenceOrganizer",
    "LegalEvidence",
    "LegalEvidenceWithPath",
    "SeverityLevel",
    "EvidenceType"
]