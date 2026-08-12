from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from utils.db import get_db, to_object_id, log_user_activity
from utils.ai_helper import ask_ai_mentor
from datetime import datetime

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/')
@ai_bp.route('/chat')
@login_required
def chat():
    db = get_db()
    history = list(db.ai_feedback.find({"user_id": to_object_id(current_user.id)}).sort("timestamp", 1).limit(20))
    return render_template('ai/chat.html', history=history)

@ai_bp.route('/ask', methods=['POST'])
@login_required
def ask():
    user_message = request.json.get('message', '').strip()
    if not user_message:
        return jsonify({"error": "Bo'sh xabar yuborib bo'lmaydi"}), 400
        
    ai_reply = ask_ai_mentor(user_message)
    
    db = get_db()
    db.ai_feedback.insert_one({
        "user_id": to_object_id(current_user.id),
        "user_message": user_message,
        "ai_reply": ai_reply,
        "timestamp": datetime.utcnow()
    })
    
    return jsonify({"reply": ai_reply})
