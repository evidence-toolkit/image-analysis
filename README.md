# Image Evidence Analyzer

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAI](https://img.shields.io/badge/Powered%20by-OpenAI-412991.svg)](https://openai.com/)

AI-powered forensic image analysis for legal evidence processing. Specializes in UK employment law violations and workplace safety documentation using OpenAI's Vision API with structured legal analysis.

Part of the [Evidence Toolkit](https://github.com/evidence-toolkit) project.

## 🚀 Features

- **AI-Powered Analysis**: Uses OpenAI GPT-4 Vision for professional forensic image analysis
- **Legal Framework Integration**: Specialized for UK employment law and workplace safety regulations
- **Structured Evidence Output**: Generates court-ready analysis with legal classifications
- **Parallel Processing**: Efficiently analyze hundreds of images with concurrent batch processing
- **Evidence Organization**: Automatically categorizes and organizes evidence by severity and type
- **Cost Management**: Transparent cost tracking and estimation (~$0.0014 per image)
- **Forensic Quality**: Expert witness-level analysis notes and compliance violation identification
- **Multiple Output Formats**: Generate organized directories, detailed reports, and JSON summaries

## ⚖️ Legal Framework Coverage

- **Health & Safety at Work Act 1974**
- **Workplace (Health, Safety and Welfare) Regulations 1992**
- **Management of Health and Safety at Work Regulations 1999**
- **Control of Substances Hazardous to Health Regulations 2002**
- **Food Safety and Hygiene Regulations**
- **Documentation and Record-keeping Requirements**

## 📦 Installation

### Requirements

- Python 3.8 or higher
- OpenAI API key
- pip or uv for package management

### Install from Source

```bash
git clone https://github.com/evidence-toolkit/image-evidence-analyzer.git
cd image-evidence-analyzer
pip install -e .
```

### API Key Setup

```bash
# Set your OpenAI API key as an environment variable
export OPENAI_API_KEY='sk-your-api-key-here'

# Or copy the example environment file and edit it
cp .env.example .env
# Edit .env file with your API key
```

## 🛠️ Quick Start

### Command Line Usage

**Analyze a directory of images:**
```bash
# Basic analysis with cost confirmation
image-analyzer analyze ./workplace_images

# Specify output directory
image-analyzer analyze ./images -o ./legal_evidence

# Use parallel processing for faster analysis
image-analyzer analyze ./images --parallel 4

# Quiet mode (no prompts)
image-analyzer analyze ./images --quiet

# Generate JSON summary
image-analyzer analyze ./images --json-output analysis_summary.json
```

**Analyze a single image:**
```bash
# Quick single image analysis
image-analyzer single suspicious_area.jpg

# Save detailed report
image-analyzer single violation.jpg -o ./reports
```

**Estimate costs before analysis:**
```bash
image-analyzer estimate ./large_image_directory
```

### Python API

```python
from image_analyzer import LegalEvidenceAnalyzer, EvidenceOrganizer

# Initialize analyzer
analyzer = LegalEvidenceAnalyzer("your-api-key")

# Analyze single image
result = analyzer.analyze_image("workplace_violation.jpg")
print(f"Severity: {result.severity_level}")
print(f"Evidence Type: {result.evidence_type}")
print(f"Action Required: {result.immediate_action_required}")

# Analyze directory with parallel processing
results = analyzer.analyze_directory_parallel("./images", num_batches=3)

# Organize evidence for legal review
organizer = EvidenceOrganizer("./evidence_output")
organizer.organize_evidence(results)
organizer.generate_summary_report(results)

print(f"Total cost: ${analyzer.total_cost:.2f}")
```

## 📊 Analysis Output

### Evidence Classification

**Severity Levels:**
- 🚨 **Critical**: Immediate legal attention required
- ⚠️ **High**: Significant regulatory violations
- 📋 **Medium**: Notable compliance issues
- ℹ️ **Low**: Minor documentation concerns

**Evidence Types:**
- **Health & Safety**: Workplace safety violations
- **Cleanliness**: Hygiene and sanitation issues
- **Critical Violation**: Serious regulatory breaches
- **Documentation**: Record-keeping and procedural issues

### Organized Output Structure

```
evidence/
├── critical_violations/           # 🚨 Urgent attention required
│   ├── image1.jpg
│   ├── image1.txt                # Detailed legal analysis
│   └── ...
├── health_safety_violations/      # ⚠️ Safety compliance issues
├── cleanliness_concerns/          # 🧽 Hygiene violations
├── documentation/                 # 📋 Procedural issues
└── evidence_summary.txt          # 📄 Comprehensive legal summary
```

## 🔍 Example Analysis Output

```
LEGAL EVIDENCE ANALYSIS
=====================

Image: fridge_contamination.jpg
Evidence Type: health_safety
Severity: critical

Legal Relevance:
This image demonstrates likely violations of food safety and hygiene standards
under the Health and Safety at Work Act 1974, Workplace (Health, Safety and
Welfare) Regulations 1992, and Food Safety Act 1990...

Compliance Violations:
The visible buildup and residue indicate a failure to comply with Food Hygiene
Regulations requiring equipment to be kept clean and free from contamination risk...

Expert Witness Notes:
The encrusted biological residue inside the refrigerated display unit indicates
prolonged neglect and poor maintenance practices. Such contamination is a known
vector for bacterial growth including pathogens such as Listeria monocytogenes...

Action Required: True
Evidence Strength: High - image clearly depicts unsanitary conditions consistent
over time rather than isolated incident, useful for tribunal proceedings...
```

## 💰 Cost Information

- **Cost per image**: ~$0.0014 (GPT-4 Vision API)
- **100 images**: ~$0.14
- **500 images**: ~$0.70
- **1000 images**: ~$1.40

The tool provides cost estimates before analysis and tracks actual spending.

## 🎯 Use Cases

### Legal Professionals
- **Employment Tribunal Preparation**: Generate expert witness-quality evidence analysis
- **Workplace Investigation**: Document safety violations with legal framework compliance
- **Case Building**: Organize evidence by severity and legal relevance

### Workplace Safety Officers
- **Compliance Auditing**: Systematic analysis of workplace safety documentation
- **Risk Assessment**: Identify and prioritize safety violations
- **Regulatory Reporting**: Generate structured reports for authorities

### Insurance & Risk Management
- **Claims Investigation**: Professional analysis of workplace incident imagery
- **Risk Documentation**: Categorize and assess workplace hazards
- **Compliance Verification**: Verify adherence to safety regulations

## ⚙️ Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional
OPENAI_API_BASE=https://api.openai.com/v1  # Custom API endpoint
MAX_CONCURRENT_REQUESTS=3                   # Parallel processing limit
DEFAULT_OUTPUT_DIR=./evidence              # Default output location
```

### Custom Analysis Parameters

```python
# Advanced usage with custom settings
analyzer = LegalEvidenceAnalyzer(
    api_key="your-key",
    custom_prompt_additions="Focus on food safety violations"
)

# Custom evidence organization
organizer = EvidenceOrganizer(
    output_dir="./custom_evidence",
    create_subdirs=True
)
```

## 📁 Project Structure

```
image-evidence-analyzer/
├── src/
│   └── image_analyzer/
│       ├── __init__.py              # Main module exports
│       ├── core_analyzer.py         # Core analysis engine (V2 architecture)
│       └── cli.py                   # Command line interface
├── examples/
│   ├── sample_images/              # Example input images
│   └── outputs/                    # Example analysis outputs
├── config/                         # Configuration files
├── tests/                          # Unit tests
├── .env.example                    # Environment configuration template
├── pyproject.toml                  # Modern Python packaging
└── README.md                       # This file
```

## 🔧 API Reference

### LegalEvidenceAnalyzer Class

Main analysis engine for forensic image processing.

#### `__init__(api_key: str)`
Initialize analyzer with OpenAI API key.

#### `analyze_image(image_path: Path) -> LegalEvidenceWithPath`
Analyze single image and return structured legal evidence.

#### `analyze_directory(images_dir: Path) -> List[LegalEvidenceWithPath]`
Analyze all images in directory sequentially.

#### `analyze_directory_parallel(images_dir: Path, num_batches: int = 2) -> List[LegalEvidenceWithPath]`
Analyze directory using parallel batch processing.

**Properties:**
- `total_cost`: Running total of API costs

### EvidenceOrganizer Class

Organize analysis results into legal case structure.

#### `__init__(output_dir: Path)`
Initialize organizer with output directory.

#### `organize_evidence(results: List[LegalEvidenceWithPath])`
Sort and copy evidence files by legal significance.

#### `generate_summary_report(results: List[LegalEvidenceWithPath])`
Create comprehensive evidence summary for legal review.

### Data Models

#### `LegalEvidence`
Core evidence analysis structure with:
- `evidence_type`: Legal category classification
- `severity_level`: Urgency rating
- `legal_relevance`: UK employment law relevance
- `compliance_violations`: Specific regulation breaches
- `expert_witness_notes`: Professional forensic observations
- `immediate_action_required`: Boolean urgency flag
- `evidence_strength`: Admissibility assessment
- `supporting_documentation_needed`: Additional evidence requirements

## 🧪 Testing

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Test with sample images (requires API key)
image-analyzer analyze examples/sample_images --output-dir test_results
```

## ⚠️ Important Considerations

### Legal Usage
- This tool provides analysis assistance but does not replace legal expertise
- All analysis should be reviewed by qualified legal professionals
- Evidence organization follows UK legal frameworks but may require jurisdiction-specific adaptation

### API Usage
- Requires active OpenAI API key with GPT-4 Vision access
- Costs apply per image analyzed (~$0.0014 each)
- Images are sent to OpenAI's servers for processing
- Consider data privacy implications for sensitive evidence

### Performance
- Parallel processing improves speed but increases concurrent API usage
- Large batches may hit API rate limits
- Monitor costs with the built-in tracking features

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [Document Evidence Analyzer](https://github.com/evidence-toolkit/document-evidence-analyzer) - Text analysis for legal documents
- [Evidence Toolkit](https://github.com/evidence-toolkit) - Complete legal evidence analysis suite

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/evidence-toolkit/image-evidence-analyzer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/evidence-toolkit/image-evidence-analyzer/discussions)
- **Documentation**: [Full Documentation](https://evidence-toolkit.github.io/image-evidence-analyzer/)

## 🙏 Acknowledgments

- Powered by [OpenAI](https://openai.com/) GPT-4 Vision API
- Legal framework analysis based on UK employment law
- Built with [Pydantic](https://pydantic.dev/) for robust data validation

---

**⚖️ Professional Legal Evidence Analysis Tool**

*Part of the Evidence Toolkit Project - Democratizing access to professional-grade legal evidence analysis tools.*