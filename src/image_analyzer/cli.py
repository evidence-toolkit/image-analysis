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

from .core_analyzer import LegalEvidenceAnalyzer, EvidenceOrganizer, LegalDomain

# Import configuration system
try:
    from ..config.config import get_config, Environment
except ImportError:
    # Fallback for direct execution
    sys.path.append(str(Path(__file__).parent.parent))
    from config.config import get_config, Environment


def create_parser(config=None) -> argparse.ArgumentParser:
    """Create command line argument parser with configuration-based defaults"""
    if config is None:
        config = get_config()

    parser = argparse.ArgumentParser(
        description="Image Evidence Analyzer - AI-powered forensic image analysis for multi-domain legal evidence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyze ./images                                    # Analyze images (employment law)
  %(prog)s analyze ./images --legal-domain personal_injury    # Personal injury analysis
  %(prog)s analyze ./images --legal-domain criminal_law       # Criminal evidence analysis
  %(prog)s analyze ./images -o ./evidence --parallel 4        # Use 4 parallel batches
  %(prog)s single image.jpg --legal-domain civil_litigation   # Single image civil analysis
  %(prog)s estimate ./images                                  # Estimate analysis costs
  %(prog)s config show                                        # Show current configuration
        """
    )

    # Add global arguments
    parser.add_argument(
        '--environment', '-e',
        choices=['development', 'testing', 'production', 'legal_production', 'demo'],
        help='Environment configuration to use'
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
        default=config.output.default_directory,
        help=f'Output directory for organized evidence (default: {config.output.default_directory})'
    )
    analyze_parser.add_argument(
        '--parallel',
        type=int,
        default=config.performance.default_parallel_batches,
        help=f'Number of parallel batches for processing (default: {config.performance.default_parallel_batches})'
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
        '--legal-domain',
        choices=['employment_law', 'personal_injury', 'criminal_law', 'civil_litigation', 'regulatory_compliance', 'family_law'],
        default='employment_law',
        help='Legal domain for evidence analysis (default: employment_law)'
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
    single_parser.add_argument(
        '--legal-domain',
        choices=['employment_law', 'personal_injury', 'criminal_law', 'civil_litigation', 'regulatory_compliance', 'family_law'],
        default='employment_law',
        help='Legal domain for evidence analysis (default: employment_law)'
    )

    # Cost estimate command
    cost_parser = subparsers.add_parser('estimate', help='Estimate analysis costs')
    cost_parser.add_argument(
        'input_dir',
        help='Directory containing images to count'
    )

    # Version command
    version_parser = subparsers.add_parser('version', help='Show version information')

    # Configuration command
    config_parser = subparsers.add_parser('config', help='Configuration management')
    config_subparsers = config_parser.add_subparsers(dest='config_action', help='Configuration actions')

    # Config show subcommand
    config_show_parser = config_subparsers.add_parser('show', help='Show current configuration')
    config_show_parser.add_argument(
        '--section',
        choices=['openai', 'performance', 'file_processing', 'output', 'legal', 'cost_control', 'analysis', 'logging', 'security'],
        help='Show specific configuration section'
    )

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


def count_images(directory: Path, config=None) -> int:
    """Count images in directory using configuration-based extensions"""
    if config is None:
        config = get_config()

    supported_extensions = set(config.file_processing.supported_extensions)
    count = 0
    for file_path in directory.iterdir():
        if file_path.suffix.lower() in supported_extensions:
            count += 1
    return count

def estimate_cost(image_count: int, legal_domain: str, config=None) -> float:
    """Estimate cost based on configuration and legal domain"""
    if config is None:
        config = get_config()

    base_cost = config.openai.cost_per_image

    # Apply domain-specific multiplier if available
    try:
        from ..config.config import get_legal_domain_config
        domain_config = get_legal_domain_config(legal_domain)
        if 'cost_multiplier' in domain_config:
            base_cost *= domain_config['cost_multiplier']
    except ImportError:
        pass

    return image_count * base_cost


def handle_analyze_command(args) -> int:
    """Handle the analyze directory command with configuration support"""
    # Load configuration based on environment
    environment = Environment(args.environment) if args.environment else None
    config = get_config(environment)

    # Import the formatter after config is loaded
    from .core_analyzer import OutputFormatter
    formatter = OutputFormatter(config)

    input_path = Path(args.input_dir)

    if not input_path.exists():
        print(formatter.format_progress('error', f"Input directory '{input_path}' does not exist"))
        return 1

    if not input_path.is_dir():
        print(formatter.format_progress('error', f"'{input_path}' is not a directory"))
        return 1

    # Get API key
    api_key = get_api_key(args)
    if not api_key:
        return 1

    # Count images and estimate cost using configuration
    image_count = count_images(input_path, config)
    if image_count == 0:
        print(formatter.format_progress('error', f"No images found in '{input_path}'"))
        return 1

    estimated_cost = estimate_cost(image_count, args.legal_domain, config)

    # Cost control and confirmation
    if not args.quiet:
        print(formatter.format_progress('info', f"Found {image_count} images"))
        print(formatter.format_progress('cost', f"Estimated cost: {formatter.format_cost(estimated_cost)}"))

        # Check against configured cost limits
        if config.cost_control.track_usage and estimated_cost > config.cost_control.confirm_above_cost:
            if estimated_cost > config.cost_control.max_daily_cost:
                error_msg = f"Estimated cost {formatter.format_cost(estimated_cost)} exceeds daily limit of {formatter.format_cost(config.cost_control.max_daily_cost)}"
                print(formatter.format_progress('error', error_msg))
                return 1

            if not config.legal.require_confirmation:
                print("⚠️  Analysis would proceed automatically (confirmation disabled in config)")
            else:
                confirm = input("Do you want to proceed? (y/N): ").lower().strip()
                if confirm != 'y':
                    print("Analysis cancelled")
                    return 0

    # Create analyzer with specified legal domain and environment
    try:
        legal_domain = LegalDomain(args.legal_domain)
        analyzer = LegalEvidenceAnalyzer(api_key, legal_domain, environment)

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

        # Organize evidence with specified legal domain
        output_path = Path(args.output_dir)
        organizer = EvidenceOrganizer(output_path, legal_domain)
        organizer.organize_evidence(results)
        organizer.generate_summary_report(results)

        if not args.quiet:
            print(f"\n✅ Analysis complete!")
            print(f"   📊 {len(results)} images analyzed")
            print(f"   {formatter.get_icon('cost')} Actual cost: {formatter.format_cost(analyzer.total_cost)}")
            print(f"   {formatter.get_icon('folder')} Evidence organized in: {output_path}")

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
                json.dump(json_data, f, indent=config.output.json_indent)

            if not args.quiet:
                print(f"   📄 JSON summary: {args.json_output}")

        return 0

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return 1


def handle_single_command(args) -> int:
    """Handle the single image analysis command with configuration support"""
    # Load configuration based on environment
    environment = Environment(args.environment) if args.environment else None
    config = get_config(environment)

    image_path = Path(args.image_path)

    if not image_path.exists():
        print(f"❌ Image file '{image_path}' does not exist")
        return 1

    # Get API key
    api_key = get_api_key(args)
    if not api_key:
        return 1

    try:
        legal_domain = LegalDomain(args.legal_domain)

        # Calculate estimated cost using configuration
        estimated_cost = estimate_cost(1, args.legal_domain, config)

        analyzer = LegalEvidenceAnalyzer(api_key, legal_domain, environment)

        print(f"🔍 Analyzing: {image_path.name}")
        print(f"💰 Estimated cost: ${estimated_cost:.4f}")

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
                json.dump(json_data, f, indent=config.output.json_indent)

            print(f"   📄 JSON saved: {args.json_output}")

        return 0

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return 1


def handle_estimate_command(args) -> int:
    """Handle the cost estimation command with configuration support"""
    # Load configuration
    config = get_config()

    input_path = Path(args.input_dir)

    if not input_path.exists():
        print(f"❌ Input directory '{input_path}' does not exist")
        return 1

    if not input_path.is_dir():
        print(f"❌ '{input_path}' is not a directory")
        return 1

    image_count = count_images(input_path, config)

    # Default to employment law for estimation if not specified
    legal_domain = getattr(args, 'legal_domain', 'employment_law')
    estimated_cost = estimate_cost(image_count, legal_domain, config)
    cost_per_image = config.openai.cost_per_image

    print(f"📊 Cost Estimation")
    print(f"   Images found: {image_count}")
    print(f"   Estimated cost: ${estimated_cost:.2f}")
    print(f"   Base cost per image: ${cost_per_image:.4f}")
    print(f"   Environment: {os.getenv('IMAGE_ANALYZER_ENV', 'development')}")

    return 0


def handle_version_command(args) -> int:
    """Handle the version command"""
    print("Image Evidence Analyzer v0.1.0")
    print("AI-powered forensic image analysis for legal evidence")
    print("Part of the Evidence Toolkit project")
    return 0


def handle_config_command(args) -> int:
    """Handle the configuration command"""
    if args.config_action == 'show':
        return handle_config_show(args)
    else:
        print("❌ Unknown config action")
        return 1


def handle_config_show(args) -> int:
    """Show current configuration"""
    try:
        # Load configuration
        environment = Environment(args.environment) if args.environment else None
        config = get_config(environment)

        current_env = os.getenv('IMAGE_ANALYZER_ENV', 'development')
        print(f"📋 Configuration (Environment: {current_env})")
        print("=" * 50)

        if args.section:
            # Show specific section
            section = getattr(config, args.section, None)
            if section:
                print(f"\n[{args.section.upper()}]")
                for field_name, field_value in section.__dict__.items():
                    print(f"  {field_name}: {field_value}")
            else:
                print(f"❌ Unknown section: {args.section}")
                return 1
        else:
            # Show all sections
            for section_name in ['openai', 'performance', 'file_processing', 'output', 'legal', 'cost_control', 'analysis', 'logging', 'security']:
                section = getattr(config, section_name, None)
                if section:
                    print(f"\n[{section_name.upper()}]")
                    for field_name, field_value in section.__dict__.items():
                        print(f"  {field_name}: {field_value}")

        print(f"\n💡 Use --environment to view different environment configurations")
        print(f"💡 Available environments: development, testing, production, legal_production, demo")

        return 0

    except Exception as e:
        print(f"❌ Error showing configuration: {e}")
        return 1


def main() -> int:
    """Main CLI entry point with configuration support"""
    # Set environment variable if provided before loading config
    if len(sys.argv) > 1 and '--environment' in sys.argv:
        env_index = sys.argv.index('--environment')
        if env_index + 1 < len(sys.argv):
            os.environ['IMAGE_ANALYZER_ENV'] = sys.argv[env_index + 1]

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
    elif args.command == 'config':
        return handle_config_command(args)
    else:
        print(f"❌ Unknown command: {args.command}")
        return 1


if __name__ == '__main__':
    sys.exit(main())