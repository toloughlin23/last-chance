from typing import Dict, Any, List
import math


def score_article(article: Dict[str, Any]) -> float:
    """Score a single Polygon news article in [-1, 1].
    Deterministic: combines title length, presence of neg/pos cues, and impact signals.
    """
    title = (article.get("title") or "").lower()
    description = (article.get("description") or "").lower()
    amp_score = 0.0

    # Basic positive/negative cues
    positives = ["beat", "surge", "rally", "upgrade", "record", "growth", "raise guidance"]
    negatives = ["miss", "fall", "drop", "downgrade", "cut guidance", "lawsuit", "probe"]

    pos_hits = sum(1 for w in positives if w in title or w in description)
    neg_hits = sum(1 for w in negatives if w in title or w in description)

    base = pos_hits - neg_hits

    # Title length moderation (shorter titles get less weight)
    length = max(10, min(160, len(title)))
    length_factor = (length - 10) / 150.0  # 0..1

    # Publisher weighting (if present)
    publisher = (article.get("publisher") or {}).get("name") or ""
    trusted_publishers = ["Bloomberg", "Reuters", "The Wall Street Journal", "Financial Times"]
    trust = 0.1 if any(tp.lower() in publisher.lower() for tp in trusted_publishers) else 0.0

    # Impact heuristic: mentions of earnings, guidance, SEC, investigation
    impact_terms = ["earnings", "guidance", "sec", "investigation", "merger", "acquisition"]
    impact_hits = sum(1 for w in impact_terms if w in title or w in description)
    impact = min(0.2, 0.05 * impact_hits)

    score = (base * 0.5 + impact) * (0.4 + 0.6 * length_factor) + trust
    # Squash into [-1, 1]
    return max(-1.0, min(1.0, score))


def aggregate_symbol_sentiment(articles: List[Dict[str, Any]]) -> float:
    """Aggregate articles into a single symbol score in [-1, 1]."""
    if not articles:
        return 0.0
    scores = [score_article(a) for a in articles]
    avg = sum(scores) / len(scores)
    # Confidence by article count (sqrt law)
    conf = min(1.0, math.sqrt(len(scores)) / 5.0)  # ~1.0 at 25 articles
    return max(-1.0, min(1.0, avg * (0.5 + 0.5 * conf)))

