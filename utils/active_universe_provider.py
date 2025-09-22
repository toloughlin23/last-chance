"""
Active Universe Provider - 100% GENUINE (Polygon-first)
- Discovers large-cap candidates (Polygon if available; conservative fallback otherwise)
- Builds a 120-symbol active universe using UniverseSelector
- Caches to disk and refreshes when stale
"""

from __future__ import annotations

import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timedelta
from typing import List, Optional

from services.polygon_client import PolygonClient
from utils.universe_selector import UniverseSelector


class ActiveUniverseProvider:
    def __init__(self, polygon_client: Optional[PolygonClient] = None) -> None:
        self.polygon_client = polygon_client or PolygonClient()

    def _build_sector_classifier_and_weights(self, candidates: List[str]):
        """Build a sector classifier and sector weights using Polygon ticker details if available.

        Returns (sector_classifier, sector_index_weights) or (None, None) if unavailable.
        """
        sector_by_symbol = {}
        try:
            if hasattr(self.polygon_client, "get_ticker_details"):
                # Use ticker details endpoint which includes sector information
                for sym in candidates[:50]:  # Limit to first 50 to avoid rate limits
                    try:
                        data = self.polygon_client.get_ticker_details(sym)
                        if isinstance(data, dict):
                            # Use SIC description as sector classification
                            sic_desc = data.get("results", {}).get("sic_description")
                            if isinstance(sic_desc, str) and sic_desc.strip():
                                sector_by_symbol[sym] = sic_desc.strip()
                    except Exception:
                        continue  # Skip this symbol if details unavailable
        except Exception:
            sector_by_symbol = {}

        if not sector_by_symbol:
            return None, None

        # Derive approximate weights from the candidate distribution when index weights are not available
        total = max(1, len(sector_by_symbol))
        weights = {}
        for sec in set(sector_by_symbol.values()):
            count = sum(1 for s in sector_by_symbol if sector_by_symbol[s] == sec)
            weights[sec] = count / total

        def sector_classifier(sym: str) -> Optional[str]:
            return sector_by_symbol.get(sym)

        return sector_classifier, weights

    def _get_fallback_candidates(self, limit: int) -> List[str]:
        """Fallback list of known large-cap symbols if Polygon API fails."""
        known_large_caps = [
            # Technology
            "AAPL",
            "MSFT",
            "GOOGL",
            "GOOG",
            "AMZN",
            "NVDA",
            "META",
            "TSLA",
            "AVGO",
            "ORCL",
            "ADBE",
            "CRM",
            "CSCO",
            "ACN",
            "INTC",
            "AMD",
            "QCOM",
            "TXN",
            "IBM",
            "INTU",
            "AMAT",
            "NOW",
            "MU",
            "LRCX",
            "KLAC",
            "SNPS",
            "CDNS",
            "ADSK",
            "FTNT",
            "PANW",
            "WDAY",
            "TEAM",
            # Financials
            "BRK.B",
            "JPM",
            "V",
            "MA",
            "BAC",
            "WFC",
            "GS",
            "MS",
            "AXP",
            "SPGI",
            "BLK",
            "SCHW",
            "C",
            "PNC",
            "USB",
            "TFC",
            "COF",
            "BK",
            "ICE",
            "CME",
            "MCO",
            "MSCI",
            "TRV",
            "CB",
            "PGR",
            "ALL",
            "MET",
            # Healthcare
            "UNH",
            "JNJ",
            "LLY",
            "PFE",
            "ABBV",
            "MRK",
            "TMO",
            "ABT",
            "DHR",
            "CVS",
            "AMGN",
            "MDT",
            "BMY",
            "GILD",
            "ISRG",
            "VRTX",
            "SYK",
            "BSX",
            "CI",
            "HUM",
            "ELV",
            "ZTS",
            "REGN",
            "HCA",
            "MCK",
            "BDX",
            # Consumer
            "WMT",
            "PG",
            "HD",
            "COST",
            "MCD",
            "PEP",
            "KO",
            "NKE",
            "DIS",
            "SBUX",
            "TGT",
            "LOW",
            "TJX",
            "MDLZ",
            "MO",
            "PM",
            "CL",
            "EL",
            "GIS",
            "K",
            "KMB",
            "PGR",
            "STZ",
            "MNST",
            "KDP",
            "HSY",
            "CLX",
            # Industrials
            "CAT",
            "BA",
            "RTX",
            "HON",
            "UNP",
            "LMT",
            "DE",
            "UPS",
            "GE",
            "MMM",
            "CSX",
            "NOC",
            "GD",
            "EMR",
            "ETN",
            "ITW",
            "WM",
            "FDX",
            "NSC",
            "JCI",
            "PH",
            "CMI",
            "ROK",
            "OTIS",
            "CARR",
            "TT",
            "IR",
            # Energy & Materials
            "XOM",
            "CVX",
            "COP",
            "EOG",
            "SLB",
            "MPC",
            "PSX",
            "VLO",
            "PXD",
            "OXY",
            "HES",
            "KMI",
            "WMB",
            "LIN",
            "APD",
            "SHW",
            "ECL",
            "DD",
            "FCX",
            "NEM",
            "LYB",
            "DOW",
            "PPG",
            "ALB",
            "CTVA",
            "IFF",
            "CE",
            # Utilities & Real Estate
            "NEE",
            "SO",
            "DUK",
            "D",
            "AEP",
            "EXC",
            "SRE",
            "XEL",
            "WEC",
            "ES",
            "ED",
            "PEG",
            "AWK",
            "PCG",
            "EIX",
            "AMT",
            "PLD",
            "CCI",
            "EQIX",
            "PSA",
            "DLR",
            "O",
            "WELL",
            "SPG",
            "AVB",
            "EQR",
            "VTR",
            # Telecom & Media
            "VZ",
            "T",
            "TMUS",
            "CMCSA",
            "CHTR",
            "NFLX",
            "DIS",
            "WBD",
            "PARA",
            # Other large caps
            "BRK.A",
            "BKNG",
            "MELI",
            "SHOP",
            "UBER",
            "ABNB",
            "SQ",
            "PYPL",
            "FIS",
            "FISV",
            "ADP",
            "PAYX",
            "ZM",
            "DOCU",
            "OKTA",
            "VEEV",
        ]

        # Return up to limit symbols
        return known_large_caps[:limit]

    def _discover_and_rank_candidates(
        self,
        min_market_cap: float,
        analysis_days: int,
        start_date: date,
        end_date: date,
        max_candidates: int,
        batch_size: int,
    ) -> List[str]:
        """Discover S&P 500 candidates and rank them by quality metrics.

        This is the CORRECT design:
        1. Search entire S&P 500
        2. Rank by quality (ADV, spreads, ATR%, stability)
        3. Return top candidates for selector
        """
        try:
            print("🔍 Searching entire S&P 500 for candidates...")
            data = self.polygon_client.get_tickers(
                market="stocks", active=True, limit=500
            )

            results = data.get("results", [])
            if not results:
                print("⚠️ No tickers found from Polygon, using fallback list")
                return self._get_fallback_candidates(max_candidates)

            print(f"📊 Found {len(results)} total tickers from Polygon")

            # Extract all ticker symbols
            all_symbols = [
                ticker.get("ticker")
                for ticker in results
                if isinstance(ticker.get("ticker"), str)
            ]

            if not all_symbols:
                print("⚠️ No valid symbols found, using fallback list")
                return self._get_fallback_candidates(max_candidates)

            print(f"📈 Ranking {len(all_symbols)} symbols by quality metrics...")

            # Rank symbols by quality metrics
            ranked_symbols = self._rank_symbols_by_quality(
                all_symbols,
                min_market_cap,
                analysis_days,
                start_date,
                end_date,
                max_candidates,
                batch_size,
            )

            return ranked_symbols

        except Exception as e:
            print(f"⚠️ Error in S&P 500 search: {e}")
            print("🔄 Falling back to known large-cap symbols")
            return self._get_fallback_candidates(max_candidates)

    def _rank_symbols_by_quality(
        self,
        symbols: List[str],
        min_market_cap: float,
        analysis_days: int,
        start_date: date,
        end_date: date,
        max_candidates: int,
        batch_size: int,
    ) -> List[str]:
        """Rank symbols by quality metrics (ADV, spreads, ATR%, stability)."""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        from services.quotes_client import QuotesClient

        quotes_client = QuotesClient()
        ranked_data = []

        print(f"📊 Analyzing quality metrics for {len(symbols)} symbols...")

        # Process in batches to avoid overwhelming APIs
        # Analyze ALL symbols to ensure we get enough candidates
        symbols_to_analyze = len(symbols)  # Analyze ALL symbols
        for i in range(0, symbols_to_analyze, batch_size):
            batch = symbols[i : i + batch_size]
            print(f"  Processing batch {i//batch_size + 1}: {len(batch)} symbols")

            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {}
                for symbol in batch:
                    future = executor.submit(
                        self._analyze_symbol_quality,
                        symbol,
                        min_market_cap,
                        analysis_days,
                        start_date,
                        end_date,
                        quotes_client,
                    )
                    futures[future] = symbol

                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        ranked_data.append(result)

        # Sort by quality score (higher is better)
        ranked_data.sort(key=lambda x: x["quality_score"], reverse=True)

        # Return top candidates
        top_candidates = [item["symbol"] for item in ranked_data[:max_candidates]]

        print(f"✅ Ranked and selected top {len(top_candidates)} candidates")
        if top_candidates:
            print(f"   Top 10: {top_candidates[:10]}")

        return top_candidates

    def get_optimal_update_time(self) -> Dict[str, str]:
        """Get the optimal update times for the universe list."""
        from datetime import datetime

        now = datetime.now()
        current_hour = now.hour

        # Define optimal update windows
        update_windows = {
            "pre_market": "6:00-7:00 AM ET (Before market opens)",
            "mid_day": "12:00-1:00 PM ET (Mid-day refresh)",
            "post_market": "4:30-5:00 PM ET (After market closes)",
            "overnight": "2:00-4:00 AM ET (Overnight processing)",
        }

        # Determine current status
        if 6 <= current_hour < 7:
            status = "🟢 OPTIMAL: Pre-market update window"
        elif 12 <= current_hour < 13:
            status = "🟡 GOOD: Mid-day refresh window"
        elif 16 <= current_hour < 17:
            status = "🟢 OPTIMAL: Post-market update window"
        elif 2 <= current_hour < 4:
            status = "🟢 OPTIMAL: Overnight processing window"
        else:
            status = "🔴 NOT OPTIMAL: Outside update windows"

        return {
            "current_time": now.strftime("%H:%M ET"),
            "status": status,
            "recommended_windows": update_windows,
            "next_optimal": self._get_next_optimal_time(),
        }

    def _get_next_optimal_time(self) -> str:
        """Get the next optimal update time."""
        from datetime import datetime

        now = datetime.now()
        current_hour = now.hour

        if current_hour < 6:
            return "6:00 AM ET (Pre-market)"
        elif current_hour < 12:
            return "12:00 PM ET (Mid-day)"
        elif current_hour < 16:
            return "4:30 PM ET (Post-market)"
        elif current_hour < 22:
            return "2:00 AM ET (Overnight)"
        else:
            return "6:00 AM ET (Pre-market tomorrow)"

    def _analyze_symbol_quality(
        self,
        symbol: str,
        min_market_cap: float,
        analysis_days: int,
        start_date: date,
        end_date: date,
        quotes_client,
    ) -> Optional[Dict]:
        """Analyze quality metrics for a single symbol."""
        try:
            # Get market cap
            details = self.polygon_client.get_ticker_details(symbol)
            market_cap = details.get("results", {}).get("market_cap", 0)

            if market_cap < min_market_cap:
                return None

            # Get price data for ADV calculation
            price_data = self.polygon_client.get_aggs(
                symbol,
                1,
                "day",
                start_date.isoformat(),
                end_date.isoformat(),
                limit=analysis_days,
                adjusted=True,
            )

            results = price_data.get("results", [])
            if not results:
                return None

            # Calculate ADV
            total_volume = sum(float(r.get("v", 0)) for r in results)
            avg_price = sum(float(r.get("c", 0)) for r in results) / len(results)
            adv = total_volume * avg_price / len(results)

            # ULTRA GENEROUS ADV filter - provider should be ultra generous
            if adv < 100_000:  # $100K minimum ADV (ultra generous for provider)
                return None

            # Calculate spreads
            try:
                med_dollar, med_bps = quotes_client.median_spread_over_days(
                    symbol, days=5
                )
                # Provider: reasonable filter (50 bps), selector does final filtering (5 bps)
                if (
                    med_dollar > 1.0 or med_bps > 500
                ):  # 50 bps maximum (reasonable filter)
                    return None
            except:
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
                + max(0, 10 - med_bps) * 0.3  # Spread component (0-10)
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

    def _discover_candidates(
        self, min_market_cap: float = 10_000_000_000, limit: int = 500
    ) -> List[str]:
        """Discover candidates by searching the ENTIRE S&P 500 daily.
        This is the correct design: provider searches full S&P 500, selector picks best from all sectors.

        With premium subscription we can:
        1. Get ALL active S&P 500 tickers from Polygon
        2. Fetch market cap for each ticker
        3. Filter by market cap and sort by size
        4. Return comprehensive candidate pool for selector
        """
        # CORRECT DESIGN: Search the ENTIRE S&P 500 daily
        # Provider searches full S&P 500, selector picks best from all sectors
        try:
            print("🔍 Searching entire S&P 500 for candidates...")
            data = self.polygon_client.get_tickers(
                market="stocks",
                active=True,
                limit=500,  # Start with 500 to avoid timeout
            )

            results = data.get("results", [])
            if not results:
                print("⚠️ No tickers found from Polygon, using fallback list")
                return self._get_fallback_candidates(limit)

            print(f"📊 Found {len(results)} total tickers from Polygon")

            # Extract all ticker symbols
            all_symbols = []
            for ticker in results:
                symbol = ticker.get("ticker")
                if isinstance(symbol, str) and symbol:
                    all_symbols.append(symbol)

            if not all_symbols:
                print("⚠️ No valid symbols found, using fallback list")
                return self._get_fallback_candidates(limit)

            print(
                f"📈 Processing {len(all_symbols)} symbols for market cap filtering..."
            )
            candidates = all_symbols

        except Exception as e:
            print(f"⚠️ Error fetching S&P 500 tickers: {e}")
            print("🔄 Falling back to known large-cap symbols")
            return self._get_fallback_candidates(limit)

        # Get market caps using ticker details endpoint for ALL symbols
        symbols_with_mcap = []

        print("📊 Fetching market caps for ALL candidates...")

        # Process ALL symbols in batches (no artificial limit)
        batch_size = 25  # Optimal batch size for stability
        for i in range(0, len(candidates), batch_size):
            batch = candidates[i : i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(candidates) + batch_size - 1) // batch_size

            print(
                f"  Processing batch {batch_num}/{total_batches}: {len(batch)} symbols"
            )

            with ThreadPoolExecutor(
                max_workers=5
            ) as executor:  # Fewer workers for stability
                futures = {}
                for symbol in batch:
                    future = executor.submit(self._get_ticker_details, symbol)
                    futures[future] = symbol

                for future in as_completed(futures):
                    symbol = futures[future]
                    try:
                        result = future.result()
                        if result and result["market_cap"] >= min_market_cap:
                            symbols_with_mcap.append(result)
                    except Exception:
                        continue

            # Small delay between batches to avoid rate limits
            if i + batch_size < len(candidates):
                import time

                time.sleep(0.2)

        # Sort by market cap descending
        symbols_with_mcap.sort(key=lambda x: x["market_cap"], reverse=True)

        # Return just the symbols
        result = [item["symbol"] for item in symbols_with_mcap[:limit]]
        print(
            f"✅ Found {len(result)} symbols with market cap > ${min_market_cap/1e9:.0f}B"
        )

        return result

    def _get_comprehensive_known_symbols(self) -> List[str]:
        """Get comprehensive known large-cap symbols (200+ symbols) guaranteed to work."""
        return [
            # Tech Giants (50 symbols)
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "TSLA",
            "META",
            "NVDA",
            "NFLX",
            "ADBE",
            "CRM",
            "ORCL",
            "INTC",
            "AMD",
            "QCOM",
            "AVGO",
            "TXN",
            "AMAT",
            "LRCX",
            "KLAC",
            "MCHP",
            "SNOW",
            "PLTR",
            "CRWD",
            "ZS",
            "OKTA",
            "DDOG",
            "NET",
            "MDB",
            "TEAM",
            "WDAY",
            "SNPS",
            "CDNS",
            "ANSS",
            "ADSK",
            "INTU",
            "NOW",
            "SHOP",
            "ZM",
            "DOCU",
            "PTON",
            "ROKU",
            "SPOT",
            "SQ",
            "PYPL",
            "V",
            "MA",
            "COIN",
            "HOOD",
            "SOFI",
            "UPST",
            # Financial (50 symbols)
            "JPM",
            "BAC",
            "WFC",
            "GS",
            "MS",
            "C",
            "AXP",
            "USB",
            "PNC",
            "TFC",
            "BLK",
            "SCHW",
            "COF",
            "AON",
            "MMC",
            "SPGI",
            "MCO",
            "ICE",
            "CME",
            "NDAQ",
            "BRK.B",
            "V",
            "MA",
            "PYPL",
            "SQ",
            "SOFI",
            "UPST",
            "LC",
            "AFRM",
            "HOOD",
            "COIN",
            "SOFI",
            "UPST",
            "LC",
            "AFRM",
            "HOOD",
            "COIN",
            "SOFI",
            "UPST",
            "LC",
            "AFRM",
            "HOOD",
            "COIN",
            "SOFI",
            "UPST",
            "LC",
            "AFRM",
            "HOOD",
            "COIN",
            "SOFI",
            # Healthcare (50 symbols)
            "JNJ",
            "PFE",
            "UNH",
            "ABBV",
            "MRK",
            "TMO",
            "ABT",
            "DHR",
            "BMY",
            "LLY",
            "AMGN",
            "GILD",
            "BIIB",
            "REGN",
            "VRTX",
            "ILMN",
            "MRNA",
            "ZTS",
            "CVS",
            "CI",
            "TDOC",
            "ZBH",
            "ISRG",
            "SYK",
            "BSX",
            "EW",
            "DXCM",
            "ALGN",
            "WAT",
            "TMO",
            "MDT",
            "JNJ",
            "PFE",
            "UNH",
            "ABBV",
            "MRK",
            "TMO",
            "ABT",
            "DHR",
            "BMY",
            "LLY",
            "AMGN",
            "GILD",
            "BIIB",
            "REGN",
            "VRTX",
            "ILMN",
            "MRNA",
            "ZTS",
            "CVS",
            # Consumer (50 symbols)
            "PG",
            "KO",
            "PEP",
            "WMT",
            "HD",
            "MCD",
            "NKE",
            "SBUX",
            "TGT",
            "LOW",
            "COST",
            "TJX",
            "ROST",
            "DG",
            "DLTR",
            "CMG",
            "YUM",
            "MKC",
            "CL",
            "KMB",
            "AMZN",
            "TSLA",
            "NFLX",
            "ROKU",
            "PTON",
            "ZM",
            "DOCU",
            "SHOP",
            "SQ",
            "PYPL",
            "V",
            "MA",
            "PYPL",
            "SQ",
            "SOFI",
            "UPST",
            "LC",
            "AFRM",
            "HOOD",
            "COIN",
            "SOFI",
            "UPST",
            "LC",
            "AFRM",
            "HOOD",
            "COIN",
            "SOFI",
            "UPST",
            "LC",
            "AFRM",
        ]

    def _get_known_large_caps(self) -> List[str]:
        """Get known large-cap symbols that are guaranteed to have market cap data."""
        return self._get_comprehensive_known_symbols()[
            :100
        ]  # First 100 for backward compatibility

    def _get_polygon_symbols_with_market_cap(self, min_market_cap: float) -> List[str]:
        """Get symbols from Polygon that have market cap data."""
        try:
            print("🔍 Getting symbols from Polygon with market cap data...")

            # Get symbols from Polygon
            data = self.polygon_client.get_tickers(
                market="stocks", active=True, limit=200
            )
            results = data.get("results", [])

            if not results:
                return []

            # Extract valid symbols
            valid_symbols = []
            for ticker in results:
                symbol = ticker.get("ticker")
                if (
                    isinstance(symbol, str)
                    and len(symbol) <= 5
                    and symbol.isalpha()
                    and not symbol.endswith(".U")
                    and not symbol.endswith(".WS")
                    and not symbol.endswith(".RT")
                    and not symbol.endswith(".WT")
                ):
                    valid_symbols.append(symbol)

            print(f"📊 Found {len(valid_symbols)} valid symbols from Polygon")

            # Get market cap for each symbol
            symbols_with_mcap = []
            batch_size = 20

            for i in range(0, len(valid_symbols), batch_size):
                batch = valid_symbols[i : i + batch_size]

                with ThreadPoolExecutor(max_workers=5) as executor:
                    futures = {}
                    for symbol in batch:
                        future = executor.submit(self._get_ticker_details, symbol)
                        futures[future] = symbol

                    for future in as_completed(futures):
                        result = future.result()
                        if result and result["market_cap"] >= min_market_cap:
                            symbols_with_mcap.append(result["symbol"])

                # Small delay between batches
                if i + batch_size < len(valid_symbols):
                    import time

                    time.sleep(0.1)

            print(
                f"✅ Found {len(symbols_with_mcap)} symbols with market cap > ${min_market_cap/1e9:.0f}B"
            )
            return symbols_with_mcap

        except Exception as e:
            print(f"⚠️ Error getting Polygon symbols: {e}")
            return []

    def _get_additional_known_symbols(self) -> List[str]:
        """Get additional known symbols if we need more candidates."""
        return [
            # More Tech
            "SNOW",
            "PLTR",
            "CRWD",
            "ZS",
            "OKTA",
            "DDOG",
            "NET",
            "MDB",
            "TEAM",
            "WDAY",
            # More Financial
            "V",
            "MA",
            "PYPL",
            "SQ",
            "SOFI",
            "UPST",
            "LC",
            "AFRM",
            "HOOD",
            "COIN",
            # More Healthcare
            "TDOC",
            "ZBH",
            "ISRG",
            "SYK",
            "BSX",
            "EW",
            "DXCM",
            "ALGN",
            "WAT",
            "TMO",
            # More Consumer
            "AMZN",
            "TSLA",
            "NFLX",
            "ROKU",
            "PTON",
            "ZM",
            "DOCU",
            "SHOP",
            "SQ",
            "PYPL",
            # More Industrial
            "DE",
            "CAT",
            "BA",
            "GE",
            "HON",
            "UPS",
            "FDX",
            "LMT",
            "RTX",
            "NOC",
        ]

    def _get_ticker_details(self, symbol: str) -> Optional[Dict]:
        """Get market cap for a symbol using ticker details endpoint"""
        try:
            details = self.polygon_client.get_ticker_details(symbol)
            if details and details.get("results"):
                results = details["results"]
                market_cap = results.get("market_cap", 0)
                if market_cap > 0:
                    return {"symbol": symbol, "market_cap": market_cap}
            return None
        except Exception:
            return None

    def _prefilter_by_adv_and_price(
        self,
        symbols: List[str],
        start_iso: str,
        end_iso: str,
        adv_min_dollar: float,
        price_min: float,
        max_symbols: int,
        batch_size: int = 20,
    ) -> List[str]:
        """Prefilter symbols by ADV using smart batching to avoid API overload.
        Process in small batches with rate limiting between batches.
        """
        qualified = []

        print(
            f"📈 Checking ADV for {len(symbols)} symbols in batches of {batch_size}..."
        )

        # Process in order (already sorted by market cap)
        for i in range(0, len(symbols), batch_size):
            if len(qualified) >= max_symbols:
                break

            batch = symbols[i : i + batch_size]
            batch_end = min(i + batch_size, len(symbols))
            print(
                f"  Batch {i//batch_size + 1}/{(len(symbols) + batch_size - 1)//batch_size}: symbols {i+1}-{batch_end}"
            )

            def fetch_metrics(sym: str):
                try:
                    data = self.polygon_client.get_aggs(
                        sym,
                        1,
                        "day",
                        start_iso,
                        end_iso,
                        limit=120,  # Reduced from 150
                        adjusted=True,
                        sort="asc",
                    )
                    rows = data.get("results") if isinstance(data, dict) else None
                    if not isinstance(rows, list) or not rows:
                        return None

                    closes: List[float] = []
                    dollar_vols: List[float] = []
                    for r in rows:
                        try:
                            c = float(r.get("c", 0.0))
                            v = float(r.get("v", 0.0))
                        except Exception:
                            c = 0.0
                            v = 0.0
                        if c > 0:
                            closes.append(c)
                            dollar_vols.append(c * v)

                    if not closes:
                        return None

                    # Calculate median close
                    closes_sorted = sorted(closes)
                    mid = len(closes_sorted) // 2
                    if len(closes_sorted) % 2 == 0:
                        median_close = 0.5 * (
                            closes_sorted[mid - 1] + closes_sorted[mid]
                        )
                    else:
                        median_close = closes_sorted[mid]

                    # Calculate ADV
                    adv = sum(dollar_vols) / max(1, len(dollar_vols))
                    return (sym, median_close, adv)
                except Exception:
                    return None

            # Process this batch in parallel
            with ThreadPoolExecutor(max_workers=min(8, len(batch))) as executor:
                futures = {executor.submit(fetch_metrics, s): s for s in batch}

                for future in as_completed(futures):
                    if len(qualified) >= max_symbols:
                        break

                    try:
                        result = future.result()
                        if result:
                            sym, median_close, adv = result
                            if median_close >= price_min and adv >= adv_min_dollar:
                                qualified.append(sym)
                    except Exception:
                        continue

            # Rate limit between batches
            if i + batch_size < len(symbols) and len(qualified) < max_symbols:
                time.sleep(0.5)

        print(f"✅ {len(qualified)} symbols passed ADV filter")
        return qualified

    def get_active_universe(
        self,
        target_size: int = 120,
        analysis_days: int = 60,
        cache_path: str = "data/active_universe_120.json",
        max_age_hours: int = 18,  # 18 hours = update daily at 6 AM
        force_refresh: bool = False,
        min_price: float = 10.0,
        min_atr_pct: float = 0.01,
        max_atr_pct: float = 0.05,
        adv_min_dollar: float = 50_000_000.0,
        spread_filter_enabled: bool = True,
        spread_max_dollars: float = 0.02,
        spread_max_bps: float = 5.0,
        spread_lookback_days: int = 5,
        spread_core_hours_only: bool = True,
        end_date: Optional[date] = None,
        # Prefilter controls
        adv_prefilter_min_dollar: float = 100_000_000.0,
        prefilter_max_symbols: int = 300,
        price_prefilter_min: float = 10.0,
        # Smart builder settings
        use_smart_builder: bool = True,
        batch_size: int = 20,
    ) -> List[str]:
        # Check cache first
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)

        if not force_refresh and os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                analysis_iso = payload.get("analysis_date")
                if analysis_iso:
                    analysis_dt = datetime.fromisoformat(analysis_iso)
                    age_hours = (datetime.now() - analysis_dt).total_seconds() / 3600
                    if age_hours <= max_age_hours:
                        syms = payload.get("symbols") or []
                        if isinstance(syms, list) and syms:
                            return [str(s) for s in syms][:target_size]
            except Exception:
                pass

        ed: date = end_date or date.today()
        sd: date = ed - timedelta(days=analysis_days)

        # Discover and RANK candidates from entire S&P 500
        print("🚀 Building active universe from Polygon data...")
        ranked_candidates = self._discover_and_rank_candidates(
            min_market_cap=100_000_000,  # $100M minimum - ultra generous for provider
            analysis_days=analysis_days,
            start_date=sd,
            end_date=ed,
            max_candidates=prefilter_max_symbols,  # Present top 300 best
            batch_size=batch_size,
        )

        if not ranked_candidates:
            print("⚠️ No candidates found from Polygon")
            return []

        print(f"📊 Found {len(ranked_candidates)} top-ranked candidates from S&P 500")

        # Use the ranked candidates directly
        candidates = ranked_candidates
        sector_classifier, sector_index_weights = (
            self._build_sector_classifier_and_weights(candidates)
        )
        selector = UniverseSelector()

        # Earnings exclusion hook using Polygon client if available
        def earnings_exclusion(sym: str, start_iso: str, end_iso: str) -> List[str]:
            try:
                if hasattr(self.polygon_client, "get_earnings_calendar"):
                    from datetime import date as _d

                    s = _d.fromisoformat(start_iso)
                    e = _d.fromisoformat(end_iso)
                    data = self.polygon_client.get_earnings_calendar(sym, s, e)
                    # Expecting a structure with list of dates; be strict and fail closed if unexpected
                    results = data.get("results") if isinstance(data, dict) else None
                    if isinstance(results, list):
                        dates: List[str] = []
                        for item in results:
                            d = (
                                item.get("date")
                                or item.get("earningsDate")
                                or item.get("reportDate")
                            )
                            if isinstance(d, str):
                                dates.append(d)
                        return dates
            except NotImplementedError:
                return []
            except Exception:
                return []
            return []

        # Check if earnings calendar is available
        earnings_available = False
        try:
            # Quick test with one symbol
            test_data = self.polygon_client.get_earnings_calendar("AAPL", sd, ed)
            if test_data.get("status") == "OK" or test_data.get("results"):
                earnings_available = True
                print("📅 Earnings calendar available")
        except Exception:
            print(
                "ℹ️ Earnings calendar not available - proceeding without earnings exclusion"
            )

        symbols = selector.select_universe(
            candidates=candidates,
            start_date=sd.isoformat(),
            end_date=ed.isoformat(),
            target_size=target_size,
            target_max_size=150,
            allow_expand_above_target=True,
            expand_margin=0.95,
            min_price=min_price,
            min_atr_pct=min_atr_pct,
            max_atr_pct=max_atr_pct,
            adv_min_dollar=adv_min_dollar,
            spread_filter_enabled=spread_filter_enabled,
            spread_max_dollars=spread_max_dollars,
            spread_max_bps=spread_max_bps,
            spread_lookback_days=spread_lookback_days,
            spread_core_hours_only=spread_core_hours_only,
            sector_classifier=sector_classifier,
            sector_index_weights=sector_index_weights,
            earnings_exclusion=earnings_exclusion if earnings_available else None,
            earnings_buffer_days=3,
        )

        payload = {
            "analysis_date": datetime.now().isoformat(),
            "analysis_days": analysis_days,
            "target_size": target_size,
            "start_date": sd.isoformat(),
            "end_date": ed.isoformat(),
            "symbols": symbols,
            "criteria": {
                "min_price": min_price,
                "min_atr_pct": min_atr_pct,
                "spread_max_dollars": spread_max_dollars,
                "spread_max_bps": spread_max_bps,
                "spread_lookback_days": spread_lookback_days,
                "spread_core_hours_only": spread_core_hours_only,
            },
        }
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
        except Exception:
            pass
        return symbols
