#!/usr/bin/env python3
"""
🚀 SIMPLE CONTAMINATION SCANNER
==============================
Quick contamination check before training
"""

import os
import re
import sys
from datetime import datetime
from typing import List, Dict, Any

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath('.')))

from utils.enhanced_logging_system import training_logger

class SimpleContaminationScanner:
    """🚀 SIMPLE: Quick contamination scanner for pre-training check"""
    
    def __init__(self):
        self.contamination_patterns = [
            # Placeholder patterns
            (r'placeholder', 'Placeholder text found'),
            (r'lorem ipsum', 'Lorem ipsum text found'),
            (r'mock data', 'Mock data found'),
            (r'dummy data', 'Dummy data found'),
            (r'fake data', 'Fake data found'),
            (r'stubbed', 'Stubbed code found'),
            (r'REPLACE_ME', 'Replace me marker found'),
            (r'CHANGEME', 'Change me marker found'),
            (r'YOUR_API_KEY', 'API key placeholder found'),
            (r'example\.com/api', 'Example API endpoint found'),
            (r'np\.random\.uniform\(', 'Random placeholder found'),
            (r'random\.uniform\(', 'Random placeholder found'),
            (r'# TODO:', 'TODO comment found'),
            (r'# FIXME:', 'FIXME comment found'),
            (r'# HACK:', 'HACK comment found'),
        ]
        
        self.excluded_dirs = {
            '__pycache__', '.git', 'node_modules', '.env', 'venv', 'env'
        }
        
        self.excluded_files = {
            '.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe'
        }

    def scan_file(self, file_path: str) -> List[Dict[str, Any]]:
        """🚀 SIMPLE: Scan a single file for contamination"""
        contaminations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    for pattern, description in self.contamination_patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            contaminations.append({
                                'file': file_path,
                                'line': line_num,
                                'pattern': pattern,
                                'description': description,
                                'content': line.strip(),
                                'severity': 'high' if 'placeholder' in pattern.lower() or 'mock' in pattern.lower() else 'medium'
                            })
                            
        except Exception as e:
            training_logger.warning(f"⚠️ Error scanning {file_path}: {e}", operation="enhanced_logging")
            
        return contaminations

    def scan_directory(self, directory: str) -> Dict[str, Any]:
        """🚀 SIMPLE: Scan directory for contamination"""
        start_time = datetime.now()
        all_contaminations = []
        total_files = 0
        scanned_files = 0
        
        training_logger.info("🚀 SIMPLE CONTAMINATION SCANNER STARTING", operation="enhanced_logging")
        training_logger.info("=" * 60, operation="enhanced_logging")
        
        for root, dirs, files in os.walk(directory):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                total_files += 1
                
                # Skip excluded file types
                if any(file.endswith(ext) for ext in self.excluded_files):
                    continue
                    
                # Only scan Python files for now
                if not file.endswith('.py'):
                    continue
                    
                scanned_files += 1
                contaminations = self.scan_file(file_path)
                all_contaminations.extend(contaminations)
                
                if contaminations:
                    training_logger.info(f"⚠️ {file_path}: {len(contaminations)} contaminations found", operation="enhanced_logging")
        
        end_time = datetime.now()
        scan_duration = (end_time - start_time).total_seconds()
        
        # Calculate results
        contaminated_files = len(set(c['file'] for c in all_contaminations))
        contamination_rate = (contaminated_files / scanned_files * 100) if scanned_files > 0 else 0
        
        results = {
            'scan_summary': {
                'total_files': total_files,
                'scanned_files': scanned_files,
                'contaminated_files': contaminated_files,
                'contamination_rate': contamination_rate,
                'is_system_clean': contaminated_files == 0
            },
            'contamination_details': all_contaminations,
            'scan_duration': scan_duration,
            'scan_timestamp': datetime.now().isoformat()
        }
        
        return results

    def print_results(self, results: Dict[str, Any]) -> None:
        """🚀 SIMPLE: Print scan results"""
        summary = results['scan_summary']
        contaminations = results['contamination_details']
        
        training_logger.info("\n🚀 SIMPLE CONTAMINATION SCAN RESULTS", operation="enhanced_logging")
        training_logger.info("=" * 60, operation="enhanced_logging")
        
        # Summary
        training_logger.info(f"📊 SCAN SUMMARY:", operation="enhanced_logging")
        training_logger.info(f"   Total files: {summary['total_files']}", operation="enhanced_logging")
        training_logger.info(f"   Scanned files: {summary['scanned_files']}", operation="enhanced_logging")
        training_logger.info(f"   Contaminated files: {summary['contaminated_files']}", operation="enhanced_logging")
        training_logger.info(f"   Contamination rate: {summary['contamination_rate']:.2f}%", operation="enhanced_logging")
        training_logger.info(f"   Scan duration: {results['scan_duration']:.2f} seconds", operation="enhanced_logging")
        
        # System status
        if summary['is_system_clean']:
            training_logger.info("\n✅ SYSTEM STATUS: CLEAN - Ready for training!", operation="enhanced_logging")
        else:
            training_logger.info(f"\n⚠️ SYSTEM STATUS: {summary['contaminated_files']} contaminated files found", operation="enhanced_logging")
            
        # Contamination details
        if contaminations:
            training_logger.info(f"\n🔍 CONTAMINATION DETAILS:", operation="enhanced_logging")
            for i, cont in enumerate(contaminations[:10], 1):  # Show first 10
                training_logger.info(f"   {i}. {cont['file']}:{cont['line']} - {cont['description']}", operation="enhanced_logging")
                training_logger.info(f"      Content: {cont['content'][:80]}...", operation="enhanced_logging")
                
            if len(contaminations) > 10:
                training_logger.info(f"   ... and {len(contaminations) - 10} more contaminations", operation="enhanced_logging")
        
        training_logger.info("\n" + "=" * 60, operation="enhanced_logging")

def main():
    """🚀 SIMPLE: Main function"""
    scanner = SimpleContaminationScanner()
    
    # Scan current directory
    results = scanner.scan_directory('.')
    
    # Print results
    scanner.print_results(results)
    
    # Return exit code based on results
    if results['scan_summary']['is_system_clean']:
        training_logger.info("✅ CONTAMINATION SCAN PASSED - System is clean!", operation="enhanced_logging")
        return 0
    else:
        training_logger.info("⚠️ CONTAMINATION SCAN FAILED - Contaminations found!", operation="enhanced_logging")
        return 1

if __name__ == "__main__":
    exit(main())
