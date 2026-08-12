from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from utils.db import get_db, to_object_id, log_user_activity
from utils.ai_helper import evaluate_writing_essay
from datetime import datetime

writing_bp = Blueprint('writing', __name__, url_prefix='/writing')

@writing_bp.route('/')
@login_required
def index():
    db = get_db()
    task_type = request.args.get('type', 'all')
    query = {} if task_type == 'all' else {"task_type": task_type}
    
    prompts = list(db.writing_prompts.find(query))
    user_id = to_object_id(current_user.id)
    recent_submissions = list(db.writing_submissions.find({"user_id": user_id}).sort("created_at", -1).limit(5))
    
    return render_template('writing/index.html', prompts=prompts, recent_submissions=recent_submissions, task_type=task_type)

@writing_bp.route('/test/<prompt_id>')
@login_required
def test_detail(prompt_id):
    db = get_db()
    prompt = db.writing_prompts.find_one({"_id": to_object_id(prompt_id)})
    if not prompt:
        flash("Writing mavzusi topilmadi!", "danger")
        return redirect(url_for('writing.index'))
        
    return render_template('writing/test.html', prompt=prompt)

@writing_bp.route('/submit/<prompt_id>', methods=['POST'])
@login_required
def submit_essay(prompt_id):
    db = get_db()
    prompt_obj = db.writing_prompts.find_one({"_id": to_object_id(prompt_id)})
    essay_text = request.form.get('essay_text', '').strip()
    
    if not essay_text or len(essay_text.split()) < 20:
        flash("Insho matni o'ta qisqa! Kamida 20 ta so'z yozishingiz kerak.", "danger")
        return redirect(url_for('writing.test_detail', prompt_id=prompt_id))
        
    task_type = prompt_obj.get('task_type', 'Task 2') if prompt_obj else 'Task 2'
    prompt_text = prompt_obj.get('prompt_text', '') if prompt_obj else ''
    
    # Run AI Evaluation
    eval_result = evaluate_writing_essay(task_type, prompt_text, essay_text)
    
    submission_doc = {
        "user_id": to_object_id(current_user.id),
        "prompt_id": to_object_id(prompt_id),
        "prompt_title": prompt_obj.get('title') if prompt_obj else "Insho",
        "task_type": task_type,
        "essay_text": essay_text,
        "overall_band": eval_result.get("overall_band", 6.0),
        "task_response_band": eval_result.get("task_response_band", 6.0),
        "coherence_band": eval_result.get("coherence_band", 6.0),
        "lexical_band": eval_result.get("lexical_band", 6.0),
        "grammar_band": eval_result.get("grammar_band", 6.0),
        "word_count": eval_result.get("word_count", len(essay_text.split())),
        "evaluation": eval_result,
        "created_at": datetime.utcnow()
    }
    
    res = db.writing_submissions.insert_one(submission_doc)
    log_user_activity(current_user.id, "writing", f"Writing {task_type} topshirildi", f"AI Bahosi: Band {eval_result.get('overall_band')}")
    
    return redirect(url_for('writing.result', submission_id=str(res.inserted_id)))

@writing_bp.route('/result/<submission_id>')
@login_required
def result(submission_id):
    db = get_db()
    sub = db.writing_submissions.find_one({"_id": to_object_id(submission_id)})
    if not sub:
        flash("Topshiriq natijasi topilmadi!", "danger")
        return redirect(url_for('writing.index'))
        
    return render_template('writing/result.html', submission=sub)
