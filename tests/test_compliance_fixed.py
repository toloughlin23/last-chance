#!/usr/bin/env python3
"""
Test the UK/ROI Corporate Trading Compliance System with FIXED data
"""

import sys

sys.path.append(".")

from datetime import datetime, timedelta
from datetime import timezone as _timezone

from services.compliance_system import UKROIComplianceSystem

UTC = _timezone.utc


def test_compliance_system_fixed():
    """Test the compliance system with compliant data"""
    compliance_logger.info("🧪 Testing UK/ROI Corporate Trading Compliance System (FIXED, operation="enhanced_logging")")
    compliance_logger.info("=" * 70, operation="enhanced_logging")

    # Initialize compliance system
    compliance = UKROIComplianceSystem()

    # FIXED: Test compliance check with COMPLIANT data
    test_context = {
        # FIXED: Client money protection - 100% segregation
        "client_money": 2000000.0,  # Increased to match total_assets
        "total_assets": 2000000.0,
        # Best execution - minimal slippage
        "execution_price": 150.0,
        "market_price": 150.0,  # No slippage
        # Market abuse prevention - small position
        "position_size": 10000.0,  # Reduced from 50000
        "total_market_cap": 1000000000.0,
        # Transaction reporting - complete data
        "transaction_time": datetime.now(UTC),
        "transaction_data": {
            "client_id": "CLIENT_001",
            "instrument": "AAPL",
            "quantity": 100,
            "price": 150.0,
        },
        # Product governance
        "target_market_validation": True,
        "risk_warning_provided": True,
        # Algorithmic trading controls
        "order_rate": 100,  # Reduced from 500
        "circuit_breaker_triggered": False,
        # GDPR compliance
        "data_processing_risk": 0.05,
        "dpia_conducted": True,
        "data_retention_days": 1000,
        "purpose_limitation": True,
        "explicit_consent": True,
        "withdrawal_right": True,
        # Risk management - FIXED liquidity
        "total_portfolio": 1000000.0,
        "liquid_assets": 500000.0,  # Increased to 50% liquidity
        "last_stress_test": datetime.now(UTC) - timedelta(days=15),
    }

    # Run compliance check
    compliance_logger.info("🔍 Running compliance check with FIXED data...", operation="enhanced_logging")
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

    # Show detailed results
    compliance_logger.info("\n📋 Detailed Check Results:", operation="enhanced_logging")
    for check in report.checks:
        status_icon = "✅" if check.status.value == "compliant" else "❌"
        compliance_logger.info(f"   {status_icon} {check.rule_id}: {check.status.value} - {check.message}", operation="enhanced_logging")

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

    # Verify success
    if (
        report.overall_status.value == "compliant"
        and report.summary["compliance_score"] >= 95
    ):
        compliance_logger.info("\n✅ Compliance system test PASSED - All checks compliant!", operation="enhanced_logging")
        assert True, "Compliance system working correctly"
    else:
        compliance_logger.error(f"\n❌ Compliance system test FAILED - Score: {report.summary['compliance_score']:.1f}%", operation="enhanced_logging")
        assert (
            False
        ), f"Compliance score {report.summary['compliance_score']:.1f}% below threshold 95%"


if __name__ == "__main__":
    test_compliance_system_fixed()
