from main import route_after_verification


def test_verifier_approved_routes_to_end():
    state = {
        "verification_report":
            "DURUM: UYGUN",
        "revision_count": 0
    }

    result = route_after_verification(
        state
    )

    assert result == "end"


def test_verifier_problem_routes_to_revision():
    state = {
        "verification_report":
            "DURUM: DÜZELTME GEREKLİ",
        "revision_count": 0
    }

    result = route_after_verification(
        state
    )

    assert result == "revise"


def test_max_revision_routes_to_end():
    state = {
        "verification_report":
            "DURUM: DÜZELTME GEREKLİ",
        "revision_count": 1
    }

    result = route_after_verification(
        state
    )

    assert result == "end"