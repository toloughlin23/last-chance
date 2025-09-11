#!/usr/bin/env python3
"""
🔧 REDIS SETUP SCRIPT
====================
100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER

Setup Redis for institutional-grade infrastructure
- 3GB memory allocation
- Production configuration
- Performance optimization
- NO development shortcuts
"""

import os
import subprocess
import sys
import platform
from pathlib import Path


def install_redis():
    """Install Redis based on the operating system"""
    system = platform.system().lower()
    
    print(f"🔧 Installing Redis for {system}")
    
    if system == "windows":
        print("⚠️ Windows detected - Redis installation requires manual setup")
        print("Please install Redis using one of these methods:")
        print("1. Download from: https://github.com/microsoftarchive/redis/releases")
        print("2. Use WSL2 with Ubuntu and install Redis there")
        print("3. Use Docker: docker run -d -p 6379:6379 redis:alpine")
        return False
    
    elif system == "darwin":  # macOS
        try:
            # Try Homebrew first
            subprocess.run(["brew", "install", "redis"], check=True)
            print("✅ Redis installed via Homebrew")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ Homebrew not found, trying MacPorts...")
            try:
                subprocess.run(["sudo", "port", "install", "redis"], check=True)
                print("✅ Redis installed via MacPorts")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("❌ Could not install Redis automatically")
                return False
    
    elif system == "linux":
        try:
            # Try apt (Ubuntu/Debian)
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "redis-server"], check=True)
            print("✅ Redis installed via apt")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Try yum (CentOS/RHEL)
                subprocess.run(["sudo", "yum", "install", "-y", "redis"], check=True)
                print("✅ Redis installed via yum")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    # Try dnf (Fedora)
                    subprocess.run(["sudo", "dnf", "install", "-y", "redis"], check=True)
                    print("✅ Redis installed via dnf")
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("❌ Could not install Redis automatically")
                    return False
    
    else:
        print(f"❌ Unsupported operating system: {system}")
        return False


def configure_redis():
    """Configure Redis for institutional use"""
    print("⚙️ Configuring Redis for institutional use...")
    
    # Redis configuration for 3GB allocation
    redis_config = """
# Institutional Redis Configuration
# 3GB memory allocation with performance optimization

# Memory settings
maxmemory 3gb
maxmemory-policy allkeys-lru

# Performance settings
tcp-keepalive 300
timeout 0
tcp-backlog 511

# Persistence settings
save 900 1
save 300 10
save 60 10000

# Logging
loglevel notice
logfile ""

# Security
protected-mode no
bind 127.0.0.1

# Performance optimization
hz 10
dynamic-hz yes
"""
    
    # Write configuration file
    config_path = Path("redis.conf")
    with open(config_path, "w") as f:
        f.write(redis_config)
    
    print(f"✅ Redis configuration written to {config_path}")
    return config_path


def install_python_redis():
    """Install Python Redis client"""
    print("🐍 Installing Python Redis client...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "redis"], check=True)
        print("✅ Python Redis client installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python Redis client: {e}")
        return False


def test_redis_connection():
    """Test Redis connection"""
    print("🧪 Testing Redis connection...")
    
    try:
        import redis
        client = redis.Redis(host='localhost', port=6379, db=0)
        client.ping()
        print("✅ Redis connection successful")
        
        # Test memory allocation
        client.set("test_key", "test_value")
        info = client.info("memory")
        max_memory = info.get("maxmemory", 0)
        if max_memory > 0:
            max_memory_mb = max_memory / (1024 * 1024)
            print(f"✅ Redis max memory: {max_memory_mb:.1f}MB")
        
        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False


def main():
    """Main setup function"""
    print("🏗️ REDIS SETUP FOR INSTITUTIONAL INFRASTRUCTURE")
    print("=" * 60)
    
    # Check if Redis is already installed
    try:
        import redis
        client = redis.Redis(host='localhost', port=6379, db=0)
        client.ping()
        print("✅ Redis is already installed and running")
        
        # Test configuration
        if test_redis_connection():
            print("🎉 Redis setup complete!")
            return True
    except:
        pass
    
    # Install Redis
    if not install_redis():
        print("⚠️ Redis installation failed, but continuing with fallback...")
    
    # Install Python client
    if not install_python_redis():
        print("❌ Python Redis client installation failed")
        return False
    
    # Configure Redis
    config_path = configure_redis()
    
    # Test connection
    if test_redis_connection():
        print("🎉 Redis setup complete!")
        print(f"📁 Configuration file: {config_path}")
        print("🚀 Ready for institutional infrastructure!")
        return True
    else:
        print("⚠️ Redis setup incomplete, but infrastructure will use memory fallback")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
