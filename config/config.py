#!/usr/bin/env python3
"""
Configuration Management for Image Evidence Analyzer
Handles loading and merging of configuration files
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum


class Environment(str, Enum):
    """Supported environment types"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"
    LEGAL_PRODUCTION = "legal_production"
    DEMO = "demo"


class OpenAIConfig(BaseModel):
    """OpenAI API configuration"""
    model: str = Field(default="gpt-4.1-mini", description="OpenAI model for analysis")
    cost_per_image: float = Field(default=0.0014, ge=0.0, description="Estimated cost per image analysis (USD)")
    max_tokens: Optional[int] = Field(default=None, ge=1, description="Max tokens per request")
    temperature: float = Field(default=0.1, ge=0.0, le=2.0, description="Model temperature for consistency")
    timeout: int = Field(default=60, ge=1, description="Request timeout in seconds")

    @validator('model')
    def validate_model(cls, v):
        valid_models = ['gpt-4.1-mini', 'gpt-4o', 'gpt-4o-mini', 'gpt-4']
        if v not in valid_models:
            raise ValueError(f'Model must be one of {valid_models}')
        return v


class PerformanceConfig(BaseModel):
    """Performance and concurrency configuration"""
    max_workers: int = Field(default=3, ge=1, le=10, description="Max concurrent API calls")
    default_parallel_batches: int = Field(default=2, ge=1, le=8, description="Default number of parallel processing batches")
    max_parallel_batches: int = Field(default=8, ge=1, le=20, description="Maximum allowed parallel batches")
    request_delay: float = Field(default=0.1, ge=0.0, description="Delay between requests to respect rate limits (seconds)")


class FileProcessingConfig(BaseModel):
    """File processing configuration"""
    supported_extensions: List[str] = Field(
        default=['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif'],
        description="Supported image file extensions"
    )
    max_file_size_mb: int = Field(default=20, ge=1, le=100, description="Maximum file size in MB")
    image_quality_threshold: float = Field(default=0.3, ge=0.0, le=1.0, description="Minimum image quality score (0.0-1.0)")


class OutputConfig(BaseModel):
    """Output configuration"""
    default_directory: str = Field(default="./evidence", description="Default output directory")
    create_summary_report: bool = Field(default=True, description="Generate summary reports")
    create_json_output: bool = Field(default=False, description="Generate JSON output by default")
    include_timestamps: bool = Field(default=True, description="Include timestamps in filenames")
    preserve_originals: bool = Field(default=True, description="Keep copies of original images")

    # Formatting Configuration
    json_indent: int = Field(default=2, ge=0, description="JSON indentation spaces")
    cost_decimal_places: int = Field(default=2, ge=0, le=10, description="Decimal places for cost display")
    cost_precision_places: int = Field(default=4, ge=0, le=10, description="Decimal places for precise costs")
    summary_truncation: int = Field(default=100, ge=10, description="Characters to show in summaries")

    # Progress Indicators Configuration
    use_emojis: bool = Field(default=True, description="Enable emoji progress indicators")
    success_icon: str = Field(default="✓", description="Success indicator")
    error_icon: str = Field(default="❌", description="Error indicator")
    info_icon: str = Field(default="🔍", description="Information indicator")
    cost_icon: str = Field(default="💰", description="Cost indicator")
    folder_icon: str = Field(default="📁", description="Folder indicator")
    processing_icon: str = Field(default="🔄", description="Processing indicator")


class LegalConfig(BaseModel):
    """Legal framework configuration"""
    default_domain: str = Field(default="employment_law", description="Default legal domain")
    require_confirmation: bool = Field(default=True, description="Require user confirmation before analysis")
    chain_of_custody: bool = Field(default=True, description="Enable chain of custody tracking")
    audit_logging: bool = Field(default=True, description="Enable detailed audit logging")

    # Audit Logging Configuration
    audit_log_file: str = Field(default="audit.log", description="Audit log filename")
    audit_log_format: str = Field(default="json", description="Format: json, text, or structured")
    include_full_analysis: bool = Field(default=False, description="Include complete analysis in audit log")
    log_api_calls: bool = Field(default=True, description="Log API call details")
    log_file_operations: bool = Field(default=True, description="Log file copy/move operations")
    log_cost_tracking: bool = Field(default=True, description="Log cost-related events")

    # Chain of Custody Configuration
    chain_of_custody_file: str = Field(default="chain_of_custody.json", description="Chain of custody log")
    include_checksums: bool = Field(default=True, description="Calculate and store file checksums")
    include_timestamps: bool = Field(default=True, description="Detailed timestamp tracking")
    include_environment_info: bool = Field(default=True, description="Log system environment details")

    @validator('audit_log_format')
    def validate_audit_format(cls, v):
        valid_formats = ['json', 'text', 'structured']
        if v not in valid_formats:
            raise ValueError(f'Audit log format must be one of {valid_formats}')
        return v

    @validator('default_domain')
    def validate_domain(cls, v):
        valid_domains = ['employment_law', 'personal_injury', 'criminal_law', 'civil_litigation', 'regulatory_compliance', 'family_law']
        if v not in valid_domains:
            raise ValueError(f'Legal domain must be one of {valid_domains}')
        return v


