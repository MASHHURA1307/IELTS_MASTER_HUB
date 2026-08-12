import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from utils.db import get_db, to_object_id, log_user_activity
from utils.ai_helper import evaluate_speaking_response
from datetime import datetime

speaking_bp = Blueprint('speaking', __name__, url_prefix='/speaking')

@speaking_bp.route('/')
@login_required
def index():
    db = get_db()
    part = request.args.get('part', 'all')
    query = {} if part == 'all' else {"part": int(part)}
    
    questions = list(db.speaking_questions.find(query))
    user_id = to_object_id(current_user.id)
    records = list(db.speaking_records.find({"user_id": user_id}).sort("created_at", -1).limit(5))
    
    return render_template('speaking/index.html', questions=questions, records=records, current_part=part)

@speaking_bp.route('/test/<question_id>')
@login_required
def test_detail(question_id):
    db = get_db()
    q = db.speaking_questions.find_one({"_id": to_object_id(question_id)})
    if not q:
        flash("Speaking savoli topilmadi!", "danger")
        return redirect(url_for('speaking.index'))
        
    return render_template('speaking/test.html', question=q)

@speaking_bp.route('/submit/<question_id>', methods=['POST'])
@login_required
def submit_speech(question_id):
    db = get_db()
    q = db.speaking_questions.find_one({"_id": to_object_id(question_id)})
    if not q:
        return jsonify({"error": "Savol topilmadi"}), 444
        
    transcript = request.form.get('transcript', '').strip()
    audio_file = request.files.get('audio_data')
    audio_path = ""
    
    if audio_file and audio_file.filename != '':
        filename = secure_filename(f"speaking_{current_user.id}_{int(datetime.utcnow().timestamp())}.webm")
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'audio')
        os.makedirs(upload_dir, exist_ok=True)
        save_path = os.path.join(upload_dir, filename)
        audio_file.save(save_path)
        audio_path = f"/static/uploads/audio/{filename}"

    part_num = q.get('part', 1)
    q_text = q.get('question', '')
    
    # Run AI evaluation
    eval_res = evaluate_speaking_response(part_num, q_text, transcript or "Ovozli audio javob topshirildi.")
    
    record_doc = {
        "user_id": to_object_id(current_user.id),
        "question_id": to_object_id(question_id),
        "question_text": q_text,
        "part": part_num,
        "transcript": transcript,
        "audio_path": audio_path,
        "overall_band": eval_res.get("overall_band", 6.5),
        "fluency_band": eval_res.get("fluency_band", 6.5),
        "vocabulary_band": eval_res.get("vocabulary_band", 6.5),
        "grammar_band": eval_res.get("grammar_band", 6.0),
        "pronunciation_band": eval_res.get("pronunciation_band", 7.0),
        "evaluation": eval_res,
        "created_at": datetime.utcnow()
    }
    
    res = db.speaking_records.insert_one(record_doc)
    log_user_activity(current_user.id, "speaking", f"Speaking Part {part_num} topshirildi", f"AI Bahosi: Band {eval_res.get('overall_band')}")
    
    return redirect(url_for('speaking.result', record_id=str(res.inserted_id)))

@speaking_bp.route('/result/<record_id>')
@login_required
def result(record_id):
    db = get_db()
    record = db.speaking_records.find_one({"_id": to_object_id(record_id)})
    if not record:
        flash("Natija topilmadi!", "danger")
        return redirect(url_for('speaking.index'))
        
    return render_template('speaking/result.html', record=record)
