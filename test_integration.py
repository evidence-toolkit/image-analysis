#!/usr/bin/env python3
"""
Integration test for Pydantic configuration with LegalEvidenceAnalyzer
"""

import sys
import os
from pathlib import Path

# Add the module to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_analyzer_integration():
    """Test that LegalEvidenceAnalyzer works with Pydantic configuration"""
    print("🧪 Testing LegalEvidenceAnalyzer Integration")
    print("=" * 50)

    try:
        from image_analyzer.core_analyzer import LegalEvidenceAnalyzer, LegalDomain
        from config.config import Environment

        # Test that analyzer can be initialized with different environments
        print("🔧 Testing analyzer initialization...")

        # Set a dummy API key for testing
        os.environ['OPENAI_API_KEY'] = 'test-key-for-config-only'

        # Test development environment
        analyzer_dev = LegalEvidenceAnalyzer(
            api_key="test-key",
            legal_domain=LegalDomain.employment_law,
            environment=Environment.DEVELOPMENT
        )
        print(f"✅ Development environment: Model={analyzer_dev.config.openai.model}")

        # Test production environment
        analyzer_prod = LegalEvidenceAnalyzer(
            api_key="test-key",
            legal_domain=LegalDomain.employment_law,
            environment=Environment.PRODUCTION
        )
        print(f"✅ Production environment: Model={analyzer_prod.config.openai.model}")

        # Test legal production environment
        analyzer_legal = LegalEvidenceAnalyzer(
            api_key="test-key",
            legal_domain=LegalDomain.employment_law,
            environment=Environment.LEGAL_PRODUCTION
        )
        print(f"✅ Legal production environment: Model={analyzer_legal.config.openai.model}")

        # Test configuration attributes
        print("\n🔍 Testing configuration access...")
        print(f"✅ Max workers: {analyzer_dev.config.performance.max_workers}")
        print(f"✅ Confidence threshold: {analyzer_dev.config.analysis.confidence_threshold}")
        print(f"✅ Audit logging: {analyzer_dev.config.legal.audit_logging}")
        print(f"✅ Cost per image: ${analyzer_dev.config.openai.cost_per_image}")
        print(f"✅ Request delay: {analyzer_dev.config.performance.request_delay}s")

        # Test audit logging initialization
        print("\n📋 Testing audit logging initialization...")
        test_output_dir = Path("./test_output")
        test_output_dir.mkdir(exist_ok=True)

        analyzer_dev.initialize_audit_logging(test_output_dir)
        has_audit_logger = analyzer_dev.audit_logger is not None
        has_custody_tracker = analyzer_dev.custody_tracker is not None

        print(f"✅ Audit logger initialized: {has_audit_logger}")
        print(f"✅ Custody tracker initialized: {has_custody_tracker}")

        # Clean up test directory
        if test_output_dir.exists():
            import shutil
            shutil.rmtree(test_output_dir)

        print("\n🎉 All integration tests passed!")
        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_analyzer_integration()
    sys.exit(0 if success else 1)