from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from utils.db import get_db, to_object_id, log_user_activity
from datetime import datetime

subscription_bp = Blueprint('subscription', __name__, url_prefix='/subscription')

@subscription_bp.route('/')
@login_required
def index():
    return render_template('subscription/index.html')

@subscription_bp.route('/upgrade', methods=['POST'])
@login_required
def upgrade():
    plan_type = request.form.get('plan_type', 'premium_monthly')
    db = get_db()
    user_id = to_object_id(current_user.id)
    
    # Save subscription and payment simulation
    db.subscriptions.insert_one({
        "user_id": user_id,
        "plan": plan_type,
        "status": "active",
        "start_date": datetime.utcnow(),
        "amount": 99000 if plan_type == 'premium_monthly' else 799000
    })
    
    db.payments.insert_one({
        "user_id": user_id,
        "amount": 99000 if plan_type == 'premium_monthly' else 799000,
        "currency": "UZS",
        "provider": "Payme / Click",
        "status": "completed",
        "created_at": datetime.utcnow()
    })
    
    db.users.update_one({"_id": user_id}, {"$set": {"subscription": "premium"}})
    
    log_user_activity(current_user.id, "subscription", "Premium obuna faollashtirildi", f"Tarif: {plan_type}")
    flash("Tabriklaymiz! Premium obuna muvaffaqiyatli faollashtirildi. Barcha imkoniyatlar ochildi!", "success")
    
    return redirect(url_for('dashboard.index'))
