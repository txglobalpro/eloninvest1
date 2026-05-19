from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from core.extensions import db, verified_required
from core.models import Referral
from sqlalchemy import func

referral_bp = Blueprint('referral', __name__, template_folder='../../templates/referral')

@referral_bp.route('/')
@login_required
@verified_required
def index():
    referrals = Referral.query.filter_by(referrer_id=current_user.id).order_by(Referral.created_at.desc()).all()
    stats = {
        'level1': Referral.query.filter_by(referrer_id=current_user.id, level=1).count(),
        'level2': Referral.query.filter_by(referrer_id=current_user.id, level=2).count(),
        'level3': Referral.query.filter_by(referrer_id=current_user.id, level=3).count(),
        'total_commission': db.session.query(func.coalesce(func.sum(Referral.commission), 0)).filter_by(referrer_id=current_user.id).scalar()
    }
    return render_template('referral/index.html', referrals=referrals, stats=stats)
