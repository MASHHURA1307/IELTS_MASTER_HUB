from flask import Blueprint, render_template
from flask_login import login_required
from utils.db import get_db

leaderboard_bp = Blueprint('leaderboard', __name__, url_prefix='/leaderboard')

@leaderboard_bp.route('/')
@login_required
def index():
    db = get_db()
    
    # Top users by band score
    top_band = list(db.users.find().sort("current_band", -1).limit(10))
    # Top users by streak
    top_streak = list(db.users.find().sort("streak", -1).limit(10))
    # Highest mock exam scores
    mock_leaders = list(db.mock_results.find().sort("overall_band", -1).limit(10))
    
    return render_template(
        'leaderboard/index.html',
        top_band=top_band,
        top_streak=top_streak,
        mock_leaders=mock_leaders
    )
