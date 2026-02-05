import html
import re
import unicodedata
from datetime import datetime

# Known NYT scraper boilerplate phrases to remove from article content
_nyt_boilerplate_phrases = [
    "We are having trouble retrieving the article content",
    "Please enable JavaScript in your browser settings",
    "Thank you for your patience while we verify access",
    "Already a subscriber? Log in",
    "Want all of The Times? Subscribe",
]


def remove_whitespace_and_html(text: str) -> str:
    """Remove extra whitespace and HTML artifacts from text."""
    if not text or not isinstance(text, str):
        return ""
    # Strip HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Decode HTML entities (e.g. &amp; -> &, &quot; -> ")
    text = html.unescape(text)
    # Collapse multiple spaces/newlines/tabs into a single space
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def remove_nyt_boilerplate(text: str) -> str:
    """Remove known NYT access/paywall boilerplate phrases from content."""
    if not text or not isinstance(text, str):
        return ""
    result = text
    for phrase in _nyt_boilerplate_phrases:
        result = result.replace(phrase, " ")
    result = re.sub(r"\s+", " ", result)
    return result.strip()


def normalize_encoding(text: str) -> str:
    """Normalize text to UTF-8 and fix common encoding issues."""
    if not text or not isinstance(text, str):
        return ""
    # Normalize unicode (NFC is a common standard)
    text = unicodedata.normalize("NFC", text)
    # Replace replacement character and other common mojibake if present
    text = text.replace("\ufffd", "")
    return text.strip()


def standardize_date(date_value: str) -> str:
    """Convert various date formats to ISO format (YYYY-MM-DD)."""
    if not date_value or not isinstance(date_value, str):
        return ""
    date_value = date_value.strip()
    if not date_value:
        return ""
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%m-%d-%Y",
        "%Y/%m/%d",
        "%d %b %Y",
        "%d %B %Y",
        "%b %d, %Y",
        "%B %d, %Y",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_value, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return ""


def handle_special_characters(text: str) -> str:
    """Handle special characters: normalize unicode, remove or replace problematic ones."""
    if not text or not isinstance(text, str):
        return ""
    # Normalize to NFKC (compatibility decomposition then canonical composition)
    text = unicodedata.normalize("NFKC", text)
    # Replace curly quotes and similar with ASCII equivalents
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Remove control characters
    text = "".join(c for c in text if unicodedata.category(c) != "Cc")
    return text


def clean_text(text: str) -> str:
    """Apply all cleaning steps to a text string."""
    if not text or not isinstance(text, str):
        return ""
    text = normalize_encoding(text)
    text = remove_whitespace_and_html(text)
    text = handle_special_characters(text)
    return text.strip()


def clean_record(article: dict) -> dict:
    """Clean a single article: title and content via clean_text, strip url, leave published unchanged."""
    out = dict(article)
    out["title"] = clean_text(article.get("title") or "")
    content = clean_text(article.get("content") or "")
    out["content"] = remove_nyt_boilerplate(content)
    if "url" in article and article["url"] is not None:
        out["url"] = (article["url"] or "").strip()
    return out


def clean_dataset(data: dict) -> dict:
    """Clean dataset with structure { "generated_at": "...", "articles": [ ... ] }. Preserves generated_at."""
    out = {"generated_at": data.get("generated_at", ""), "articles": []}
    for article in data.get("articles", []):
        out["articles"].append(clean_record(article))
    return out
