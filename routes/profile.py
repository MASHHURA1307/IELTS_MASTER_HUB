from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from utils.db import get_db, to_object_id
from utils.helpers import get_user_badges

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/')
@login_required
def index():
    db = get_db()
    user_id = to_object_id(current_user.id)
    
    # Calculate results summary for badges
    r_count = db.reading_results.count_documents({"user_id": user_id})
    w_count = db.writing_submissions.count_documents({"user_id": user_id})
    mock_count = db.mock_results.count_documents({"user_id": user_id})
    
    summary = {
        "reading_band": current_user.current_band,
        "writing_count": w_count,
        "mock_count": mock_count
    }
    
    badges = get_user_badges({"streak": current_user.streak}, summary)
    
    return render_template('profile/index.html', badges=badges)

@profile_bp.route('/update', methods=['POST'])
@login_required
def update_profile():
    db = get_db()
    full_name = request.form.get('full_name', '').strip()
    target_band = float(request.form.get('target_band', current_user.target_band))
    
    if full_name:
        db.users.update_one(
            {"_id": to_object_id(current_user.id)},
            {"$set": {"full_name": full_name, "target_band": target_band}}
        )
        flash("Profil ma'lumotlari yangilandi!", "success")
    return redirect(url_for('profile.index'))

@profile_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    db = get_db()
    new_password = request.form.get('new_password', '')
    if new_password and len(new_password) >= 6:
        db.users.update_one(
            {"_id": to_object_id(current_user.id)},
            {"$set": {"password_hash": generate_password_hash(new_password)}}
        )
        flash("Parol muvaffaqiyatli almashtirildi!", "success")
    else:
        flash("Parol kamida 6 ta belgidan iborat bo'lishi kerak!", "warning")
    return redirect(url_for('profile.index'))
