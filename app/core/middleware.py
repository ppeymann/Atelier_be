from contextvars import ContextVar
request_id_ctx_var: [str | None] = ContextVar("request_id", default=None)