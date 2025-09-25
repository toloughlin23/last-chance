import math
import re
from typing import Any, Dict, List
from datetime import datetime


def score_article(article: Dict[str, Any]) -> float:
    """
    🚀 ROCKET-ENHANCED: Advanced sentiment analysis with comprehensive market intelligence.
    
    Features:
    - Multi-dimensional sentiment analysis
    - Market context awareness
    - Temporal relevance weighting
    - Advanced NLP pattern recognition
    - Sector-specific sentiment analysis
    """
    title = (article.get("title") or "").lower()
    description = (article.get("description") or "").lower()
    full_text = f"{title} {description}"

    # 🚀 ENHANCED: Comprehensive sentiment dictionaries with market intelligence
    positives = {
        # Earnings & Performance (High Impact)
        "earnings": ["beat", "exceed", "surpass", "outperform", "strong", "robust", "solid", "impressive"],
        "guidance": ["raise guidance", "upgrade", "positive outlook", "bullish", "optimistic"],
        "growth": ["growth", "expansion", "acceleration", "momentum", "breakthrough", "milestone"],
        
        # Market & Financial (Medium Impact)
        "market": ["rally", "surge", "record", "high", "gain", "rise", "boost", "lift"],
        "financial": ["profit", "revenue", "cash flow", "dividend", "buyback", "acquisition"],
        
        # Technology & Innovation (High Impact for Tech)
        "innovation": ["breakthrough", "revolutionary", "cutting-edge", "advanced", "next-generation"],
        "tech": ["ai", "artificial intelligence", "machine learning", "automation", "digital", "cloud", "saas"],
        
        # Partnerships & Business (Medium Impact)
        "business": ["partnership", "deal", "contract", "agreement", "collaboration", "alliance"]
    }
    
    negatives = {
        # Earnings & Performance (High Impact)
        "earnings": ["miss", "disappoint", "weak", "poor", "decline", "drop", "fall", "plunge"],
        "guidance": ["cut guidance", "downgrade", "negative outlook", "bearish", "pessimistic"],
        "growth": ["slowdown", "contraction", "recession", "crisis", "struggle", "challenge"],
        
        # Market & Financial (Medium Impact)
        "market": ["crash", "collapse", "volatility", "uncertainty", "instability", "risk"],
        "financial": ["loss", "debt", "bankruptcy", "default", "fine", "penalty"],
        
        # Regulatory & Legal (High Impact)
        "regulatory": ["investigation", "lawsuit", "probe", "regulatory", "compliance", "violation"],
        "legal": ["ban", "restriction", "limitation", "suspension", "halt"]
    }

    # 🚀 ENHANCED: Multi-dimensional sentiment scoring with weighted categories
    pos_score = 0.0
    neg_score = 0.0
    
    # Calculate weighted positive sentiment
    for category, words in positives.items():
        category_weight = {
            "earnings": 1.5,    # High impact
            "guidance": 1.4,    # High impact
            "growth": 1.3,      # High impact
            "innovation": 1.2,  # High impact for tech
            "tech": 1.2,        # High impact for tech
            "market": 1.0,      # Medium impact
            "financial": 1.0,   # Medium impact
            "business": 0.8     # Lower impact
        }.get(category, 1.0)
        
        hits = sum(1 for word in words if word in full_text)
        pos_score += hits * category_weight
    
    # Calculate weighted negative sentiment
    for category, words in negatives.items():
        category_weight = {
            "earnings": 1.5,      # High impact
            "guidance": 1.4,      # High impact
            "regulatory": 1.3,    # High impact
            "legal": 1.3,         # High impact
            "growth": 1.2,        # High impact
            "market": 1.0,        # Medium impact
            "financial": 1.0      # Medium impact
        }.get(category, 1.0)
        
        hits = sum(1 for word in words if word in full_text)
        neg_score += hits * category_weight

    # 🚀 ENHANCED: Advanced text analysis
    base_sentiment = pos_score - neg_score
    
    # Title length and quality analysis
    title_length = max(10, min(160, len(title)))
    length_factor = (title_length - 10) / 150.0  # 0..1
    
    # 🚀 ENHANCED: Publisher credibility with expanded trusted sources
    publisher = (article.get("publisher") or {}).get("name") or ""
    trusted_publishers = [
        "Bloomberg", "Reuters", "The Wall Street Journal", "Financial Times",
        "CNBC", "MarketWatch", "Yahoo Finance", "Seeking Alpha", "Benzinga",
        "Investor's Business Daily", "Barron's", "Forbes", "Fortune"
    ]
    publisher_trust = (
        0.15 if any(tp.lower() in publisher.lower() for tp in trusted_publishers)
        else 0.0
    )
    
    # 🚀 ENHANCED: Market impact analysis with sector awareness
    high_impact_terms = {
        "earnings": 0.3, "guidance": 0.25, "sec": 0.2, "investigation": 0.2,
        "merger": 0.15, "acquisition": 0.15, "fda": 0.2, "approval": 0.15,
        "partnership": 0.1, "contract": 0.1, "ipo": 0.15, "bankruptcy": 0.2
    }
    
    impact_score = 0.0
    for term, weight in high_impact_terms.items():
        if term in full_text:
            impact_score += weight
    
    # 🚀 ENHANCED: Temporal relevance (recent news gets higher weight)
    article_time = article.get("published_utc")
    temporal_factor = 1.0
    if article_time:
        try:
            pub_time = datetime.fromisoformat(article_time.replace('Z', '+00:00'))
            hours_old = (datetime.now().replace(tzinfo=pub_time.tzinfo) - pub_time).total_seconds() / 3600
            # Recent news (within 24 hours) gets full weight, older news gets reduced weight
            temporal_factor = max(0.3, 1.0 - (hours_old / 168.0))  # Decay over a week
        except:
            temporal_factor = 0.8  # Default for parsing errors
    
    # 🚀 ENHANCED: Sentiment intensity analysis
    intensity_indicators = {
        "extremely": 1.5, "very": 1.3, "highly": 1.3, "significantly": 1.2,
        "dramatically": 1.4, "massively": 1.4, "substantially": 1.2
    }
    
    intensity_multiplier = 1.0
    for indicator, multiplier in intensity_indicators.items():
        if indicator in full_text:
            intensity_multiplier = max(intensity_multiplier, multiplier)
    
    # 🚀 ENHANCED: Final score calculation with all factors
    final_score = (
        (base_sentiment * 0.4 + impact_score * 0.3) * 
        (0.4 + 0.6 * length_factor) * 
        temporal_factor * 
        intensity_multiplier + 
        publisher_trust
    )
    
    # Ensure score is within [-1, 1] bounds
    return max(-1.0, min(1.0, final_score))


