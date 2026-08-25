import os
import sys

# Ensure VERCEL env is set so config.py picks up the right settings
os.environ.setdefault("VERCEL", "1")

# Add the project root to sys.path so all imports resolve correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
except Exception as e:
    # Log the import error for debugging in Vercel logs
    import traceback
    traceback.print_exc()
    
    # Create a minimal WSGI app that returns the error for debugging
    def app(environ, start_response):
        status = "500 Internal Server Error"
        body = f"App failed to start: {e}".encode("utf-8")
        start_response(status, [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(body))),
        ])
        return [body]

# Vercel looks for a module-level WSGI callable named `app`.
application = app
