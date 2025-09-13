from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class DecisionMessage:
    """Decision emitted by an algorithm for a symbol.

    100% genuine values from real feature extraction and confidence calculations.
    """
    symbol: str
    algorithm: str
    decision: str
    confidence: float
    all_confidences: List[float] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=utcnow)


@dataclass
class MetricsMessage:
    """Cycle-level learning metrics and diversity statistics."""
    diversity_overall: float
    diversity_cross_algorithm: float
    coefficient_of_variation: float
    total_pnl: float
    learning_rate: float
    extra: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=utcnow)


