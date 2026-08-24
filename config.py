import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or os.getenv("secret-key") or "ielts_master_hub_default_secret_key"
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/ielts_master_hub")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Flask URL building configuration
    SERVER_NAME = os.getenv("SERVER_NAME", "127.0.0.1:5000")
    APPLICATION_ROOT = "/"
    PREFERRED_URL_SCHEME = "http"
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    if os.getenv("VERCEL") == "1":
        UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "/tmp/uploads")
        REPORT_FOLDER = os.getenv("REPORT_FOLDER", "/tmp/reports")
    else:
        UPLOAD_FOLDER = os.path.join(BASE_DIR, os.getenv("UPLOAD_FOLDER", "uploads"))
        REPORT_FOLDER = os.path.join(BASE_DIR, os.getenv("REPORT_FOLDER", "reports"))
    
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024)) # 16 MB max
    ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'webm'}
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg'}
