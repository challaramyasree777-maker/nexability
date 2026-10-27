from app.services.accessibility.statuses import AccessibilityStatus


def test_accessibility_statuses_are_distinct() -> None:
    assert AccessibilityStatus.CONFIRMED != AccessibilityStatus.UNVERIFIED
    assert AccessibilityStatus.MISSING != AccessibilityStatus.UNKNOWN