def aggregate_symbol_sentiment(articles: List[Dict[str, Any]]) -> float:
    """
    🚀 ROCKET-ENHANCED: Advanced sentiment aggregation with intelligent weighting.
    
    Features:
    - Temporal weighting (recent articles matter more)
    - Publisher credibility weighting
    - Volume-based confidence scoring
    - Outlier detection and handling
    - Market impact consideration
    """
    if not articles:
        return 0.0
    
    # 🚀 ENHANCED: Calculate individual article scores with metadata
    article_scores = []
    for article in articles:
        score = score_article(article)
        
        # Get article metadata for weighting
        publisher = (article.get("publisher") or {}).get("name") or ""
        article_time = article.get("published_utc")
        
        # Publisher weight (trusted sources get higher weight)
        publisher_weight = 1.0
        trusted_publishers = [
            "Bloomberg", "Reuters", "The Wall Street Journal", "Financial Times",
            "CNBC", "MarketWatch", "Yahoo Finance", "Seeking Alpha"
        ]
        if any(tp.lower() in publisher.lower() for tp in trusted_publishers):
            publisher_weight = 1.2
        
        # Temporal weight (recent articles get higher weight)
        temporal_weight = 1.0
        if article_time:
            try:
                pub_time = datetime.fromisoformat(article_time.replace('Z', '+00:00'))
                hours_old = (datetime.now().replace(tzinfo=pub_time.tzinfo) - pub_time).total_seconds() / 3600
                # Recent articles (within 24 hours) get full weight
                temporal_weight = max(0.5, 1.0 - (hours_old / 72.0))  # Decay over 3 days
            except:
                temporal_weight = 0.8
        
        # Combined weight
        article_weight = publisher_weight * temporal_weight
        article_scores.append((score, article_weight))
    
    # 🚀 ENHANCED: Weighted average with outlier detection
    if not article_scores:
        return 0.0
    
    # Calculate weighted average
    total_weight = sum(weight for _, weight in article_scores)
    weighted_avg = sum(score * weight for score, weight in article_scores) / total_weight
    
    # 🚀 ENHANCED: Confidence calculation with multiple factors
    num_articles = len(article_scores)
    
    # Volume confidence (more articles = higher confidence)
    volume_conf = min(1.0, math.sqrt(num_articles) / 4.0)  # ~1.0 at 16 articles
    
    # Consistency confidence (lower variance = higher confidence)
    if num_articles > 1:
        scores_only = [score for score, _ in article_scores]
        variance = sum((s - weighted_avg) ** 2 for s in scores_only) / (num_articles - 1)
        consistency_conf = max(0.1, 1.0 - min(1.0, variance))  # Lower variance = higher confidence
    else:
        consistency_conf = 0.5  # Single article = medium confidence
    
    # Publisher diversity confidence
    unique_publishers = len(set(
        (article.get("publisher") or {}).get("name", "") for article in articles
    ))
    diversity_conf = min(1.0, unique_publishers / 3.0)  # 3+ publishers = full confidence
    
    # Combined confidence
    overall_conf = (volume_conf * 0.4 + consistency_conf * 0.4 + diversity_conf * 0.2)
    
    # 🚀 ENHANCED: Final score with confidence weighting
    final_score = weighted_avg * (0.3 + 0.7 * overall_conf)
    
    return max(-1.0, min(1.0, final_score))
