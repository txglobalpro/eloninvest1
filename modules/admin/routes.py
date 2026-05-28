from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from functools import wraps
from core.extensions import db
from core.models import User, Transaction, Investment, Plan, PaymentMethod, Referral, Reward, NETWORK_OPTIONS, CRYPTO_CURRENCIES
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__, template_folder='../../templates/admin')

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/')
@login_required
@admin_required
def index():
    stats = {
        'total_users': User.query.count(),
        'total_deposits': db.session.query(func.coalesce(func.sum(Transaction.amount), 0)).filter_by(type='deposit', status='completed').scalar(),
        'total_withdrawals': db.session.query(func.coalesce(func.sum(Transaction.amount), 0)).filter_by(type='withdraw', status='completed').scalar(),
        'total_profits': db.session.query(func.coalesce(func.sum(Transaction.amount), 0)).filter_by(type='profit', status='completed').scalar(),
        'pending_withdrawals': Transaction.query.filter_by(type='withdraw', status='pending').count(),
        'pending_deposits': Transaction.query.filter_by(type='deposit', status='pending').count(),
    }
    return render_template('admin/index.html', stats=stats)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users)

@admin_bp.route('/users/<int:user_id>/balance', methods=['POST'])
@login_required
@admin_required
def update_balance(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin.users'))
    amount = float(request.form.get('amount', 0))
    user.balance = round(user.balance + amount, 2)
    tx = Transaction(user_id=user.id, type='adjustment', amount=amount, status='completed', note=f'Admin adjustment by {current_user.username}')
    db.session.add(tx)
    db.session.commit()
    current_app.logger.info(f'Admin {current_user.username} adjusted {user.username}\'s balance by ${amount}')
    flash(f'Balance adjusted by ${amount:.2f}', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/transactions')
@login_required
@admin_required
def transactions():
    all_tx = Transaction.query.order_by(Transaction.created_at.desc()).all()
    return render_template('admin/transactions.html', transactions=all_tx)

@admin_bp.route('/transactions/<int:tx_id>/approve-deposit', methods=['POST'])
@login_required
@admin_required
def approve_deposit(tx_id):
    tx = db.session.get(Transaction, tx_id)
    if not tx or tx.type != 'deposit' or tx.status != 'pending':
        flash('Invalid transaction', 'danger')
        return redirect(url_for('admin.transactions'))
    user = db.session.get(User, tx.user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin.transactions'))
    amount = tx.amount
    user.balance = round(user.balance + amount, 2)
    user.total_deposits = round(user.total_deposits + amount, 2)
    if not user.first_deposit_date:
        user.first_deposit_date = datetime.utcnow()
    from services.referral import distribute_referral_commission
    distribute_referral_commission(user, amount, current_app._get_current_object())
    existing_completed = Transaction.query.filter_by(user_id=user.id, type='deposit', status='completed').count()
    if existing_completed == 0:
        from services.rewards import grant_first_deposit_reward
        grant_first_deposit_reward(user, amount, current_app._get_current_object())
    tx.status = 'completed'
    tx.note = f'Approved by {current_user.username}'
    db.session.commit()
    current_app.logger.info(f'Deposit ${amount} approved for user {user.username}')
    flash(f'Deposit of ${amount:.2f} approved', 'success')
    return redirect(url_for('admin.transactions'))

@admin_bp.route('/transactions/<int:tx_id>/approve-withdraw', methods=['POST'])
@login_required
@admin_required
def approve_withdraw(tx_id):
    tx = db.session.get(Transaction, tx_id)
    if not tx or tx.type != 'withdraw' or tx.status != 'pending':
        flash('Invalid transaction', 'danger')
        return redirect(url_for('admin.transactions'))
    user = db.session.get(User, tx.user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin.transactions'))
    if user.balance < tx.amount:
        flash('Insufficient balance to approve withdrawal', 'danger')
        return redirect(url_for('admin.transactions'))
    user.balance = round(user.balance - tx.amount, 2)
    user.total_withdrawn = round(user.total_withdrawn + tx.amount, 2)
    tx.status = 'completed'
    tx.note = f'Approved by {current_user.username}'
    db.session.commit()
    current_app.logger.info(f'Withdrawal ${tx.amount} approved for user {user.username}')
    flash('Withdrawal approved', 'success')
    return redirect(url_for('admin.transactions'))

@admin_bp.route('/transactions/<int:tx_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_tx(tx_id):
    tx = db.session.get(Transaction, tx_id)
    if not tx or tx.status != 'pending':
        flash('Invalid transaction', 'danger')
        return redirect(url_for('admin.transactions'))
    tx.status = 'rejected'
    tx.note = f'Rejected by {current_user.username}'
    db.session.commit()
    current_app.logger.info(f'Transaction {tx_id} rejected')
    flash('Transaction rejected', 'success')
    return redirect(url_for('admin.transactions'))

@admin_bp.route('/users/<int:user_id>/ban', methods=['POST'])
@login_required
@admin_required
def ban_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin.users'))
    if user.id == current_user.id:
        flash('You cannot ban yourself', 'danger')
        return redirect(url_for('admin.users'))
    user.is_banned = not user.is_banned
    db.session.commit()
    current_app.logger.info(f'Admin {current_user.username} {"banned" if user.is_banned else "unbanned"} user {user.username}')
    flash(f'User {user.username} {"banned" if user.is_banned else "unbanned"}', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin.users'))
    if user.id == current_user.id:
        flash('You cannot delete yourself', 'danger')
        return redirect(url_for('admin.users'))
    name = user.username
    # Delete related records
    Transaction.query.filter_by(user_id=user.id).delete()
    Investment.query.filter_by(user_id=user.id).delete()
    Reward.query.filter_by(user_id=user.id).delete()
    Referral.query.filter_by(referrer_id=user.id).delete()
    Referral.query.filter_by(referred_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    current_app.logger.info(f'Admin {current_user.username} deleted user {name}')
    flash(f'User {name} deleted', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user_detail(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin.users'))
    investments = Investment.query.filter_by(user_id=user.id).order_by(Investment.start_date.desc()).all()
    transactions = Transaction.query.filter_by(user_id=user.id).order_by(Transaction.created_at.desc()).limit(20).all()
    plans = Plan.query.all()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'adjust_balance':
            amount = float(request.form.get('amount', 0))
            user.balance = round(user.balance + amount, 2)
            tx = Transaction(user_id=user.id, type='adjustment', amount=amount, status='completed', note=f'Admin adjustment by {current_user.username}')
            db.session.add(tx)
            current_app.logger.info(f'Admin {current_user.username} adjusted {user.username}\'s balance by ${amount}')
            flash(f'Balance adjusted by ${amount:.2f}', 'success')

        elif action == 'set_balance':
            amount = float(request.form.get('amount', 0))
            user.balance = round(amount, 2)
            current_app.logger.info(f'Admin {current_user.username} set {user.username}\'s balance to ${amount}')
            flash(f'Balance set to ${amount:.2f}', 'success')

        elif action == 'change_password':
            new_pw = request.form.get('new_password', '')
            if len(new_pw) >= 4:
                user.set_password(new_pw)
                current_app.logger.info(f'Admin {current_user.username} changed {user.username}\'s password')
                flash('Password changed successfully', 'success')
            else:
                flash('Password must be at least 4 characters', 'danger')

        elif action == 'set_payment':
            user.payment_method = request.form.get('payment_method', '')
            current_app.logger.info(f'Admin {current_user.username} updated {user.username}\'s payment method')
            flash('Payment method updated', 'success')

        elif action == 'change_plan':
            plan_id = request.form.get('plan_id', type=int)
            inv_id = request.form.get('investment_id', type=int)
            if inv_id and plan_id:
                inv = db.session.get(Investment, inv_id)
                if inv and inv.user_id == user.id:
                    plan = db.session.get(Plan, plan_id)
                    if plan:
                        inv.plan_id = plan_id
                        flash(f'Investment plan changed to {plan.name}', 'success')
                    else:
                        flash('Plan not found', 'danger')
                else:
                    flash('Investment not found', 'danger')

        elif action == 'toggle_admin':
            if user.id == current_user.id:
                flash('You cannot change your own admin status', 'danger')
            else:
                user.is_admin = not user.is_admin
                flash(f'Admin status toggled for {user.username}', 'success')

        elif action == 'verify_email':
            user.email_verified = not user.email_verified
            flash(f'Email verification toggled for {user.username}', 'success')

        elif action == 'approve_kyc':
            if user.kyc_status == 'pending':
                user.kyc_status = 'approved'
                user.kyc_reviewed_at = datetime.utcnow()
                flash(f'KYC approved for {user.username}', 'success')
            else:
                flash('KYC is not pending', 'warning')

        elif action == 'reject_kyc':
            if user.kyc_status == 'pending':
                user.kyc_status = 'rejected'
                user.kyc_reviewed_at = datetime.utcnow()
                user.kyc_review_notes = request.form.get('reject_reason', '')
                flash(f'KYC rejected for {user.username}', 'warning')
            else:
                flash('KYC is not pending', 'warning')

        elif action == 'reset_kyc':
            user.kyc_status = 'none'
            user.kyc_reviewed_at = None
            user.kyc_review_notes = ''
            flash(f'KYC reset for {user.username}', 'info')

        db.session.commit()
        return redirect(url_for('admin.user_detail', user_id=user.id))

    return render_template('admin/user_detail.html', user=user, investments=investments, transactions=transactions, plans=plans)

@admin_bp.route('/plans', methods=['GET', 'POST'])
@login_required
@admin_required
def plans():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            name = request.form.get('name')
            company = request.form.get('company')
            min_amt = float(request.form.get('min_amount', 0))
            max_amt = float(request.form.get('max_amount', 0))
            daily_roi = float(request.form.get('daily_roi', 0)) / 100
            duration = int(request.form.get('duration_days', 0))
            description = request.form.get('description', '')
            if name and company:
                plan = Plan(name=name, company=company, min_amount=min_amt, max_amount=max_amt, daily_roi=daily_roi, duration_days=duration, description=description)
                db.session.add(plan)
                db.session.commit()
                current_app.logger.info(f'Admin {current_user.username} created plan: {name}')
                flash(f'Plan "{name}" created', 'success')
        return redirect(url_for('admin.plans'))
    all_plans = Plan.query.order_by(Plan.id).all()
    return render_template('admin/plans.html', plans=all_plans)

@admin_bp.route('/plans/<int:plan_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit_plan(plan_id):
    plan = db.session.get(Plan, plan_id)
    if not plan:
        flash('Plan not found', 'danger')
        return redirect(url_for('admin.plans'))
    plan.name = request.form.get('name', plan.name)
    plan.company = request.form.get('company', plan.company)
    plan.min_amount = float(request.form.get('min_amount', plan.min_amount))
    plan.max_amount = float(request.form.get('max_amount', plan.max_amount))
    plan.daily_roi = float(request.form.get('daily_roi', plan.daily_roi * 100)) / 100
    plan.duration_days = int(request.form.get('duration_days', plan.duration_days))
    plan.description = request.form.get('description', plan.description)
    db.session.commit()
    current_app.logger.info(f'Admin {current_user.username} edited plan: {plan.name}')
    flash(f'Plan "{plan.name}" updated', 'success')
    return redirect(url_for('admin.plans'))

@admin_bp.route('/plans/<int:plan_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_plan(plan_id):
    plan = db.session.get(Plan, plan_id)
    if not plan:
        flash('Plan not found', 'danger')
        return redirect(url_for('admin.plans'))
    name = plan.name
    db.session.delete(plan)
    db.session.commit()
    current_app.logger.info(f'Admin {current_user.username} deleted plan: {name}')
    flash(f'Plan "{name}" deleted', 'success')
    return redirect(url_for('admin.plans'))

@admin_bp.route('/payment-methods', methods=['GET', 'POST'])
@login_required
@admin_required
def payment_methods():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            pm = PaymentMethod(
                type=request.form.get('type'),
                label=request.form.get('label'),
                details=request.form.get('details', ''),
                is_active=True
            )
            db.session.add(pm)
            db.session.commit()
            current_app.logger.info(f'Admin {current_user.username} added payment method: {pm.label}')
            flash(f'Payment method "{pm.label}" added', 'success')
        elif action == 'toggle':
            pm = db.session.get(PaymentMethod, int(request.form.get('pm_id', 0)))
            if pm:
                pm.is_active = not pm.is_active
                db.session.commit()
                flash(f'Payment method "{pm.label}" toggled', 'success')
        return redirect(url_for('admin.payment_methods'))
    methods = PaymentMethod.query.order_by(PaymentMethod.id).all()
    return render_template('admin/payment_methods.html', methods=methods, network_options=NETWORK_OPTIONS, crypto_currencies=CRYPTO_CURRENCIES)

@admin_bp.route('/payment-methods/<int:pm_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit_payment_method(pm_id):
    pm = db.session.get(PaymentMethod, pm_id)
    if not pm:
        flash('Payment method not found', 'danger')
        return redirect(url_for('admin.payment_methods'))
    pm.type = request.form.get('type', pm.type)
    pm.label = request.form.get('label', pm.label)
    pm.details = request.form.get('details', pm.details)
    db.session.commit()
    flash(f'Payment method "{pm.label}" updated', 'success')
    return redirect(url_for('admin.payment_methods'))

@admin_bp.route('/payment-methods/<int:pm_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_payment_method(pm_id):
    pm = db.session.get(PaymentMethod, pm_id)
    if not pm:
        flash('Payment method not found', 'danger')
        return redirect(url_for('admin.payment_methods'))
    label = pm.label
    db.session.delete(pm)
    db.session.commit()
    flash(f'Payment method "{label}" deleted', 'success')
    return redirect(url_for('admin.payment_methods'))
