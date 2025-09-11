from dataclasses import dataclass
from typing import List, Dict, Any
import math


@dataclass
class SentimentData:
    overall_sentiment: float
    confidence_level: float
    market_impact_estimate: float
    news_volume: float


@dataclass
class MarketData:
    price_momentum: float
    volatility: float
    volume_ratio: float
    price: float = 0.0
    volume: float = 0.0


@dataclass
class EnrichedData:
    sentiment_analysis: SentimentData
    market_data: MarketData
    data_quality_score: float


def _safe_div(n: float, d: float, default: float = 0.0) -> float:
    return n / d if d != 0 else default


def build_enriched_from_aggs(aggs: Dict[str, Any]) -> EnrichedData:
    """Derive an EnrichedData snapshot from Polygon aggs response.

    Uses only real fields from the response. No randomness or mocks.
    """
    results: List[Dict[str, Any]] = aggs.get("results", []) or []
    if not results:
        # Conservative minimal valid enriched data
        sentiment = 0.0
        conf = 0.5
        impact = 0.0
        news_vol = 0.0
        price_mom = 0.0
        vol = 0.02
        vol_ratio = 1.0
        dq = 0.6
        return EnrichedData(
            sentiment_analysis=SentimentData(sentiment, conf, impact, news_vol),
            market_data=MarketData(price_mom, vol, vol_ratio),
            data_quality_score=dq,
        )

    # Use first and last bars to compute changes
    first = results[0]
    last = results[-1]

    # Close prices - handle both list and single value formats
    c_first_raw = first.get("c", first.get("o", 0.0))
    c_last_raw = last.get("c", last.get("o", 0.0))
    
    # Extract first element if it's a list, otherwise use as-is
    c_first = float(c_first_raw[0] if isinstance(c_first_raw, list) and c_first_raw else c_first_raw)
    c_last = float(c_last_raw[0] if isinstance(c_last_raw, list) and c_last_raw else c_last_raw)

    # Price momentum (relative change)
    price_momentum = _safe_div(c_last - c_first, c_first, 0.0)

    # Intraperiod volatility proxy: avg range / price
    ranges = []
    volumes = []
    for bar in results:
        h = float(bar.get("h", 0.0))
        l = float(bar.get("l", 0.0))
        
        # Handle price extraction for both list and single value formats
        p_raw = bar.get("c", bar.get("o", 0.0))
        p = float(p_raw[0] if isinstance(p_raw, list) and p_raw else p_raw)
        
        v = float(bar.get("v", 0.0))
        if p > 0:
            ranges.append(_safe_div(h - l, p, 0.0))
        volumes.append(v)

    avg_range = sum(ranges) / len(ranges) if ranges else 0.0
    avg_volume = sum(volumes) / len(volumes) if volumes else 0.0

    # Volatility scaled
    volatility = max(0.0, avg_range)

    # Volume ratio relative to a nominal baseline
    volume_ratio = _safe_div(avg_volume, 15000.0, 1.0)

    # Sentiment proxy from price change (bounded)
    raw_sentiment = math.tanh(price_momentum * 3.0)

    # Confidence from volume stability (more volume -> more confidence)
    confidence = max(0.2, min(0.95, 0.4 + min(0.5, avg_volume / 500000.0)))

    # Market impact estimate from average range
    market_impact = max(0.0, min(1.0, avg_range * 10))

    # Use bar count as "news volume" stand-in (data availability proxy)
    news_volume = float(len(results))

    # Data quality: mix of bar count and presence of key fields
    key_ok = all(k in first for k in ("o", "h", "l", "c", "v"))
    dq = max(0.5, min(1.0, 0.5 + 0.02 * len(results) + (0.1 if key_ok else 0.0)))

    # Price/volume from last bar for completeness
    # Handle last price extraction for both list and single value formats
    last_price_raw = last.get("c", last.get("o", 0.0))
    last_price = float(last_price_raw[0] if isinstance(last_price_raw, list) and last_price_raw else last_price_raw)
    last_volume = float(last.get("v", 0.0))

    return EnrichedData(
        sentiment_analysis=SentimentData(
            overall_sentiment=raw_sentiment,
            confidence_level=confidence,
            market_impact_estimate=market_impact,
            news_volume=news_volume,
        ),
        market_data=MarketData(
            price_momentum=price_momentum,
            volatility=volatility,
            volume_ratio=volume_ratio,
            price=last_price,
            volume=last_volume,
        ),
        data_quality_score=dq,
    )

