from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from core.extensions import db
from core.models import Investment, Transaction, Referral

user_bp = Blueprint('user', __name__, template_folder='../../templates/user')

@user_bp.route('/dashboard')
@login_required
def dashboard():
    investments = Investment.query.filter_by(user_id=current_user.id, status='active').order_by(Investment.start_date.desc()).all()
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).limit(10).all()
    pending_withdrawals = Transaction.query.filter_by(user_id=current_user.id, type='withdraw', status='pending').count()
    pending_deposits = Transaction.query.filter_by(user_id=current_user.id, type='deposit', status='pending').count()
    total_invested = current_user.total_invested or 0
    return render_template('user/dashboard.html', investments=investments, transactions=transactions, pending_withdrawals=pending_withdrawals, pending_deposits=pending_deposits, total_invested=total_invested, now=datetime.utcnow())

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.payment_method = request.form.get('payment_method', current_user.payment_method)
        current_user.lang = request.form.get('lang', current_user.lang)
        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('user.profile'))
    referrals_count = Referral.query.filter_by(referrer_id=current_user.id).count()
    investments_count = Investment.query.filter_by(user_id=current_user.id).count()
    transactions_count = Transaction.query.filter_by(user_id=current_user.id).count()
    return render_template('user/profile.html', referrals_count=referrals_count, investments_count=investments_count, transactions_count=transactions_count)
