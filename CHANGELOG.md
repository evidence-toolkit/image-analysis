# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-09-23

### Fixed
- Fixed dynamic version reporting in CLI command
- Updated version handling to use __version__ from package

### Changed
- CLI version command now dynamically reads version from package metadata
- Improved version consistency across project files

### Development
- Added pytest as development dependency
- Added safety for security auditing
- Enhanced development toolchain with uv package management

## [0.1.0] - 2025-09-23

### Added
- Initial release of Image Evidence Analyzer
- AI-powered forensic image analysis for legal evidence processing
- Support for UK employment law compliance frameworks
- CLI interface with analyze, single, estimate, and version commands
- Configuration system with environment-aware operation
- Parallel processing capabilities for batch analysis
- Cost estimation functionality
- Comprehensive legal evidence data models
- Evidence organization and reporting features
- OpenAI GPT-4 Vision API integration
- Support for multiple image formats (JPEG, PNG, BMP, TIFF, WebP, GIF)

### Features
- **Core Analysis Engine**: LegalEvidenceAnalyzer with structured outputs
- **Legal Evidence Models**: Pydantic-based data validation
- **Evidence Organization**: Automatic categorization by severity and legal type
- **CLI Interface**: Full command-line interface with subcommands
- **Configuration System**: Pydantic-based configuration management
- **Parallel Processing**: ThreadPoolExecutor for concurrent API calls
- **Cost Tracking**: Thread-safe cost accumulation across operations
- **Environment Support**: Development, testing, production, legal production modes

### Security
- Comprehensive dependency security scanning
- Zero known vulnerabilities in dependencies
- Secure handling of API keys and sensitive data