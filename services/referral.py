from core.extensions import db
from core.models import User, Referral, Transaction

COMMISSION_LEVELS = {1: 0.05, 2: 0.03, 3: 0.02}

def distribute_referral_commission(user, deposit_amount, app):
    levels = {}
    current = user
    for level in range(1, 4):
        if current.referred_by_id:
            referrer = db.session.get(User, current.referred_by_id)
            if referrer:
                levels[level] = referrer
                current = referrer
            else:
                break
        else:
            break

    for level, referrer in levels.items():
        commission = round(deposit_amount * COMMISSION_LEVELS[level], 2)
        if commission <= 0:
            continue
        referrer.balance = round(referrer.balance + commission, 2)
        ref = Referral(referrer_id=referrer.id, referred_id=user.id, level=level, commission=commission)
        tx = Transaction(user_id=referrer.id, type='referral', amount=commission, status='completed',
                        note=f'Level {level} commission from {user.username}\'s deposit')
        db.session.add(ref)
        db.session.add(tx)
        app.logger.info(f'Referral commission: ${commission} (level {level}) to {referrer.username}')
