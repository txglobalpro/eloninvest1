from datetime import datetime
from flask import has_app_context
from core.extensions import db
from core.models import Investment, Transaction, User

def _run_profits(app):
    investments = Investment.query.filter_by(status='active').all()
    now = datetime.utcnow()
    count = 0
    for inv in investments:
        end = inv.end_date.replace(tzinfo=None) if inv.end_date else None
        if end and now >= end:
            inv.status = 'completed'
            db.session.commit()
            app.logger.info(f'Investment {inv.id} completed')
            continue

        profit = round(inv.amount * inv.plan.daily_roi, 2)
        if profit <= 0:
            continue

        user = db.session.get(User, inv.user_id)
        if not user:
            continue

        user.balance = round(user.balance + profit, 2)
        user.total_profit = round(user.total_profit + profit, 2)
        tx = Transaction(user_id=user.id, type='profit', amount=profit, status='completed',
                        note=f'Daily profit from {inv.plan.name}')
        db.session.add(tx)
        count += 1

    if count > 0:
        db.session.commit()
        app.logger.info(f'Distributed daily profits to {count} investments')

def distribute_daily_profits(app):
    if has_app_context():
        _run_profits(app)
    else:
        with app.app_context():
            _run_profits(app)
