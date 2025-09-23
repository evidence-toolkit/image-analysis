#!/usr/bin/env python3
"""
Command Line Interface for Image Evidence Analyzer
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

from .core_analyzer import LegalEvidenceAnalyzer, EvidenceOrganizer


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Image Evidence Analyzer - AI-powered forensic image analysis for legal evidence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyze ./images                       # Analyze images in directory
  %(prog)s analyze ./images -o ./evidence        # Save results to evidence directory
  %(prog)s analyze ./images --parallel 4         # Use 4 parallel batches
  %(prog)s analyze ./images --api-key sk-...     # Specify API key directly
  %(prog)s single image.jpg                      # Analyze single image
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Analyze directory command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze directory of images')
    analyze_parser.add_argument(
        'input_dir',
        help='Directory containing images to analyze'
    )
    analyze_parser.add_argument(
        '-o', '--output-dir',
        default='./evidence',
        help='Output directory for organized evidence (default: ./evidence)'
    )
    analyze_parser.add_argument(
        '--parallel',
        type=int,
        default=2,
        help='Number of parallel batches for processing (default: 2)'
    )
    analyze_parser.add_argument(
        '--api-key',
        help='OpenAI API key (can also use OPENAI_API_KEY env var)'
    )
    analyze_parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress verbose output'
    )
    analyze_parser.add_argument(
        '--json-output',
        help='Save analysis results as JSON to specified file'
    )

    # Single image command
    single_parser = subparsers.add_parser('single', help='Analyze single image')
    single_parser.add_argument(
        'image_path',
        help='Path to image file to analyze'
    )
    single_parser.add_argument(
        '-o', '--output-dir',
        help='Output directory for results (default: current directory)'
    )
    single_parser.add_argument(
        '--api-key',
        help='OpenAI API key (can also use OPENAI_API_KEY env var)'
    )
    single_parser.add_argument(
        '--json-output',
        help='Save analysis results as JSON to specified file'
    )

    # Cost estimate command
    cost_parser = subparsers.add_parser('estimate', help='Estimate analysis costs')
    cost_parser.add_argument(
        'input_dir',
        help='Directory containing images to count'
    )

    # Version command
    version_parser = subparsers.add_parser('version', help='Show version information')

    return parser


def get_api_key(args) -> Optional[str]:
    """Get API key from args or environment"""
    if args.api_key:
        return args.api_key

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OpenAI API key not found!")
        print("   Set OPENAI_API_KEY environment variable or use --api-key option")
        print("   Example: export OPENAI_API_KEY='sk-your-key-here'")
        return None

    return api_key


def count_images(directory: Path) -> int:
    """Count images in directory"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    count = 0
    for file_path in directory.iterdir():
        if file_path.suffix.lower() in image_extensions:
            count += 1
    return count


def handle_analyze_command(args) -> int:
    """Handle the analyze directory command"""
    input_path = Path(args.input_dir)

    if not input_path.exists():
        print(f"❌ Input directory '{input_path}' does not exist")
        return 1

    if not input_path.is_dir():
        print(f"❌ '{input_path}' is not a directory")
        return 1

    # Get API key
    api_key = get_api_key(args)
    if not api_key:
        return 1

    # Count images and estimate cost
    image_count = count_images(input_path)
    if image_count == 0:
        print(f"❌ No images found in '{input_path}'")
        return 1

    estimated_cost = image_count * 0.0014  # Approximate cost per image

    if not args.quiet:
        print(f"🔍 Found {image_count} images")
        print(f"💰 Estimated cost: ${estimated_cost:.2f}")

        confirm = input("Do you want to proceed? (y/N): ").lower().strip()
        if confirm != 'y':
            print("Analysis cancelled")
            return 0

    # Create analyzer
    try:
        analyzer = LegalEvidenceAnalyzer(api_key)

        if not args.quiet:
            print(f"\n🚀 Starting analysis of {image_count} images...")

        # Run analysis
        if args.parallel > 1:
            results = analyzer.analyze_directory_parallel(input_path, args.parallel)
        else:
            results = analyzer.analyze_directory(input_path)

        if not results:
            print("❌ No images were successfully analyzed")
            return 1

        # Organize evidence
        output_path = Path(args.output_dir)
        organizer = EvidenceOrganizer(output_path)
        organizer.organize_evidence(results)
        organizer.generate_summary_report(results)

        if not args.quiet:
            print(f"\n✅ Analysis complete!")
            print(f"   📊 {len(results)} images analyzed")
            print(f"   💰 Actual cost: ${analyzer.total_cost:.2f}")
            print(f"   📁 Evidence organized in: {output_path}")

        # Save JSON output if requested
        if args.json_output:
            json_data = {
                'total_images': len(results),
                'total_cost': analyzer.total_cost,
                'output_directory': str(output_path),
                'analysis_summary': {
                    'critical': len([r for r in results if r.severity_level.value == 'critical']),
                    'high': len([r for r in results if r.severity_level.value == 'high']),
                    'medium': len([r for r in results if r.severity_level.value == 'medium']),
                    'low': len([r for r in results if r.severity_level.value == 'low'])
                }
            }

            with open(args.json_output, 'w') as f:
                json.dump(json_data, f, indent=2)

            if not args.quiet:
                print(f"   📄 JSON summary: {args.json_output}")

        return 0

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return 1


