from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from utils.db import get_db, to_object_id, log_user_activity
from datetime import datetime
import random

vocab_bp = Blueprint('vocabulary', __name__, url_prefix='/vocabulary')

@vocab_bp.route('/')
@login_required
def index():
    db = get_db()
    topic = request.args.get('topic', 'all')
    query = {} if topic == 'all' else {"topic": topic}
    
    words = list(db.vocabulary_words.find(query))
    user_id = to_object_id(current_user.id)
    user_words = list(db.user_vocabulary.find({"user_id": user_id}))
    learned_ids = [str(w.get('word_id')) for w in user_words if w.get('status') == 'learned']
    
    return render_template(
        'vocabulary/index.html',
        words=words,
        learned_ids=learned_ids,
        current_topic=topic,
        learned_count=len(learned_ids),
        total_count=len(words)
    )

@vocab_bp.route('/flashcards')
@login_required
def flashcards():
    db = get_db()
    words = list(db.vocabulary_words.find().limit(20))
    random.shuffle(words)
    return render_template('vocabulary/flashcards.html', words=words)

@vocab_bp.route('/quiz')
@login_required
def quiz():
    db = get_db()
    all_words = list(db.vocabulary_words.find())
    if len(all_words) < 4:
        flash("Quiz uchun yetarli so'zlar topilmadi!", "warning")
        return redirect(url_for('vocabulary.index'))
        
    sample = random.sample(all_words, min(10, len(all_words)))
    quiz_data = []
    
    for w in sample:
        wrong_options = [x.get('meaning_uz') for x in all_words if str(x['_id']) != str(w['_id'])]
        options = random.sample(wrong_options, min(3, len(wrong_options))) + [w.get('meaning_uz')]
        random.shuffle(options)
        
        quiz_data.append({
            "id": str(w['_id']),
            "word": w.get('word'),
            "phonetic": w.get('phonetic', ''),
            "correct_meaning": w.get('meaning_uz'),
            "options": options
        })
        
    return render_template('vocabulary/quiz.html', quiz_data=quiz_data)

@vocab_bp.route('/notebook', methods=['GET', 'POST'])
@login_required
def notebook():
    db = get_db()
    user_id = to_object_id(current_user.id)
    
    if request.method == 'POST':
        word = request.form.get('word', '').strip()
        meaning = request.form.get('meaning', '').strip()
        example = request.form.get('example', '').strip()
        
        if word and meaning:
            db.user_notebook.insert_one({
                "user_id": user_id,
                "word": word,
                "meaning": meaning,
                "example": example,
                "created_at": datetime.utcnow()
            })
            flash(f"'{word}' lug'atingizga qo'shildi!", "success")
            return redirect(url_for('vocabulary.notebook'))
            
    notes = list(db.user_notebook.find({"user_id": user_id}).sort("created_at", -1))
    return render_template('vocabulary/notebook.html', notes=notes)

@vocab_bp.route('/toggle-learned/<word_id>', methods=['POST'])
@login_required
def toggle_learned(word_id):
    db = get_db()
    user_id = to_object_id(current_user.id)
    w_id = to_object_id(word_id)
    
    existing = db.user_vocabulary.find_one({"user_id": user_id, "word_id": w_id})
    if existing:
        new_status = 'learned' if existing.get('status') != 'learned' else 'learning'
        db.user_vocabulary.update_one({"_id": existing['_id']}, {"$set": {"status": new_status, "updated_at": datetime.utcnow()}})
        return jsonify({"status": new_status})
    else:
        db.user_vocabulary.insert_one({"user_id": user_id, "word_id": w_id, "status": 'learned', "updated_at": datetime.utcnow()})
        return jsonify({"status": 'learned'})
