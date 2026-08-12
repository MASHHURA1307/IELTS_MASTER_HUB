import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import db

class DummyApp:
    pass

a = DummyApp()
a.config = {'MONGO_URI': 'mongodb+srv://invalid:bad@cluster.example.mongodb.net/test'}
a.logger = type('L', (), {'info': lambda *args, **kwargs: None, 'error': lambda *args, **kwargs: None, 'warning': lambda *args, **kwargs: None})()

db.init_db(a)
print(db.db.users.count_documents({}))
print([u['email'] for u in db.db.users.find({}, {'email': 1})])
