#!/usr/bin/env python3
"""
Test the Ultra-Institutional Execution Bridge
"""

import sys
sys.path.append('.')

from services.execution_bridge import UltraInstitutionalExecutionBridge, OrderSide, OrderType
from decimal import Decimal

def test_execution_bridge():
    """Test the execution bridge"""
    print("🧪 Testing Ultra-Institutional Execution Bridge")
    print("=" * 60)
    
    # Initialize execution bridge
    bridge = UltraInstitutionalExecutionBridge()
    
    # Test portfolio metrics
    print("📊 Testing portfolio metrics...")
    metrics = bridge.get_portfolio_metrics()
    print(f"   Total Value: ${metrics.total_value:,.2f}")
    print(f"   Total P&L: ${metrics.total_pnl:,.2f} ({metrics.total_pnl_percent:.2f}%)")
    print(f"   Cash Balance: ${metrics.cash_balance:,.2f}")
    print(f"   Buying Power: ${metrics.buying_power:,.2f}")
    print(f"   Positions: {metrics.positions_count}")
    
    # Test execution metrics
    print("\n📈 Testing execution metrics...")
    exec_metrics = bridge.get_execution_metrics()
    print(f"   Total Orders: {exec_metrics['total_orders_executed']}")
    print(f"   Successful: {exec_metrics['successful_orders']}")
    print(f"   Failed: {exec_metrics['failed_orders']}")
    print(f"   Average Execution Time: {exec_metrics['average_execution_time_ms']:.1f}ms")
    
    # Test risk assessment
    print("\n⚠️ Testing risk assessment...")
    risk_level, risk_score, risk_message = bridge._assess_risk("AAPL", Decimal('100'), Decimal('150'), OrderSide.BUY)
    print(f"   Risk Level: {risk_level.value}")
    print(f"   Risk Score: {risk_score:.2f}")
    print(f"   Risk Message: {risk_message}")
    
    # Test compliance check
    print("\n🏛️ Testing compliance check...")
    compliance_ok, compliance_message = bridge._check_compliance("AAPL", Decimal('100'), Decimal('150'), OrderSide.BUY)
    print(f"   Compliance OK: {compliance_ok}")
    print(f"   Compliance Message: {compliance_message}")
    
    # Test position size calculation
    print("\n📏 Testing position size calculation...")
    position_size = bridge._calculate_position_size("AAPL", 0.8, Decimal('150'), Decimal('100000'))
    print(f"   Position Size: {position_size:.2%}")
    
    # Test order creation
    print("\n📝 Testing order creation...")
    order = bridge._create_order("AAPL", OrderSide.BUY, Decimal('100'), OrderType.MARKET, Decimal('150'))
    print(f"   Order ID: {order.order_id}")
    print(f"   Symbol: {order.symbol}")
    print(f"   Side: {order.side.value}")
    print(f"   Quantity: {order.quantity}")
    print(f"   Price: {order.price}")
    print(f"   Status: {order.status.value}")
    
    # Test active orders
    print("\n📋 Testing active orders...")
    active_orders = bridge.get_active_orders()
    print(f"   Active Orders: {len(active_orders)}")
    
    # Test risk limits
    print("\n🛡️ Testing risk limits...")
    print(f"   Max Position Size: {bridge.max_position_size:.2%}")
    print(f"   Max Daily Loss: {bridge.max_daily_loss:.2%}")
    print(f"   Max Order Value: ${bridge.max_order_value:,.2f}")
    print(f"   Min Order Value: ${bridge.min_order_value:,.2f}")
    
    # Test risk limits details
    print("\n📊 Testing risk limits details...")
    for limit_name, limit_value in bridge.risk_limits.items():
        print(f"   {limit_name}: {limit_value:.2%}")
    
    # Shutdown
    bridge.shutdown()
    print("\n✅ Execution bridge test completed")

if __name__ == "__main__":
    test_execution_bridge()
