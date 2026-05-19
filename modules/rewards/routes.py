from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from core.extensions import db, verified_required
from core.models import Reward
from services.rewards import grant_daily_streak_reward, grant_loyalty_reward

rewards_bp = Blueprint('rewards', __name__, template_folder='../../templates/rewards')

@rewards_bp.route('/')
@login_required
@verified_required
def index():
    grant_loyalty_reward(current_user, current_app._get_current_object())
    db.session.commit()
    claimed = {
        'welcome': Reward.query.filter_by(user_id=current_user.id, type='welcome').first() is not None,
        'first_deposit': Reward.query.filter_by(user_id=current_user.id, type='first_deposit').first() is not None,
        'loyalty': Reward.query.filter_by(user_id=current_user.id, type='loyalty').first() is not None,
    }
    rewards = Reward.query.filter_by(user_id=current_user.id).order_by(Reward.claimed_at.desc()).all()
    daily_amount = min(current_user.daily_streak + 1, 5) if current_user.last_daily_claim else 1
    from datetime import date
    if current_user.last_daily_claim == date.today():
        daily_amount = min(current_user.daily_streak, 5)
    return render_template('rewards/index.html', claimed=claimed, rewards=rewards, daily_amount=daily_amount)

@rewards_bp.route('/claim-daily', methods=['POST'])
@login_required
@verified_required
def claim_daily():
    amount = grant_daily_streak_reward(current_user, current_app._get_current_object())
    db.session.commit()
    if amount > 0:
        flash(f'Daily reward claimed: ${amount:.2f}!', 'success')
    else:
        flash('Already claimed today. Come back tomorrow!', 'info')
    return redirect(url_for('rewards.index'))
