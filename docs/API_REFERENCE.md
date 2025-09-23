# API Reference - Legal Evidence Analysis System

## Table of Contents

1. [Core Analysis Engine](#core-analysis-engine)
2. [Legal Evidence Models](#legal-evidence-models)
3. [Evidence Organization](#evidence-organization)
4. [Domain Configuration](#domain-configuration)
5. [Cost Tracking](#cost-tracking)
6. [Error Handling](#error-handling)
7. [Thread Safety](#thread-safety)

---

## Core Analysis Engine

### `LegalEvidenceAnalyzer`

The primary class for forensic image analysis using OpenAI's structured output capabilities.

#### Constructor

```python
LegalEvidenceAnalyzer(
    api_key: str,
    legal_domain: LegalDomain = LegalDomain.employment_law,
    environment: Optional[Environment] = None
)
```

**Parameters:**
- `api_key` (str): OpenAI API key for GPT-4 Vision access
- `legal_domain` (LegalDomain): Legal specialization domain (default: employment_law)
- `environment` (Optional[Environment]): Configuration environment (default: development)

**Available Environments:**
- `Environment.DEVELOPMENT`: Conservative settings, cost-effective models
- `Environment.TESTING`: Test-optimized configuration
- `Environment.PRODUCTION`: High-performance settings with GPT-4o
- `Environment.LEGAL_PRODUCTION`: Maximum security with full audit logging
- `Environment.DEMO`: Cost-optimized for demonstrations

**Example:**
```python
from image_analyzer import LegalEvidenceAnalyzer, LegalDomain

# Employment law analysis (default)
analyzer = LegalEvidenceAnalyzer("sk-your-openai-key")

# Personal injury analysis
analyzer = LegalEvidenceAnalyzer(
    "sk-your-openai-key",
    LegalDomain.personal_injury
)
```

#### Methods

##### `analyze_image(image_path: Path) -> LegalEvidenceWithPath`

Analyzes a single image for legal evidence using OpenAI Responses API.

**Parameters:**
- `image_path` (Path): Path to the image file

**Returns:**
- `LegalEvidenceWithPath`: Structured legal evidence analysis with source path

**API Pattern Used:**
```python
# ✅ CORRECT - Uses OpenAI Responses API (V2 System)
response = self.client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": [{
            "type": "input_text",
            "text": analysis_prompt
        }, {
            "type": "input_image",
            "image_url": f"data:image/jpeg;base64,{encoded_image}"
        }]
    }],
    text={
        "format": {
            "type": "json_schema",
            "name": "legal_evidence",
            "schema": legal_evidence_schema
        }
    }
)
```

**Cost:** ~$0.0014 per image (GPT-4.1 Mini pricing)

**Thread Safety:** Yes - uses thread-safe cost tracking with locks

**Example:**
```python
from pathlib import Path

# Analyze workplace safety image
result = analyzer.analyze_image(Path("workplace_hazard.jpg"))
print(f"Evidence Type: {result.evidence_type}")
print(f"Severity: {result.severity_level}")
print(f"Action Required: {result.immediate_action_required}")
```

##### `analyze_directory(images_dir: Path) -> List[LegalEvidenceWithPath]`

Sequential analysis of all images in a directory.

**Parameters:**
- `images_dir` (Path): Directory containing images to analyze

**Returns:**
- `List[LegalEvidenceWithPath]`: List of analysis results

**Supported Formats:** .jpg, .jpeg, .png, .bmp, .tiff

**Example:**
```python
# Analyze all images in evidence folder
results = analyzer.analyze_directory(Path("./evidence_images"))
print(f"Analyzed {len(results)} images")
```

##### `analyze_directory_parallel(images_dir: Path, num_batches: int = 2) -> List[LegalEvidenceWithPath]`

Parallel batch processing for high-volume analysis.

**Parameters:**
- `images_dir` (Path): Directory containing images
- `num_batches` (int): Number of parallel processing batches (default: 2)

**Returns:**
- `List[LegalEvidenceWithPath]`: List of analysis results

**Performance:** Optimized for OpenAI API rate limits with configurable batch sizes

**Thread Safety:** Full concurrent processing with thread-safe cost accumulation

**Example:**
```python
# Process 100 images using 4 parallel batches
results = analyzer.analyze_directory_parallel(
    Path("./large_evidence_set"),
    num_batches=4
)
```

##### `analyze_image_batch(image_paths: List[Path], batch_name: str = "") -> List[LegalEvidenceWithPath]`

Process a specific batch of images in parallel.

**Parameters:**
- `image_paths` (List[Path]): List of image file paths
- `batch_name` (str): Optional batch identifier for logging

**Returns:**
- `List[LegalEvidenceWithPath]`: Analysis results for the batch

**Thread Pool:** Uses ThreadPoolExecutor with max_workers=3 for optimal API usage

##### `initialize_audit_logging(output_dir: Path) -> None`

Initialize comprehensive audit logging and chain of custody tracking.

**Parameters:**
- `output_dir` (Path): Directory where audit logs will be stored

**Generated Files:**
- `audit.log`: JSON-formatted audit trail with timestamps
- `chain_of_custody.json`: Complete evidence chain documentation

**Logged Events:**
- File access with SHA-256 checksums
- API calls with costs and success/failure
- Evidence classifications and confidence scores
- Expert review requirements and reasons
- Cost tracking events

**Example:**
```python
# Enable comprehensive audit logging
analyzer.initialize_audit_logging(Path("./evidence_output"))

# All subsequent operations are automatically logged
results = analyzer.analyze_directory(Path("./images"))

# Audit files are automatically created and maintained
```

##### Configuration Access

The analyzer provides access to its Pydantic configuration:

```python
# Access configuration sections
print(f"Model: {analyzer.config.openai.model}")
print(f"Max workers: {analyzer.config.performance.max_workers}")
print(f"Confidence threshold: {analyzer.config.analysis.confidence_threshold}")
print(f"Audit logging enabled: {analyzer.config.legal.audit_logging}")

# Access legal domain configuration
domain_config = analyzer.legal_domain_config
evidence_types = domain_config.get('evidence_types', [])
require_review = domain_config.get('require_expert_review', False)
```

---

## Legal Evidence Models

### Core Pydantic Models

All models use Pydantic v2 for data validation and structured outputs.

#### `LegalEvidence`

Core structured output for forensic analysis.

```python
class LegalEvidence(BaseModel):
    # Evidence Classification
    evidence_type: EvidenceType
    severity_level: SeverityLevel

    # Legal Content
    legal_relevance: str
    compliance_violations: str
    expert_witness_notes: str

    # Actionable Intelligence
    immediate_action_required: bool
    evidence_strength: str
    supporting_documentation_needed: str
```

**Field Descriptions:**

- **evidence_type**: Primary legal category (see EvidenceType enum)
- **severity_level**: Legal urgency rating (low, medium, high, critical)
- **legal_relevance**: Direct relevance to applicable legal framework
- **compliance_violations**: Specific regulation violations identified
- **expert_witness_notes**: Professional forensic observations suitable for court
- **immediate_action_required**: Boolean flag for urgent legal attention
- **evidence_strength**: Quality and admissibility assessment
- **supporting_documentation_needed**: Additional evidence requirements

#### `LegalEvidenceWithPath`

Extended model including source file tracking for evidence chain documentation.

```python
class LegalEvidenceWithPath(LegalEvidence):
    image_path: str  # Path to source image file
```

**Example Usage:**
```python
# Access analysis results
evidence = analyzer.analyze_image(Path("safety_violation.jpg"))
print(f"Source: {evidence.image_path}")
print(f"Type: {evidence.evidence_type}")
print(f"Expert Notes: {evidence.expert_witness_notes}")
```

### Enumerations

#### `SeverityLevel`

Legal priority classification for evidence triage.

```python
class SeverityLevel(str, Enum):
    low = "low"           # Minor violations, documentation purposes
    medium = "medium"     # Standard violations requiring attention
    high = "high"         # Serious violations, prompt action needed
    critical = "critical" # Immediate legal action required
```

#### `EvidenceType`

Multi-domain legal evidence categories.

```python
class EvidenceType(str, Enum):
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

    # Backwards Compatibility
    critical_violation = "critical_violation"
    health_safety = "workplace_safety"    # Alias
    cleanliness = "workplace_safety"      # Maps to workplace safety
```

#### `LegalDomain`

Legal specialization domains for evidence analysis.

```python
class LegalDomain(str, Enum):
    employment_law = "employment_law"
    personal_injury = "personal_injury"
    criminal_law = "criminal_law"
    civil_litigation = "civil_litigation"
    regulatory_compliance = "regulatory_compliance"
    family_law = "family_law"
```

---

## Evidence Organization

### `EvidenceOrganizer`

Automated evidence categorization and file management system.

#### Constructor

```python
EvidenceOrganizer(output_dir: Path, legal_domain: LegalDomain = LegalDomain.employment_law)
```

**Parameters:**
- `output_dir` (Path): Target directory for organized evidence
- `legal_domain` (LegalDomain): Legal domain for organization structure

#### Methods

##### `organize_evidence(results: List[LegalEvidenceWithPath])`

Categorizes and organizes evidence files by legal significance.

**Directory Structure (Employment Law Example):**
```
evidence/
├── critical_violations/           # Critical severity evidence
├── workplace_safety_violations/   # Safety-related violations
├── discrimination_evidence/       # Discrimination/harassment cases
└── documentation/                # General documentation
```

**File Organization:**
- Original images copied to appropriate directories
- Analysis reports generated as .txt files alongside images
- Maintains chain of custody documentation

**Example:**
```python
organizer = EvidenceOrganizer(Path("./case_evidence"), LegalDomain.employment_law)
organizer.organize_evidence(analysis_results)
```

##### `generate_summary_report(results: List[LegalEvidenceWithPath])`

Creates comprehensive evidence summary for legal review.

**Report Contents:**
- Total images analyzed
- Severity distribution (critical, high, medium, low)
- Critical violations requiring immediate attention
- High-priority violations summary
- Recommended legal actions

**Output:** `evidence_summary.txt` in the output directory

---

## Domain Configuration

### `DomainConfig`

Static configuration class for legal domain-specific settings.

#### Methods

##### `get_evidence_types(domain: LegalDomain) -> List[str]`

Returns relevant evidence types for a specific legal domain.

**Example:**
```python
# Get evidence types for personal injury cases
types = DomainConfig.get_evidence_types(LegalDomain.personal_injury)
# Returns: ["negligence", "premises_liability", "product_defect", "medical_evidence", "critical_violation"]
```

##### `get_directory_structure(domain: LegalDomain) -> List[str]`

Returns appropriate evidence organization directories for a legal domain.

**Example:**
```python
# Get directory structure for criminal law
dirs = DomainConfig.get_directory_structure(LegalDomain.criminal_law)
# Returns: ["critical_evidence", "crime_scene_evidence", "forensic_evidence", "witness_evidence", "documentation"]
```

##### `get_analysis_prompt(domain: LegalDomain) -> str`

Returns domain-specific analysis prompt for forensic examination.

**Legal Frameworks by Domain:**

- **Employment Law**: Health & Safety at Work Act, discrimination, harassment
- **Personal Injury**: Negligence, premises liability, product defects
- **Criminal Law**: Crime scene analysis, evidence tampering, forensic procedures
- **Civil Litigation**: Contract breaches, property damage, procedural violations
- **Regulatory Compliance**: Industry standards, regulatory violations
- **Family Law**: Property documentation, living environments, custody evidence

---

## Cost Tracking

### Thread-Safe Cost Management

The system provides accurate cost tracking across all analysis operations.

**Cost Structure:**
- **GPT-4.1 Mini**: ~$0.0014 per image
- **Thread-Safe Accumulation**: Uses threading.Lock for concurrent operations
- **Real-Time Tracking**: Updated after each successful analysis

**Access Cost Information:**
```python
analyzer = LegalEvidenceAnalyzer(api_key)
results = analyzer.analyze_directory(Path("images"))
print(f"Total analysis cost: ${analyzer.total_cost:.2f}")
```

**Estimation Before Analysis:**
```python
def estimate_cost(image_directory: Path) -> float:
    image_count = len([f for f in image_directory.iterdir()
                      if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}])
    return image_count * 0.0014
```

---

## Error Handling

### Exception Types and Handling

The system provides comprehensive error handling for production legal environments.

#### Common Exceptions

1. **API Key Issues:**
```python
try:
    analyzer = LegalEvidenceAnalyzer("invalid-key")
    result = analyzer.analyze_image(Path("image.jpg"))
except Exception as e:
    print(f"API Error: {e}")
```

2. **Invalid Image Files:**
```python
try:
    result = analyzer.analyze_image(Path("corrupted.jpg"))
except Exception as e:
    print(f"Image Processing Error: {e}")
```

3. **JSON Schema Validation:**
```python
try:
    result = analyzer.analyze_image(Path("image.jpg"))
except ValueError as e:
    print(f"Schema Validation Error: {e}")
```

#### Best Practices

1. **Validate API Key:**
```python
import os
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable required")
```

2. **Check Image Formats:**
```python
valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
if image_path.suffix.lower() not in valid_extensions:
    raise ValueError(f"Unsupported image format: {image_path.suffix}")
```

3. **Handle Batch Processing Errors:**
```python
def safe_analyze_batch(analyzer, image_paths):
    results = []
    for path in image_paths:
        try:
            result = analyzer.analyze_image(path)
            results.append(result)
        except Exception as e:
            print(f"Failed to analyze {path.name}: {e}")
    return results
```

---

## Thread Safety

### Concurrent Processing Design

The Legal Evidence Analysis System is designed for safe concurrent operation in production legal environments.

#### Thread-Safe Components

1. **Cost Tracking:**
```python
class LegalEvidenceAnalyzer:
    def __init__(self, api_key: str, legal_domain: LegalDomain = LegalDomain.employment_law):
        self.total_cost = 0.0
        self.lock = threading.Lock()  # Thread-safe cost tracking

    def analyze_image(self, image_path: Path):
        # ... analysis logic ...
        with self.lock:
            self.total_cost += 0.0014  # Thread-safe cost update
```

2. **Parallel Batch Processing:**
```python
# ThreadPoolExecutor for API calls
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    future_to_path = {executor.submit(analyze_single, path): path for path in image_paths}
    for future in concurrent.futures.as_completed(future_to_path):
        result = future.result()
        if result:
            results.append(result)
```

3. **Rate Limit Compliance:**
- Default max_workers=3 for optimal OpenAI API usage
- Configurable batch sizes for different processing volumes
- Automatic retry mechanisms for transient API failures

#### Usage in Multi-Threaded Environments

```python
import threading
from concurrent.futures import ThreadPoolExecutor

def process_legal_cases(case_directories):
    """Process multiple legal cases concurrently"""

    def analyze_case(case_dir):
        analyzer = LegalEvidenceAnalyzer(api_key, LegalDomain.employment_law)
        return analyzer.analyze_directory(case_dir)

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(analyze_case, case_dir): case_dir
                   for case_dir in case_directories}

        results = {}
        for future in concurrent.futures.as_completed(futures):
            case_dir = futures[future]
            try:
                results[case_dir] = future.result()
            except Exception as e:
                print(f"Case {case_dir} failed: {e}")

        return results
```

---

## Integration Examples

### Complete Workflow Example

```python
from pathlib import Path
from image_analyzer import LegalEvidenceAnalyzer, EvidenceOrganizer, LegalDomain

# 1. Initialize analyzer for employment law
analyzer = LegalEvidenceAnalyzer(
    api_key=os.getenv('OPENAI_API_KEY'),
    legal_domain=LegalDomain.employment_law
)

# 2. Analyze evidence images
evidence_dir = Path("./workplace_incident_photos")
results = analyzer.analyze_directory_parallel(evidence_dir, num_batches=3)

# 3. Organize evidence for legal review
output_dir = Path("./case_evidence_organized")
organizer = EvidenceOrganizer(output_dir, LegalDomain.employment_law)
organizer.organize_evidence(results)
organizer.generate_summary_report(results)

# 4. Generate case summary
print(f"Evidence Analysis Complete:")
print(f"  - Images analyzed: {len(results)}")
print(f"  - Critical violations: {len([r for r in results if r.severity_level.value == 'critical'])}")
print(f"  - Total cost: ${analyzer.total_cost:.2f}")
print(f"  - Evidence organized in: {output_dir}")

# 5. Extract high-priority evidence for immediate review
critical_evidence = [r for r in results if r.severity_level.value == 'critical']
for evidence in critical_evidence:
    print(f"CRITICAL: {Path(evidence.image_path).name}")
    print(f"  Legal Issue: {evidence.legal_relevance}")
    print(f"  Action Required: {evidence.immediate_action_required}")
```

This API reference provides complete technical documentation for integrating the Legal Evidence Analysis System into professional legal workflows while maintaining court-ready evidence standards and GDPR compliance.