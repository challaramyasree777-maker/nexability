from enum import StrEnum


class AccessibilityStatus(StrEnum):
    CONFIRMED = "confirmed"
    UNVERIFIED = "unverified"
    MISSING = "missing"
    UNKNOWN = "unknown"
