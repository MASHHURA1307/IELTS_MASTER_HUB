"""Restore the original request path when Vercel invokes a Python entry file."""

_ENTRY_PATHS = {
    "/api/index",
    "/api/index.py",
    "/index.py",
    "/app.py",
    "/app",
}


def _header_path(environ, *keys):
    for key in keys:
        value = environ.get(key)
        if not value:
            continue
        path = value.split("?")[0].strip()
        if path and path not in _ENTRY_PATHS:
            if not path.startswith("/"):
                path = "/" + path
            return path
    return None


def vercel_path_fix(wsgi_app):
    def middleware(environ, start_response):
        path = environ.get("PATH_INFO") or "/"
        normalized = path if path.startswith("/") else "/" + path

        if normalized.rstrip("/") in {p.rstrip("/") for p in _ENTRY_PATHS} or normalized in _ENTRY_PATHS:
            restored = _header_path(
                environ,
                "HTTP_X_VERCEL_ORIGINAL_PATH",
                "HTTP_X_FORWARDED_URI",
                "HTTP_X_ORIGINAL_URL",
                "HTTP_X_REWRITE_URL",
                "RAW_URI",
                "REQUEST_URI",
            )
            environ["PATH_INFO"] = restored or "/"
            environ["SCRIPT_NAME"] = ""

        return wsgi_app(environ, start_response)

    return middleware
