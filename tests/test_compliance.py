#!/usr/bin/env python3
"""
Test the UK/ROI Corporate Trading Compliance System
"""

import sys

sys.path.append(".")

from datetime import datetime, timedelta
from datetime import timezone as _timezone

from services.compliance_system import UKROIComplianceSystem

UTC = _timezone.utc


def test_compliance_system():
    """Test the compliance system"""
    compliance_logger.info("🧪 Testing UK/ROI Corporate Trading Compliance System", operation="enhanced_logging")
    compliance_logger.info("=" * 60, operation="enhanced_logging")

    # Initialize compliance system
    compliance = UKROIComplianceSystem()

    # Test compliance check with sample context
    test_context = {
        "client_money": 1000000.0,
        "total_assets": 2000000.0,
        "execution_price": 150.0,
        "market_price": 150.1,
        "position_size": 50000.0,
        "total_market_cap": 1000000000.0,
        "transaction_time": datetime.now(UTC),
        "transaction_data": {
            "client_id": "CLIENT_001",
            "instrument": "AAPL",
            "quantity": 100,
            "price": 150.0,
        },
        "target_market_validation": True,
        "risk_warning_provided": True,
        "order_rate": 500,
        "circuit_breaker_triggered": False,
        "data_processing_risk": 0.05,
        "dpia_conducted": True,
        "data_retention_days": 1000,
        "purpose_limitation": True,
        "explicit_consent": True,
        "withdrawal_right": True,
        "total_portfolio": 1000000.0,
        "liquid_assets": 400000.0,
        "last_stress_test": datetime.now(UTC) - timedelta(days=15),
    }

    # Run compliance check
    compliance_logger.info("🔍 Running compliance check...", operation="enhanced_logging")
    report = compliance.run_compliance_check(test_context)

    compliance_logger.info("📊 Compliance Report:", operation="enhanced_logging")
    compliance_logger.info(f"   Overall Status: {report.overall_status.value}", operation="enhanced_logging")
    compliance_logger.info(f"   Compliance Score: {report.summary['compliance_score']:.1f}%", operation="enhanced_logging")
    compliance_logger.info(f"   Total Checks: {report.total_checks}", operation="enhanced_logging")
    compliance_logger.info(f"   Passed: {report.passed_checks}", operation="enhanced_logging")
    compliance_logger.error(f"   Failed: {report.failed_checks}", operation="enhanced_logging")
    compliance_logger.warning(f"   Warnings: {report.warning_checks}", operation="enhanced_logging")
    compliance_logger.error(f"   Critical Violations: {report.summary['critical_violations']}", operation="enhanced_logging")
    compliance_logger.info(f"   Regulatory Coverage: {report.summary['regulatory_coverage']}", operation="enhanced_logging")

    # Get compliance status
    status = compliance.get_compliance_status()
    compliance_logger.info(f"\n📈 Current Status: {status['status']}", operation="enhanced_logging")
    compliance_logger.info(f"   Message: {status['message']}", operation="enhanced_logging")
    compliance_logger.info(f"   Compliance Score: {status['compliance_score']:.1f}%", operation="enhanced_logging")

    # Get metrics
    metrics = compliance.get_compliance_metrics()
    compliance_logger.info("\n📊 Compliance Metrics:", operation="enhanced_logging")
    compliance_logger.info(f"   Total Checks Performed: {metrics['total_checks_performed']}", operation="enhanced_logging")
    compliance_logger.info(f"   Compliance Violations: {metrics['compliance_violations']}", operation="enhanced_logging")
    compliance_logger.info(f"   Last Compliance Score: {metrics['last_compliance_score']:.1f}%", operation="enhanced_logging")
    compliance_logger.info(f"   Regulatory Alerts: {metrics['regulatory_alerts']}", operation="enhanced_logging")

    compliance_logger.info("\n✅ Compliance system test completed", operation="enhanced_logging")


if __name__ == "__main__":
    test_compliance_system()
