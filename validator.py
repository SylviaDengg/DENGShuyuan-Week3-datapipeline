from urllib.parse import urlparse

REQUIRED_FIELDS = ("title", "content", "url")
DEFAULT_MIN_CONTENT_LENGTH = 120


def has_required_fields(record: dict) -> tuple[bool, list[str]]:
    """Check that record has required fields: title, content, url."""
    reasons = []
    for field in REQUIRED_FIELDS:
        if field not in record:
            reasons.append(f"missing field: {field}")
        elif record[field] is None or (isinstance(record[field], str) and not record[field].strip()):
            reasons.append(f"empty field: {field}")
    return (len(reasons) == 0, reasons)


def is_valid_url(url: str) -> bool:
    """Check URL: only http/https scheme and non-empty netloc."""
    if not url or not isinstance(url, str):
        return False
    url = url.strip()
    if not url:
        return False
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def check_content_length(content: str, min_length: int = DEFAULT_MIN_CONTENT_LENGTH) -> tuple[bool, list[str]]:
    """Check that content meets minimum length. Returns (ok, reasons)."""
    reasons = []
    if content is None:
        reasons.append("empty field: content")
        return (False, reasons)
    if not isinstance(content, str):
        reasons.append("empty field: content")
        return (False, reasons)
    if len(content.strip()) < min_length:
        reasons.append(f"content too short (<{min_length} chars)")
        return (False, reasons)
    return (True, reasons)


def validate_record(
    record: dict,
    min_content_length: int = DEFAULT_MIN_CONTENT_LENGTH,
) -> tuple[bool, list[str]]:
    """
    Validate a single record. Returns (is_valid, list of reasons).
    Reasons are only set when the record is invalid.
    """
    reasons = []

    ok, field_reasons = has_required_fields(record)
    if not ok:
        reasons.extend(field_reasons)

    if "url" in record and record["url"]:
        if not is_valid_url(record["url"]):
            reasons.append("invalid url")

    if "content" in record:
        ok, length_reasons = check_content_length(record["content"], min_content_length)
        if not ok:
            reasons.extend(length_reasons)

    return (len(reasons) == 0, reasons)


def validate_records(
    records: list[dict],
    min_content_length: int = DEFAULT_MIN_CONTENT_LENGTH,
) -> list[tuple[dict, bool, list[str]]]:
    """
    Validate a list of records. Returns a list of (record, is_valid, reasons).
    """
    results = []
    for record in records:
        is_valid, reasons = validate_record(record, min_content_length)
        results.append((record, is_valid, reasons))
    return results
