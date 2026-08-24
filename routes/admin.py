from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from utils.db import get_db, to_object_id
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash("Ushbu sahifaga kirish uchun Admin huquqi talab etiladi!", "danger")
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_super_admin():
            flash("Ushbu amaliyot uchun Super Admin huquqi talab etiladi!", "danger")
            return redirect(url_for('admin.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def index():
    db = get_db()
    
    total_users = db.users.count_documents({})
    premium_users = db.users.count_documents({"subscription": "premium"})
    reading_count = db.reading_tests.count_documents({})
    listening_count = db.listening_tests.count_documents({})
    writing_count = db.writing_prompts.count_documents({})
    total_tests_completed = db.reading_results.count_documents({}) + db.writing_submissions.count_documents({})
    
    recent_users = list(db.users.find().sort("created_at", -1).limit(5))
    
    return render_template(
        'admin/index.html',
        total_users=total_users,
        premium_users=premium_users,
        reading_count=reading_count,
        listening_count=listening_count,
        writing_count=writing_count,
        total_tests_completed=total_tests_completed,
        recent_users=recent_users
    )

@admin_bp.route('/users')
@login_required
@admin_required
def users_list():
    db = get_db()
    users = list(db.users.find().sort("created_at", -1))
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/toggle-premium/<user_id>', methods=['POST'])
@login_required
@super_admin_required
def toggle_premium(user_id):
    db = get_db()
    obj_id = to_object_id(user_id)
    u = db.users.find_one({"_id": obj_id})
    if u:
        new_sub = "free" if u.get("subscription") == "premium" else "premium"
        db.users.update_one({"_id": obj_id}, {"$set": {"subscription": new_sub}})
        flash(f"Foydalanuvchi obuna holati '{new_sub}' ga o'zgartirildi!", "success")
    return redirect(url_for('admin.users_list'))

@admin_bp.route('/content')
@login_required
@admin_required
def content_management():
    db = get_db()
    r_tests = list(db.reading_tests.find())
    l_tests = list(db.listening_tests.find())
    w_prompts = list(db.writing_prompts.find())
    s_questions = list(db.speaking_questions.find())
    
    return render_template(
        'admin/content.html',
        r_tests=r_tests,
        l_tests=l_tests,
        w_prompts=w_prompts,
        s_questions=s_questions
    )

@admin_bp.route('/content/reading/add', methods=['GET', 'POST'])
@login_required
@super_admin_required
def add_reading():
    if request.method == 'POST':
        db = get_db()
        title = request.form.get('title')
        difficulty = request.form.get('difficulty')
        passage_text = request.form.get('passage_text')
        
        new_test = {
            "title": title,
            "difficulty": difficulty,
            "passage_text": passage_text,
            "questions": [] # soddalashtirilgan
        }
        db.reading_tests.insert_one(new_test)
        flash("Yangi Reading testi muvaffaqiyatli qo'shildi!", "success")
        return redirect(url_for('admin.content_management'))
        
    return render_template('admin/add_reading.html')

@admin_bp.route('/content/writing/add', methods=['GET', 'POST'])
@login_required
@super_admin_required
def add_writing():
    if request.method == 'POST':
        db = get_db()
        title = request.form.get('title')
        task_type = request.form.get('task_type')
        prompt_text = request.form.get('prompt_text')
        
        new_prompt = {
            "title": title,
            "task_type": task_type,
            "prompt_text": prompt_text
        }
        db.writing_prompts.insert_one(new_prompt)
        flash("Yangi Writing mavzusi muvaffaqiyatli qo'shildi!", "success")
        return redirect(url_for('admin.content_management'))
        
    return render_template('admin/add_writing.html')
