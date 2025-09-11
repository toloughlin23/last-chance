#!/usr/bin/env python3
"""
Test the UK/ROI Corporate Trading Compliance System
"""

import sys
sys.path.append('.')

from services.compliance_system import UKROIComplianceSystem
from datetime import datetime, UTC, timedelta

def test_compliance_system():
    """Test the compliance system"""
    print("🧪 Testing UK/ROI Corporate Trading Compliance System")
    print("=" * 60)
    
    # Initialize compliance system
    compliance = UKROIComplianceSystem()
    
    # Test compliance check with sample context
    test_context = {
        'client_money': 1000000.0,
        'total_assets': 2000000.0,
        'execution_price': 150.0,
        'market_price': 150.1,
        'position_size': 50000.0,
        'total_market_cap': 1000000000.0,
        'transaction_time': datetime.now(UTC),
        'transaction_data': {
            'client_id': 'CLIENT_001',
            'instrument': 'AAPL',
            'quantity': 100,
            'price': 150.0
        },
        'target_market_validation': True,
        'risk_warning_provided': True,
        'order_rate': 500,
        'circuit_breaker_triggered': False,
        'data_processing_risk': 0.05,
        'dpia_conducted': True,
        'data_retention_days': 1000,
        'purpose_limitation': True,
        'explicit_consent': True,
        'withdrawal_right': True,
        'total_portfolio': 1000000.0,
        'liquid_assets': 400000.0,
        'last_stress_test': datetime.now(UTC) - timedelta(days=15)
    }
    
    # Run compliance check
    print("🔍 Running compliance check...")
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
    
    print("\n✅ Compliance system test completed")

if __name__ == "__main__":
    test_compliance_system()
