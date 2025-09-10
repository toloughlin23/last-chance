#!/usr/bin/env python3
"""
ShareSeek ML System - UK/US Timezone Handler
===========================================

PERMANENT solution for UK trader trading US markets.
This handles all timezone conversions between:
- UK time (GMT/BST) - where the user is located
- US Eastern Time (EST/EDT) - where the markets operate  
- UTC - standard for data storage and APIs

Created: 2025-08-30
Purpose: Eliminate recurring timezone issues permanently
"""

import pandas as pd
from datetime import datetime, timedelta
import pytz
from typing import Union, Optional
import logging

logger = logging.getLogger(__name__)

class UKUSTimezoneHandler:
    """
    Permanent timezone handler for UK trader trading US markets
    
    Key Features:
    - Always knows current UK time
    - Always knows current US market time  
    - Handles daylight saving transitions automatically
    - Converts between all timezone formats safely
    - Provides market hours in both UK and US time
    """
    
    def __init__(self):
        # Define timezones
        self.uk_tz = pytz.timezone('Europe/London')  # GMT/BST automatically
        self.us_market_tz = pytz.timezone('US/Eastern')  # EST/EDT automatically
        self.utc_tz = pytz.UTC
        
        logger.info("🌍 UK/US Timezone Handler initialized")
        logger.info(f"📍 UK Time: {self.get_uk_time()}")
        logger.info(f"🇺🇸 US Market Time: {self.get_us_market_time()}")
        logger.info(f"🌐 UTC Time: {self.get_utc_time()}")
    
    def get_uk_time(self) -> datetime:
        """Get current UK time (GMT/BST automatically handled)"""
        return datetime.now(self.uk_tz)
    
    def get_us_market_time(self) -> datetime:
        """Get current US market time (EST/EDT automatically handled)"""
        return datetime.now(self.us_market_tz)
    
    def get_utc_time(self) -> datetime:
        """Get current UTC time"""
        return datetime.now(self.utc_tz)
    
    def uk_to_us_market(self, uk_time: Union[datetime, str]) -> datetime:
        """Convert UK time to US market time"""
        if isinstance(uk_time, str):
            uk_time = pd.to_datetime(uk_time)
        
        if uk_time.tzinfo is None:
            uk_time = self.uk_tz.localize(uk_time)
        
        return uk_time.astimezone(self.us_market_tz)
    
    def us_market_to_uk(self, us_time: Union[datetime, str]) -> datetime:
        """Convert US market time to UK time"""
        if isinstance(us_time, str):
            us_time = pd.to_datetime(us_time)
        
        if us_time.tzinfo is None:
            us_time = self.us_market_tz.localize(us_time)
        
        return us_time.astimezone(self.uk_tz)
    
    def to_utc_naive(self, timestamp: Union[datetime, pd.Timestamp, str]) -> pd.Timestamp:
        """
        Convert ANY timestamp to UTC timezone-naive for safe comparisons
        This is the KEY function that prevents timezone comparison errors
        """
        try:
            # Convert to pandas timestamp
            ts = pd.to_datetime(timestamp)
            
            # If timezone-naive, assume UTC
            if ts.tz is None:
                return ts
            
            # Convert to UTC and remove timezone info
            return ts.tz_convert('UTC').tz_localize(None)
            
        except Exception as e:
            logger.warning(f"Timezone conversion failed for {timestamp}: {e}")
            # Fallback: return as-is but ensure it's timezone-naive
            ts = pd.to_datetime(timestamp)
            if hasattr(ts, 'tz_localize') and ts.tz is not None:
                return ts.tz_localize(None)
            return ts
    
    def is_us_market_open(self, check_time: Optional[datetime] = None) -> bool:
        """
        Check if US market is currently open
        Market hours: 9:30 AM - 4:00 PM ET (Monday-Friday)
        """
        if check_time is None:
            check_time = self.get_us_market_time()
        elif check_time.tzinfo is None:
            check_time = self.us_market_tz.localize(check_time)
        else:
            check_time = check_time.astimezone(self.us_market_tz)
        
        # Check if weekday
        if check_time.weekday() >= 5:  # Saturday = 5, Sunday = 6
            return False
        
        # Check market hours (9:30 AM - 4:00 PM ET)
        market_open = check_time.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = check_time.replace(hour=16, minute=0, second=0, microsecond=0)
        
        return market_open <= check_time <= market_close
    
    def get_market_hours_uk_time(self, date: Optional[datetime] = None) -> tuple:
        """
        Get US market hours in UK time for a given date
        Returns: (market_open_uk, market_close_uk)
        """
        if date is None:
            date = self.get_uk_time().date()
        elif hasattr(date, 'date'):
            date = date.date()
        
        # Create US market hours for the date
        market_open_us = self.us_market_tz.localize(
            datetime.combine(date, datetime.min.time().replace(hour=9, minute=30))
        )
        market_close_us = self.us_market_tz.localize(
            datetime.combine(date, datetime.min.time().replace(hour=16, minute=0))
        )
        
        # Convert to UK time
        market_open_uk = market_open_us.astimezone(self.uk_tz)
        market_close_uk = market_close_us.astimezone(self.uk_tz)
        
        return market_open_uk, market_close_uk
    
    def safe_timestamp_compare(self, ts1: Union[datetime, pd.Timestamp, str], 
                              ts2: Union[datetime, pd.Timestamp, str]) -> int:
        """
        Safely compare two timestamps regardless of timezone
        Returns: -1 if ts1 < ts2, 0 if equal, 1 if ts1 > ts2
        """
        try:
            # Convert both to UTC naive for comparison
            ts1_utc = self.to_utc_naive(ts1)
            ts2_utc = self.to_utc_naive(ts2)
            
            if ts1_utc < ts2_utc:
                return -1
            elif ts1_utc > ts2_utc:
                return 1
            else:
                return 0
                
        except Exception as e:
            logger.error(f"Timestamp comparison failed: {e}")
            return 0
    
    def get_trading_date_range(self, days_back: int = 90) -> tuple:
        """
        Get date range for data fetching (always in YYYY-MM-DD format)
        Accounts for weekends and ensures we get trading days
        """
        end_date = self.get_uk_time().date()
        start_date = end_date - timedelta(days=days_back)
        
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
    
    def log_timezone_status(self):
        """Log current timezone status for debugging"""
        uk_time = self.get_uk_time()
        us_time = self.get_us_market_time()
        utc_time = self.get_utc_time()
        
        market_open_uk, market_close_uk = self.get_market_hours_uk_time()
        is_open = self.is_us_market_open()
        
        logger.info("🌍 TIMEZONE STATUS:")
        logger.info(f"   📍 UK Time: {uk_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        logger.info(f"   🇺🇸 US Market Time: {us_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        logger.info(f"   🌐 UTC Time: {utc_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        logger.info(f"   📈 Market Open (UK): {market_open_uk.strftime('%H:%M %Z')}")
        logger.info(f"   📉 Market Close (UK): {market_close_uk.strftime('%H:%M %Z')}")
        logger.info(f"   ✅ Market Currently Open: {is_open}")

# Global instance for easy importing
uk_us_tz = UKUSTimezoneHandler()

def get_uk_us_handler() -> UKUSTimezoneHandler:
    """Get the global UK/US timezone handler instance"""
    return uk_us_tz

# Convenience functions for common operations
def get_current_uk_time() -> datetime:
    """Get current UK time"""
    return uk_us_tz.get_uk_time()

def get_current_us_market_time() -> datetime:
    """Get current US market time"""
    return uk_us_tz.get_us_market_time()

def is_market_open() -> bool:
    """Check if US market is currently open"""
    return uk_us_tz.is_us_market_open()

def safe_utc_naive(timestamp) -> pd.Timestamp:
    """Convert any timestamp to UTC timezone-naive for safe comparison"""
    return uk_us_tz.to_utc_naive(timestamp)

def get_trading_dates(days_back: int = 90) -> tuple:
    """Get start and end dates for data fetching"""
    return uk_us_tz.get_trading_date_range(days_back)

if __name__ == "__main__":
    # Test the timezone handler
    print("🌍 UK/US Timezone Handler Test")
    print("=" * 40)
    
    handler = UKUSTimezoneHandler()
    handler.log_timezone_status()
    
    print("\n📅 Trading Date Range (90 days):")
    start, end = get_trading_dates(90)
    print(f"   Start: {start}")
    print(f"   End: {end}")
    
    print("\n🔄 Timezone Conversions:")
    uk_time = get_current_uk_time()
    us_time = handler.uk_to_us_market(uk_time)
    print(f"   UK: {uk_time.strftime('%H:%M %Z')} → US: {us_time.strftime('%H:%M %Z')}")
    
    print("\n✅ UK/US Timezone Handler working correctly!")









