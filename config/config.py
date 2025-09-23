#!/usr/bin/env python3
"""
Configuration Management for Image Evidence Analyzer
Handles loading and merging of configuration files
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class Environment(str, Enum):
    """Supported environment types"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"
    LEGAL_PRODUCTION = "legal_production"
    DEMO = "demo"


@dataclass
class OpenAIConfig:
    """OpenAI API configuration"""
    model: str = "gpt-4.1-mini"
    cost_per_image: float = 0.0014
    max_tokens: Optional[int] = None
    temperature: float = 0.1
    timeout: int = 60


@dataclass
class PerformanceConfig:
    """Performance and concurrency configuration"""
    max_workers: int = 3
    default_parallel_batches: int = 2
    max_parallel_batches: int = 8
    request_delay: float = 0.1


@dataclass
class FileProcessingConfig:
    """File processing configuration"""
    supported_extensions: list = field(default_factory=lambda: [
        '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif'
    ])
    max_file_size_mb: int = 20
    image_quality_threshold: float = 0.3


@dataclass
class OutputConfig:
    """Output configuration"""
    default_directory: str = "./evidence"
    create_summary_report: bool = True
    create_json_output: bool = False
    include_timestamps: bool = True
    preserve_originals: bool = True


@dataclass
class LegalConfig:
    """Legal framework configuration"""
    default_domain: str = "employment_law"
    require_confirmation: bool = True
    chain_of_custody: bool = True
    audit_logging: bool = True


@dataclass
class CostControlConfig:
    """Cost control configuration"""
    max_daily_cost: float = 50.0
    warning_threshold: float = 10.0
    confirm_above_cost: float = 5.0
    track_usage: bool = True


@dataclass
class AnalysisConfig:
    """Analysis configuration"""
    confidence_threshold: float = 0.7
    require_expert_review: bool = False
    enable_preprocessing: bool = False
    max_retries: int = 2


@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    enable_file_logging: bool = True
    log_directory: str = "./logs"
    max_log_size_mb: int = 10
    backup_count: int = 5


@dataclass
class SecurityConfig:
    """Security configuration"""
    sanitize_filenames: bool = True
    validate_file_types: bool = True
    max_path_length: int = 255
    restrict_output_paths: bool = True


@dataclass
class Config:
    """Main configuration class"""
    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    file_processing: FileProcessingConfig = field(default_factory=FileProcessingConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    legal: LegalConfig = field(default_factory=LegalConfig)
    cost_control: CostControlConfig = field(default_factory=CostControlConfig)
    analysis: AnalysisConfig = field(default_factory=AnalysisConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)


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
        """Convert dictionary to Config dataclass"""
        config = Config()

        # Map configuration sections to dataclass fields
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

        for section_name, section_class in section_mapping.items():
            if section_name in config_data:
                section_data = config_data[section_name]
                # Create instance with filtered kwargs (only valid fields)
                valid_fields = {f.name for f in section_class.__dataclass_fields__.values()}
                filtered_data = {k: v for k, v in section_data.items() if k in valid_fields}
                setattr(config, section_name, section_class(**filtered_data))

        return config

    def save_user_config(self, config_updates: Dict[str, Any]):
        """Save user configuration overrides"""
        user_config_path = self.config_dir / 'user.yaml'

        # Load existing user config if present
        existing_config = {}
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