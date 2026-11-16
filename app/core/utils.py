def normalize_string(value: str) -> str:
    """Trim whitespace and lowercase a string for case-insensitive matching."""
    return value.strip().lower()
