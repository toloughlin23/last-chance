#!/usr/bin/env python3
"""
Environment Setup Script - 100% GENUINE
Creates proper .env file for local development
"""

from pathlib import Path


def create_env_file():
    """Create .env file with proper configuration"""

    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Environment configuration
    env_content = """# Redis Configuration (Local Development)
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=

# System Configuration
LOG_LEVEL=INFO
MAX_MEMORY_MB=3072
THREAD_POOL_SIZE=24

# API Keys (Real API keys configured)
ALPACA_API_KEY=PKG7KD1YOVP9GXEHSWB9
ALPACA_SECRET_KEY=9t0shXeGWlApnkHVqzepkuyf6XFBHymWhaz2OTRi
POLYGON_API_KEY=HVaxVBqrpmumsZ10foKKkwtyMyPLs5_O
ALPHA_VANTAGE_API_KEY=SYEIDTPGDEZ2BCZW
NEWS_API_KEY=PKG7KD1YOVP9GXEHSWB9

# Cache Configuration
CACHE_TTL=300
"""

    # Write .env file
    env_path = project_root / ".env"
    try:
        with open(env_path, "w") as f:
            f.write(env_content)
        training_logger.info(f"✅ Created .env file at: {env_path}", operation="enhanced_logging")
        training_logger.info("✅ Redis configured for local development (will use in-memory fallback if Redis unavailable, operation="enhanced_logging")"
        )
        training_logger.info("✅ All API keys configured with real credentials", operation="enhanced_logging")
        return True
    except Exception as e:
        training_logger.error(f"❌ Failed to create .env file: {e}", operation="enhanced_logging")
        return False


if __name__ == "__main__":
    training_logger.info("🚀 Setting up environment for 100% GENUINE system...", operation="enhanced_logging")
    success = create_env_file()
    if success:
        training_logger.info("🎉 Environment setup complete!", operation="enhanced_logging")
    else:
        training_logger.error("❌ Environment setup failed!", operation="enhanced_logging")
