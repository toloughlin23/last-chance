#!/usr/bin/env python3
"""
Enhanced Contamination Scanner - 100% GENUINE
Detects mock data, placeholders, saturation patterns, and hardcoded values
Focused on our actual codebase, not dependencies
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Directories to scan (our actual codebase)
SCAN_DIRECTORIES = [
    'CORE_SUPER_BANDITS',
    'core',
    'learning', 
    'services',
    'utils',
    'tests',
    'scripts'
]

# Files to exclude
EXCLUDE_PATTERNS = [
    '.venv',
    '__pycache__',
    '.git',
    'node_modules',
    'contamination_scanner',
    'enhanced_contamination_scanner',
    'check_no_mocks',
    'deep_genuine_verification',
    'ULTRA_ADVANCED_CONTAMINATION',
    '.pytest_cache',
    'contamination_scanner.py',
    'enhanced_contamination_scanner.py'
]

# Contamination patterns to detect
CONTAMINATION_PATTERNS = [
    # Random data generators - CRITICAL VIOLATIONS
    r'np\.random\.',
    r'random\.random',
    r'random\.normal',
    r'random\.uniform',
    r'random\.randint',
    r'random\.choice',
    r'random\.shuffle',
    r'random\.seed',
    r'numpy\.random',
    r'simulated_pnl',
    r'simulate.*data',
    
    # Mock data patterns
    r'lorem\s+ipsum',
    r'mock\s+data',
    r'dummy\s+data',
    r'fake\s+data',
    r'placeholder',
    r'stubbed',
    r'REPLACE_ME',
    r'CHANGEME',
    r'YOUR_API_KEY',
    r'example\.com/api',
    
    # Algorithm saturation patterns (CRITICAL)
    r'0\.6000',
    r'0\.9000', 
    r'0\.9500',
    r'0\.1000',
    r'mapped=0\.600',
    r'mapped=0\.900',
    r'mapped=0\.950',
    
    # Hard-coded identical values
    r'return\s+0\.6000',
    r'return\s+0\.9000',
    r'return\s+0\.9500',
    r'return\s+0\.1000',
    
    # Identical confidence patterns
    r'confidence.*=.*0\.6000',
    r'confidence.*=.*0\.9000',
    r'confidence.*=.*0\.9500',
    r'confidence.*=.*0\.1000',
    
    # Algorithm saturation patterns
    r'std=0\.000000',
    r'Unique values.*1/10',
    r'min=.*max=.*std=0\.000000',
    
    # Hard-coded mapping patterns
    r'raw=0\.400.*mapped=0\.600',
    r'raw=0\.400.*mapped=0\.900',
    r'raw=0\.400.*mapped=0\.950',
]

def should_scan_file(file_path: Path) -> bool:
    """Check if file should be scanned"""
    # Check if in scan directories
    in_scan_dir = any(str(file_path).startswith(d) for d in SCAN_DIRECTORIES)
    if not in_scan_dir:
        return False
    
    # Check if matches exclude patterns
    for pattern in EXCLUDE_PATTERNS:
        if pattern in str(file_path):
            return False
    
    return True

def scan_file(file_path: Path) -> List[Dict[str, Any]]:
    """Scan a single file for contamination patterns"""
    violations = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern in CONTAMINATION_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        violations.append({
                            'file': str(file_path),
                            'line': line_num,
                            'pattern': pattern,
                            'content': line.strip()
                        })
    except Exception as e:
        print(f'Error scanning {file_path}: {e}')
    
    return violations

def check_algorithm_saturation(file_path: str) -> List[str]:
    """Check for algorithm saturation patterns in specific files"""
    issues = []
    if not os.path.exists(file_path):
        return [f"File not found: {file_path}"]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Look for hard-coded confidence values
            hardcoded_patterns = [
                r'return\s+0\.\d{4}',
                r'confidence.*=.*0\.\d{4}',
                r'mapped.*=.*0\.\d{4}',
                r'min.*0\.\d{4}.*max.*0\.\d{4}',
            ]
            
            for pattern in hardcoded_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    issues.append(f"Found hardcoded values: {matches[:5]}")
                    
    except Exception as e:
        issues.append(f"Error reading file: {e}")
    
    return issues

def test_algorithm_diversity() -> Dict[str, Any]:
    """Test algorithm diversity to detect saturation"""
    try:
        import numpy as np

        from CORE_SUPER_BANDITS.optimized_linucb_institutional import OptimizedInstitutionalLinUCB
        from CORE_SUPER_BANDITS.optimized_neural_bandit_institutional import OptimizedInstitutionalNeuralBandit
        from CORE_SUPER_BANDITS.optimized_ucbv_institutional import OptimizedInstitutionalUCBV

        # Test with REAL deterministic feature sets - NO RANDOM DATA
        test_features = [
            np.array([0.1, -0.2, 0.3, -0.4, 0.5, -0.6, 0.7, -0.8, 0.9, -1.0, 0.8, -0.7, 0.6, -0.5, 0.4]),  # High volatility
            np.array([0.01, -0.02, 0.03, -0.04, 0.05, -0.01, 0.02, -0.03, 0.04, -0.05, 0.01, -0.02, 0.03, -0.04, 0.05]),  # Low volatility
            np.array([5.0, -4.5, 4.0, -3.5, 3.0, -2.5, 2.0, -1.5, 1.0, -0.5, 0.5, -1.0, 1.5, -2.0, 2.5]),  # Extreme values
            np.zeros(15),  # Zero features
            np.ones(15),  # Ones
        ]
        
        linucb = OptimizedInstitutionalLinUCB()
        neural = OptimizedInstitutionalNeuralBandit()
        ucbv = OptimizedInstitutionalUCBV()
        
        linucb_confs = []
        neural_confs = []
        ucbv_confs = []
        
        for features in test_features:
            linucb_confs.append(linucb.get_confidence_for_context('buy_signal', features))
            neural_confs.append(neural.get_confidence_for_context('buy_signal', features))
            ucbv_confs.append(ucbv.get_confidence_for_context('buy_signal', features))
        
        # Check for saturation
        linucb_unique = len(set(linucb_confs))
        neural_unique = len(set(neural_confs))
        ucbv_unique = len(set(ucbv_confs))
        
        linucb_std = np.std(linucb_confs)
        neural_std = np.std(neural_confs)
        ucbv_std = np.std(ucbv_confs)
        
        return {
            'linucb_unique': linucb_unique,
            'neural_unique': neural_unique,
            'ucbv_unique': ucbv_unique,
            'linucb_std': linucb_std,
            'neural_std': neural_std,
            'ucbv_std': ucbv_std,
            'linucb_confs': linucb_confs,
            'neural_confs': neural_confs,
            'ucbv_confs': ucbv_confs
        }
    except Exception as e:
        return {'error': str(e)}

def main():
    print('🔍 ENHANCED CONTAMINATION SCAN - 100% GENUINE')
    print('=' * 60)
    
    # Scan our actual codebase
    all_violations = []
    python_files = []
    
    for scan_dir in SCAN_DIRECTORIES:
        if os.path.exists(scan_dir):
            for file_path in Path(scan_dir).rglob('*.py'):
                if should_scan_file(file_path):
                    python_files.append(file_path)
                    violations = scan_file(file_path)
                    all_violations.extend(violations)
    
    print(f'\n📊 SCAN RESULTS: {len(all_violations)} violations found across {len(python_files)} files')
    print(f'Directories scanned: {SCAN_DIRECTORIES}')
    print(f'Total files scanned: {len(python_files)}')
    print(f'Violations found: {len(all_violations)}')
    
    if all_violations:
        print(f'\n🚨 CONTAMINATION VIOLATIONS DETECTED: {len(all_violations)} issues requiring immediate fix!')
        print('=' * 60)
        
        # Group by file
        by_file = {}
        for v in all_violations:
            if v['file'] not in by_file:
                by_file[v['file']] = []
            by_file[v['file']].append(v)
        
        for file_path, violations in by_file.items():
            print(f'\n📁 {file_path}:')
            for v in violations:
                print(f'  Line {v["line"]:3d}: {v["pattern"]} -> "{v["content"]}"')
    else:
        print('\n✅ NO CONTAMINATION VIOLATIONS DETECTED')
    
    # Check for algorithm saturation patterns specifically
    print('\n🔍 ALGORITHM SATURATION CHECK: Testing 3 core algorithms (LinUCB, Neural, UCB-V) for genuine variation')
    print('=' * 40)
    
    saturation_files = [
        'CORE_SUPER_BANDITS/optimized_linucb_institutional.py',
        'CORE_SUPER_BANDITS/optimized_neural_bandit_institutional.py', 
        'CORE_SUPER_BANDITS/optimized_ucbv_institutional.py'
    ]
    
    for file_path in saturation_files:
        print(f'\n📁 {file_path}:')
        issues = check_algorithm_saturation(file_path)
        if issues:
            for issue in issues:
                print(f'  ⚠️  {issue}')
        else:
            print('  ✅ No saturation patterns detected')
    
    # Test algorithm diversity
    print('\n🧪 ALGORITHM DIVERSITY TEST: Measuring confidence variation across 3 core algorithms')
    print('=' * 40)
    
    diversity_results = test_algorithm_diversity()
    if 'error' in diversity_results:
        print(f'  ❌ Error testing diversity: {diversity_results["error"]}')
    else:
        print(f'  LinUCB: {diversity_results["linucb_unique"]}/5 unique, std={diversity_results["linucb_std"]:.6f}')
        print(f'  Neural: {diversity_results["neural_unique"]}/5 unique, std={diversity_results["neural_std"]:.6f}')
        print(f'  UCB-V:  {diversity_results["ucbv_unique"]}/5 unique, std={diversity_results["ucbv_std"]:.6f}')
        
        # Check for saturation
        if diversity_results["ucbv_unique"] < 3:
            print('  ⚠️  UCB-V showing low variation - potential saturation')
        if diversity_results["linucb_unique"] < 3:
            print('  ⚠️  LinUCB showing low variation - potential saturation')
        if diversity_results["neural_unique"] < 3:
            print('  ⚠️  Neural showing low variation - potential saturation')
    
    # Summary
    print(f'\n📋 SUMMARY: Scan completed at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Total violations: {len(all_violations)}')
    if len(all_violations) > 0:
        print('❌ CONTAMINATION DETECTED - FIX REQUIRED')
        return 1
    else:
        print('✅ NO CONTAMINATION DETECTED')
        return 0

if __name__ == '__main__':
    exit(main())
