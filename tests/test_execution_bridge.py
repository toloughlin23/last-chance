#!/usr/bin/env python3
"""
Test the Ultra-Institutional Execution Bridge
"""

import sys

sys.path.append(".")

from decimal import Decimal

from services.execution_bridge import (
    OrderSide,
    OrderType,
    UltraInstitutionalExecutionBridge,
)


def test_execution_bridge():
    """Test the execution bridge"""
    training_logger.info("🧪 Testing Ultra-Institutional Execution Bridge", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")

    # Initialize execution bridge
    bridge = UltraInstitutionalExecutionBridge()

    # Test portfolio metrics
    training_logger.info("📊 Testing portfolio metrics...", operation="enhanced_logging")
    metrics = bridge.get_portfolio_metrics()
    training_logger.info(f"   Total Value: ${metrics.total_value:,.2f}", operation="enhanced_logging")
    training_logger.info(f"   Total P&L: ${metrics.total_pnl:,.2f} ({metrics.total_pnl_percent:.2f}%, operation="enhanced_logging")")
    training_logger.info(f"   Cash Balance: ${metrics.cash_balance:,.2f}", operation="enhanced_logging")
    training_logger.info(f"   Buying Power: ${metrics.buying_power:,.2f}", operation="enhanced_logging")
    training_logger.info(f"   Positions: {metrics.positions_count}", operation="enhanced_logging")

    # Test execution metrics
    training_logger.info("\n📈 Testing execution metrics...", operation="enhanced_logging")
    exec_metrics = bridge.get_execution_metrics()
    training_logger.info(f"   Total Orders: {exec_metrics['total_orders_executed']}", operation="enhanced_logging")
    training_logger.info(f"   Successful: {exec_metrics['successful_orders']}", operation="enhanced_logging")
    training_logger.error(f"   Failed: {exec_metrics['failed_orders']}", operation="enhanced_logging")
    training_logger.info(f"   Average Execution Time: {exec_metrics['average_execution_time_ms']:.1f}ms", operation="enhanced_logging")

    # Test risk assessment
    training_logger.warning("\n⚠️ Testing risk assessment...", operation="enhanced_logging")
    risk_level, risk_score, risk_message = bridge._assess_risk(
        "AAPL", Decimal("100"), Decimal("150"), OrderSide.BUY
    )
    training_logger.info(f"   Risk Level: {risk_level.value}", operation="enhanced_logging")
    training_logger.info(f"   Risk Score: {risk_score:.2f}", operation="enhanced_logging")
    training_logger.info(f"   Risk Message: {risk_message}", operation="enhanced_logging")

    # Test compliance check
    training_logger.info("\n🏛️ Testing compliance check...", operation="enhanced_logging")
    compliance_ok, compliance_message = bridge._check_compliance(
        "AAPL", Decimal("100"), Decimal("150"), OrderSide.BUY
    )
    training_logger.info(f"   Compliance OK: {compliance_ok}", operation="enhanced_logging")
    training_logger.info(f"   Compliance Message: {compliance_message}", operation="enhanced_logging")

    # Test position size calculation
    training_logger.info("\n📏 Testing position size calculation...", operation="enhanced_logging")
    position_size = bridge._calculate_position_size(
        "AAPL", 0.8, Decimal("150"), Decimal("100000")
    )
    training_logger.info(f"   Position Size: {position_size:.2%}", operation="enhanced_logging")

    # Test order creation
    training_logger.info("\n📝 Testing order creation...", operation="enhanced_logging")
    order = bridge._create_order(
        "AAPL", OrderSide.BUY, Decimal("100"), OrderType.MARKET, Decimal("150")
    )
    training_logger.info(f"   Order ID: {order.order_id}", operation="enhanced_logging")
    training_logger.info(f"   Symbol: {order.symbol}", operation="enhanced_logging")
    training_logger.info(f"   Side: {order.side.value}", operation="enhanced_logging")
    training_logger.info(f"   Quantity: {order.quantity}", operation="enhanced_logging")
    training_logger.info(f"   Price: {order.price}", operation="enhanced_logging")
    training_logger.info(f"   Status: {order.status.value}", operation="enhanced_logging")

    # Test active orders
    training_logger.info("\n📋 Testing active orders...", operation="enhanced_logging")
    active_orders = bridge.get_active_orders()
    training_logger.info(f"   Active Orders: {len(active_orders, operation="enhanced_logging")}")

    # Test risk limits
    training_logger.info("\n🛡️ Testing risk limits...", operation="enhanced_logging")
    training_logger.info(f"   Max Position Size: {bridge.max_position_size:.2%}", operation="enhanced_logging")
    training_logger.info(f"   Max Daily Loss: {bridge.max_daily_loss:.2%}", operation="enhanced_logging")
    training_logger.info(f"   Max Order Value: ${bridge.max_order_value:,.2f}", operation="enhanced_logging")
    training_logger.info(f"   Min Order Value: ${bridge.min_order_value:,.2f}", operation="enhanced_logging")

    # Test risk limits details
    training_logger.info("\n📊 Testing risk limits details...", operation="enhanced_logging")
    for limit_name, limit_value in bridge.risk_limits.items():
        training_logger.info(f"   {limit_name}: {limit_value:.2%}", operation="enhanced_logging")

    # Shutdown
    bridge.shutdown()
    training_logger.info("\n✅ Execution bridge test completed", operation="enhanced_logging")


if __name__ == "__main__":
    test_execution_bridge()
