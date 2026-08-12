from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from utils.db import get_db, to_object_id, log_user_activity
from datetime import datetime

grammar_bp = Blueprint('grammar', __name__, url_prefix='/grammar')

@grammar_bp.route('/')
@login_required
def index():
    db = get_db()
    lessons = list(db.grammar_lessons.find())
    user_progress = list(db.user_grammar_progress.find({"user_id": to_object_id(current_user.id)}))
    completed_slugs = [p.get('topic_slug') for p in user_progress if p.get('completed')]
    
    return render_template('grammar/index.html', lessons=lessons, completed_slugs=completed_slugs)

@grammar_bp.route('/lesson/<slug>')
@login_required
def lesson_detail(slug):
    db = get_db()
    lesson = db.grammar_lessons.find_one({"slug": slug})
    if not lesson:
        flash("Grammatika darsi topilmadi!", "danger")
        return redirect(url_for('grammar.index'))
        
    return render_template('grammar/lesson.html', lesson=lesson)

@grammar_bp.route('/check/<slug>', methods=['POST'])
@login_required
def check_exercises(slug):
    db = get_db()
    lesson = db.grammar_lessons.find_one({"slug": slug})
    if not lesson:
        return jsonify({"error": "Dars topilmadi"}), 444
        
    exercises = lesson.get('exercises', [])
    correct_count = 0
    total = len(exercises)
    results = []
    
    for ex in exercises:
        ex_id = str(ex.get('id'))
        user_ans = request.form.get(f'ex_{ex_id}', '').strip().lower()
        correct_ans = str(ex.get('correct_answer', '')).strip().lower()
        
        is_correct = (user_ans == correct_ans)
        if is_correct:
            correct_count += 1
            
        results.append({
            "id": ex_id,
            "question": ex.get('question'),
            "user_answer": user_ans,
            "correct_answer": correct_ans,
            "is_correct": is_correct,
            "explanation": ex.get('explanation')
        })
        
    score_pct = round((correct_count / total) * 100) if total > 0 else 0
    is_passed = score_pct >= 70
    
    # Save progress
    db.user_grammar_progress.update_one(
        {"user_id": to_object_id(current_user.id), "topic_slug": slug},
        {"$set": {
            "score": score_pct,
            "completed": is_passed,
            "updated_at": datetime.utcnow()
        }},
        upsert=True
    )
    
    if is_passed:
        log_user_activity(current_user.id, "grammar", f"Grammar: {lesson.get('title')}", f"Natija: {score_pct}%")
        
    return jsonify({
        "score_pct": score_pct,
        "correct_count": correct_count,
        "total": total,
        "is_passed": is_passed,
        "results": results
    })
