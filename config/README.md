# Configuration System

The Image Evidence Analyzer uses a flexible, environment-aware configuration system that allows for different settings across development, testing, and production environments.

## Configuration Files

### Core Configuration Files

- **`defaults.yaml`** - Base default settings for all environments
- **`environments.yaml`** - Environment-specific overrides (dev, test, prod, etc.)
- **`legal_domains.yaml`** - Legal domain-specific configurations and prompts
- **`config.py`** - Python configuration management module

### User Configuration (Optional)

- **`user.yaml`** - User-specific overrides (not tracked in git)

## Environment Configuration

Set the `IMAGE_ANALYZER_ENV` environment variable to control which configuration is loaded:

```bash
# Development (default)
export IMAGE_ANALYZER_ENV=development

# Testing
export IMAGE_ANALYZER_ENV=testing

# Production
export IMAGE_ANALYZER_ENV=production

# Legal Production (high security)
export IMAGE_ANALYZER_ENV=legal_production

# Demo
export IMAGE_ANALYZER_ENV=demo
```

## Configuration Sections

### OpenAI Configuration
- Model selection (gpt-4.1-mini, gpt-4o, etc.)
- Cost per image tracking
- Temperature and timeout settings
- Token limits

### Performance Configuration
- Maximum concurrent workers
- Parallel batch processing settings
- Request rate limiting

### File Processing
- Supported image formats
- File size limits
- Quality thresholds

### Legal Framework
- Default legal domain
- Chain of custody requirements
- Audit logging settings

### Cost Control
- Daily spending limits
- Warning thresholds
- Usage tracking

### Output Configuration
- Default output directories
- Report generation settings
- File preservation options

### Security Settings
- File validation requirements
- Path restrictions
- Filename sanitization

## Usage Examples

### Basic Usage

```python
from config.config import get_config, Environment

# Load development config
config = get_config(Environment.DEVELOPMENT)

# Access configuration values
model = config.openai.model
max_workers = config.performance.max_workers
cost_per_image = config.openai.cost_per_image
```

### Legal Domain Configuration

```python
from config.config import get_legal_domain_config

# Load employment law configuration
employment_config = get_legal_domain_config("employment_law")
evidence_types = employment_config["evidence_types"]
prompt = employment_config["analysis_prompts"]["system_prompt"]
```

### Custom Configuration Directory

```python
from config.config import set_config_directory
from pathlib import Path

# Use custom config directory
set_config_directory(Path("/custom/config/path"))
config = get_config()
```

## Environment-Specific Behavior

### Development
- Uses cheaper GPT-4.1-mini model
- Lower cost limits ($5/day)
- Verbose debug logging
- Reduced concurrency for stability

### Testing
- Single-threaded processing for predictable tests
- Very low cost limits ($2/day)
- Minimal logging
- Simplified output options

### Production
- Uses premium GPT-4o model for best accuracy
- Higher concurrency and cost limits
- Enhanced security settings
- Comprehensive logging

### Legal Production
- Maximum security and audit requirements
- Highest confidence thresholds
- Mandatory expert review
- Full chain of custody tracking

## Customization

### User-Specific Overrides

Create a `user.yaml` file to override settings without modifying tracked files:

```yaml
# user.yaml
openai:
  model: "gpt-4o"  # Override to use premium model

performance:
  max_workers: 8   # Increase concurrency

cost_control:
  max_daily_cost: 100.0  # Higher spending limit
```

### Legal Domain Customization

Add new legal domains or modify existing ones in `legal_domains.yaml`:

```yaml
# Add new domain
insurance_law:
  evidence_types:
    - claim_documentation
    - damage_assessment
    - policy_violation

  directory_structure:
    - claims_evidence
    - damage_documentation
    - policy_violations

  analysis_prompts:
    system_prompt: |
      You are a forensic image analyst specializing in insurance claim evidence...
```

## Configuration Validation

The system includes built-in validation to ensure:
- Required fields are present
- Values are within acceptable ranges
- File paths are valid and secure
- Cost limits are reasonable

## Security Considerations

- User configuration files should not be committed to version control
- API keys should still be managed via environment variables
- Path restrictions prevent unauthorized file access
- Filename sanitization prevents security vulnerabilities

## Migration from Hardcoded Values

The configuration system replaces these previously hardcoded values:

| Hardcoded Value | Configuration Path |
|---|---|
| `"gpt-4.1-mini"` | `config.openai.model` |
| `0.0014` | `config.openai.cost_per_image` |
| `max_workers=3` | `config.performance.max_workers` |
| `default=2` | `config.performance.default_parallel_batches` |
| `"./evidence"` | `config.output.default_directory` |
| File extensions | `config.file_processing.supported_extensions` |

This provides much greater flexibility while maintaining backward compatibility through sensible defaults.