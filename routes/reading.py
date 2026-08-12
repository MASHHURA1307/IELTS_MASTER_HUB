from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from utils.db import get_db, to_object_id, log_user_activity
from utils.helpers import raw_score_to_reading_band
from datetime import datetime

reading_bp = Blueprint('reading', __name__, url_prefix='/reading')

@reading_bp.route('/')
@login_required
def index():
    db = get_db()
    difficulty = request.args.get('difficulty', 'all')
    query = {} if difficulty == 'all' else {"difficulty": difficulty}
    
    tests = list(db.reading_tests.find(query))
    user_results = list(db.reading_results.find({"user_id": to_object_id(current_user.id)}))
    completed_ids = [str(r.get('test_id')) for r in user_results]
    
    return render_template('reading/index.html', tests=tests, completed_ids=completed_ids, current_diff=difficulty)

@reading_bp.route('/test/<test_id>')
@login_required
def test_detail(test_id):
    db = get_db()
    obj_id = to_object_id(test_id)
    test = db.reading_tests.find_one({"_id": obj_id})
    if not test:
        flash("O'qish matni topilmadi!", "danger")
        return redirect(url_for('reading.index'))
        
    return render_template('reading/test.html', test=test)

@reading_bp.route('/submit/<test_id>', methods=['POST'])
@login_required
def submit_test(test_id):
    db = get_db()
    obj_id = to_object_id(test_id)
    test = db.reading_tests.find_one({"_id": obj_id})
    if not test:
        return jsonify({"error": "Test topilmadi"}), 444
        
    questions = test.get('questions', [])
    user_answers = {}
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
            
        user_answers[q_id] = user_ans
        answer_details.append({
            "question_id": q_id,
            "question_text": q.get('question'),
            "user_answer": user_ans,
            "correct_answer": correct_ans,
            "is_correct": is_correct,
            "explanation": q.get('explanation', "To'g'ri javob matndagi kalit so'zlarga asoslangan.")
        })
        
    # Scale correct score to 40 for IELTS band conversion
    raw_scaled = round((correct_count / total_q) * 40) if total_q > 0 else 0
    band_score = raw_score_to_reading_band(raw_scaled)
    
    result_doc = {
        "user_id": to_object_id(current_user.id),
        "test_id": obj_id,
        "test_title": test.get('title'),
        "correct_count": correct_count,
        "total_questions": total_q,
        "raw_score": raw_scaled,
        "band_score": band_score,
        "answers": answer_details,
        "time_spent": request.form.get('time_spent', '15:00'),
        "created_at": datetime.utcnow()
    }
    
    res = db.reading_results.insert_one(result_doc)
    log_user_activity(current_user.id, "reading", f"Reading Test: {test.get('title')}", f"Natija: Band {band_score}")
    
    return redirect(url_for('reading.result', result_id=str(res.inserted_id)))

@reading_bp.route('/result/<result_id>')
@login_required
def result(result_id):
    db = get_db()
    result_doc = db.reading_results.find_one({"_id": to_object_id(result_id)})
    if not result_doc:
        flash("Natija topilmadi!", "danger")
        return redirect(url_for('reading.index'))
        
    return render_template('reading/result.html', result=result_doc)

@reading_bp.route('/bookmark/<test_id>', methods=['POST'])
@login_required
def bookmark(test_id):
    db = get_db()
    user_id = to_object_id(current_user.id)
    t_id = to_object_id(test_id)
    
    existing = db.bookmarks.find_one({"user_id": user_id, "test_id": t_id, "type": "reading"})
    if existing:
        db.bookmarks.delete_one({"_id": existing["_id"]})
        return jsonify({"status": "removed"})
    else:
        db.bookmarks.insert_one({"user_id": user_id, "test_id": t_id, "type": "reading", "created_at": datetime.utcnow()})
        return jsonify({"status": "added"})
