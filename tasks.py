from apscheduler.schedulers.background import BackgroundScheduler
from services.profit import distribute_daily_profits

scheduler = BackgroundScheduler()

def post_daily_news(app):
    from modules.telegram_bot import run_daily_news
    run_daily_news(app)

def init_scheduler(app):
    if not scheduler.running:
        scheduler.add_job(
            func=lambda: distribute_daily_profits(app),
            trigger='interval',
            hours=24,
            id='daily_profits',
            name='Distribute daily investment profits',
            replace_existing=True
        )
        scheduler.add_job(
            func=lambda: post_daily_news(app),
            trigger='interval',
            hours=24,
            id='daily_news',
            name='Post Elon Musk news to Telegram',
            replace_existing=True
        )
        scheduler.start()
        app.logger.info('Scheduler started: daily profits + Telegram news jobs registered')
