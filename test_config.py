#!/usr/bin/env python3
"""
Test script for Pydantic configuration system
"""

import sys
from pathlib import Path

# Add the config module to path
sys.path.append(str(Path(__file__).parent))

from config.config import get_config, Environment

def test_configuration():
    """Test configuration loading with Pydantic models"""
    print("🧪 Testing Pydantic Configuration System")
    print("=" * 50)

    try:
        # Test development environment
        config = get_config(Environment.DEVELOPMENT)
        print("✅ Configuration loading successful!")
        print(f"📄 OpenAI Model: {config.openai.model}")
        print(f"⚡ Max Workers: {config.performance.max_workers}")
        print(f"🎯 Confidence Threshold: {config.analysis.confidence_threshold}")
        print(f"📋 Audit Logging: {config.legal.audit_logging}")
        print(f"💰 Cost per Image: ${config.openai.cost_per_image}")
        print(f"🔒 Security Validation: {config.security.validate_file_types}")

        # Test validation
        print("\n🔍 Testing Pydantic Validation...")
        print(f"✅ OpenAI temperature within bounds: {config.openai.temperature}")
        print(f"✅ Max workers within bounds: {config.performance.max_workers}")
        print(f"✅ Confidence threshold within bounds: {config.analysis.confidence_threshold}")

        # Test different environments
        print("\n🌍 Testing Different Environments...")
        for env in [Environment.TESTING, Environment.PRODUCTION, Environment.LEGAL_PRODUCTION]:
            env_config = get_config(env)
            print(f"✅ {env.value}: Model={env_config.openai.model}, Confidence={env_config.analysis.confidence_threshold}")

        print("\n🎉 All configuration tests passed!")
        return True

    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_configuration()
    sys.exit(0 if success else 1)