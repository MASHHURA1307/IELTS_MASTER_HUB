from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from utils.db import get_db, to_object_id, log_user_activity
from utils.helpers import raw_score_to_listening_band
from datetime import datetime

listening_bp = Blueprint('listening', __name__, url_prefix='/listening')

@listening_bp.route('/')
@login_required
def index():
    db = get_db()
    tests = list(db.listening_tests.find())
    user_results = list(db.listening_results.find({"user_id": to_object_id(current_user.id)}))
    completed_ids = [str(r.get('test_id')) for r in user_results]
    
    return render_template('listening/index.html', tests=tests, completed_ids=completed_ids)

@listening_bp.route('/test/<test_id>')
@login_required
def test_detail(test_id):
    db = get_db()
    test = db.listening_tests.find_one({"_id": to_object_id(test_id)})
    if not test:
        flash("Listening mashqi topilmadi!", "danger")
        return redirect(url_for('listening.index'))
        
    return render_template('listening/test.html', test=test)

@listening_bp.route('/submit/<test_id>', methods=['POST'])
@login_required
def submit_test(test_id):
    db = get_db()
    obj_id = to_object_id(test_id)
    test = db.listening_tests.find_one({"_id": obj_id})
    if not test:
        return jsonify({"error": "Test topilmadi"}), 444
        
    questions = test.get('questions', [])
    correct_count = 0
    total_q = len(questions)
    answer_details = []
    
    for q in questions:
        q_id = str(q.get('id'))
        user_ans = request.form.get(f'question_{q_id}', '').strip().lower()
        correct_ans = str(q.get('correct_answer', '')).strip().lower()
        
        is_correct = (user_ans == correct_ans)
        if is_correct:
            correct_count += 1
            
        answer_details.append({
            "question_id": q_id,
            "question_text": q.get('question'),
            "user_answer": user_ans,
            "correct_answer": correct_ans,
            "is_correct": is_correct,
            "explanation": q.get('explanation', "Audio transkriptida to'g'ri kalit ma'lumot berilgan.")
        })
        
    raw_scaled = round((correct_count / total_q) * 40) if total_q > 0 else 0
    band_score = raw_score_to_listening_band(raw_scaled)
    
    result_doc = {
        "user_id": to_object_id(current_user.id),
        "test_id": obj_id,
        "test_title": test.get('title'),
        "correct_count": correct_count,
        "total_questions": total_q,
        "raw_score": raw_scaled,
        "band_score": band_score,
        "answers": answer_details,
        "created_at": datetime.utcnow()
    }
    
    res = db.listening_results.insert_one(result_doc)
    log_user_activity(current_user.id, "listening", f"Listening Test: {test.get('title')}", f"Natija: Band {band_score}")
    
    return redirect(url_for('listening.result', result_id=str(res.inserted_id)))

@listening_bp.route('/result/<result_id>')
@login_required
def result(result_id):
    db = get_db()
    result_doc = db.listening_results.find_one({"_id": to_object_id(result_id)})
    if not result_doc:
        flash("Natija topilmadi!", "danger")
        return redirect(url_for('listening.index'))
        
    return render_template('listening/result.html', result=result_doc)
