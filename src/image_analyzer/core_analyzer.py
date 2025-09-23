#!/usr/bin/env python3
"""
Legal Evidence Analysis System V2 - Core Architecture
Simple, powerful design focused on OpenAI structured outputs for legal evidence.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from pathlib import Path
import base64
import json
import concurrent.futures
import threading
import time
import os
import hashlib
import platform
import uuid
import functools
import random
from datetime import datetime
from openai import OpenAI

# Import configuration system
try:
    from ..config.config import get_config, get_legal_domain_config, Environment  # type: ignore
except ImportError:
    # Fallback for direct execution
    import sys
    sys.path.append(str(Path(__file__).parent.parent))
    from config.config import get_config, get_legal_domain_config, Environment  # type: ignore

# =============================================================================
# CORE MODELS - The Heart of V2 System
# =============================================================================

class SeverityLevel(str, Enum):
    """Evidence severity for legal prioritization"""
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class LegalDomain(str, Enum):
    """Legal domain specializations for evidence analysis"""
    employment_law = "employment_law"
    personal_injury = "personal_injury"
    criminal_law = "criminal_law"
    civil_litigation = "civil_litigation"
    regulatory_compliance = "regulatory_compliance"
    family_law = "family_law"

class EvidenceType(str, Enum):
    """Flexible legal evidence categories adaptable to different legal domains"""
    # Employment Law
    workplace_safety = "workplace_safety"
    discrimination = "discrimination"
    harassment = "harassment"
    policy_violation = "policy_violation"

    # Personal Injury
    negligence = "negligence"
    premises_liability = "premises_liability"
    product_defect = "product_defect"
    medical_evidence = "medical_evidence"

    # Criminal Law
    crime_scene = "crime_scene"
    evidence_tampering = "evidence_tampering"
    forensic_evidence = "forensic_evidence"
    witness_evidence = "witness_evidence"

    # Civil/General
    contract_breach = "contract_breach"
    property_damage = "property_damage"
    documentation = "documentation"
    procedural_violation = "procedural_violation"

    # Regulatory
    regulatory_violation = "regulatory_violation"
    compliance_failure = "compliance_failure"

    # Severity-based (backwards compatibility)
    critical_violation = "critical_violation"

    # Legacy (backwards compatibility)
    health_safety = "workplace_safety"  # Alias for backwards compatibility
    cleanliness = "workplace_safety"     # Maps to workplace safety

# =============================================================================
# DOMAIN CONFIGURATION - Legal Framework Specifications
# =============================================================================

class DomainConfig:
    """Configuration for legal domain-specific analysis - now loads from config files"""

    @staticmethod
    def get_evidence_types(domain: LegalDomain) -> List[str]:
        """Get relevant evidence types for a legal domain from configuration"""
        try:
            domain_config = get_legal_domain_config(domain.value)
            if 'evidence_types' in domain_config:
                return domain_config['evidence_types']
        except Exception:
            pass

        # Fallback to hardcoded values for backward compatibility
        evidence_map = {
            LegalDomain.employment_law: [
                "workplace_safety", "discrimination", "harassment", "policy_violation", "critical_violation"
            ],
            LegalDomain.personal_injury: [
                "negligence", "premises_liability", "product_defect", "medical_evidence", "critical_violation"
            ],
            LegalDomain.criminal_law: [
                "crime_scene", "evidence_tampering", "forensic_evidence", "witness_evidence", "critical_violation"
            ],
            LegalDomain.civil_litigation: [
                "contract_breach", "property_damage", "documentation", "procedural_violation"
            ],
            LegalDomain.regulatory_compliance: [
                "regulatory_violation", "compliance_failure", "documentation", "critical_violation"
            ],
            LegalDomain.family_law: [
                "documentation", "procedural_violation", "property_damage"
            ]
        }
        return evidence_map.get(domain, ["documentation", "critical_violation"])

    @staticmethod
    def get_directory_structure(domain: LegalDomain) -> List[str]:
        """Get evidence organization directories for a legal domain from configuration"""
        try:
            domain_config = get_legal_domain_config(domain.value)
            if 'directory_structure' in domain_config:
                return domain_config['directory_structure']
        except Exception:
            pass

        # Fallback to hardcoded values for backward compatibility
        structure_map = {
            LegalDomain.employment_law: [
                "critical_violations", "workplace_safety_violations", "discrimination_evidence", "documentation"
            ],
            LegalDomain.personal_injury: [
                "critical_violations", "negligence_evidence", "premises_liability", "medical_evidence", "documentation"
            ],
            LegalDomain.criminal_law: [
                "critical_evidence", "crime_scene_evidence", "forensic_evidence", "witness_evidence", "documentation"
            ],
            LegalDomain.civil_litigation: [
                "contract_evidence", "property_damage", "procedural_evidence", "documentation"
            ],
            LegalDomain.regulatory_compliance: [
                "critical_violations", "regulatory_violations", "compliance_failures", "documentation"
            ],
            LegalDomain.family_law: [
                "evidence", "property_documentation", "procedural_evidence", "documentation"
            ]
        }
        return structure_map.get(domain, ["critical_violations", "evidence", "documentation"])

    @staticmethod
    def get_analysis_prompt(domain: LegalDomain) -> str:
        """Get domain-specific analysis prompt for legal evidence from configuration"""
        try:
            domain_config = get_legal_domain_config(domain.value)
            if 'analysis_prompts' in domain_config and 'system_prompt' in domain_config['analysis_prompts']:
                return domain_config['analysis_prompts']['system_prompt']
        except Exception:
            pass

        # Fallback to hardcoded values for backward compatibility
        prompts = {
            LegalDomain.employment_law: """You are a forensic image analyst specializing in employment law evidence.

Analyze this image with the expertise of a professional forensic examiner preparing evidence for employment law proceedings.

Focus on:
- Health & Safety at Work Act violations
- Workplace discrimination evidence
- Harassment documentation
- Policy violations
- Regulatory compliance issues
- Documentation and record-keeping problems

Provide thorough, objective analysis suitable for employment law proceedings.""",

            LegalDomain.personal_injury: """You are a forensic image analyst specializing in personal injury evidence.

