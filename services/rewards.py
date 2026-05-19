from datetime import datetime, date
from core.extensions import db
from core.models import User, Reward, Transaction

def grant_welcome_reward(user, app):
    existing = Reward.query.filter_by(user_id=user.id, type='welcome').first()
    if existing:
        return
    amount = 5.0
    user.balance = round(user.balance + amount, 2)
    reward = Reward(user_id=user.id, type='welcome', amount=amount)
    tx = Transaction(user_id=user.id, type='reward', amount=amount, status='completed', note='Welcome reward')
    db.session.add(reward)
    db.session.add(tx)
    app.logger.info(f'Welcome reward ${amount} granted to {user.username}')

def grant_first_deposit_reward(user, deposit_amount, app):
    existing = Reward.query.filter_by(user_id=user.id, type='first_deposit').first()
    if existing:
        return
    amount = round(deposit_amount * 0.10, 2)
    if amount <= 0:
        return
    user.balance = round(user.balance + amount, 2)
    reward = Reward(user_id=user.id, type='first_deposit', amount=amount)
    tx = Transaction(user_id=user.id, type='reward', amount=amount, status='completed', note='First deposit reward (10%)')
    db.session.add(reward)
    db.session.add(tx)
    app.logger.info(f'First deposit reward ${amount} granted to {user.username}')

def grant_daily_streak_reward(user, app):
    today = date.today()
    if user.last_daily_claim == today:
        return 0
    if user.last_daily_claim and (today - user.last_daily_claim).days == 1:
        user.daily_streak += 1
    else:
        user.daily_streak = 1
    amount = min(user.daily_streak, 5)
    user.last_daily_claim = today
    user.balance = round(user.balance + amount, 2)
    reward = Reward(user_id=user.id, type='daily', amount=amount)
    tx = Transaction(user_id=user.id, type='reward', amount=amount, status='completed', note=f'Daily streak reward (day {user.daily_streak})')
    db.session.add(reward)
    db.session.add(tx)
    app.logger.info(f'Daily streak reward ${amount} (day {user.daily_streak}) for {user.username}')
    return amount

def grant_loyalty_reward(user, app):
    existing_count = Reward.query.filter_by(user_id=user.id, type='loyalty').count()
    days_since_reg = (datetime.utcnow() - user.created_at).days
    eligible_months = days_since_reg // 30
    if eligible_months > existing_count:
        amount = 10.0
        user.balance = round(user.balance + amount, 2)
        reward = Reward(user_id=user.id, type='loyalty', amount=amount)
        tx = Transaction(user_id=user.id, type='reward', amount=amount, status='completed', note=f'Loyalty reward (month {existing_count + 1})')
        db.session.add(reward)
        db.session.add(tx)
        app.logger.info(f'Loyalty reward ${amount} (month {existing_count + 1}) for {user.username}')
