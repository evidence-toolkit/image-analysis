"""
Image Evidence Analyzer

AI-powered forensic image analysis for legal evidence processing.
Supports multiple legal domains including employment law, personal injury, criminal law, civil litigation, regulatory compliance, and family law.
"""

from .core_analyzer import (
    LegalEvidenceAnalyzer,
    EvidenceOrganizer,
    LegalEvidence,
    LegalEvidenceWithPath,
    SeverityLevel,
    EvidenceType,
    LegalDomain,
    DomainConfig
)

__version__ = "0.1.0"
__author__ = "Evidence Toolkit Contributors"

__all__ = [
    "LegalEvidenceAnalyzer",
    "EvidenceOrganizer",
    "LegalEvidence",
    "LegalEvidenceWithPath",
    "SeverityLevel",
    "EvidenceType",
    "LegalDomain",
    "DomainConfig"
]