Analyze this image with the expertise of a professional forensic examiner preparing evidence for personal injury litigation.

Focus on:
- Negligence evidence
- Premises liability conditions
- Product defects or failures
- Medical evidence documentation
- Accident scene analysis
- Safety hazards and violations

Provide thorough, objective analysis suitable for personal injury litigation.""",

            LegalDomain.criminal_law: """You are a forensic image analyst specializing in criminal evidence.

Analyze this image with the expertise of a professional forensic examiner preparing evidence for criminal proceedings.

Focus on:
- Crime scene documentation
- Evidence tampering indicators
- Forensic evidence preservation
- Witness evidence corroboration
- Chain of custody considerations
- Criminal activity indicators

Provide thorough, objective analysis suitable for criminal court proceedings.""",

            LegalDomain.civil_litigation: """You are a forensic image analyst specializing in civil litigation evidence.

Analyze this image with the expertise of a professional forensic examiner preparing evidence for civil court proceedings.

Focus on:
- Contract breach evidence
- Property damage documentation
- Procedural violations
- Documentation authenticity
- Compliance with civil procedures
- Damages assessment support

Provide thorough, objective analysis suitable for civil litigation.""",

            LegalDomain.regulatory_compliance: """You are a forensic image analyst specializing in regulatory compliance evidence.

Analyze this image with the expertise of a professional forensic examiner preparing evidence for regulatory proceedings.

Focus on:
- Regulatory violations
- Compliance failures
- Industry standard deviations
- Documentation deficiencies
- Safety standard violations
- Procedural non-compliance

Provide thorough, objective analysis suitable for regulatory proceedings.""",

            LegalDomain.family_law: """You are a forensic image analyst specializing in family law evidence.

Analyze this image with the expertise of a professional forensic examiner preparing evidence for family court proceedings.

Focus on:
- Property condition documentation
- Living environment assessment
- Safety concerns for minors
- Procedural evidence
- Documentation authenticity
- Custody-related evidence

Provide thorough, objective analysis suitable for family law proceedings."""
        }

        return prompts.get(domain, """You are a forensic image analyst specializing in legal evidence.

Analyze this image with the expertise of a professional forensic examiner preparing evidence for legal proceedings.

Focus on:
- Evidence documentation
- Procedural violations
- Documentation authenticity
- Legal relevance assessment
- Expert witness considerations

