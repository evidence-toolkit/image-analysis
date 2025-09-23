#!/usr/bin/env python3
"""
Legal Evidence Analysis System V2 - Core Architecture
Simple, powerful design focused on OpenAI structured outputs for legal evidence.
"""

from typing import List
from pydantic import BaseModel, Field
from enum import Enum
from pathlib import Path
import base64
import json
import concurrent.futures
import threading
from openai import OpenAI

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
    """Configuration for legal domain-specific analysis"""

    @staticmethod
    def get_evidence_types(domain: LegalDomain) -> List[str]:
        """Get relevant evidence types for a legal domain"""
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
        """Get evidence organization directories for a legal domain"""
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
        """Get domain-specific analysis prompt for legal evidence"""
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

# =============================================================================
# CORE ANALYZER - The Analysis Engine
# =============================================================================

class LegalEvidenceAnalyzer:
    """OpenAI-powered forensic image analysis for multi-domain legal evidence"""

    def __init__(self, api_key: str, legal_domain: LegalDomain = LegalDomain.employment_law):
        self.client = OpenAI(api_key=api_key)
        self.legal_domain = legal_domain
        self.total_cost = 0.0
        self.lock = threading.Lock()  # For thread-safe cost tracking

    def encode_image(self, image_path: Path) -> str:
        """Convert image to base64 for OpenAI Vision API"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_image(self, image_path: Path) -> LegalEvidenceWithPath:
        """Generate forensic legal analysis of image evidence for specified legal domain"""

        encoded_image = self.encode_image(image_path)
        # TODO: Add image pre-processing if needed (e.g., resizing, enhancing)
        # TODO: Look into adding rag/similar for extra context (e.g., domain-specific regulations context)

        # Get domain-specific analysis prompt
        prompt = DomainConfig.get_analysis_prompt(self.legal_domain)

        # Use OpenAI Responses API with structured output for guaranteed schema
        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"{prompt}\n\nAnalyze this image for legal evidence relevant to the specified domain."
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    ]
                }
            ],
            text={
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
        )

        # Track costs (GPT-4.1 Mini: approximately $0.0014 per image) - thread safe
        with self.lock:
            self.total_cost += 0.0014

        # Parse the structured response and add source path
        try:
            parsed_result = json.loads(response.output_text)
            evidence = LegalEvidence(**parsed_result)
            # Convert to extended model with path
            return LegalEvidenceWithPath(**evidence.model_dump(), image_path=str(image_path))
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse OpenAI response: {e}")

    def analyze_directory(self, images_dir: Path) -> List[LegalEvidenceWithPath]:
        """Analyze all images in directory"""
        results = []
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}

        for image_path in images_dir.iterdir():
            if image_path.suffix.lower() in image_extensions:
                try:
                    evidence = self.analyze_image(image_path)
                    results.append(evidence)
                    print(f"✓ Analyzed: {image_path.name}")
                except Exception as e:
                    print(f"✗ Failed: {image_path.name} - {e}")

        return results

    def analyze_image_batch(self, image_paths: List[Path], batch_name: str = "") -> List[LegalEvidenceWithPath]:
        """Analyze a batch of images in parallel"""
        results = []

        def analyze_single(image_path):
            try:
                evidence = self.analyze_image(image_path)
                print(f"✓ {batch_name}Analyzed: {image_path.name}")
                return evidence
            except Exception as e:
                print(f"✗ {batch_name}Failed: {image_path.name} - {e}")
                return None

        # Use ThreadPoolExecutor for parallel API calls
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_path = {executor.submit(analyze_single, path): path for path in image_paths}

            for future in concurrent.futures.as_completed(future_to_path):
                result = future.result()
                if result:
                    results.append(result)

        return results

    def analyze_directory_parallel(self, images_dir: Path, num_batches: int = 2) -> List[LegalEvidenceWithPath]:
        """Analyze all images in directory using parallel batches"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}

        # Collect all image files
        all_images = [
            image_path for image_path in images_dir.iterdir()
            if image_path.suffix.lower() in image_extensions
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

    def organize_evidence(self, results: List[LegalEvidenceWithPath]):
        """Sort evidence by legal significance and domain-specific categories"""

        for evidence in results:
            target_dir = self._determine_target_directory(evidence)

            # Copy image to appropriate directory
            source_path = Path(evidence.image_path)
            target_path = self.output_dir / target_dir / source_path.name

            import shutil
            shutil.copy2(source_path, target_path)

            # Create analysis report
            report_path = target_path.with_suffix('.txt')
            with open(report_path, 'w') as f:
                f.write(f"LEGAL EVIDENCE ANALYSIS\n")
                f.write(f"=====================\n\n")
                f.write(f"Image: {source_path.name}\n")
                f.write(f"Evidence Type: {evidence.evidence_type}\n")
                f.write(f"Severity: {evidence.severity_level}\n\n")
                f.write(f"Legal Relevance:\n{evidence.legal_relevance}\n\n")
                f.write(f"Compliance Violations:\n{evidence.compliance_violations}\n\n")
                f.write(f"Expert Witness Notes:\n{evidence.expert_witness_notes}\n\n")
                f.write(f"Immediate Action Required: {'Yes' if evidence.immediate_action_required else 'No'}\n\n")
                f.write(f"Evidence Strength:\n{evidence.evidence_strength}\n\n")
                f.write(f"Supporting Documentation Needed:\n{evidence.supporting_documentation_needed}\n")

    def _determine_target_directory(self, evidence: LegalEvidenceWithPath) -> str:
        """Determine appropriate directory based on evidence type, severity, and legal domain"""

        # Critical violations always go to critical directory (if exists)
        if evidence.severity_level == SeverityLevel.critical:
            dirs = DomainConfig.get_directory_structure(self.legal_domain)
            for dir_name in dirs:
                if "critical" in dir_name.lower():
                    return dir_name

        # Domain-specific evidence type mapping
        evidence_type_str = evidence.evidence_type.value

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

        with open(summary_path, 'w') as f:
            f.write("LEGAL EVIDENCE ANALYSIS SUMMARY\n")
            f.write("==============================\n\n")
            f.write(f"Total Images Analyzed: {len(results)}\n")
            f.write(f"Critical Violations: {len(critical)}\n")
            f.write(f"High Severity: {len(high)}\n")
            f.write(f"Medium Severity: {len(medium)}\n")
            f.write(f"Low Severity: {len(low)}\n\n")

            if critical:
                f.write("🚨 CRITICAL VIOLATIONS - IMMEDIATE ATTENTION REQUIRED\n")
                f.write("================================================\n")
                for evidence in critical:
                    f.write(f"• {Path(evidence.image_path).name}: {evidence.legal_relevance[:100]}...\n")
                f.write("\n")

            if high:
                f.write("⚠️  HIGH SEVERITY VIOLATIONS\n")
                f.write("===========================\n")
                for evidence in high:
                    f.write(f"• {Path(evidence.image_path).name}: {evidence.compliance_violations[:100]}...\n")
                f.write("\n")

            f.write("RECOMMENDED LEGAL ACTION\n")
            f.write("=======================\n")
            f.write("1. Review all critical violations immediately\n")
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
        organizer = EvidenceOrganizer(evidence_dir)
        organizer.organize_evidence(results)
        organizer.generate_summary_report(results)

        print(f"\n✓ Analysis complete!")
        print(f"✓ {len(results)} images processed")
        print(f"✓ Evidence organized in: {evidence_dir}")
        print(f"✓ Total cost: ${analyzer.total_cost:.2f}")

    else:
        print("Invalid command. Use 'demo' or 'analyze <directory>'")

if __name__ == "__main__":
    main()