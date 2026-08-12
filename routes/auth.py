from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from utils.db import get_db, User, log_user_activity, update_user_streak

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        target_band = float(request.form.get('target_band', 7.0))
        
        if not full_name or not email or not password:
            flash("Iltimos, barcha majburiy maydonlarni to'ldiring!", "danger")
            return render_template('auth/register.html')
            
        db = get_db()
        existing_user = db.users.find_one({"email": email})
        if existing_user:
            flash("Ushbu email manzil allaqachon ro'yxatdan o'tgan!", "warning")
            return render_template('auth/register.html')
            
        user_doc = {
            "full_name": full_name,
            "email": email,
            "password_hash": generate_password_hash(password),
            "target_band": target_band,
            "current_band": 5.5, # Initial baseline
            "subscription": "free",
            "role": "user",
            "created_at": datetime.utcnow(),
            "streak": 1,
            "last_login_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "avatar": f"https://api.dicebear.com/7.x/avataaars/svg?seed={email}"
        }
        
        res = db.users.insert_one(user_doc)
        user_doc["_id"] = res.inserted_id
        user = User(user_doc)
        
        # Initialize default study plan for user
        db.study_plans.insert_one({
            "user_id": res.inserted_id,
            "target_band": target_band,
            "exam_date": "2026-12-31",
            "daily_hours": 2,
            "completed_tasks": [],
            "created_at": datetime.utcnow()
        })
        
        login_user(user)
        log_user_activity(user.id, "register", "Xush kelibsiz!", "Platformaga muvaffaqiyatli ro'yxatdan o'tdingiz")
        flash(f"Xush kelibsiz, {user.full_name}! Hisobingiz yaratildi.", "success")
        return redirect(url_for('dashboard.index'))
        
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = True if request.form.get('remember') else False
        
        user = User.get_by_email(email)
        if not user or not check_password_hash(user.doc.get('password_hash', ''), password):
            flash("Email yoki parol noto'g'ri kiritildi!", "danger")
            return render_template('auth/login.html')
            
        login_user(user, remember=remember)
        update_user_streak(user.id)
        log_user_activity(user.id, "login", "Tizimga kirish", "Muvaffaqiyatli tizimga kirdi")
        flash(f"Qaytib kelganingiz bilan, {user.full_name}!", "success")
        
        next_page = request.args.get('next')
        return redirect(next_page or url_for('dashboard.index'))
        
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Tizimdan muvaffaqiyatli chiqdingiz.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/google-login')
def google_login():
    flash("Google orqali kirish tez orada faollashtiriladi! Hozircha email orqali kiring.", "info")
    return redirect(url_for('auth.login'))
