from flask import Flask, session, request, render_template
from config import Config
from core.extensions import db, login_manager, mail, migrate
from core.logger import setup_logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    setup_logging(app)

    from modules.auth.routes import auth_bp
    from modules.user.routes import user_bp
    from modules.investment.routes import investment_bp
    from modules.referral.routes import referral_bp
    from modules.rewards.routes import rewards_bp
    from modules.market.routes import market_bp
    from modules.admin.routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(investment_bp, url_prefix='/investment')
    app.register_blueprint(referral_bp, url_prefix='/referral')
    app.register_blueprint(rewards_bp, url_prefix='/rewards')
    app.register_blueprint(market_bp, url_prefix='/market')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('pages/about.html')

    @app.route('/privacy')
    def privacy():
        return render_template('pages/privacy.html')

    @app.route('/terms')
    def terms():
        return render_template('pages/terms.html')

    @app.route('/api/chatbot', methods=['POST'])
    def chatbot():
        from modules.chatbot import get_response
        from flask import request, jsonify
        data = request.get_json()
        msg = (data or {}).get('message', '').strip()
        agent = (data or {}).get('agent')
        if not msg:
            return jsonify({'reply': 'Please type a message.' if session.get('lang', 'en') == 'en' else 'الرجاء كتابة رسالة.', 'agent': agent or {'name': 'Support', 'role': ''}, 'typing_delay': 300})
        result = get_response(msg, agent)
        return jsonify(result)

    @app.before_request
    def before_request():
        lang = request.args.get('lang')
        if lang and lang in ['en', 'ar']:
            session['lang'] = lang
        if 'lang' not in session:
            session['lang'] = 'en'

    @app.context_processor
    def inject_globals():
        lang = session.get('lang', 'en')
        from core.i18n import _
        def t(text):
            return _(text, lang)
        telegram_url = app.config.get('TELEGRAM_CHANNEL_URL', 'https://t.me/eloniinvest')
        social_links = [
            {'key': 'telegram', 'url': telegram_url, 'icon': 'bi-telegram', 'label': 'Telegram', 'color': '#08c'},
            {'key': 'website', 'url': app.config.get('WEBSITE_URL', '#'), 'icon': 'bi-globe2', 'label': 'Website', 'color': '#f0b90b'},
        ]
        chat_agents_en = [
            {'name': 'Sarah', 'role': 'Senior Support'},
            {'name': 'Adam', 'role': 'Support Specialist'},
            {'name': 'Layla', 'role': 'Client Relations'},
            {'name': 'Omar', 'role': 'Technical Support'},
            {'name': 'Emma', 'role': 'Account Manager'},
            {'name': 'Yousef', 'role': 'Investment Advisor'},
        ]
        chat_agents_ar = [
            {'name': 'سارة', 'role': 'دعم أول'},
            {'name': 'آدم', 'role': 'أخصائي دعم'},
            {'name': 'ليلى', 'role': 'علاقات العملاء'},
            {'name': 'عمر', 'role': 'دعم فني'},
            {'name': 'إيما', 'role': 'مدير حسابات'},
            {'name': 'يوسف', 'role': 'مستشار استثمار'},
        ]
        return {'lang': lang, 't': t, 'telegram_url': telegram_url, 'social_links': social_links,
                'chat_agents': chat_agents_en if lang == 'en' else chat_agents_ar}

    from tasks import init_scheduler
    init_scheduler(app)

    from core.i18n import load_translations, _
    load_translations()
    app.jinja_env.globals.update(_t=_)

    with app.app_context():
        from core import models
        db.create_all()
        from core.models import User, Plan, PaymentMethod
        if not User.query.filter_by(is_admin=True).first():
            admin = User(username='admin', email='admin@eloninvest.com', is_admin=True, email_verified=True)
            admin.set_password('admin123')
            db.session.add(admin)
            app.logger.info('Default admin created: admin@eloninvest.com / admin123')
        if not Plan.query.first():
            plans = [
                Plan(name='Tesla Starter', company='Tesla', min_amount=10, max_amount=100, daily_roi=0.02, duration_days=30),
                Plan(name='SpaceX Voyager', company='SpaceX', min_amount=50, max_amount=500, daily_roi=0.035, duration_days=45),
                Plan(name='Neuralink Pioneer', company='Neuralink', min_amount=100, max_amount=1000, daily_roi=0.05, duration_days=60),
                Plan(name='X Premium', company='X', min_amount=200, max_amount=2000, daily_roi=0.065, duration_days=75),
                Plan(name='Boring Elite', company='The Boring Company', min_amount=500, max_amount=5000, daily_roi=0.08, duration_days=90),
            ]
            for p in plans:
                db.session.add(p)
            app.logger.info('Investment plans seeded')
        if not PaymentMethod.query.filter_by(label='USDT').first():
            db.session.add(PaymentMethod(
                type='crypto',
                label='USDT',
                details='Deposit Address: TTYdsoYhYabq9e4kByamzACpYj5PzP3Q5e\nNetwork: TRX\nMin Deposit: $0',
                is_active=True
            ))
            app.logger.info('USDT payment method seeded')
        db.session.commit()

    return app

app = create_app()
