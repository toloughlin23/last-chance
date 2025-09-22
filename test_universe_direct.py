#!/usr/bin/env python3
"""
Direct Universe Test - Bypass terminal tool
"""

import os
import sys
from dotenv import load_dotenv

# Set environment
os.environ['PYTHONPATH'] = '.'

def main():
    print("🚀 DIRECT UNIVERSE TEST")
    print("=" * 40)
    
    try:
        # Load environment
        load_dotenv()
        print("✅ Environment loaded")
        
        # Import modules
        from utils.active_universe_provider import ActiveUniverseProvider
        print("✅ Modules imported")
        
        # Initialize provider
        provider = ActiveUniverseProvider()
        print("✅ Provider initialized")
        
        # Generate universe
        print("🔄 Generating universe...")
        universe = provider.get_active_universe(
            target_size=5, 
            force_refresh=True, 
            batch_size=5
        )
        
        print(f"✅ Generated {len(universe)} symbols: {universe}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


