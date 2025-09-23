# Configuration Reference

This document provides comprehensive information about the Image Evidence Analyzer's configuration system, built with Pydantic models for type safety and validation.

## Overview

The configuration system uses a hierarchical approach with environment-specific overrides:

1. **Base Configuration** (`config/defaults.yaml`) - Default settings for all environments
2. **Environment Overrides** (`config/environments.yaml`) - Environment-specific customizations
3. **Legal Domain Configuration** (`config/legal_domains.yaml`) - Domain-specific analysis settings
4. **User Overrides** (`config/user.yaml`) - Optional user customizations

## Environment Types

### Development (`development`)
- Conservative settings for testing
- Lower cost models (gpt-4.1-mini)
- Slower processing with safety margins
- Enhanced logging for debugging

### Testing (`testing`)
- Similar to development
- Optimized for automated testing
- Predictable behavior

### Production (`production`)
- High-performance settings
- Premium models (gpt-4o)
- Optimized parallel processing
- Higher confidence thresholds

### Legal Production (`legal_production`)
- Maximum security and compliance
- Mandatory audit logging
- Chain of custody tracking
- Highest confidence requirements
- Expert review requirements

### Demo (`demo`)
- Cost-optimized for demonstrations
- Lower cost thresholds
- Simplified settings

## Configuration Sections

### OpenAI Configuration

```yaml
openai:
  model: "gpt-4.1-mini"           # Model: gpt-4.1-mini, gpt-4o, gpt-4o-mini, gpt-4
  cost_per_image: 0.0014          # Estimated cost per image (USD)
  max_tokens: null                # Max tokens (null = model default)
  temperature: 0.1                # Temperature (0.0-2.0)
  timeout: 60                     # Request timeout (seconds)
```

**Validation Rules:**
- `model`: Must be in approved list
- `cost_per_image`: ≥ 0.0
- `max_tokens`: ≥ 1 or null
- `temperature`: 0.0 ≤ temperature ≤ 2.0
- `timeout`: ≥ 1

### Performance Configuration

```yaml
performance:
  max_workers: 3                  # Concurrent API calls (1-10)
  default_parallel_batches: 2     # Default parallel batches (1-8)
  max_parallel_batches: 8         # Maximum parallel batches (1-20)
  request_delay: 0.1              # Delay between requests (≥0.0)
```

**Validation Rules:**
- `max_workers`: 1 ≤ workers ≤ 10
- `default_parallel_batches`: 1 ≤ batches ≤ 8
- `max_parallel_batches`: 1 ≤ batches ≤ 20
- `request_delay`: ≥ 0.0

### File Processing Configuration

```yaml
file_processing:
  supported_extensions:           # Supported image formats
    - .jpg
    - .jpeg
    - .png
    - .bmp
    - .tiff
    - .webp
    - .gif
  max_file_size_mb: 20           # Maximum file size (1-100 MB)
  image_quality_threshold: 0.3   # Quality threshold (0.0-1.0)
```

### Analysis Configuration

```yaml
analysis:
  confidence_threshold: 0.7       # Evidence confidence threshold (0.0-1.0)
  enable_confidence_filtering: true  # Enable filtering by confidence
  require_expert_review: false    # Require expert review
  enable_preprocessing: false     # Enable image preprocessing

  # Retry Configuration
  max_retries: 3                 # Maximum retries (0-10)
  retry_delay_base: 1.0          # Base retry delay (≥0.0)
  retry_delay_max: 60.0          # Maximum retry delay (≥1.0)
  retry_on_rate_limit: true      # Retry on rate limits
  retry_on_timeout: true         # Retry on timeouts
  retry_on_connection_error: true # Retry on connection errors
```

### Legal Framework Configuration

```yaml
legal:
  default_domain: "employment_law"  # Default legal domain
  require_confirmation: true        # Require user confirmation
  chain_of_custody: true           # Enable chain of custody
  audit_logging: true              # Enable audit logging

  # Audit Logging
  audit_log_file: "audit.log"      # Audit log filename
  audit_log_format: "json"         # Format: json, text, structured
  include_full_analysis: false     # Include full analysis in logs
  log_api_calls: true              # Log API calls
  log_file_operations: true        # Log file operations
  log_cost_tracking: true          # Log cost events

  # Chain of Custody
  chain_of_custody_file: "chain_of_custody.json"
  include_checksums: true          # Calculate file checksums
  include_timestamps: true         # Detailed timestamps
  include_environment_info: true   # System environment info
```

**Validation Rules:**
- `audit_log_format`: Must be "json", "text", or "structured"
- `default_domain`: Must be valid legal domain

### Cost Control Configuration

```yaml
cost_control:
  max_daily_cost: 50.0           # Maximum daily spending (≥0.0)
  warning_threshold: 10.0        # Cost warning threshold (≥0.0)
  confirm_above_cost: 5.0        # Confirmation threshold (≥0.0)
  track_usage: true              # Enable usage tracking
```

### Output Configuration

```yaml
output:
  default_directory: "./evidence"  # Default output directory
  create_summary_report: true      # Generate summary reports
  create_json_output: false       # Generate JSON output
  include_timestamps: true         # Include timestamps
  preserve_originals: true        # Keep original images

  # Formatting
  json_indent: 2                  # JSON indentation (≥0)
  cost_decimal_places: 2          # Cost display decimals (0-10)
  cost_precision_places: 4        # Precise cost decimals (0-10)
  summary_truncation: 100         # Summary length (≥10)

  # Progress Indicators
  use_emojis: true               # Enable emoji indicators
  success_icon: "✓"              # Success indicator
  error_icon: "❌"                # Error indicator
  info_icon: "🔍"                 # Information indicator
  cost_icon: "💰"                 # Cost indicator
  folder_icon: "📁"               # Folder indicator
  processing_icon: "🔄"          # Processing indicator
```