class CostControlConfig(BaseModel):
    """Cost control configuration"""
    max_daily_cost: float = Field(default=50.0, ge=0.0, description="Maximum daily spending limit (USD)")
    warning_threshold: float = Field(default=10.0, ge=0.0, description="Cost warning threshold (USD)")
    confirm_above_cost: float = Field(default=5.0, ge=0.0, description="Require confirmation above this cost (USD)")
    track_usage: bool = Field(default=True, description="Enable usage tracking")


class AnalysisConfig(BaseModel):
    """Analysis configuration"""
    confidence_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="Minimum confidence for evidence classification")
    enable_confidence_filtering: bool = Field(default=True, description="Enable filtering of low-confidence evidence")
    require_expert_review: bool = Field(default=False, description="Flag high-severity items for expert review")
    enable_preprocessing: bool = Field(default=False, description="Enable image preprocessing (enhancement, etc.)")

    # Retry Configuration
    max_retries: int = Field(default=3, ge=0, le=10, description="Maximum retries for failed analyses")
    retry_delay_base: float = Field(default=1.0, ge=0.0, description="Base delay in seconds for exponential backoff")
    retry_delay_max: float = Field(default=60.0, ge=1.0, description="Maximum delay between retries (seconds)")
    retry_on_rate_limit: bool = Field(default=True, description="Retry on rate limit errors")
    retry_on_timeout: bool = Field(default=True, description="Retry on timeout errors")
    retry_on_connection_error: bool = Field(default=True, description="Retry on connection errors")


class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = Field(default="INFO", description="Log level: DEBUG, INFO, WARNING, ERROR")
    enable_file_logging: bool = Field(default=True, description="Enable logging to file")
    log_directory: str = Field(default="./logs", description="Log file directory")
    max_log_size_mb: int = Field(default=10, ge=1, le=100, description="Maximum log file size before rotation")
    backup_count: int = Field(default=5, ge=1, le=20, description="Number of backup log files to keep")

    @validator('level')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level must be one of {valid_levels}')
        return v.upper()


class SecurityConfig(BaseModel):
    """Security configuration"""
    sanitize_filenames: bool = Field(default=True, description="Sanitize filenames for security")
    validate_file_types: bool = Field(default=True, description="Validate file types beyond extensions")
    max_path_length: int = Field(default=255, ge=50, le=4096, description="Maximum file path length")
    restrict_output_paths: bool = Field(default=True, description="Restrict output to safe directories")


class Config(BaseModel):
    """Main configuration class"""
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig, description="OpenAI API configuration")
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig, description="Performance and concurrency settings")
    file_processing: FileProcessingConfig = Field(default_factory=FileProcessingConfig, description="File processing configuration")
    output: OutputConfig = Field(default_factory=OutputConfig, description="Output configuration")
    legal: LegalConfig = Field(default_factory=LegalConfig, description="Legal framework configuration")
    cost_control: CostControlConfig = Field(default_factory=CostControlConfig, description="Cost control configuration")
    analysis: AnalysisConfig = Field(default_factory=AnalysisConfig, description="Analysis configuration")
    logging: LoggingConfig = Field(default_factory=LoggingConfig, description="Logging configuration")
    security: SecurityConfig = Field(default_factory=SecurityConfig, description="Security configuration")


