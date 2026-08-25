import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import db


def test_init_db_falls_back_to_mongomock_when_mongo_uri_is_invalid():
    class DummyApp:
        def __init__(self):
            self.config = {"MONGO_URI": "mongodb+srv://invalid:bad@cluster.example.mongodb.net/test"}
            self.logger = type("Logger", (), {
                "info": lambda *a, **k: None,
                "warning": lambda *a, **k: None,
                "error": lambda *a, **k: None,
            })()

    app = DummyApp()
    db.init_db(app)
    assert db.db is not None
    assert db.db.name == "test"
