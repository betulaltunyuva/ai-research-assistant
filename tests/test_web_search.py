from utils.web_search import (
    get_domain,
    calculate_source_score
)


def test_get_domain():
    domain = get_domain(
        "https://learn.microsoft.com/en-us/test"
    )

    assert "microsoft.com" in domain


def test_source_score_returns_number():
    score = calculate_source_score(
        "https://learn.microsoft.com/test"
    )

    assert isinstance(score, int)