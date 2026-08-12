from flask_login import UserMixin
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, date
from werkzeug.security import generate_password_hash
import logging

try:
    import mongomock
except Exception:  # pragma: no cover - optional dependency
    mongomock = None

mongo_client = None
db = None


def _seed_default_users_if_needed():
    global db
    if db is None:
        return

    try:
        if db.users.count_documents({}) == 0:
            db.users.insert_many([
                {
                    "full_name": "Admin Manager",
                    "email": "admin@ielts.uz",
                    "password_hash": generate_password_hash("admin123"),
                    "target_band": 8.0,
                    "current_band": 8.0,
                    "subscription": "premium",
                    "role": "admin",
                    "created_at": datetime.utcnow(),
                    "streak": 15,
                    "last_login_date": datetime.utcnow().strftime("%Y-%m-%d"),
                    "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=admin@ielts.uz"
                },
                {
                    "full_name": "Bekzod Rahimov",
                    "email": "user@ielts.uz",
                    "password_hash": generate_password_hash("user123"),
                    "target_band": 7.0,
                    "current_band": 6.5,
                    "subscription": "free",
                    "role": "user",
                    "created_at": datetime.utcnow(),
                    "streak": 5,
                    "last_login_date": datetime.utcnow().strftime("%Y-%m-%d"),
                    "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=user@ielts.uz"
                }
            ])
    except Exception as e:
        logging.getLogger(__name__).warning(f"Unable to seed default users: {e}")


def init_db(app):
    global mongo_client, db
    try:
        mongo_uri = app.config.get("MONGO_URI", "mongodb://localhost:27017/ielts_master_hub")
        db_name = mongo_uri.rstrip("/").split("/")[-1].split("?")[0] or "ielts_master_hub"
        if not db_name:
            db_name = "ielts_master_hub"

        if "mongodb+srv" in mongo_uri.lower() or "mongodb://" in mongo_uri.lower():
            mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            db = mongo_client[db_name]
            db.list_collection_names()
            app.logger.info(f"Connected to MongoDB database: {db_name}")
        else:
            raise ValueError("Unsupported MongoDB URI")
    except Exception as e:
        app.logger.error(f"Error connecting to MongoDB: {e}")
        if mongomock is not None:
            mongo_client = mongomock.MongoClient()
            db = mongo_client[db_name]
            app.logger.warning(f"Falling back to in-memory MongoDB for {db_name}")
        else:
            db = None

    if db is not None:
        _seed_default_users_if_needed()


def get_db():
    global db
    if db is None:
        from config import Config
        try:
            mongo_client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=3000)
            db_name = Config.MONGO_URI.rstrip("/").split("/")[-1].split("?")[0] or "ielts_master_hub"
            db = mongo_client[db_name]
            db.list_collection_names()
        except Exception as e:
            if mongomock is not None:
                mongo_client = mongomock.MongoClient()
                db_name = Config.MONGO_URI.rstrip("/").split("/")[-1].split("?")[0] or "ielts_master_hub"
                db = mongo_client[db_name]
            else:
                raise RuntimeError(f"Unable to initialize MongoDB: {e}") from e
    if db is not None:
        _seed_default_users_if_needed()
    return db

def to_object_id(id_str):
    if isinstance(id_str, ObjectId):
        return id_str
    try:
        return ObjectId(id_str)
    except Exception:
        return None

class User(UserMixin):
    def __init__(self, user_doc):
        self.doc = user_doc or {}
        self.id = str(self.doc.get("_id", ""))
        self.email = self.doc.get("email", "")
        self.full_name = self.doc.get("full_name", "")
        self.role = self.doc.get("role", "user")
        self.target_band = float(self.doc.get("target_band", 7.0))
        self.current_band = float(self.doc.get("current_band", 5.5))
        self.subscription = self.doc.get("subscription", "free") # 'free' or 'premium'
        self.created_at = self.doc.get("created_at", datetime.utcnow())
        self.streak = int(self.doc.get("streak", 1))
        self.last_login_date = self.doc.get("last_login_date", None)
        self.avatar = self.doc.get("avatar", "")

    def is_admin(self):
        return self.role == "admin"

    def is_premium(self):
        return self.subscription == "premium" or self.role == "admin"

    @staticmethod
    def get_by_id(user_id):
        database = get_db()
        obj_id = to_object_id(user_id)
        if not obj_id:
            return None
        doc = database.users.find_one({"_id": obj_id})
        return User(doc) if doc else None

    @staticmethod
    def get_by_email(email):
        database = get_db()
        doc = database.users.find_one({"email": email.lower().strip()})
        return User(doc) if doc else None

def log_user_activity(user_id, activity_type, title, details=""):
    database = get_db()
    obj_id = to_object_id(user_id)
    activity_doc = {
        "user_id": obj_id,
        "type": activity_type,
        "title": title,
        "details": details,
        "timestamp": datetime.utcnow()
    }
    database.activity_logs.insert_one(activity_doc)

def update_user_streak(user_id):
    database = get_db()
    obj_id = to_object_id(user_id)
    user_doc = database.users.find_one({"_id": obj_id})
    if not user_doc:
        return
    
    today_str = date.today().isoformat()
    last_login = user_doc.get("last_login_date")
    current_streak = user_doc.get("streak", 0)

    if not last_login:
        new_streak = 1
    elif last_login == today_str:
        return # Already logged today
    else:
        try:
            last_date = datetime.strptime(last_login, "%Y-%m-%d").date()
            delta = (date.today() - last_date).days
            if delta == 1:
                new_streak = current_streak + 1
            else:
                new_streak = 1
        except Exception:
            new_streak = 1

    database.users.update_one(
        {"_id": obj_id},
        {"$set": {"streak": new_streak, "last_login_date": today_str}}
    )