### Logging Configuration

```yaml
logging:
  level: "INFO"                  # Log level: DEBUG, INFO, WARNING, ERROR
  enable_file_logging: true      # Enable file logging
  log_directory: "./logs"        # Log directory
  max_log_size_mb: 10           # Max log size (1-100 MB)
  backup_count: 5               # Backup files (1-20)
```

**Validation Rules:**
- `level`: Must be valid log level
- `max_log_size_mb`: 1 ≤ size ≤ 100
- `backup_count`: 1 ≤ count ≤ 20

### Security Configuration

```yaml
security:
  sanitize_filenames: true       # Sanitize filenames
  validate_file_types: true     # Validate file types
  max_path_length: 255          # Max path length (50-4096)
  restrict_output_paths: true   # Restrict output paths
```

## Legal Domain Configuration

Each legal domain has specialized settings:

### Employment Law

```yaml
employment_law:
  confidence_threshold: 0.8
  require_expert_review: true
  evidence_types:
    - workplace_safety
    - discrimination
    - harassment
    - policy_violation
    - critical_violation
  directory_structure:
    - critical_violations
    - workplace_safety_violations
    - discrimination_evidence
    - documentation
  cost_multiplier: 1.0
```

### Personal Injury

```yaml
personal_injury:
  confidence_threshold: 0.85
  require_expert_review: true
  cost_multiplier: 1.2          # Higher cost for detailed analysis
```

### Criminal Law

```yaml
criminal_law:
  confidence_threshold: 0.9     # Highest threshold
  require_expert_review: true
  chain_of_custody_required: true
  cost_multiplier: 1.5
```

### Civil Litigation

```yaml
civil_litigation:
  confidence_threshold: 0.75
  require_expert_review: false
  cost_multiplier: 0.8          # Lower cost
```

### Regulatory Compliance

```yaml
regulatory_compliance:
  confidence_threshold: 0.8
  require_expert_review: true
  cost_multiplier: 1.1
```

### Family Law

```yaml
family_law:
  confidence_threshold: 0.75
  require_expert_review: false
  privacy_enhanced: true        # Extra privacy controls
  cost_multiplier: 0.9
```

## Environment Variables

The system also supports environment variable overrides:

```bash
export IMAGE_ANALYZER_ENV=production
export OPENAI_API_KEY=your_api_key_here
export USER=your_username       # For chain of custody
```

## Custom Configuration

### User Configuration File

Create `config/user.yaml` for custom overrides:

```yaml
# config/user.yaml
openai:
  model: "gpt-4o"              # Override default model

performance:
  max_workers: 5               # Increase concurrency

cost_control:
  max_daily_cost: 100.0        # Increase budget

output:
  use_emojis: false            # Disable emojis
```

### Programmatic Configuration

```python
from config.config import ConfigManager, Environment

# Custom configuration directory
config_manager = ConfigManager(config_dir=Path("./custom_config"))
config = config_manager.load_config(Environment.PRODUCTION)

# Save user overrides
config_manager.save_user_config({
    "openai": {"model": "gpt-4o"},
    "performance": {"max_workers": 6}
})
```

## Validation and Error Handling

The Pydantic-based configuration system provides:

- **Type Safety**: All fields are strongly typed
- **Range Validation**: Numeric values within acceptable bounds
- **Format Validation**: String values match expected formats
- **Required Field Validation**: Critical fields must be present
- **Custom Validators**: Domain-specific validation rules

### Common Validation Errors

```
ValidationError: Model must be one of ['gpt-4.1-mini', 'gpt-4o', 'gpt-4o-mini', 'gpt-4']
ValidationError: max_workers: Input should be less than or equal to 10
ValidationError: confidence_threshold: Input should be less than or equal to 1.0
```

## Best Practices

1. **Environment-Specific Settings**: Use environment overrides rather than modifying defaults
2. **Cost Controls**: Set appropriate daily limits for your use case
3. **Audit Logging**: Enable for production and legal environments
4. **Confidence Thresholds**: Adjust based on legal domain requirements
5. **Performance Tuning**: Balance speed vs. cost based on volume
6. **Security**: Enable validation and path restrictions in production

## Migration Guide

If upgrading from previous versions:

1. **Backup Existing Config**: Save any custom settings
2. **Update Dependencies**: Ensure Pydantic ≥2.0.0 is installed
3. **Review Validation**: Check for any validation errors
4. **Test Configuration**: Run configuration tests
5. **Update Documentation**: Review new capabilities

## Troubleshooting

### Configuration Loading Issues

```python
# Test configuration loading
from config.config import get_config, Environment

try:
    config = get_config(Environment.DEVELOPMENT)
    print("✅ Configuration loaded successfully")
except Exception as e:
    print(f"❌ Configuration error: {e}")
```

### Validation Errors

Check the specific validation message and adjust configuration values to meet the constraints defined in the Pydantic models.

### Missing Files

The system gracefully handles missing configuration files by using defaults. Ensure configuration directory is accessible and files are properly formatted YAML.