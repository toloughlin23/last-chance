#!/usr/bin/env python3
"""
🚀 ENHANCED: Fixed contamination status checker with proper data structure access
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.contamination_prevention_system import UltraAdvancedContaminationPreventionSystem

def main():
    scanner = UltraAdvancedContaminationPreventionSystem()
    results = scanner.scan_directory()
    
    print("=== 🚀 ENHANCED CONTAMINATION STATUS REPORT ===")
    
    # Fix: Access the correct nested structure
    summary = results['scan_summary']
    analytics = results['contamination_analytics']
    details = results['contamination_details']
    
    print(f"Total files scanned: {summary['total_files']}")
    print(f"Clean files: {summary['clean_files']}")
    print(f"Contaminated files: {summary['contaminated_files']}")
    print(f"Contamination rate: {summary['contamination_rate']:.2f}%")
    print(f"System is clean: {summary['is_system_clean']}")
    
    print("\n=== TOP CONTAMINATION CATEGORIES ===")
    for category, count in sorted(analytics['by_category'].items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{category}: {count}")
    
    print("\n=== CONTAMINATION BY SEVERITY ===")
    for severity, count in sorted(analytics['by_severity'].items(), key=lambda x: x[1], reverse=True):
        print(f"{severity}: {count}")
    
    print("\n=== SAMPLE CONTAMINATIONS ===")
    for i, contamination in enumerate(details[:5]):
        print(f"\n{i+1}. File: {contamination['file']}")
        print(f"   Category: {contamination['category']}")
        print(f"   Severity: {contamination['severity']}")
        print(f"   Content: {contamination['content'][:80]}...")
    
    # Enhanced compliance check
    contamination_rate = summary['contamination_rate']
    if contamination_rate < 10:
        print("\n✅ SYSTEM IS EXCELLENT - Very low contamination rate")
    elif contamination_rate < 25:
        print("\n✅ SYSTEM IS COMPLIANT - Acceptable contamination rate")
    elif contamination_rate < 50:
        print("\n⚠️ SYSTEM NEEDS ATTENTION - Moderate contamination rate")
    else:
        print("\n❌ SYSTEM NOT COMPLIANT - High contamination rate")
    
    # Performance metrics
    perf = results['performance_metrics']
    print(f"\n=== PERFORMANCE METRICS ===")
    print(f"Scan duration: {perf['scan_duration']:.2f} seconds")
    print(f"Files per second: {perf['files_per_second']:.2f}")
    print(f"Cache hit rate: {perf['cache_hit_rate']:.2f}%")
    print(f"Threads used: {perf['threads_used']}")

if __name__ == "__main__":
    main()
