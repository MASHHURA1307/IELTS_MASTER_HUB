import os
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from config import Config
from utils.db import init_db, User
from utils.helpers import format_uzbek_date
from datetime import datetime, timezone

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))

    # Ensure required directories exist
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)
    except OSError:
        app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
        app.config['REPORT_FOLDER'] = '/tmp/reports'
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)

    # Initialize Database
    init_db(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Ushbu sahifadan foydalanish uchun tizimga kiring!"
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    # Template Filters & Context Processors
    @app.template_filter('uz_date')
    def uzbek_date_filter(dt):
        return format_uzbek_date(dt)

    @app.context_processor
    def inject_global_vars():
        return {
            'now': datetime.now(timezone.utc) if 'datetime' in globals() else None
        }

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.reading import reading_bp
    from routes.listening import listening_bp
    from routes.writing import writing_bp
    from routes.speaking import speaking_bp
    from routes.grammar import grammar_bp
    from routes.vocabulary import vocab_bp
    from routes.mock_exam import mock_bp
    from routes.ai import ai_bp
    from routes.planner import planner_bp
    from routes.analytics import analytics_bp
    from routes.leaderboard import leaderboard_bp
    from routes.subscription import subscription_bp
    from routes.profile import profile_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(reading_bp)
    app.register_blueprint(listening_bp)
    app.register_blueprint(writing_bp)
    app.register_blueprint(speaking_bp)
    app.register_blueprint(grammar_bp)
    app.register_blueprint(vocab_bp)
    app.register_blueprint(mock_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(planner_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(subscription_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    from datetime import datetime
    app.run(host='0.0.0.0', port=5000, debug=True)
