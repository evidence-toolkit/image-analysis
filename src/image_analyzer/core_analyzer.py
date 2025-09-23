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

class EvidenceType(str, Enum):
    """Legal evidence categories for UK employment law"""
    health_safety = "health_safety"
    cleanliness = "cleanliness"
    documentation = "documentation"
    critical_violation = "critical_violation"

class LegalEvidence(BaseModel):
    """Core structured output for legal evidence analysis"""

    # Evidence Classification
    evidence_type: EvidenceType = Field(description="Primary legal category")
    severity_level: SeverityLevel = Field(description="Legal urgency rating")

    # Legal Content
    legal_relevance: str = Field(description="Direct relevance to UK employment law")
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
    """OpenAI-powered forensic image analysis for UK employment law"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.total_cost = 0.0
        self.lock = threading.Lock()  # For thread-safe cost tracking

    def encode_image(self, image_path: Path) -> str:
        """Convert image to base64 for OpenAI Vision API"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_image(self, image_path: Path) -> LegalEvidenceWithPath:
        """Generate forensic legal analysis of workplace image"""

        encoded_image = self.encode_image(image_path)
        # TODO: Add image pre-processing if needed (e.g., resizing, enhancing)
        # TODO: Look into adding rag/similar for extra context (e.g., H&S regulations context)

        # Professional legal analysis prompt
        prompt = """You are a forensic image analyst specializing in UK employment law evidence.

Analyze this workplace image with the expertise of a professional forensic examiner preparing evidence for employment tribunal proceedings.

Focus on:
- Health & Safety at Work Act 1974 violations
- Workplace (Health, Safety and Welfare) Regulations 1992
- Management of Health and Safety at Work Regulations 1999
- Control of Substances Hazardous to Health Regulations 2002
- Food safety and hygiene violations
- Documentation and record-keeping issues

Provide thorough, objective analysis suitable for UK employment law proceedings."""

        # Use OpenAI Responses API with structured output for guaranteed schema
        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"{prompt}\n\nAnalyze this workplace image for UK employment law evidence."
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
                                "enum": ["health_safety", "cleanliness", "documentation", "critical_violation"],
                                "description": "Primary legal category"
                            },
                            "severity_level": {
                                "type": "string",
                                "enum": ["low", "medium", "high", "critical"],
                                "description": "Legal urgency rating"
                            },
                            "legal_relevance": {
                                "type": "string",
                                "description": "Direct relevance to UK employment law"
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

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.setup_directories()

    def setup_directories(self):
        """Create organized evidence directory structure"""
        dirs = [
            "critical_violations",
            "health_safety_violations",
            "cleanliness_concerns",
            "documentation"
        ]

        for dir_name in dirs:
            (self.output_dir / dir_name).mkdir(parents=True, exist_ok=True)

    def organize_evidence(self, results: List[LegalEvidenceWithPath]):
        """Sort evidence by legal significance"""

        for evidence in results:
            # Determine target directory based on evidence type and severity
            if evidence.severity_level == SeverityLevel.critical:
                target_dir = "critical_violations"
            elif evidence.evidence_type == EvidenceType.health_safety:
                target_dir = "health_safety_violations"
            elif evidence.evidence_type == EvidenceType.cleanliness:
                target_dir = "cleanliness_concerns"
            else:
                target_dir = "documentation"

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
                f.write(f"Action Required: {evidence.immediate_action_required}\n")
                f.write(f"Evidence Strength: {evidence.evidence_strength}\n")
                f.write(f"Supporting Documentation Needed:\n{evidence.supporting_documentation_needed}\n")

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