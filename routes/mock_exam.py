import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, current_app
from flask_login import login_required, current_user
from utils.db import get_db, to_object_id, log_user_activity
from utils.helpers import calculate_overall_band
from utils.pdf_generator import generate_mock_exam_pdf
from datetime import datetime

mock_bp = Blueprint('mock_exam', __name__, url_prefix='/mock-exam')

@mock_bp.route('/')
@login_required
def index():
    db = get_db()
    mocks = list(db.mock_tests.find())
    results = list(db.mock_results.find({"user_id": to_object_id(current_user.id)}).sort("created_at", -1))
    
    return render_template('mock_exam/index.html', mocks=mocks, results=results)

@mock_bp.route('/start/<mock_id>')
@login_required
def start_test(mock_id):
    db = get_db()
    mock = db.mock_tests.find_one({"_id": to_object_id(mock_id)})
    if not mock:
        flash("Mock imtihon topilmadi!", "danger")
        return redirect(url_for('mock_exam.index'))
        
    return render_template('mock_exam/test.html', mock=mock)

@mock_bp.route('/submit/<mock_id>', methods=['POST'])
@login_required
def submit_mock(mock_id):
    db = get_db()
    mock = db.mock_tests.find_one({"_id": to_object_id(mock_id)})
    
    # Calculate section scores from submitted inputs
    listening_band = float(request.form.get('listening_band', 6.0))
    reading_band = float(request.form.get('reading_band', 6.5))
    writing_band = float(request.form.get('writing_band', 6.0))
    speaking_band = float(request.form.get('speaking_band', 7.0))
    
    overall = calculate_overall_band(listening_band, reading_band, writing_band, speaking_band)
    
    mock_result_doc = {
        "user_id": to_object_id(current_user.id),
        "mock_id": to_object_id(mock_id) if mock else None,
        "title": mock.get('title') if mock else "IELTS Full Mock Simulation",
        "listening_band": listening_band,
        "reading_band": reading_band,
        "writing_band": writing_band,
        "speaking_band": speaking_band,
        "overall_band": overall,
        "completed_at": datetime.utcnow()
    }
    
    res = db.mock_results.insert_one(mock_result_doc)
    log_user_activity(current_user.id, "mock", "Full Mock Exam topshirildi", f"Natija: Overall Band {overall}")
    
    # Update current user score
    db.users.update_one({"_id": to_object_id(current_user.id)}, {"$set": {"current_band": overall}})
    
    return redirect(url_for('mock_exam.result', result_id=str(res.inserted_id)))

@mock_bp.route('/result/<result_id>')
@login_required
def result(result_id):
    db = get_db()
    res_doc = db.mock_results.find_one({"_id": to_object_id(result_id)})
    if not res_doc:
        flash("Natija topilmadi!", "danger")
        return redirect(url_for('mock_exam.index'))
        
    return render_template('mock_exam/result.html', result=res_doc)

@mock_bp.route('/download-pdf/<result_id>')
@login_required
def download_pdf(result_id):
    db = get_db()
    res_doc = db.mock_results.find_one({"_id": to_object_id(result_id)})
    if not res_doc:
        flash("Natija topilmadi!", "danger")
        return redirect(url_for('mock_exam.index'))
        
    report_folder = current_app.config['REPORT_FOLDER']
    filename = os.path.join(report_folder, f"mock_certificate_{result_id}.pdf")
    
    generate_mock_exam_pdf(filename, current_user.full_name, res_doc)
    
    return send_file(
        filename,
        as_attachment=True,
        download_name=f"IELTS_Certificate_{current_user.full_name.replace(' ', '_')}.pdf",
        mimetype="application/pdf"
    )
