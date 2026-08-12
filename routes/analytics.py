from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from utils.db import get_db, to_object_id

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics_bp.route('/')
@login_required
def index():
    db = get_db()
    user_id = to_object_id(current_user.id)
    
    r_count = db.reading_results.count_documents({"user_id": user_id})
    l_count = db.listening_results.count_documents({"user_id": user_id})
    w_count = db.writing_submissions.count_documents({"user_id": user_id})
    s_count = db.speaking_records.count_documents({"user_id": user_id})
    
    total_tests = r_count + l_count + w_count + s_count
    
    # Calculate estimated accuracy
    r_docs = list(db.reading_results.find({"user_id": user_id}))
    avg_accuracy = round(sum([d.get('correct_count', 0) / max(1, d.get('total_questions', 13)) * 100 for d in r_docs]) / max(1, len(r_docs))) if r_docs else 75
    
    return render_template(
        'analytics/index.html',
        r_count=r_count,
        l_count=l_count,
        w_count=w_count,
        s_count=s_count,
        total_tests=total_tests,
        avg_accuracy=avg_accuracy
    )
