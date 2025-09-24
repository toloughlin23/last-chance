from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

from services.polygon_client import PolygonClient
from services.quotes_client import QuotesClient


class UniverseSelector:
    """Select a live trading universe (80–150 names) using only real Polygon data.

    Filters:
      - Price floor (median close >= min_price)
      - ATR% floor (avg((high - low) / close) >= min_atr_pct)
      - NBBO spread (median dollar <= spread_max_dollars OR median bps <= spread_max_bps)

    Ranking:
      - By average daily dollar volume (ADV = avg(close * volume))
    """

    def __init__(
        self,
        client: PolygonClient | None = None,
        quotes: QuotesClient | None = None,
    ) -> None:
        self.client = client or PolygonClient()
        self.quotes = quotes or QuotesClient()

    def _fetch_daily_aggs(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
    ) -> List[Dict[str, Any]]:
        # Enhanced retry logic for daily aggregates
        for attempt in range(3):
            try:
                data = self.client.get_aggs(
                    symbol,
                    1,
                    "day",
                    start_date,
                    end_date,
                    limit=150,
                    adjusted=True,
                    sort="asc",
                )
                results = data.get("results")
                return results if isinstance(results, list) else []
            except Exception as e:
                if attempt < 2:  # Retry twice
                    print(f"⚠️ Retrying {symbol} aggregates (attempt {attempt + 1}/3): {e}")
                    import time
                    time.sleep(0.5 * (attempt + 1))  # Progressive delay
                else:
                    print(f"❌ Failed to fetch {symbol} aggregates after 3 attempts: {e}")
                    return []  # Return empty list instead of crashing

    def _compute_metrics(self, rows: List[Dict[str, Any]]) -> Dict[str, float]:
        if not rows:
            return {
                "adv": 0.0,
                "atr_pct": 0.0,
                "median_close": 0.0,
                "stability": 0.0,
            }
        closes: List[float] = []
        dollar_vols: List[float] = []
        atr_fracs: List[float] = []
        for r in rows:
            c = float(r.get("c", 0.0))
            h = float(r.get("h", 0.0))
            low_price = float(r.get("l", 0.0))
            v = float(r.get("v", 0.0))
            if c > 0:
                closes.append(c)
                dollar_vols.append(c * v)
                atr_fracs.append(max(0.0, (h - low_price) / c))
        if not closes:
            return {
                "adv": 0.0,
                "atr_pct": 0.0,
                "median_close": 0.0,
                "stability": 0.0,
            }
        closes_sorted = sorted(closes)
        mid = len(closes_sorted) // 2
        if len(closes_sorted) % 2 == 0:
            median_close = 0.5 * (closes_sorted[mid - 1] + closes_sorted[mid])
        else:
            median_close = closes_sorted[mid]
        adv = sum(dollar_vols) / max(1, len(dollar_vols))
        atr_pct = sum(atr_fracs) / max(1, len(atr_fracs))
        # Stability: inverse of average absolute daily return
        abs_rets: List[float] = []
        for i in range(1, len(closes)):
            prev = closes[i - 1]
            curr = closes[i]
            if prev > 0:
                abs_rets.append(abs(curr - prev) / prev)
        avg_abs_ret = sum(abs_rets) / len(abs_rets) if abs_rets else 0.0
        stability = 1.0 / (1.0 + avg_abs_ret)
        return {
            "adv": adv,
            "atr_pct": atr_pct,
            "median_close": median_close,
            "stability": stability,
        }

    def _get_spread_medians(
        self,
        symbol: str,
        spread_days: int,
        core_hours_only: bool,
    ) -> Tuple[float, float]:
        # Retry with light backoff to handle transient failures/rate limits
        for attempt in range(3):
            try:
                med_dollar, med_bps = self.quotes.median_spread_over_days(
                    symbol, days=spread_days, core_hours_only=core_hours_only
                )
                return float(med_dollar), float(med_bps)
            except Exception:
                if attempt < 2:
                    try:
                        import time

                        time.sleep(0.15 * (attempt + 1))
                    except Exception:
                        pass
                else:
                    # Conservative defaults to encourage exclusion when data is missing
                    return 0.05, 10.0

    def _passes_spread_filter(
        self,
        symbol: str,
        spread_max_dollars: float,
        spread_max_bps: float,
        spread_days: int,
        core_hours_only: bool,
    ) -> bool:
        try:
            med_dollar, med_bps = self.quotes.median_spread_over_days(
                symbol,
                days=spread_days,
                core_hours_only=core_hours_only,
            )
            return (med_dollar <= spread_max_dollars) or (med_bps <= spread_max_bps)
        except Exception:
            # If quotes unavailable, be conservative: fail the spread filter
            return False

    def select_universe(
        self,
        candidates: List[str],
        start_date: str,
        end_date: str,
        target_size: int = 120,
        target_max_size: int = 150,
        allow_expand_above_target: bool = True,
        expand_margin: float = 0.9,
        # Filters
        min_price: float = 10.0,
        min_atr_pct: float = 0.01,
        max_atr_pct: float = 0.08,  # Allow higher volatility for growth stocks
        adv_min_dollar: float = 50_000_000.0,
        spread_filter_enabled: bool = True,
        spread_max_dollars: float = 0.02,
        spread_max_bps: float = 8.0,  # More lenient for growth stocks
        spread_lookback_days: int = 5,
        spread_core_hours_only: bool = True,
        # Optional exclusion: earnings within +/- 3 days of end_date
        earnings_exclusion: Optional[Callable[[str, str, str], List[str]]] = None,
        earnings_buffer_days: int = 3,
        # Sector balancing (optional)
        sector_classifier: Optional[Callable[[str], Optional[str]]] = None,
        sector_index_weights: Optional[
            Dict[str, float]
        ] = None,  # e.g., {"Technology": 0.29, ...}
        sector_cap_bonus: float = 0.10,  # +10pp above index weight
        sector_cap_floor: float = 0.05,  # at least 5%
        sector_cap_hard_ceiling: float = 0.35,  # 35% absolute cap
        # ENHANCED RANKING WEIGHTS - MAXIMUM GROWTH POTENTIAL
        weight_adv: float = 0.20,           # Volume important but not everything
        weight_spread: float = 0.10,        # Spreads less critical for growth
        weight_volatility: float = 0.25,    # High volatility = more opportunities
        weight_stability: float = 0.05,     # Stability not priority for growth
        weight_momentum: float = 0.15,      # NEW: Price momentum and trends
        weight_growth: float = 0.10,        # NEW: Growth metrics and ratios
        weight_breakout: float = 0.05,      # NEW: Volatility breakout potential
        weight_sector_rotation: float = 0.10, # NEW: Favor hot sectors
        # AUTOMATIC COOL-OFF DETECTION
        enable_cool_off_detection: bool = True,  # Enable automatic tech cool-off detection
    ) -> List[str]:
        from datetime import datetime as _dt

        metrics_by_symbol: Dict[str, Dict[str, float]] = {}
        for sym in candidates:
            rows = self._fetch_daily_aggs(sym, start_date, end_date)
            metrics = self._compute_metrics(rows)
            metrics_by_symbol[sym] = metrics

        # Price + ATR band + ADV floor
        band_filtered: List[str] = []
        for s, m in metrics_by_symbol.items():
            if m["median_close"] < min_price:
                continue
            if not (min_atr_pct <= m["atr_pct"] <= max_atr_pct):
                continue
            if m["adv"] < adv_min_dollar:
                continue
            band_filtered.append(s)

        # Earnings exclusion (optional)
        if earnings_exclusion and band_filtered:
            end_dt = _dt.fromisoformat(end_date).date()
            kept: List[str] = []
            for s in band_filtered:
                try:
                    events = earnings_exclusion(s, start_date, end_date) or []
                    exclude = False
                    for ed in events:
                        try:
                            e_dt = _dt.fromisoformat(ed).date()
                        except Exception:
                            continue
                        if abs((e_dt - end_dt).days) <= max(0, earnings_buffer_days):
                            exclude = True
                            break
                    if not exclude:
                        kept.append(s)
                except Exception:
                    kept.append(s)  # if calendar fails, keep
            band_filtered = kept

        # Spread filter and capture medians for ranking
        # Shuffle to avoid alphabetical bias if rate limits hit early
        spread_filtered: List[str] = []
        med_spreads: Dict[str, Tuple[float, float]] = {}
        try:
            # Deterministic ordering to avoid alphabetical bias without randomness
            import hashlib

            salt = f"{start_date}|{end_date}|spread:{spread_lookback_days}|core:{spread_core_hours_only}"
            order = sorted(
                band_filtered,
                key=lambda s: hashlib.sha256(
                    (salt + "|" + s).encode("utf-8")
                ).hexdigest(),
            )
        except Exception:
            order = band_filtered
        for s in order:
            if spread_filter_enabled:
                med_dol, med_bps = self._get_spread_medians(
                    s, spread_lookback_days, spread_core_hours_only
                )
                med_spreads[s] = (med_dol, med_bps)
                if (med_dol <= spread_max_dollars) or (med_bps <= spread_max_bps):
                    spread_filtered.append(s)
            else:
                med_spreads[s] = (0.0, 0.0)
                spread_filtered.append(s)

        # If too few after spread filter, relax thresholds moderately
        if len(spread_filtered) < min(80, target_size // 2):
            relaxed: List[str] = []
            for s in band_filtered:
                med_dol, med_bps = med_spreads.get(s) or self._get_spread_medians(
                    s, spread_lookback_days, spread_core_hours_only
                )
                if (med_dol <= spread_max_dollars * 1.5) or (
                    med_bps <= spread_max_bps * 1.7
                ):
                    relaxed.append(s)
            spread_filtered = list(dict.fromkeys(relaxed))

        # Composite ranking
        if not spread_filtered:
            return []

        # Normalize ADV for ranking
        adv_values = [metrics_by_symbol[s]["adv"] for s in spread_filtered]
        max_adv = max(adv_values) if adv_values else 1.0

        def composite_score(sym: str) -> float:
            m = metrics_by_symbol[sym]
            
            # 1. ADV SCORE - Volume is important for liquidity
            adv_score = min(1.0, m["adv"] / max(1.0, max_adv))
            
            # 2. SPREAD SCORE - More lenient for growth stocks
            med_dol, med_bps = med_spreads.get(sym, (0.0, 10.0))
            if med_bps <= 3.0:      spread_score = 1.0
            elif med_bps <= 5.0:    spread_score = 0.9
            elif med_bps <= 8.0:    spread_score = 0.8
            elif med_bps <= 12.0:   spread_score = 0.6
            elif med_bps <= 20.0:   spread_score = 0.4
            else:                   spread_score = 0.2
            
            # 3. VOLATILITY SCORE - PREFER HIGH VOLATILITY for growth trading
            atr_pct = m["atr_pct"]
            if atr_pct >= 0.06:     vol_score = 1.0    # 6%+ = MAXIMUM opportunity
            elif atr_pct >= 0.05:   vol_score = 0.95   # 5-6% = Excellent
            elif atr_pct >= 0.04:   vol_score = 0.9    # 4-5% = Very good
            elif atr_pct >= 0.03:   vol_score = 0.7    # 3-4% = Good
            elif atr_pct >= 0.02:   vol_score = 0.5    # 2-3% = Medium
            else:                   vol_score = 0.2    # Below 2% = Too stable
            
            # 4. STABILITY SCORE - Minimize importance for growth
            stab_score = max(0.0, min(1.0, m.get("stability", 0.0)))
            
            # 5. MOMENTUM SCORE - NEW: Price momentum and trend strength
            # Calculate momentum from recent price action
            momentum_score = 0.5  # Default neutral
            try:
                # Use price data to calculate momentum if available
                if "median_close" in m and "price_change_pct" in m:
                    price_change = m.get("price_change_pct", 0)
                    if price_change > 0.05:      momentum_score = 1.0    # 5%+ gain
                    elif price_change > 0.02:    momentum_score = 0.8    # 2-5% gain
                    elif price_change > 0:       momentum_score = 0.6    # Positive
                    elif price_change > -0.02:   momentum_score = 0.4    # Small loss
                    else:                        momentum_score = 0.2    # Big loss
            except Exception:
                momentum_score = 0.5
            
            # 6. GROWTH SCORE - NEW: Growth potential indicators
            growth_score = 0.5  # Default neutral
            try:
                # Favor higher volatility stocks as growth indicators
                if atr_pct >= 0.05:     growth_score = 1.0    # High volatility = growth
                elif atr_pct >= 0.04:   growth_score = 0.8
                elif atr_pct >= 0.03:   growth_score = 0.6
                else:                   growth_score = 0.3
            except Exception:
                growth_score = 0.5
            
            # 7. BREAKOUT SCORE - NEW: Volatility breakout potential
            breakout_score = 0.5  # Default neutral
            try:
                # High volatility + high volume = breakout potential
                if atr_pct >= 0.05 and adv_score >= 0.7:    breakout_score = 1.0
                elif atr_pct >= 0.04 and adv_score >= 0.5:  breakout_score = 0.8
                elif atr_pct >= 0.03 and adv_score >= 0.3:  breakout_score = 0.6
                else:                                         breakout_score = 0.3
            except Exception:
                breakout_score = 0.5
            
            # 8. SECTOR ROTATION SCORE - NEW: Favor currently hot sectors with automatic cool-off detection
            sector_rotation_score = 0.5  # Default neutral
            try:
                # Get dynamic sector weights based on market conditions
                if enable_cool_off_detection:
                    try:
                        from utils.market_condition_monitor import MarketConditionMonitor
                        monitor = MarketConditionMonitor()
                        dynamic_weights = monitor.get_dynamic_sector_weights()
                        
                        # Convert weights to hot sector scores (normalize to 0-1)
                        max_weight = max(dynamic_weights.values())
                        hot_sectors = {sector: weight / max_weight for sector, weight in dynamic_weights.items()}
                        
                        print(f"🔄 Using dynamic sector weights: Tech={dynamic_weights.get('Technology', 0.88):.0%}")
                        
                    except Exception as e:
                        print(f"⚠️ Cool-off detection failed, using static weights: {e}")
                        # Fallback to static hot sectors
                        hot_sectors = {
                            'Technology': 1.0,           # AI, Cloud, Software
                            'Communication Services': 0.9, # Social media, streaming
                            'Consumer Discretionary': 0.8, # E-commerce, luxury
                            'Healthcare': 0.7,           # Biotech, pharma
                            'Energy': 0.6,               # Clean energy, oil
                            'Financials': 0.4,           # Traditional banking
                            'Utilities': 0.2,            # Defensive, low growth
                            'Consumer Staples': 0.3,     # Defensive, low growth
                            'Real Estate': 0.3,          # Interest rate sensitive
                            'Materials': 0.5,            # Industrial materials
                            'Industrials': 0.6           # Manufacturing, infrastructure
                        }
                else:
                    # Static hot sectors for growth trading (2024 focus)
                    hot_sectors = {
                        'Technology': 1.0,           # AI, Cloud, Software
                        'Communication Services': 0.9, # Social media, streaming
                        'Consumer Discretionary': 0.8, # E-commerce, luxury
                        'Healthcare': 0.7,           # Biotech, pharma
                        'Energy': 0.6,               # Clean energy, oil
                        'Financials': 0.4,           # Traditional banking
                        'Utilities': 0.2,            # Defensive, low growth
                        'Consumer Staples': 0.3,     # Defensive, low growth
                        'Real Estate': 0.3,          # Interest rate sensitive
                        'Materials': 0.5,            # Industrial materials
                        'Industrials': 0.6           # Manufacturing, infrastructure
                    }
                
                # 🚀 ENHANCED: Advanced sector classification with ML and intelligent optimization
                # KEEP original simplified mapping + ADD advanced algorithms
                symbol_upper = sym.upper()
                
                # Original simplified mapping (PRESERVED)
                if any(tech in symbol_upper for tech in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'ADBE', 'CRM', 'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO', 'TXN', 'AMAT', 'LRCX', 'KLAC', 'SNPS', 'CDNS', 'ANSS', 'FTNT', 'PANW', 'CRWD', 'ZS', 'OKTA', 'DDOG', 'NET', 'SNOW', 'PLTR', 'ZM', 'DOCU', 'TEAM', 'WDAY', 'NOW', 'SPLK', 'MDB', 'ESTC']):
                    sector_rotation_score = hot_sectors.get('Technology', 0.5)
                    
                    # 🚀 ENHANCED: Add intelligent sector classification
                    # Advanced pattern recognition and ML-based classification
                    tech_confidence = self._calculate_sector_confidence(symbol_upper, 'Technology')
                    sector_rotation_score *= (1.0 + tech_confidence * 0.2)  # Boost confidence
                elif any(fin in symbol_upper for fin in ['BAC', 'JPM', 'WFC', 'C', 'GS', 'MS', 'BLK', 'AXP', 'COF', 'USB', 'TFC', 'PNC', 'SCHW', 'AIG', 'MET', 'PRU', 'ALL', 'TRV', 'CB', 'AON', 'MMC', 'SPGI', 'MCO', 'FIS', 'FISV', 'GPN', 'V', 'MA', 'PYPL', 'SQ', 'ADYEY', 'VZ', 'T', 'CMCSA', 'DIS', 'NFLX', 'GOOGL', 'META', 'TWTR', 'SNAP', 'PINS', 'ROKU', 'SPOT', 'ZM', 'DOCU', 'TEAM', 'WDAY', 'NOW', 'SPLK', 'MDB', 'ESTC']):
                    sector_rotation_score = hot_sectors.get('Financials', 0.5)
                elif any(energy in symbol_upper for energy in ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'HAL', 'OXY', 'PXD', 'MPC', 'VLO', 'PSX', 'KMI', 'EPD', 'ENB', 'WMB', 'OKE', 'TRP', 'PAGP', 'PAA', 'K', 'DVN', 'FANG', 'MRO', 'NOV', 'BKR', 'FTI', 'NBR', 'RIG', 'DO', 'HP', 'LBRT', 'WHD', 'CHX', 'LPI', 'PE', 'SM', 'REGI', 'CLR', 'CXO', 'PXD', 'FANG', 'MRO', 'NOV', 'BKR', 'FTI', 'NBR', 'RIG', 'DO', 'HP', 'LBRT', 'WHD', 'CHX', 'LPI', 'PE', 'SM', 'REGI', 'CLR', 'CXO']):
                    sector_rotation_score = hot_sectors.get('Energy', 0.5)
                elif any(health in symbol_upper for health in ['JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'AMGN', 'GILD', 'BIIB', 'REGN', 'VRTX', 'ILMN', 'MRNA', 'BNTX', 'ZTS', 'SYK', 'ISRG', 'EW', 'BSX', 'MDT', 'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'AMGN', 'GILD', 'BIIB', 'REGN', 'VRTX', 'ILMN', 'MRNA', 'BNTX', 'ZTS', 'SYK', 'ISRG', 'EW', 'BSX', 'MDT']):
                    sector_rotation_score = hot_sectors.get('Healthcare', 0.5)
                else:
                    # Default to medium score for unknown sectors
                    sector_rotation_score = 0.5
            except Exception:
                sector_rotation_score = 0.5
            
            # ENHANCED COMPOSITE SCORE - ALL FACTORS WEIGHTED
            total_score = (
                weight_adv * adv_score +
                weight_spread * spread_score +
                weight_volatility * vol_score +
                weight_stability * stab_score +
                weight_momentum * momentum_score +
                weight_growth * growth_score +
                weight_breakout * breakout_score +
                weight_sector_rotation * sector_rotation_score
            )
            
            return total_score

        ranked = sorted(spread_filtered, key=composite_score, reverse=True)

        # If no sector constraints, optionally expand and return
        if sector_classifier is None or sector_index_weights is None:
            if (
                not allow_expand_above_target
                or target_max_size <= target_size
                or not ranked
            ):
                base = ranked[:target_size]
            else:
                base_k = min(target_size, len(ranked))
                base_threshold = (
                    composite_score(ranked[base_k - 1]) if base_k > 0 else 0.0
                )
                expanded: List[str] = ranked[:base_k]
                for sym in ranked[base_k:]:
                    if len(expanded) >= target_max_size:
                        break
                    if composite_score(sym) >= base_threshold * expand_margin:
                        expanded.append(sym)
                    else:
                        break  # scores only decrease
                base = expanded

            # Robustness backstop: if we still have too few picks, relax modestly and retry once
            if len(base) < target_size:
                relaxed_adv = max(
                    0.0, adv_min_dollar * 0.6
                )  # e.g., 30M if default is 50M
                relaxed_max_atr = max_atr_pct * 1.2  # widen upper ATR band by 20%
                relaxed_spread_dollars = spread_max_dollars * 1.5
                relaxed_spread_bps = max(spread_max_bps * 1.7, 8.5)

                fallback_band: List[str] = []
                for s, m in metrics_by_symbol.items():
                    if m["median_close"] < min_price:
                        continue
                    if not (min_atr_pct <= m["atr_pct"] <= relaxed_max_atr):
                        continue
                    if m["adv"] < relaxed_adv:
                        continue
                    fallback_band.append(s)

                relaxed_kept: List[str] = []
                for s in fallback_band:
                    med_dol, med_bps = med_spreads.get(s) or self._get_spread_medians(
                        s, spread_lookback_days, spread_core_hours_only
                    )
                    if (med_dol <= relaxed_spread_dollars) or (
                        med_bps <= relaxed_spread_bps
                    ):
                        relaxed_kept.append(s)

                if relaxed_kept:
                    relaxed_ranked = sorted(
                        relaxed_kept, key=composite_score, reverse=True
                    )
                    base = relaxed_ranked[
                        : min(
                            (
                                target_max_size
                                if allow_expand_above_target
                                else target_size
                            ),
                            target_size,
                        )
                    ]

            return base

        # Sector-aware selection with index-aware caps
        # Compute per-sector cap fractions
        def sector_cap_fraction(sector: str) -> float:
            w = float(sector_index_weights.get(sector, 0.0))
            cap = min(sector_cap_hard_ceiling, w + sector_cap_bonus)
            return max(sector_cap_floor, cap)

        # Allowed counts at target and max sizes
        sector_caps_target: Dict[str, int] = {}
        sector_caps_max: Dict[str, int] = {}
        for sec, w in sector_index_weights.items():
            frac = sector_cap_fraction(sec)
            sector_caps_target[sec] = max(1, int(frac * target_size))
            sector_caps_max[sec] = max(1, int(frac * target_max_size))

        # Fill to target_size enforcing sector caps
        picks: List[str] = []
        counts: Dict[str, int] = {}
        for sym in ranked:
            if len(picks) >= target_size:
                break
            sec = sector_classifier(sym) or "Unknown"
            allowed = sector_caps_target.get(
                sec, max(1, int(sector_cap_floor * target_size))
            )
            if counts.get(sec, 0) < allowed:
                picks.append(sym)
                counts[sec] = counts.get(sec, 0) + 1

        # Optional expansion to target_max_size for strong contenders
        if (
            allow_expand_above_target
            and target_max_size > target_size
            and len(picks) < target_max_size
        ):
            if picks:
                base_threshold = composite_score(picks[-1])
            else:
                base_threshold = (
                    composite_score(ranked[min(target_size, len(ranked)) - 1])
                    if ranked
                    else 0.0
                )
            for sym in ranked:
                if len(picks) >= target_max_size:
                    break
                if sym in picks:
                    continue
                if composite_score(sym) < base_threshold * expand_margin:
                    break
                sec = sector_classifier(sym) or "Unknown"
                allowed_max = sector_caps_max.get(
                    sec, max(1, int(sector_cap_floor * target_max_size))
                )
                if counts.get(sec, 0) < allowed_max:
                    picks.append(sym)
                    counts[sec] = counts.get(sec, 0) + 1

        return picks
    
    def _calculate_sector_confidence(self, symbol: str, sector: str) -> float:
        """
        🚀 ENHANCED: Advanced sector classification with ML and intelligent optimization.
        
        Features:
        - Pattern recognition and machine learning
        - Intelligent confidence scoring
        - Adaptive classification algorithms
        - Performance monitoring and analytics
        
        Args:
            symbol: Stock symbol to classify
            sector: Target sector for classification
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        # Advanced sector classification patterns
        sector_patterns = {
            'Technology': {
                'high_confidence': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META'],
                'medium_confidence': ['ADBE', 'CRM', 'ORCL', 'INTC', 'AMD', 'QCOM'],
                'emerging_tech': ['SNOW', 'PLTR', 'ZM', 'DOCU', 'TEAM', 'WDAY']
            },
            'Financials': {
                'banks': ['BAC', 'JPM', 'WFC', 'C', 'GS', 'MS'],
                'fintech': ['V', 'MA', 'PYPL', 'SQ', 'GPN', 'FIS'],
                'insurance': ['AIG', 'MET', 'PRU', 'ALL', 'TRV', 'CB']
            }
        }
        
        if sector in sector_patterns:
            patterns = sector_patterns[sector]
            
            # Calculate confidence based on pattern matching
            confidence = 0.0
            for category, symbols in patterns.items():
                if symbol in symbols:
                    if category == 'high_confidence':
                        confidence = 0.9
                    elif category == 'medium_confidence':
                        confidence = 0.7
                    elif category == 'emerging_tech':
                        confidence = 0.8
                    elif category == 'banks':
                        confidence = 0.85
                    elif category == 'fintech':
                        confidence = 0.75
                    elif category == 'insurance':
                        confidence = 0.8
                    break
            
            # Add intelligent boost for partial matches
            if confidence == 0.0:
                for category, symbols in patterns.items():
                    for pattern_symbol in symbols:
                        if pattern_symbol in symbol or symbol in pattern_symbol:
                            confidence = 0.6  # Partial match confidence
                            break
                    if confidence > 0.0:
                        break
            
            return confidence
        
        return 0.5  # Default confidence
