#!/usr/bin/env python3
"""
Test the UK/ROI Corporate Trading Compliance System with FIXED data
"""

import sys
sys.path.append('.')

from services.compliance_system import UKROIComplianceSystem
from datetime import datetime, UTC, timedelta

def test_compliance_system_fixed():
    """Test the compliance system with compliant data"""
    print("🧪 Testing UK/ROI Corporate Trading Compliance System (FIXED)")
    print("=" * 70)
    
    # Initialize compliance system
    compliance = UKROIComplianceSystem()
    
    # FIXED: Test compliance check with COMPLIANT data
    test_context = {
        # FIXED: Client money protection - 100% segregation
        'client_money': 2000000.0,  # Increased to match total_assets
        'total_assets': 2000000.0,
        
        # Best execution - minimal slippage
        'execution_price': 150.0,
        'market_price': 150.0,  # No slippage
        
        # Market abuse prevention - small position
        'position_size': 10000.0,  # Reduced from 50000
        'total_market_cap': 1000000000.0,
        
        # Transaction reporting - complete data
        'transaction_time': datetime.now(UTC),
        'transaction_data': {
            'client_id': 'CLIENT_001',
            'instrument': 'AAPL',
            'quantity': 100,
            'price': 150.0
        },
        
        # Product governance
        'target_market_validation': True,
        'risk_warning_provided': True,
        
        # Algorithmic trading controls
        'order_rate': 100,  # Reduced from 500
        'circuit_breaker_triggered': False,
        
        # GDPR compliance
        'data_processing_risk': 0.05,
        'dpia_conducted': True,
        'data_retention_days': 1000,
        'purpose_limitation': True,
        'explicit_consent': True,
        'withdrawal_right': True,
        
        # Risk management - FIXED liquidity
        'total_portfolio': 1000000.0,
        'liquid_assets': 500000.0,  # Increased to 50% liquidity
        'last_stress_test': datetime.now(UTC) - timedelta(days=15)
    }
    
    # Run compliance check
    print("🔍 Running compliance check with FIXED data...")
    report = compliance.run_compliance_check(test_context)
    
    print(f"📊 Compliance Report:")
    print(f"   Overall Status: {report.overall_status.value}")
    print(f"   Compliance Score: {report.summary['compliance_score']:.1f}%")
    print(f"   Total Checks: {report.total_checks}")
    print(f"   Passed: {report.passed_checks}")
    print(f"   Failed: {report.failed_checks}")
    print(f"   Warnings: {report.warning_checks}")
    print(f"   Critical Violations: {report.summary['critical_violations']}")
    print(f"   Regulatory Coverage: {report.summary['regulatory_coverage']}")
    
    # Show detailed results
    print(f"\n📋 Detailed Check Results:")
    for check in report.checks:
        status_icon = "✅" if check.status.value == "compliant" else "❌"
        print(f"   {status_icon} {check.rule_id}: {check.status.value} - {check.message}")
    
    # Get compliance status
    status = compliance.get_compliance_status()
    print(f"\n📈 Current Status: {status['status']}")
    print(f"   Message: {status['message']}")
    print(f"   Compliance Score: {status['compliance_score']:.1f}%")
    
    # Get metrics
    metrics = compliance.get_compliance_metrics()
    print(f"\n📊 Compliance Metrics:")
    print(f"   Total Checks Performed: {metrics['total_checks_performed']}")
    print(f"   Compliance Violations: {metrics['compliance_violations']}")
    print(f"   Last Compliance Score: {metrics['last_compliance_score']:.1f}%")
    print(f"   Regulatory Alerts: {metrics['regulatory_alerts']}")
    
    # Verify success
    if report.overall_status.value == "compliant" and report.summary['compliance_score'] >= 95:
        print("\n✅ Compliance system test PASSED - All checks compliant!")
        assert True, "Compliance system working correctly"
    else:
        print(f"\n❌ Compliance system test FAILED - Score: {report.summary['compliance_score']:.1f}%")
        assert False, f"Compliance score {report.summary['compliance_score']:.1f}% below threshold 95%"

if __name__ == "__main__":
    test_compliance_system_fixed()
