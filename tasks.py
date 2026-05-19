from apscheduler.schedulers.background import BackgroundScheduler
from services.profit import distribute_daily_profits

scheduler = BackgroundScheduler()

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
        scheduler.start()
        app.logger.info('Scheduler started: daily profits job registered')
