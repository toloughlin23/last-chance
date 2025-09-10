from typing import List

from services.snapshot_client import SnapshotClient
from services.earnings_client import EarningsClient
from services.ssr_client import SSRClient
from uk_us_timezone_handler import get_uk_us_handler


class Hygiene:
    def __init__(self, snapshot: SnapshotClient | None = None, earnings: EarningsClient | None = None, ssr: SSRClient | None = None):
        self.snapshot = snapshot or SnapshotClient()
        self.earnings = earnings or EarningsClient()
        self.ssr = ssr or SSRClient()
        self.tz = get_uk_us_handler()

    def filter_symbols(
        self,
        symbols: List[str],
        strategy_profile: str = "mean_reversion",
        earnings_exclude: bool | None = None,
        halts_exclude: bool | None = None,
        ssr_exclude: bool | None = None,
    ) -> List[str]:
        if not symbols:
            return []
        # Auto defaults
        if earnings_exclude is None:
            earnings_exclude = (strategy_profile != "momentum")
        if halts_exclude is None:
            halts_exclude = True
        if ssr_exclude is None:
            ssr_exclude = (strategy_profile != "long_only")

        filtered = list(symbols)

        # Halts
        if halts_exclude:
            halted_map = self.snapshot.fetch_trading_halts(filtered)
            filtered = [s for s in filtered if not halted_map.get(s, False)]
            if not filtered:
                return []

        # Earnings on current US date
        if earnings_exclude and filtered:
            us_today = self.tz.get_us_market_time().date().isoformat()
            e_map = self.earnings.tickers_with_earnings_on(filtered, us_today)
            filtered = [s for s in filtered if not e_map.get(s, False)]
            if not filtered:
                return []

        # SSR (current day −10% from prior close)
        if ssr_exclude and filtered:
            now_us = self.tz.get_us_market_time()
            ssr_map = self.ssr.ssr_active_today(filtered, now_us.replace(hour=9, minute=30, second=0, microsecond=0))
            filtered = [s for s in filtered if not ssr_map.get(s, False)]

        return filtered
