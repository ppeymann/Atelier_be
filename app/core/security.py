from __future__ import annotations

import hmac
import secrets

from app.core.config import get_setting

def generate_secure_token(n_bytes: int = 32) -> str:
    return secrets.token_urlsafe(n_bytes)

def constant_time_compare(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)

def refresh_cookie_settings() -> dict[str, object]:
    settings = get_setting()
    return {
        "httponly": True,
        "secure":settings.is_production,
        "samesite":"lax",
        "path":"/api/v1/auth"
    }
    