class ConfigManager:
    """Configuration manager for loading and merging configurations"""

    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path(__file__).parent
        self._config_cache: Dict[str, Any] = {}

    def load_config(self, environment: Optional[Environment] = None) -> Config:
        """Load configuration with environment-specific overrides"""

        # Detect environment from ENV var if not specified
        if environment is None:
            env_name = os.getenv('IMAGE_ANALYZER_ENV', 'development')
            try:
                environment = Environment(env_name)
            except ValueError:
                environment = Environment.DEVELOPMENT

        # Load base defaults
        config_data = self._load_yaml_file('defaults.yaml')

        # Load environment-specific overrides
        env_data = self._load_yaml_file('environments.yaml')
        if environment.value in env_data:
            config_data = self._merge_configs(config_data, env_data[environment.value])

            # Handle 'extends' directive for environment inheritance
            if 'extends' in env_data[environment.value]:
                parent_env = env_data[environment.value]['extends']
                if parent_env in env_data:
                    parent_config = env_data[parent_env]
                    config_data = self._merge_configs(parent_config, config_data)

        # Load user overrides if present
        user_config_path = self.config_dir / 'user.yaml'
        if user_config_path.exists():
            user_data = self._load_yaml_file('user.yaml')
            config_data = self._merge_configs(config_data, user_data)

        return self._dict_to_config(config_data)

    def load_legal_domain_config(self, domain: str) -> Dict[str, Any]:
        """Load legal domain-specific configuration"""
        legal_data = self._load_yaml_file('legal_domains.yaml')
        return legal_data.get(domain, {})

    def _load_yaml_file(self, filename: str) -> Dict[str, Any]:
        """Load and cache YAML configuration file"""
        if filename not in self._config_cache:
            file_path = self.config_dir / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    self._config_cache[filename] = yaml.safe_load(f) or {}
            else:
                self._config_cache[filename] = {}

        return self._config_cache[filename].copy()

    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two configuration dictionaries"""
        result = base.copy()

        for key, value in override.items():
            if key == 'extends':
                continue  # Skip extends directive

            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def _dict_to_config(self, config_data: Dict[str, Any]) -> Config:
        """Convert dictionary to Config Pydantic model"""
        # Map configuration sections to Pydantic model classes
        section_mapping = {
            'openai': OpenAIConfig,
            'performance': PerformanceConfig,
            'file_processing': FileProcessingConfig,
            'output': OutputConfig,
            'legal': LegalConfig,
            'cost_control': CostControlConfig,
            'analysis': AnalysisConfig,
            'logging': LoggingConfig,
            'security': SecurityConfig,
        }

        # Process each section with Pydantic validation
        processed_sections = {}
        for section_name, section_class in section_mapping.items():
            if section_name in config_data:
                try:
                    # Pydantic automatically validates and filters fields
                    processed_sections[section_name] = section_class(**config_data[section_name])
                except Exception as e:
                    # Log validation error and use defaults
                    print(f"Warning: Invalid configuration for {section_name}: {e}")
                    processed_sections[section_name] = section_class()
            else:
                # Use default configuration if section is missing
                processed_sections[section_name] = section_class()

        # Create main Config with validated sections
        return Config(**processed_sections)

    def save_user_config(self, config_updates: Dict[str, Any]):
        """Save user configuration overrides"""
        user_config_path = self.config_dir / 'user.yaml'

        # Load existing user config if present
        existing_config: Dict[str, Any] = {}
        if user_config_path.exists():
            with open(user_config_path, 'r') as f:
                existing_config = yaml.safe_load(f) or {}

        # Merge with updates
        merged_config = self._merge_configs(existing_config, config_updates)

        # Save back to file
        with open(user_config_path, 'w') as f:
            yaml.dump(merged_config, f, default_flow_style=False, indent=2)


# Global configuration manager instance
_config_manager = None

def get_config(environment: Optional[Environment] = None) -> Config:
    """Get global configuration instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager.load_config(environment)

def get_legal_domain_config(domain: str) -> Dict[str, Any]:
    """Get legal domain-specific configuration"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager.load_legal_domain_config(domain)

def set_config_directory(config_dir: Path):
    """Set custom configuration directory"""
    global _config_manager
    _config_manager = ConfigManager(config_dir)


if __name__ == "__main__":
    # Demo/testing
    config = get_config(Environment.DEVELOPMENT)
    print(f"OpenAI Model: {config.openai.model}")
    print(f"Max Workers: {config.performance.max_workers}")
    print(f"Cost per Image: ${config.openai.cost_per_image}")

    legal_config = get_legal_domain_config("employment_law")
    print(f"Employment Law Evidence Types: {legal_config.get('evidence_types', [])}")