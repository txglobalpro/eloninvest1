from apscheduler.schedulers.background import BackgroundScheduler
from services.profit import distribute_daily_profits

scheduler = BackgroundScheduler()

def post_telegram_content(app):
    from modules.telegram_bot import run_auto_poster
    run_auto_poster(app)

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
            func=lambda: post_telegram_content(app),
            trigger='interval',
            hours=1,
            id='telegram_auto_poster',
            name='Auto-post content to Telegram every hour',
            replace_existing=True
        )
        scheduler.start()
        app.logger.info('Scheduler started: daily profits + hourly Telegram content poster')