def handle_single_command(args) -> int:
    """Handle the single image analysis command"""
    image_path = Path(args.image_path)

    if not image_path.exists():
        print(f"❌ Image file '{image_path}' does not exist")
        return 1

    # Get API key
    api_key = get_api_key(args)
    if not api_key:
        return 1

    try:
        analyzer = LegalEvidenceAnalyzer(api_key)

        print(f"🔍 Analyzing: {image_path.name}")
        print(f"💰 Estimated cost: $0.0014")

        # Analyze single image
        result = analyzer.analyze_image(image_path)

        print(f"\n✅ Analysis complete!")
        print(f"   Evidence Type: {result.evidence_type}")
        print(f"   Severity: {result.severity_level}")
        print(f"   Action Required: {result.immediate_action_required}")
        print(f"   💰 Cost: ${analyzer.total_cost:.4f}")

        # Save results if output directory specified
        if args.output_dir:
            output_path = Path(args.output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # Save analysis report
            report_path = output_path / f"{image_path.stem}_analysis.txt"
            with open(report_path, 'w') as f:
                f.write(f"LEGAL EVIDENCE ANALYSIS\n")
                f.write(f"=====================\n\n")
                f.write(f"Image: {image_path.name}\n")
                f.write(f"Evidence Type: {result.evidence_type}\n")
                f.write(f"Severity: {result.severity_level}\n\n")
                f.write(f"Legal Relevance:\n{result.legal_relevance}\n\n")
                f.write(f"Compliance Violations:\n{result.compliance_violations}\n\n")
                f.write(f"Expert Witness Notes:\n{result.expert_witness_notes}\n\n")
                f.write(f"Action Required: {result.immediate_action_required}\n")
                f.write(f"Evidence Strength: {result.evidence_strength}\n")
                f.write(f"Supporting Documentation Needed:\n{result.supporting_documentation_needed}\n")

            print(f"   📄 Report saved: {report_path}")

        # Save JSON output if requested
        if args.json_output:
            json_data = result.model_dump()
            json_data['analysis_cost'] = analyzer.total_cost

            with open(args.json_output, 'w') as f:
                json.dump(json_data, f, indent=2)

            print(f"   📄 JSON saved: {args.json_output}")

        return 0

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return 1


def handle_estimate_command(args) -> int:
    """Handle the cost estimation command"""
    input_path = Path(args.input_dir)

    if not input_path.exists():
        print(f"❌ Input directory '{input_path}' does not exist")
        return 1

    if not input_path.is_dir():
        print(f"❌ '{input_path}' is not a directory")
        return 1

    image_count = count_images(input_path)
    estimated_cost = image_count * 0.0014

    print(f"📊 Cost Estimation")
    print(f"   Images found: {image_count}")
    print(f"   Estimated cost: ${estimated_cost:.2f}")
    print(f"   Cost per image: $0.0014")

    return 0


def handle_version_command(args) -> int:
    """Handle the version command"""
    print("Image Evidence Analyzer v0.1.0")
    print("AI-powered forensic image analysis for legal evidence")
    print("Part of the Evidence Toolkit project")
    return 0


def main() -> int:
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == 'analyze':
        return handle_analyze_command(args)
    elif args.command == 'single':
        return handle_single_command(args)
    elif args.command == 'estimate':
        return handle_estimate_command(args)
    elif args.command == 'version':
        return handle_version_command(args)
    else:
        print(f"❌ Unknown command: {args.command}")
        return 1


if __name__ == '__main__':
    sys.exit(main())