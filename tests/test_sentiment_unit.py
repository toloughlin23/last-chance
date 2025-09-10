from services.sentiment import score_article, aggregate_symbol_sentiment


def test_score_article_basic():
    a_pos = {"title": "Company beats earnings and raises guidance", "description": "Strong growth"}
    a_neg = {"title": "Company misses estimates and cuts guidance", "description": "Investigation ongoing"}
    s_pos = score_article(a_pos)
    s_neg = score_article(a_neg)
    assert s_pos > s_neg
    assert -1.0 <= s_pos <= 1.0
    assert -1.0 <= s_neg <= 1.0


def test_aggregate_symbol_sentiment():
    articles = [
        {"title": "upgrade expected", "description": "analyst upgrade"},
        {"title": "record profit", "description": "surge in demand"}
    ]
    score = aggregate_symbol_sentiment(articles)
    assert score > 0
    assert -1.0 <= score <= 1.0

