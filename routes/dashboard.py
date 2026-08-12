from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from flask_login import login_required, current_user
from utils.db import get_db, to_object_id
from utils.helpers import calculate_overall_band
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    db = get_db()
    user_id = to_object_id(current_user.id)
    
    # Calculate average skill bands from results
    r_results = list(db.reading_results.find({"user_id": user_id}).sort("created_at", -1).limit(5))
    l_results = list(db.listening_results.find({"user_id": user_id}).sort("created_at", -1).limit(5))
    w_results = list(db.writing_submissions.find({"user_id": user_id}).sort("created_at", -1).limit(5))
    s_results = list(db.speaking_records.find({"user_id": user_id}).sort("created_at", -1).limit(5))
    
    r_band = round(sum([x.get("band_score", 5.5) for x in r_results]) / len(r_results), 1) if r_results else 5.5
    l_band = round(sum([x.get("band_score", 5.5) for x in l_results]) / len(l_results), 1) if l_results else 5.5
    w_band = round(sum([x.get("overall_band", 5.5) for x in w_results]) / len(w_results), 1) if w_results else 5.5
    s_band = round(sum([x.get("overall_band", 5.5) for x in s_results]) / len(s_results), 1) if s_results else 5.5
    
    overall_band = calculate_overall_band(l_band, r_band, w_band, s_band)
    
    # Update current user estimated band in DB
    db.users.update_one({"_id": user_id}, {"$set": {"current_band": overall_band}})
    
    # Fetch recent activities
    activities = list(db.activity_logs.find({"user_id": user_id}).sort("timestamp", -1).limit(6))
    
    # Fetch study plan tasks
    plan = db.study_plans.find_one({"user_id": user_id})
    today_tasks = [
        {"id": 1, "title": "Reading Passage 1 yechish", "type": "reading", "done": False},
        {"id": 2, "title": "Academic Word List - 15 ta so'z", "type": "vocab", "done": True},
        {"id": 3, "title": "Writing Task 2 insho topshirish", "type": "writing", "done": False},
        {"id": 4, "title": "Grammar: Conditionals mavzusi", "type": "grammar", "done": False}
    ]
    if plan and "today_tasks" in plan:
        today_tasks = plan["today_tasks"]

    # AI recommendation based on lowest score
    skills = {"Reading": r_band, "Listening": l_band, "Writing": w_band, "Speaking": s_band}
    lowest_skill = min(skills, key=skills.get)
    ai_recommendation = f"Sizning eng past ballingiz **{lowest_skill}** ({skills[lowest_skill]}). Bugun ushbu bo'lim bo'yicha kamida 45 daqiqa amaliyot o'tash tavsiya etiladi!"

    return render_template(
        'dashboard/index.html',
        r_band=r_band,
        l_band=l_band,
        w_band=w_band,
        s_band=s_band,
        overall_band=overall_band,
        activities=activities,
        today_tasks=today_tasks,
        ai_recommendation=ai_recommendation
    )

@dashboard_bp.route('/api/progress-chart')
@login_required
def progress_chart_data():
    """API endpoint providing Chart.js data for progress graph."""
    labels = ["Dush", "Sesh", "Chor", "Pay", "Jum", "Shan", "Yak"]
    # Simulated 7-day progression data or read from db
    reading_data = [5.5, 6.0, 6.0, 6.5, 6.5, 7.0, 7.0]
    listening_data = [5.0, 5.5, 6.0, 6.0, 6.5, 6.5, 7.0]
    writing_data = [5.5, 5.5, 6.0, 6.0, 6.0, 6.5, 6.5]
    speaking_data = [5.5, 6.0, 6.0, 6.5, 6.5, 6.5, 7.0]
    
    return jsonify({
        "labels": labels,
        "reading": reading_data,
        "listening": listening_data,
        "writing": writing_data,
        "speaking": speaking_data
    })
