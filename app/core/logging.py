from __future__ import annotations

import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict, Processor

from app.core.config import get_setting
from app.core.middleware import request_id_ctx_var

_SENSITIVE_KEYS = {
    "password",
    "hashed_password",
    "token",
    "access_token",
    "refresh_token",
    "authorization",
    "secret",
    "client_secret",
    "jwt_secret_key",
    "cookie",
}

def _redact_sensitive_data(event_dict: EventDict) -> EventDict:
    """Recursively scrub keys that look sensitive so we never leak secrets."""
    
    def scrub(value: Any) -> Any:
        if isinstance(value, dict):
            return {
                k: ("***REDACTED***" if k.lower() in _SENSITIVE_KEYS else scrub(v))
                for k, v in value.items()
            }
        return value
    for key in list(event_dict.keys()):
        if key.lower() in _SENSITIVE_KEYS:
            event_dict[key] = "***REDACTED***"
        else:
            event_dict[key] = scrub(event_dict[key])
    return event_dict

def _add_request_id(event_dict: EventDict) -> EventDict:
    request_id = request_id_ctx_var.get()
    if request_id:
        event_dict["request_id"] = request_id
    return event_dict

def configure_logging() -> None:
    """Configure logging for the application."""
    settings = get_setting()
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        _add_request_id,
        _redact_sensitive_data,
    ]
    if settings.LOG_FORMAT == "json":
        renderer: Processor = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)
    structlog.configure(
        processors=[
            *shared_processors,
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.warp_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True
    )
    
    formatter = logging.stdlib.ProcessorFormatter(
        processor = renderer,
        foreign_pre_chain = shared_processors,
    )
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(settings.LOG_LEVEL)
    
    for noisy in ("uvicorn.access", "sqlachemy.engine"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
        
def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
    