from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from utils.db import get_db, to_object_id
from datetime import datetime

planner_bp = Blueprint('planner', __name__, url_prefix='/planner')

@planner_bp.route('/')
@login_required
def index():
    db = get_db()
    user_id = to_object_id(current_user.id)
    plan = db.study_plans.find_one({"user_id": user_id})
    
    if not plan:
        plan = {
            "target_band": current_user.target_band,
            "exam_date": "2026-12-31",
            "daily_hours": 2,
            "today_tasks": [
                {"id": 1, "title": "Reading Passage 1: General Science", "type": "reading", "done": False},
                {"id": 2, "title": "Academic Vocabulary - 15 ta so'z", "type": "vocab", "done": True},
                {"id": 3, "title": "Writing Task 2 inshosi yozish", "type": "writing", "done": False},
                {"id": 4, "title": "Grammar: Conditionals darsini o'rganish", "type": "grammar", "done": False}
            ]
        }
        
    return render_template('planner/index.html', plan=plan)

@planner_bp.route('/save', methods=['POST'])
@login_required
def save_plan():
    db = get_db()
    user_id = to_object_id(current_user.id)
    
    exam_date = request.form.get('exam_date')
    target_band = float(request.form.get('target_band', 7.0))
    daily_hours = int(request.form.get('daily_hours', 2))
    
    db.study_plans.update_one(
        {"user_id": user_id},
        {"$set": {
            "exam_date": exam_date,
            "target_band": target_band,
            "daily_hours": daily_hours,
            "updated_at": datetime.utcnow()
        }},
        upsert=True
    )
    
    flash("Reja muvaffaqiyatli saqlandi!", "success")
    return redirect(url_for('planner.index'))

@planner_bp.route('/toggle-task/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    db = get_db()
    user_id = to_object_id(current_user.id)
    plan = db.study_plans.find_one({"user_id": user_id})
    
    if plan and "today_tasks" in plan:
        tasks = plan["today_tasks"]
        for t in tasks:
            if t.get("id") == task_id:
                t["done"] = not t.get("done", False)
                break
        db.study_plans.update_one({"user_id": user_id}, {"$set": {"today_tasks": tasks}})
        return jsonify({"status": "ok"})
        
    return jsonify({"error": "Reja topilmadi"}), 404
