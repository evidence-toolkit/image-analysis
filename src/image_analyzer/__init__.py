"""
Image Evidence Analyzer

AI-powered forensic image analysis for legal evidence processing.
Supports multiple legal domains including employment law, personal injury, criminal law, civil litigation, regulatory compliance, and family law.

Configuration system supports environment-aware operation with development, testing, production, and legal production modes.
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

# Import configuration system
try:
    from ..config.config import (
        get_config,
        get_legal_domain_config,
        Environment,
        Config,
        ConfigManager
    )
    _config_available = True
except ImportError:
    _config_available = False

__version__ = "0.1.1"
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

# Add configuration exports if available
if _config_available:
    __all__.extend([
        "get_config",
        "get_legal_domain_config",
        "Environment",
        "Config",
        "ConfigManager"
    ])