Provide thorough, objective analysis suitable for legal proceedings.""")

class LegalEvidence(BaseModel):
    """Core structured output for legal evidence analysis"""

    # Evidence Classification
    evidence_type: EvidenceType = Field(description="Primary legal category")
    severity_level: SeverityLevel = Field(description="Legal urgency rating")

    # Legal Content
    legal_relevance: str = Field(description="Direct relevance to applicable legal framework")
    compliance_violations: str = Field(description="Specific regulation violations identified")
    expert_witness_notes: str = Field(description="Professional forensic observations")

    # Actionable Intelligence
    immediate_action_required: bool = Field(description="Requires urgent legal attention")
    evidence_strength: str = Field(description="Quality and admissibility assessment")
    supporting_documentation_needed: str = Field(description="Additional evidence requirements")

class LegalEvidenceWithPath(LegalEvidence):
    """Extended evidence model with source path tracking"""
    image_path: str = Field(description="Path to source image file")

    # Expert Review Tracking
    requires_expert_review: bool = Field(default=False, description="Flagged for expert review")
    expert_review_reason: str = Field(default="", description="Reason for expert review requirement")
    confidence_score: float = Field(default=0.0, description="Calculated confidence score")

# =============================================================================
# OUTPUT FORMATTER - Configurable Output Helpers
# =============================================================================

class OutputFormatter:
    """Helper class for configurable output formatting"""

    def __init__(self, config):
        self.config = config

    def format_cost(self, cost: float, precision: bool = False) -> str:
        """Format cost with configurable decimal places"""
        if precision:
            return f"${cost:.{self.config.output.cost_precision_places}f}"
        else:
            return f"${cost:.{self.config.output.cost_decimal_places}f}"

    def get_icon(self, icon_type: str) -> str:
        """Get icon with emoji support check"""
        if not self.config.output.use_emojis:
            return ""

        icon_map = {
            'success': self.config.output.success_icon,
            'error': self.config.output.error_icon,
            'info': self.config.output.info_icon,
            'cost': self.config.output.cost_icon,
            'folder': self.config.output.folder_icon,
            'processing': self.config.output.processing_icon
        }
        return icon_map.get(icon_type, "")

    def format_progress(self, icon_type: str, message: str) -> str:
        """Format progress message with optional emoji"""
        icon = self.get_icon(icon_type)
        if icon:
            return f"{icon} {message}"
        else:
            return message

# =============================================================================
# AUDIT LOGGING AND CHAIN OF CUSTODY - Legal Compliance
# =============================================================================

class AuditLogger:
    """Configurable audit logging for legal compliance"""

    def __init__(self, config, output_dir: Path):
        self.config = config
        self.output_dir = output_dir
        self.session_id = str(uuid.uuid4())
        self.audit_log_path = output_dir / config.legal.audit_log_file

        # Ensure log directory exists
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize audit log
        if config.legal.audit_logging:
            self._log_session_start()

    def _log_session_start(self):
        """Log start of analysis session"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id,
            "event_type": "session_start",
            "environment": os.getenv('IMAGE_ANALYZER_ENV', 'development'),
            "system_info": {
                "platform": platform.platform(),
                "python_version": platform.python_version(),
                "hostname": platform.node()
            } if self.config.legal.include_environment_info else {}
        }
        self._write_audit_entry(audit_entry)

    def log_analysis_start(self, image_path: str, domain: str):
        """Log start of image analysis"""
        if not self.config.legal.audit_logging:
            return

        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id,
            "event_type": "analysis_start",
            "image_path": image_path,
            "legal_domain": domain,
            "checksum": self._calculate_checksum(image_path) if self.config.legal.include_checksums else None
        }
        self._write_audit_entry(audit_entry)

    def log_api_call(self, model: str, cost: float, success: bool, error: str = None):
        """Log API call details"""
        if not self.config.legal.log_api_calls:
            return

        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id,
            "event_type": "api_call",
            "model": model,
            "cost": cost,
            "success": success,
            "error": error
        }
        self._write_audit_entry(audit_entry)

    def log_file_operation(self, operation: str, source: str, destination: str = None):
        """Log file copy/move operations"""
        if not self.config.legal.log_file_operations:
            return

        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id,
            "event_type": "file_operation",
            "operation": operation,
            "source": source,
            "destination": destination,
            "source_checksum": self._calculate_checksum(source) if self.config.legal.include_checksums else None
        }
        self._write_audit_entry(audit_entry)

    def log_analysis_complete(self, image_path: str, evidence_type: str, severity: str, requires_expert_review: bool, confidence_score: float):
        """Log completion of analysis"""
        if not self.config.legal.audit_logging:
            return

        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id,
            "event_type": "analysis_complete",
            "image_path": image_path,
            "evidence_type": evidence_type,
            "severity": severity,
            "requires_expert_review": requires_expert_review,
            "confidence_score": confidence_score
        }
        self._write_audit_entry(audit_entry)

    def log_cost_event(self, event_type: str, amount: float, cumulative_cost: float):
        """Log cost-related events"""
        if not self.config.legal.log_cost_tracking:
            return

        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id,
            "event_type": "cost_event",
            "cost_event_type": event_type,
            "amount": amount,
            "cumulative_cost": cumulative_cost
        }
        self._write_audit_entry(audit_entry)

    def _calculate_checksum(self, file_path: str) -> str:
        """Calculate SHA-256 checksum of file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return None

    def _write_audit_entry(self, entry: dict):
        """Write audit entry to log file"""
        try:
            if self.config.legal.audit_log_format == "json":
                with open(self.audit_log_path, 'a') as f:
                    f.write(json.dumps(entry) + "\n")
            elif self.config.legal.audit_log_format == "text":
                with open(self.audit_log_path, 'a') as f:
                    f.write(f"{entry['timestamp']} - {entry['event_type']} - {entry.get('image_path', '')}\n")
        except Exception as e:
            print(f"Warning: Failed to write audit log: {e}")


class ChainOfCustodyTracker:
    """Track chain of custody for legal evidence"""

    def __init__(self, config, output_dir: Path):
        self.config = config
        self.output_dir = output_dir
        self.custody_log_path = output_dir / config.legal.chain_of_custody_file
        self.custody_data = {"session_id": str(uuid.uuid4()), "custody_entries": []}

        # Initialize chain of custody tracking
        if config.legal.chain_of_custody:
            self._initialize_custody_log()

    def _initialize_custody_log(self):
        """Initialize chain of custody log"""
        self.custody_data.update({
            "created_timestamp": datetime.utcnow().isoformat(),
            "system_info": {
                "platform": platform.platform(),
                "hostname": platform.node(),
                "user": os.getenv('USER', 'unknown'),
                "environment": os.getenv('IMAGE_ANALYZER_ENV', 'development')
            } if self.config.legal.include_environment_info else {}
        })

    def add_custody_entry(self, image_path: str, operation: str, destination: str = None):
        """Add entry to chain of custody"""
        if not self.config.legal.chain_of_custody:
            return

        custody_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "image_path": image_path,
            "operation": operation,
            "destination": destination,
            "checksum": self._calculate_checksum(image_path) if self.config.legal.include_checksums else None,
            "file_size": os.path.getsize(image_path) if os.path.exists(image_path) else None
        }

        self.custody_data["custody_entries"].append(custody_entry)
        self._save_custody_log()

    def _calculate_checksum(self, file_path: str) -> str:
        """Calculate SHA-256 checksum of file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return None

    def _save_custody_log(self):
        """Save chain of custody log to file"""
        try:
            with open(self.custody_log_path, 'w') as f:
                json.dump(self.custody_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save chain of custody log: {e}")

    def finalize_custody_log(self, total_files: int, expert_review_count: int):
        """Finalize chain of custody with summary"""
        if not self.config.legal.chain_of_custody:
            return

        self.custody_data.update({
            "completed_timestamp": datetime.utcnow().isoformat(),
            "summary": {
                "total_files_processed": total_files,
                "expert_review_required": expert_review_count,
                "total_custody_entries": len(self.custody_data["custody_entries"])
            }
        })
        self._save_custody_log()


# =============================================================================
# RETRY SYSTEM - Configurable Retry Logic for API Calls
# =============================================================================

from openai import RateLimitError, APITimeoutError, APIConnectionError

def retry_on_failure(config):
    """Decorator for retrying API calls with exponential backoff"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(config.analysis.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    # Check if we should retry this type of error
                    should_retry = (
                        (isinstance(e, RateLimitError) and config.analysis.retry_on_rate_limit) or
                        (isinstance(e, APITimeoutError) and config.analysis.retry_on_timeout) or
                        (isinstance(e, APIConnectionError) and config.analysis.retry_on_connection_error)
                    )

                    if not should_retry or attempt >= config.analysis.max_retries:
                        raise e

                    # Calculate exponential backoff delay with jitter
                    delay = min(
                        config.analysis.retry_delay_base * (2 ** attempt),
                        config.analysis.retry_delay_max
                    )
                    # Add random jitter to prevent thundering herd
                    jittered_delay = delay * (0.5 + random.random() * 0.5)

                    print(f"API call failed (attempt {attempt + 1}/{config.analysis.max_retries + 1}): {e}")
                    print(f"Retrying in {jittered_delay:.1f} seconds...")
                    time.sleep(jittered_delay)

            # If we get here, all retries failed
            raise last_exception
        return wrapper
    return decorator

# =============================================================================
# CORE ANALYZER - The Analysis Engine
# =============================================================================

class LegalEvidenceAnalyzer:
    """OpenAI-powered forensic image analysis for multi-domain legal evidence"""

    def __init__(self, api_key: str, legal_domain: LegalDomain = LegalDomain.employment_law,
                 environment: Optional[Environment] = None):
        # Load configuration
        self.config = get_config(environment)
        self.legal_domain_config = get_legal_domain_config(legal_domain.value)

        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key, timeout=self.config.openai.timeout)
        self.legal_domain = legal_domain

        # Cost tracking with thread safety
        self.total_cost = 0.0
        self.daily_cost = 0.0  # Track daily spending
        self.lock = threading.Lock()

        # Performance settings
        self.max_workers = self.config.performance.max_workers
        self.request_delay = self.config.performance.request_delay

        # Output formatter
        self.formatter = OutputFormatter(self.config)

        # Audit logging and chain of custody (initialized when output directory is set)
        self.audit_logger = None
        self.custody_tracker = None

    def initialize_audit_logging(self, output_dir: Path):
        """Initialize audit logging and chain of custody tracking"""
        if self.config.legal.audit_logging:
            self.audit_logger = AuditLogger(self.config, output_dir)

        if self.config.legal.chain_of_custody:
            self.custody_tracker = ChainOfCustodyTracker(self.config, output_dir)

    def encode_image(self, image_path: Path) -> str:
        """Convert image to base64 for OpenAI Vision API with security validation"""
        # Security validation
        if self.config.security.validate_file_types:
            if not self._validate_image_file(image_path):
                raise ValueError(f"Invalid or unsupported image file: {image_path}")

        # File size validation
        file_size_mb = image_path.stat().st_size / (1024 * 1024)
        if file_size_mb > self.config.file_processing.max_file_size_mb:
            raise ValueError(f"File too large: {file_size_mb:.2f}MB exceeds limit of {self.config.file_processing.max_file_size_mb}MB")

        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _validate_image_file(self, image_path: Path) -> bool:
        """Validate image file type and format"""
        # Check file extension
        extension = image_path.suffix.lower()
        if extension not in self.config.file_processing.supported_extensions:
            return False

        # Additional validation could be added here (file header validation, etc.)
        return True

    def _get_image_mime_type(self, image_path: Path) -> str:
        """Get appropriate MIME type for image based on extension"""
        extension = image_path.suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.bmp': 'image/bmp',
            '.tiff': 'image/tiff',
            '.webp': 'image/webp',
            '.gif': 'image/gif'
        }
        return mime_types.get(extension, 'image/jpeg')  # Default fallback

    def _call_openai_api(self, api_params: dict) -> any:
        """Make OpenAI API call with retry logic"""
        @retry_on_failure(self.config)
        def make_api_call():
            return self.client.responses.create(**api_params)

        return make_api_call()

    def analyze_image(self, image_path: Path) -> LegalEvidenceWithPath:
        """Generate forensic legal analysis of image evidence for specified legal domain"""

        # Audit logging - analysis start
        if self.audit_logger:
            self.audit_logger.log_analysis_start(str(image_path), self.legal_domain.value)

        # Chain of custody - original file access
        if self.custody_tracker:
            self.custody_tracker.add_custody_entry(str(image_path), "analysis_access")

        # Cost control check
        estimated_cost = self._get_image_cost()
        if not self._check_cost_limits(estimated_cost):
            raise ValueError(f"Cost limit exceeded. Estimated cost: ${estimated_cost:.4f}")

        # Rate limiting
        if self.request_delay > 0:
            time.sleep(self.request_delay)

        encoded_image = self.encode_image(image_path)
        mime_type = self._get_image_mime_type(image_path)

        # Get domain-specific analysis prompt (will move to config later)
        prompt = DomainConfig.get_analysis_prompt(self.legal_domain)

        # Prepare API call parameters
        api_params = {
            "model": self.config.openai.model,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"{prompt}\n\nAnalyze this image for legal evidence relevant to the specified domain."
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:{mime_type};base64,{encoded_image}"
                        }
                    ]
                }
            ],
        }

        # Add optional parameters if configured
        if self.config.openai.temperature is not None:
            api_params["temperature"] = self.config.openai.temperature
        if self.config.openai.max_tokens is not None:
            api_params["max_tokens"] = self.config.openai.max_tokens

        # Add the structured output schema to API parameters
        api_params["text"] = {
            "format": {
                "type": "json_schema",
                "name": "legal_evidence",
                "schema": {
                    "type": "object",
                    "properties": {
                        "evidence_type": {
                            "type": "string",
                            "enum": [
                                "workplace_safety", "discrimination", "harassment", "policy_violation",
                                "negligence", "premises_liability", "product_defect", "medical_evidence",
                                "crime_scene", "evidence_tampering", "forensic_evidence", "witness_evidence",
                                "contract_breach", "property_damage", "documentation", "procedural_violation",
                                "regulatory_violation", "compliance_failure", "critical_violation",
                                "health_safety", "cleanliness"
                            ],
                            "description": "Primary legal category"
                        },
                        "severity_level": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "critical"],
                            "description": "Legal urgency rating"
                        },
                        "legal_relevance": {
                            "type": "string",
                            "description": "Direct relevance to applicable legal framework"
                        },
                        "compliance_violations": {
                            "type": "string",
                            "description": "Specific regulation violations identified"
                        },
                        "expert_witness_notes": {
                            "type": "string",
                            "description": "Professional forensic observations"
                        },
                        "immediate_action_required": {
                            "type": "boolean",
                            "description": "Requires urgent legal attention"
                        },
                        "evidence_strength": {
                            "type": "string",
                            "description": "Quality and admissibility assessment"
                        },
                        "supporting_documentation_needed": {
                            "type": "string",
                            "description": "Additional evidence requirements"
                        }
                    },
                    "required": [
                        "evidence_type", "severity_level", "legal_relevance",
                        "compliance_violations", "expert_witness_notes",
                        "immediate_action_required", "evidence_strength",
                        "supporting_documentation_needed"
                    ],
                    "additionalProperties": False
                }
            }
        }

        # Use OpenAI Responses API with retry logic and structured output
        api_success = True
        api_error = None
        try:
            response = self._call_openai_api(api_params)
        except Exception as e:
            api_success = False
            api_error = str(e)
            raise

        # Track costs using configuration-based pricing - thread safe
        actual_cost = self._get_image_cost()
        with self.lock:
            self.total_cost += actual_cost
            self.daily_cost += actual_cost

        # Audit logging - API call
        if self.audit_logger:
            self.audit_logger.log_api_call(
                model=self.config.openai.model,
                cost=actual_cost,
                success=api_success,
                error=api_error
            )

        # Audit logging - cost event
        if self.audit_logger:
            self.audit_logger.log_cost_event("image_analysis", actual_cost, self.total_cost)

        # Parse the structured response and add source path
        try:
            parsed_result = json.loads(response.output_text)
            evidence = LegalEvidence(**parsed_result)

            # Apply confidence threshold validation
            evidence_with_path = LegalEvidenceWithPath(**evidence.model_dump(), image_path=str(image_path))

            # Apply expert review logic (calculates confidence score and flags for review)
            evidence_with_path = self._apply_expert_review_logic(evidence_with_path)

            # Validate evidence meets confidence thresholds
            if not self._meets_confidence_threshold(evidence_with_path):
                # Log below-threshold evidence but still return it with a note
                print(self.formatter.format_progress('info',
                    f"Evidence below confidence threshold: {image_path.name}"))

            # Log expert review requirement
            if evidence_with_path.requires_expert_review:
                print(self.formatter.format_progress('info',
                    f"Expert review required: {image_path.name} - {evidence_with_path.expert_review_reason}"))

            # Audit logging - analysis complete
            if self.audit_logger:
                self.audit_logger.log_analysis_complete(
                    image_path=str(image_path),
                    evidence_type=evidence_with_path.evidence_type.value,
                    severity=evidence_with_path.severity_level.value,
                    requires_expert_review=evidence_with_path.requires_expert_review,
                    confidence_score=evidence_with_path.confidence_score
                )

            return evidence_with_path
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse OpenAI response: {e}")

    def _get_image_cost(self) -> float:
        """Get cost per image based on configuration and legal domain"""
        base_cost = self.config.openai.cost_per_image

        # Apply domain-specific cost multiplier if configured
        if 'cost_multiplier' in self.legal_domain_config:
            base_cost *= self.legal_domain_config['cost_multiplier']

        return base_cost

    def _check_cost_limits(self, estimated_cost: float) -> bool:
        """Check if the estimated cost would exceed configured limits"""
        if not self.config.cost_control.track_usage:
            return True

        # Check daily limit
        potential_daily_cost = self.daily_cost + estimated_cost
        if potential_daily_cost > self.config.cost_control.max_daily_cost:
            return False

        return True

    def _meets_confidence_threshold(self, evidence: LegalEvidenceWithPath) -> bool:
        """Check if evidence meets configured confidence thresholds"""
        # Get confidence threshold from legal domain config, fallback to general config
        domain_threshold = self.legal_domain_config.get('confidence_threshold')
        general_threshold = self.config.analysis.confidence_threshold

        # Use domain-specific threshold if available, otherwise use general
        threshold = domain_threshold if domain_threshold is not None else general_threshold

        # Extract confidence indicators from evidence
        confidence_score = self._calculate_confidence_score(evidence)

        return confidence_score >= threshold

    def _calculate_confidence_score(self, evidence: LegalEvidenceWithPath) -> float:
        """Calculate confidence score based on evidence characteristics"""
        score = 0.0

        # Severity level contributes to confidence (higher severity = higher confidence)
        severity_scores = {
            SeverityLevel.low: 0.2,
            SeverityLevel.medium: 0.4,
            SeverityLevel.high: 0.6,
            SeverityLevel.critical: 0.8
        }
        score += severity_scores.get(evidence.severity_level, 0.2)

        # Evidence strength indicators boost confidence
        strength_keywords = ['clear', 'obvious', 'definitive', 'strong', 'compelling', 'conclusive']
        weak_keywords = ['unclear', 'uncertain', 'possible', 'potential', 'might', 'could']

        strength_text = evidence.evidence_strength.lower()
        for keyword in strength_keywords:
            if keyword in strength_text:
                score += 0.1
        for keyword in weak_keywords:
            if keyword in strength_text:
                score -= 0.1

        # Legal relevance length and specificity indicates confidence
        if len(evidence.legal_relevance) > 100:  # Detailed relevance description
            score += 0.1

        # Immediate action required indicates high confidence in findings
        if evidence.immediate_action_required:
            score += 0.1

        # Ensure score is within 0.0 to 1.0 bounds
        return max(0.0, min(1.0, score))

    def filter_evidence_by_confidence(self, evidence_list: List[LegalEvidenceWithPath]) -> List[LegalEvidenceWithPath]:
        """Filter evidence list to only include items meeting confidence threshold"""
        filtered_evidence = []
        below_threshold_count = 0

        for evidence in evidence_list:
            if self._meets_confidence_threshold(evidence):
                filtered_evidence.append(evidence)
            else:
                below_threshold_count += 1

        if below_threshold_count > 0:
            print(self.formatter.format_progress('info',
                f"Filtered {below_threshold_count} items below confidence threshold"))

        return filtered_evidence

    def _determine_expert_review_requirement(self, evidence: LegalEvidenceWithPath) -> tuple[bool, str]:
        """Determine if evidence requires expert review and provide reason"""
        # Get expert review requirements from legal domain config, fallback to general config
        domain_requires_review = self.legal_domain_config.get('require_expert_review')
        general_requires_review = self.config.analysis.require_expert_review

        # Check domain-specific requirement first
        if domain_requires_review is True:
            return True, f"Required for {self.legal_domain.value} domain"

        # Check general configuration requirement
        if general_requires_review:
            return True, "Required by system configuration"

        # Check severity-based requirements
        if evidence.severity_level == SeverityLevel.critical:
            return True, "Critical severity level"

        # Check evidence type requirements
        if evidence.evidence_type == EvidenceType.critical_violation:
            return True, "Critical violation detected"

        # Check immediate action requirement
        if evidence.immediate_action_required:
            return True, "Immediate action required"

        # Check confidence score (low confidence requires review)
        if evidence.confidence_score < 0.5:
            return True, f"Low confidence score ({evidence.confidence_score:.2f})"

        # Check evidence strength indicators
        strength_text = evidence.evidence_strength.lower()
        uncertain_keywords = ['uncertain', 'unclear', 'possible', 'potential', 'ambiguous']
        if any(keyword in strength_text for keyword in uncertain_keywords):
            return True, "Uncertain evidence strength assessment"

        return False, ""

    def _apply_expert_review_logic(self, evidence: LegalEvidenceWithPath) -> LegalEvidenceWithPath:
        """Apply expert review logic and update evidence fields"""
        # Calculate confidence score and store it
        confidence_score = self._calculate_confidence_score(evidence)
        evidence.confidence_score = confidence_score

        # Determine expert review requirement
        requires_review, reason = self._determine_expert_review_requirement(evidence)
        evidence.requires_expert_review = requires_review
        evidence.expert_review_reason = reason

        return evidence

    def get_expert_review_items(self, evidence_list: List[LegalEvidenceWithPath]) -> List[LegalEvidenceWithPath]:
        """Extract all evidence items requiring expert review"""
        review_items = [
            evidence for evidence in evidence_list
            if evidence.requires_expert_review
        ]

        if review_items:
            print(self.formatter.format_progress('info',
                f"Found {len(review_items)} items requiring expert review"))

        return review_items

    def generate_expert_review_summary(self, evidence_list: List[LegalEvidenceWithPath]) -> str:
        """Generate summary report for expert review items"""
        review_items = self.get_expert_review_items(evidence_list)

        if not review_items:
            return "No items requiring expert review."

        summary_lines = [
            f"EXPERT REVIEW REQUIRED - {len(review_items)} Items",
            "=" * 50,
            ""
        ]

        # Group by review reason
        reasons_count = {}
        for item in review_items:
            reason = item.expert_review_reason
            if reason not in reasons_count:
                reasons_count[reason] = []
            reasons_count[reason].append(item)

        # Summary by reason
        summary_lines.append("Review Requirements Summary:")
        for reason, items in reasons_count.items():
            summary_lines.append(f"• {reason}: {len(items)} items")

        summary_lines.extend(["", "Detailed Items:", "-" * 30])

        # Detailed items
        for i, item in enumerate(review_items, 1):
            summary_lines.extend([
                f"{i}. {Path(item.image_path).name}",
                f"   Type: {item.evidence_type.value}",
                f"   Severity: {item.severity_level.value}",
                f"   Confidence: {item.confidence_score:.2f}",
                f"   Review Reason: {item.expert_review_reason}",
                f"   Evidence Strength: {item.evidence_strength[:100]}...",
                ""
            ])

        return "\n".join(summary_lines)

    def analyze_directory(self, images_dir: Path) -> List[LegalEvidenceWithPath]:
        """Analyze all images in directory using configuration-based file filtering"""
        results = []
        supported_extensions = set(self.config.file_processing.supported_extensions)

        for image_path in images_dir.iterdir():
            if image_path.suffix.lower() in supported_extensions:
                try:
                    evidence = self.analyze_image(image_path)
                    results.append(evidence)
                    print(self.formatter.format_progress('success', f"Analyzed: {image_path.name}"))
                except Exception as e:
                    print(self.formatter.format_progress('error', f"Failed: {image_path.name} - {e}"))

        # Apply confidence filtering if enabled
        if self.config.analysis.enable_confidence_filtering:
            results = self.filter_evidence_by_confidence(results)

        return results

    def analyze_image_batch(self, image_paths: List[Path], batch_name: str = "") -> List[LegalEvidenceWithPath]:
        """Analyze a batch of images in parallel"""
        results = []

        def analyze_single(image_path):
            try:
                evidence = self.analyze_image(image_path)
                print(self.formatter.format_progress('success', f"{batch_name}Analyzed: {image_path.name}"))
                return evidence
            except Exception as e:
                print(self.formatter.format_progress('error', f"{batch_name}Failed: {image_path.name} - {e}"))
                return None

        # Use ThreadPoolExecutor for parallel API calls with configured workers
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_path = {executor.submit(analyze_single, path): path for path in image_paths}

            for future in concurrent.futures.as_completed(future_to_path):
                result = future.result()
                if result:
                    results.append(result)

        # Apply confidence filtering if enabled
        if self.config.analysis.enable_confidence_filtering:
            results = self.filter_evidence_by_confidence(results)

        return results

    def analyze_directory_parallel(self, images_dir: Path, num_batches: Optional[int] = None) -> List[LegalEvidenceWithPath]:
        """Analyze all images in directory using parallel batches with configuration"""
        if num_batches is None:
            num_batches = self.config.performance.default_parallel_batches

        # Enforce maximum parallel batches limit and ensure it's positive
        num_batches = min(max(num_batches, 1), self.config.performance.max_parallel_batches)

        supported_extensions = set(self.config.file_processing.supported_extensions)

        # Collect all image files
        all_images = [
            image_path for image_path in images_dir.iterdir()
            if image_path.suffix.lower() in supported_extensions
        ]

        if not all_images:
            print("No images found to analyze")
            return []

        # Split into batches
        batch_size = len(all_images) // num_batches
        batches = []

        for i in range(num_batches):
            start_idx = i * batch_size
            if i == num_batches - 1:  # Last batch gets remaining images
                end_idx = len(all_images)
            else:
                end_idx = (i + 1) * batch_size

            batches.append(all_images[start_idx:end_idx])

        print(f"🔄 Processing {len(all_images)} images in {num_batches} parallel batches")
        for i, batch in enumerate(batches):
            print(f"   Batch {i+1}: {len(batch)} images")

        # Process batches in parallel
        all_results = []

        def process_batch(batch_info):
            batch_idx, batch_images = batch_info
            batch_name = f"[Batch {batch_idx + 1}] "
            return self.analyze_image_batch(batch_images, batch_name)

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_batches) as executor:
            batch_futures = {
                executor.submit(process_batch, (i, batch)): i
                for i, batch in enumerate(batches)
            }

            for future in concurrent.futures.as_completed(batch_futures):
                batch_results = future.result()
                all_results.extend(batch_results)

        print(f"\n🎯 Parallel processing complete: {len(all_results)} images analyzed")
        return all_results

# =============================================================================
# EVIDENCE ORGANIZER - Smart File Management
# =============================================================================

class EvidenceOrganizer:
    """Organize analysis results into legal case structure"""

    def __init__(self, output_dir: Path, legal_domain: LegalDomain = LegalDomain.employment_law):
        self.output_dir = output_dir
        self.legal_domain = legal_domain
        self.setup_directories()

    def setup_directories(self):
        """Create organized evidence directory structure based on legal domain"""
        dirs = DomainConfig.get_directory_structure(self.legal_domain)

        for dir_name in dirs:
            (self.output_dir / dir_name).mkdir(parents=True, exist_ok=True)

    def organize_evidence(self, results: List[LegalEvidenceWithPath], audit_logger=None, custody_tracker=None):
        """Sort evidence by legal significance and domain-specific categories"""

        # Create expert review directory if needed
        expert_review_items = [r for r in results if r.requires_expert_review]
        if expert_review_items:
            expert_review_dir = self.output_dir / "expert_review_required"
            expert_review_dir.mkdir(parents=True, exist_ok=True)

        for evidence in results:
            target_dir = self._determine_target_directory(evidence)

            # Copy image to appropriate directory
            source_path = Path(evidence.image_path)
            target_path = self.output_dir / target_dir / source_path.name

            import shutil
            shutil.copy2(source_path, target_path)

            # Audit logging and chain of custody for file operations
            if audit_logger:
                audit_logger.log_file_operation("copy", str(source_path), str(target_path))
            if custody_tracker:
                custody_tracker.add_custody_entry(str(source_path), "copy_to_evidence", str(target_path))

            # Also copy to expert review directory if flagged
            if evidence.requires_expert_review:
                expert_target_path = self.output_dir / "expert_review_required" / source_path.name
                shutil.copy2(source_path, expert_target_path)

                # Audit logging for expert review copy
                if audit_logger:
                    audit_logger.log_file_operation("copy_expert_review", str(source_path), str(expert_target_path))
                if custody_tracker:
                    custody_tracker.add_custody_entry(str(source_path), "copy_to_expert_review", str(expert_target_path))

            # Create analysis report
            report_path = target_path.with_suffix('.txt')
            with open(report_path, 'w') as f:
                f.write(f"LEGAL EVIDENCE ANALYSIS\n")
                f.write(f"=====================\n\n")
                f.write(f"Image: {source_path.name}\n")
                f.write(f"Evidence Type: {evidence.evidence_type}\n")
                f.write(f"Severity: {evidence.severity_level}\n")
                f.write(f"Confidence Score: {evidence.confidence_score:.2f}\n\n")

                # Expert review information
                if evidence.requires_expert_review:
                    f.write(f"⚠️  EXPERT REVIEW REQUIRED\n")
                    f.write(f"Review Reason: {evidence.expert_review_reason}\n\n")

                f.write(f"Legal Relevance:\n{evidence.legal_relevance}\n\n")
                f.write(f"Compliance Violations:\n{evidence.compliance_violations}\n\n")
                f.write(f"Expert Witness Notes:\n{evidence.expert_witness_notes}\n\n")
                f.write(f"Immediate Action Required: {'Yes' if evidence.immediate_action_required else 'No'}\n\n")
                f.write(f"Evidence Strength:\n{evidence.evidence_strength}\n\n")
                f.write(f"Supporting Documentation Needed:\n{evidence.supporting_documentation_needed}\n")

            # Create expert review specific report if flagged
            if evidence.requires_expert_review:
                expert_report_path = self.output_dir / "expert_review_required" / f"{source_path.stem}_review.txt"
                with open(expert_report_path, 'w') as f:
                    f.write(f"EXPERT REVIEW REQUIRED\n")
                    f.write(f"=====================\n\n")
                    f.write(f"Image: {source_path.name}\n")
                    f.write(f"Review Reason: {evidence.expert_review_reason}\n")
                    f.write(f"Confidence Score: {evidence.confidence_score:.2f}\n")
                    f.write(f"Severity: {evidence.severity_level.value}\n")
                    f.write(f"Evidence Type: {evidence.evidence_type.value}\n\n")
                    f.write(f"Key Points for Review:\n")
                    f.write(f"- Legal Relevance: {evidence.legal_relevance[:200]}...\n")
                    f.write(f"- Evidence Strength: {evidence.evidence_strength[:200]}...\n")
                    f.write(f"- Immediate Action: {'Yes' if evidence.immediate_action_required else 'No'}\n\n")
                    f.write(f"Full analysis available in: {target_dir}/{source_path.stem}.txt\n")

    def _determine_target_directory(self, evidence: LegalEvidenceWithPath) -> str:
        """Determine appropriate directory based on evidence type, severity, and legal domain"""

        # Critical violations always go to critical directory (if exists)
        if evidence.severity_level == SeverityLevel.critical:
            dirs = DomainConfig.get_directory_structure(self.legal_domain)
            for dir_name in dirs:
                if "critical" in dir_name.lower():
                    return dir_name

        # Domain-specific evidence type mapping from configuration
        evidence_type_str = evidence.evidence_type.value

        # Try to get mapping from configuration first
        try:
            domain_config = get_legal_domain_config(self.legal_domain.value)
            if 'evidence_type_mapping' in domain_config:
                config_mapping = domain_config['evidence_type_mapping']
                target_dir = config_mapping.get(evidence_type_str, "documentation")
            else:
                target_dir = "documentation"
        except Exception:
            # Fallback to hardcoded mapping for backward compatibility
            domain_mapping = {
                LegalDomain.employment_law: {
                    "workplace_safety": "workplace_safety_violations",
                    "health_safety": "workplace_safety_violations",  # backwards compatibility
                    "cleanliness": "workplace_safety_violations",    # backwards compatibility
                    "discrimination": "discrimination_evidence",
                    "harassment": "discrimination_evidence",
                    "policy_violation": "workplace_safety_violations",
                    "critical_violation": "critical_violations"
                },
                LegalDomain.personal_injury: {
                    "negligence": "negligence_evidence",
                    "premises_liability": "premises_liability",
                    "product_defect": "negligence_evidence",
                    "medical_evidence": "medical_evidence",
                    "critical_violation": "critical_violations"
                },
                LegalDomain.criminal_law: {
                    "crime_scene": "crime_scene_evidence",
                    "evidence_tampering": "critical_evidence",
                    "forensic_evidence": "forensic_evidence",
                    "witness_evidence": "witness_evidence",
                    "critical_violation": "critical_evidence"
                },
                LegalDomain.civil_litigation: {
                    "contract_breach": "contract_evidence",
                    "property_damage": "property_damage",
                    "procedural_violation": "procedural_evidence"
                },
                LegalDomain.regulatory_compliance: {
                    "regulatory_violation": "regulatory_violations",
                    "compliance_failure": "compliance_failures",
                    "critical_violation": "critical_violations"
                },
                LegalDomain.family_law: {
                    "property_damage": "property_documentation",
                    "procedural_violation": "procedural_evidence"
                }
            }

            # Get mapping for current domain
            type_mapping = domain_mapping.get(self.legal_domain, {})
            target_dir = type_mapping.get(evidence_type_str, "documentation")

        # Verify the directory exists in our structure
        dirs = DomainConfig.get_directory_structure(self.legal_domain)
        if target_dir not in dirs:
            target_dir = "documentation"

        return target_dir

    def generate_summary_report(self, results: List[LegalEvidenceWithPath]):
        """Create comprehensive evidence summary for legal review"""
        summary_path = self.output_dir / "evidence_summary.txt"

        # Categorize evidence
        critical = [r for r in results if r.severity_level == SeverityLevel.critical]
        high = [r for r in results if r.severity_level == SeverityLevel.high]
        medium = [r for r in results if r.severity_level == SeverityLevel.medium]
        low = [r for r in results if r.severity_level == SeverityLevel.low]
        expert_review = [r for r in results if r.requires_expert_review]

        with open(summary_path, 'w') as f:
            f.write("LEGAL EVIDENCE ANALYSIS SUMMARY\n")
            f.write("==============================\n\n")
            f.write(f"Total Images Analyzed: {len(results)}\n")
            f.write(f"Critical Violations: {len(critical)}\n")
            f.write(f"High Severity: {len(high)}\n")
            f.write(f"Medium Severity: {len(medium)}\n")
            f.write(f"Low Severity: {len(low)}\n")
            f.write(f"Expert Review Required: {len(expert_review)}\n\n")

            if critical:
                f.write("🚨 CRITICAL VIOLATIONS - IMMEDIATE ATTENTION REQUIRED\n")
                f.write("================================================\n")
                for evidence in critical:
                    truncate_length = self.config.output.summary_truncation if hasattr(self, 'config') else 100
                    f.write(f"• {Path(evidence.image_path).name}: {evidence.legal_relevance[:truncate_length]}...\n")
                f.write("\n")

            if high:
                f.write("⚠️  HIGH SEVERITY VIOLATIONS\n")
                f.write("===========================\n")
                for evidence in high:
                    truncate_length = self.config.output.summary_truncation if hasattr(self, 'config') else 100
                    f.write(f"• {Path(evidence.image_path).name}: {evidence.compliance_violations[:truncate_length]}...\n")
                f.write("\n")

            # Add expert review section
            if expert_review:
                f.write("🔍 EXPERT REVIEW REQUIRED\n")
                f.write("==========================\n")
                # Group by review reason
                review_reasons = {}
                for evidence in expert_review:
                    reason = evidence.expert_review_reason
                    if reason not in review_reasons:
                        review_reasons[reason] = []
                    review_reasons[reason].append(evidence)

                for reason, items in review_reasons.items():
                    f.write(f"\n{reason} ({len(items)} items):\n")
                    for evidence in items:
                        truncate_length = getattr(self, 'config', type('', (), {'output': type('', (), {'summary_truncation': 100})()})).output.summary_truncation
                        f.write(f"• {Path(evidence.image_path).name} (Confidence: {evidence.confidence_score:.2f})\n")
                f.write("\n")

            f.write("RECOMMENDED LEGAL ACTION\n")
            f.write("=======================\n")
            f.write("1. Review all critical violations immediately\n")
            if expert_review:
                f.write("2. Address all items requiring expert review\n")
                f.write("3. Compile supporting documentation as noted\n")
                f.write("4. Consult with employment law specialist\n")
                f.write("5. Prepare evidence chain of custody documentation\n")
            else:
                f.write("2. Compile supporting documentation as noted\n")
                f.write("3. Consult with employment law specialist\n")
                f.write("4. Prepare evidence chain of custody documentation\n")

# =============================================================================
# MAIN COMMAND INTERFACE
# =============================================================================

def main():
    """Command line interface for V2 Legal Evidence Analysis"""
    import sys
    import os

    if len(sys.argv) < 2:
        print("Usage:")
        print("  ./v2 demo                    # Run demonstration")
        print("  ./v2 analyze <images_dir>    # Analyze directory of images")
        return

    command = sys.argv[1]

    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        return

    analyzer = LegalEvidenceAnalyzer(api_key)

    if command == "demo":
        # Demo with sample image (create a simple test if needed)
        print("V2 Legal Evidence Analysis System Demo")
        print("=====================================")
        print("Demo functionality would analyze sample workplace images")
        print("and demonstrate the structured legal evidence output.")

    elif command == "analyze" and len(sys.argv) >= 3:
        images_dir = Path(sys.argv[2])
        if not images_dir.exists():
            print(f"Error: Directory {images_dir} does not exist")
            return

        print(f"Analyzing images in: {images_dir}")
        results = analyzer.analyze_directory(images_dir)

        # Organize evidence
        evidence_dir = Path("evidence")

        # Initialize audit logging and chain of custody
        analyzer.initialize_audit_logging(evidence_dir)

        organizer = EvidenceOrganizer(evidence_dir)
        organizer.organize_evidence(results, analyzer.audit_logger, analyzer.custody_tracker)
        organizer.generate_summary_report(results)

        # Finalize chain of custody
        if analyzer.custody_tracker:
            expert_review_count = len([r for r in results if r.requires_expert_review])
            analyzer.custody_tracker.finalize_custody_log(len(results), expert_review_count)

        print(f"\n✓ Analysis complete!")
        print(f"✓ {len(results)} images processed")
        print(f"✓ Evidence organized in: {evidence_dir}")
        print(f"✓ Total cost: ${analyzer.total_cost:.2f}")

    else:
        print("Invalid command. Use 'demo' or 'analyze <directory>'")

if __name__ == "__main__":
    main()