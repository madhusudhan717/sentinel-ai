import hashlib
import secrets


def generate_api_key() -> str:
    """Generate a new raw API key. Shown to the user once, never stored."""
    return f"sk_sentinel_{secrets.token_urlsafe(32)}"


def hash_api_key(raw_key: str) -> str:
    """One-way hash of an API key, safe to store in the database."""
    return hashlib.sha256(raw_key.encode()).hexdigest()