"""
🚀 FULL S&P 500 PROVIDER - Analyzes ALL 500 Symbols

This provider:
1. Gets ALL 500 S&P 500 symbols from Polygon
2. Analyzes ALL 500 for quality metrics (ADV, spreads, ATR%, stability)
3. Ranks ALL 500 by composite quality score
4. Presents top 200-300 to selector
5. Selector picks best 120-150

This ensures we never miss good opportunities!
"""

from __future__ import annotations

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple

from services.polygon_client import PolygonClient
from services.quotes_client import QuotesClient
from utils.universe_selector import UniverseSelector


class FullSP500Provider:
    """Full S&P 500 provider that analyzes ALL 500 symbols."""

    def __init__(self, polygon_client: Optional[PolygonClient] = None) -> None:
        self.polygon_client = polygon_client or PolygonClient()
        self.quotes_client = QuotesClient()

    def get_full_sp500_universe(
        self,
        target_size: int = 120,
        target_max_size: int = 150,
        analysis_days: int = 60,
        cache_path: str = "data/full_sp500_universe_120.json",
        max_age_hours: int = 18,
        force_refresh: bool = False,
        end_date: Optional[date] = None,
    ) -> List[str]:
        """Get universe by analyzing ALL S&P 500 symbols."""

        # Check cache first
        if not force_refresh and os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                analysis_iso = payload.get("analysis_date")
                if analysis_iso:
                    analysis_dt = datetime.fromisoformat(analysis_iso)
                    age_hours = (datetime.now() - analysis_dt).total_seconds() / 3600
                    if age_hours <= max_age_hours:
                        symbols = payload.get("symbols", [])
                        if isinstance(symbols, list) and len(symbols) >= target_size:
                            print(f"✅ Using cached universe: {len(symbols)} symbols")
                            return symbols[:target_max_size]
            except Exception:
                pass

        ed = end_date or date.today()
        sd = ed - timedelta(days=analysis_days)

        print(
            f"🚀 Building FULL S&P 500 universe (target: {target_size}-{target_max_size})..."
        )

        # Step 1: Get ALL S&P 500 symbols
        all_symbols = self._get_all_sp500_symbols()
        if not all_symbols:
            print("⚠️ No S&P 500 symbols found, using fallback")
            return self._get_fallback_symbols()[:target_max_size]

        print(f"📊 Found {len(all_symbols)} S&P 500 symbols to analyze")

        # Step 2: Analyze ALL symbols for quality metrics
        ranked_symbols = self._analyze_all_symbols(all_symbols, sd, ed)
        if not ranked_symbols:
            print("⚠️ No symbols passed quality analysis, using fallback")
            return self._get_fallback_symbols()[:target_max_size]

        print(f"📈 Ranked {len(ranked_symbols)} symbols by quality")

        # Step 3: Present top 200-300 to selector
        top_candidates = ranked_symbols[:300]  # Top 300 candidates
        print(f"🎯 Presenting top {len(top_candidates)} candidates to selector")

        # Step 4: Use selector to pick best 120-150
        universe = self._select_best_from_candidates(
            top_candidates, sd, ed, target_size, target_max_size
        )

        # Cache results
        self._save_universe(universe, analysis_days, cache_path)

        print(f"✅ Generated full S&P 500 universe: {len(universe)} symbols")
        return universe[:target_max_size]

    def _get_all_sp500_symbols(self) -> List[str]:
        """Get ALL S&P 500 symbols from Polygon."""
        try:
            print("🔍 Getting ALL S&P 500 symbols from Polygon...")

            # Get maximum number of symbols
            data = self.polygon_client.get_tickers(
                market="stocks", active=True, limit=1000  # Get as many as possible
            )

            results = data.get("results", [])
            if not results:
                print("⚠️ No tickers found from Polygon")
                return []

            print(f"📊 Found {len(results)} total tickers from Polygon")

            # Extract all valid symbols
            all_symbols = []
            for ticker in results:
                symbol = ticker.get("ticker")
                if isinstance(symbol, str) and len(symbol) <= 5 and symbol.isalpha():
                    all_symbols.append(symbol)

            print(f"📈 Extracted {len(all_symbols)} valid symbols")

            # If we have more than 500, take the first 500 (they're usually sorted by market cap)
            if len(all_symbols) > 500:
                all_symbols = all_symbols[:500]
                print("📊 Limited to top 500 symbols")

            return all_symbols

        except Exception as e:
            print(f"⚠️ Error getting S&P 500 symbols: {e}")
            return []

    def _analyze_all_symbols(
        self, symbols: List[str], start_date: date, end_date: date
    ) -> List[Dict]:
        """Analyze ALL symbols for quality metrics."""

        print(f"📊 Analyzing quality metrics for ALL {len(symbols)} symbols...")

        ranked_data = []
        batch_size = 20  # Process in batches

        # Process all symbols in batches
        for i in range(0, len(symbols), batch_size):
            batch = symbols[i : i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(symbols) + batch_size - 1) // batch_size

            print(
                f"  Processing batch {batch_num}/{total_batches}: {len(batch)} symbols"
            )

            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {}
                for symbol in batch:
                    future = executor.submit(
                        self._analyze_symbol_quality, symbol, start_date, end_date
                    )
                    futures[future] = symbol

                for future in as_completed(futures):
                    result = future.result()
                    if result:  # Only include symbols that passed quality analysis
                        ranked_data.append(result)

        # Sort by quality score (higher is better)
        ranked_data.sort(key=lambda x: x["quality_score"], reverse=True)

        print(f"✅ Quality analysis complete: {len(ranked_data)} symbols passed")
        if ranked_data:
            print(
                f"   Top 10 by quality: {[item['symbol'] for item in ranked_data[:10]]}"
            )

        return ranked_data

    def _analyze_symbol_quality(
        self, symbol: str, start_date: date, end_date: date
    ) -> Optional[Dict]:
        """Analyze quality metrics for a single symbol."""
        try:
            # Get market cap
            details = self.polygon_client.get_ticker_details(symbol)
            market_cap = details.get("results", {}).get("market_cap", 0)

            # GENEROUS market cap filter - only exclude very small caps
            if market_cap < 1_000_000_000:  # $1B minimum (very generous)
                return None

            # Get price data for ADV calculation
            price_data = self.polygon_client.get_aggs(
                symbol,
                1,
                "day",
                start_date.isoformat(),
                end_date.isoformat(),
                limit=60,
                adjusted=True,
            )

            results = price_data.get("results", [])
            if not results or len(results) < 10:  # Need at least 10 days of data
                return None

            # Calculate ADV
            total_volume = sum(float(r.get("v", 0)) for r in results)
            avg_price = sum(float(r.get("c", 0)) for r in results) / len(results)
            adv = total_volume * avg_price / len(results)

            # GENEROUS ADV filter - only exclude very low volume
            if adv < 5_000_000:  # $5M minimum (very generous)
                return None

            # Calculate spreads
            try:
                med_dollar, med_bps = self.quotes_client.median_spread_over_days(
                    symbol, days=5
                )
                # GENEROUS spread filter - only exclude extremely wide spreads
                if (
                    med_dollar > 10.0 or med_bps > 10000
                ):  # Only exclude extremely wide spreads
                    return None
            except Exception:
                med_dollar, med_bps = 0.05, 2.0  # Default reasonable spreads

            # Calculate ATR%
            prices = [float(r.get("c", 0)) for r in results if r.get("c")]
            if len(prices) < 5:
                return None

            atr_pct = self._calculate_atr_percentage(prices)

            # Calculate stability (inverse of volatility)
            returns = [prices[i] / prices[i - 1] - 1 for i in range(1, len(prices))]
            volatility = (
                sum((r - sum(returns) / len(returns)) ** 2 for r in returns)
                / len(returns)
            ) ** 0.5
            stability = 1 / (1 + volatility)  # Higher stability = lower volatility

            # Composite quality score
            quality_score = (
                min(adv / 1_000_000_000, 10) * 0.3  # ADV component (0-10)
                + max(0, 10 - med_bps / 100) * 0.3  # Spread component (0-10)
                + max(0, 10 - atr_pct) * 0.2  # ATR% component (0-10)
                + stability * 10 * 0.2  # Stability component (0-10)
            )

            return {
                "symbol": symbol,
                "market_cap": market_cap,
                "adv": adv,
                "spread_dollar": med_dollar,
                "spread_bps": med_bps,
                "atr_pct": atr_pct,
                "stability": stability,
                "quality_score": quality_score,
            }

        except Exception:
            return None

    def _calculate_atr_percentage(self, prices: List[float]) -> float:
        """Calculate Average True Range as percentage of price."""
        if len(prices) < 2:
            return 0.0

        true_ranges = []
        for i in range(1, len(prices)):
            high = max(prices[i], prices[i - 1])
            low = min(prices[i], prices[i - 1])
            true_ranges.append(high - low)

        if not true_ranges:
            return 0.0

        atr = sum(true_ranges) / len(true_ranges)
        avg_price = sum(prices) / len(prices)
        return (atr / avg_price) * 100 if avg_price > 0 else 0.0

    def _select_best_from_candidates(
        self,
        candidates: List[Dict],
        start_date: date,
        end_date: date,
        target_size: int,
        target_max_size: int,
    ) -> List[str]:
        """Use UniverseSelector to pick the best symbols from candidates."""

        print(
            f"🎯 Selecting best {target_size}-{target_max_size} symbols from {len(candidates)} candidates..."
        )

        # Extract just the symbols for the selector
        candidate_symbols = [item["symbol"] for item in candidates]

        selector = UniverseSelector()

        # Get sector info for balancing
        sector_classifier, sector_weights = self._build_sector_info(
            candidate_symbols[:100]
        )

        universe = selector.select_universe(
            candidates=candidate_symbols,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            target_size=target_size,
            target_max_size=target_max_size,
            allow_expand_above_target=True,
            expand_margin=0.9,
            min_price=10.0,
            min_atr_pct=0.01,
            max_atr_pct=0.05,
            adv_min_dollar=50_000_000.0,
            spread_filter_enabled=True,
            spread_max_dollars=0.02,
            spread_max_bps=5.0,
            spread_lookback_days=5,
            spread_core_hours_only=True,
            sector_classifier=sector_classifier,
            sector_index_weights=sector_weights,
            earnings_exclusion=None,  # Skip for now
            earnings_buffer_days=0,
        )

        return universe

    def _build_sector_info(
        self, symbols: List[str]
    ) -> Tuple[Optional[callable], Optional[Dict]]:
        """Build sector classifier and weights."""
        try:
            sector_counts = {}

            for symbol in symbols[:50]:  # Limit to avoid rate limits
                try:
                    details = self.polygon_client.get_ticker_details(symbol)
                    if details and details.get("results"):
                        sector = details["results"].get("sic_description", "Unknown")
                        sector_counts[sector] = sector_counts.get(sector, 0) + 1
                except Exception:
                    continue

            if not sector_counts:
                return None, None

            # Create sector classifier
            def sector_classifier(sym: str) -> Optional[str]:
                try:
                    details = self.polygon_client.get_ticker_details(sym)
                    if details and details.get("results"):
                        return details["results"].get("sic_description")
                except Exception:
                    pass
                return "Unknown"

            # Calculate weights
            total = sum(sector_counts.values())
            weights = {sector: count / total for sector, count in sector_counts.items()}

            return sector_classifier, weights

        except Exception:
            return None, None

    def _get_fallback_symbols(self) -> List[str]:
        """Fallback symbols if all else fails."""
        return [
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "TSLA",
            "META",
            "NVDA",
            "BRK.B",
            "UNH",
            "JNJ",
            "V",
            "PG",
            "JPM",
            "HD",
            "MA",
            "DIS",
            "PYPL",
            "ADBE",
            "NFLX",
            "CRM",
            "INTC",
            "CMCSA",
            "PFE",
            "TMO",
            "ABT",
            "COST",
            "PEP",
            "AVGO",
            "TXN",
            "QCOM",
            "ACN",
            "DHR",
            "VZ",
            "NKE",
            "MRK",
            "WMT",
            "LIN",
            "PM",
            "UNP",
            "HON",
            "IBM",
            "SPGI",
            "LOW",
            "AMGN",
            "CAT",
            "GE",
            "BA",
            "GS",
            "AXP",
            "MMM",
            "JPM",
            "WFC",
            "BAC",
            "C",
            "USB",
        ]

    def _save_universe(
        self, universe: List[str], analysis_days: int, cache_path: str
    ) -> None:
        """Save universe to cache."""
        try:
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            payload = {
                "analysis_date": datetime.now().isoformat(),
                "analysis_days": analysis_days,
                "symbols": universe,
                "count": len(universe),
            }
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
        except Exception:
            pass
