from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta, UTC
import json
import os

from services.news_client import NewsClient
from services.sentiment import aggregate_symbol_sentiment, score_article


def build_scores(symbols: List[str], lookback_hours: int = 16, per_symbol_limit: int = 25) -> Dict[str, float]:
    client = NewsClient()
    since = (datetime.now(UTC) - timedelta(hours=lookback_hours)).isoformat().replace("+00:00", "Z")
    scores: Dict[str, float] = {}
    for sym in symbols:
        articles = client.fetch_symbol_news(sym, published_gte_utc=since, limit=per_symbol_limit, order="desc")
        scores[sym] = aggregate_symbol_sentiment(articles)
    return scores


def build_priority(symbols: List[str], lookback_hours: int = 16, per_symbol_limit: int = 25) -> List[str]:
    scores = build_scores(symbols, lookback_hours=lookback_hours, per_symbol_limit=per_symbol_limit)
    ranked = sorted(symbols, key=lambda s: scores.get(s, 0.0), reverse=True)
    return ranked


def save_priority(symbols: List[str], filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({"symbols": symbols}, f, indent=2)


def load_priority(filepath: str) -> List[str]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        syms = data.get("symbols")
        return syms if isinstance(syms, list) else []


def save_priority_bundle(filepath: str, symbols: List[str], scores: Dict[str, float]) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({"symbols": symbols, "scores": scores}, f, indent=2)


def load_priority_bundle(filepath: str) -> Tuple[List[str], Dict[str, float]]:
    if not os.path.exists(filepath):
        return [], {}
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        syms = data.get("symbols")
        scores = data.get("scores")
        return (syms if isinstance(syms, list) else [], scores if isinstance(scores, dict) else {})
