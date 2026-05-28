from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from core.extensions import db, verified_required
from core.models import Plan, Investment, Transaction, PaymentMethod, NETWORK_OPTIONS, Referral, Reward
from services.crypto_payment import CryptoVerifier

investment_bp = Blueprint('investment', __name__, template_folder='../../templates/investment')

@investment_bp.route('/plans')
@login_required
def plans():
    all_plans = Plan.query.all()
    return render_template('investment/plans.html', plans=all_plans)

@investment_bp.route('/subscribe/<int:plan_id>', methods=['POST'])
@login_required
@verified_required
def subscribe(plan_id):
    plan = db.session.get(Plan, plan_id)
    if not plan:
        flash('Plan not found', 'danger')
        return redirect(url_for('investment.plans'))

    amount = float(request.form.get('amount', 0))
    if amount < plan.min_amount or amount > plan.max_amount:
        flash(f'Amount must be between ${plan.min_amount:.0f} and ${plan.max_amount:.0f}', 'danger')
        return redirect(url_for('investment.plans'))

    if current_user.balance < amount:
        flash('Insufficient balance', 'danger')
        return redirect(url_for('investment.plans'))

    current_user.balance -= amount
    current_user.total_invested = round(current_user.total_invested + amount, 2)
    end_date = datetime.utcnow() + timedelta(days=plan.duration_days)
    inv = Investment(user_id=current_user.id, plan_id=plan_id, amount=amount, end_date=end_date)
    tx = Transaction(user_id=current_user.id, type='investment', amount=amount, status='completed', note=f'Subscribed to {plan.name}')
    db.session.add(inv)
    db.session.add(tx)
    db.session.commit()
    current_app.logger.info(f'User {current_user.username} invested ${amount} in {plan.name}')
    flash(f'Successfully invested ${amount:.2f} in {plan.name}!', 'success')
    return redirect(url_for('user.dashboard'))

@investment_bp.route('/deposit', methods=['GET', 'POST'])
@login_required
@verified_required
def deposit():
    if request.method == 'POST':
        amount = float(request.form.get('amount', 0))
        pm_id = request.form.get('payment_method_id', type=int)
        use_trustwallet = request.form.get('use_trustwallet') == '1'
        txid = request.form.get('txid', '').strip()
        if amount <= 0:
            flash('Invalid amount', 'danger')
            return redirect(url_for('investment.deposit'))

        if use_trustwallet:
            if not txid:
                flash('Please enter the transaction hash (TXID) from your Trust Wallet', 'danger')
                return redirect(url_for('investment.deposit'))
            wallet = current_app.config.get('PLATFORM_USDT_TRC20', '')
            result = CryptoVerifier.verify_txid(txid, 'TRC-20', wallet, amount)
            if not result['valid']:
                flash(f'Verification failed: {result.get("error", "Unknown error")}', 'danger')
                return redirect(url_for('investment.deposit'))
            tx = Transaction(
                user_id=current_user.id, type='deposit', amount=amount,
                status='completed', note=f'Trust Wallet auto-verified',
                crypto_currency='USDT', crypto_network='TRC-20', txid=txid
            )
            user = current_user
            user.balance = round(user.balance + amount, 2)
            user.total_deposits = round(user.total_deposits + amount, 2)
            if not user.first_deposit_date:
                user.first_deposit_date = datetime.utcnow()
            db.session.add(tx)
            db.session.commit()
            try:
                from services.referral import distribute_referral_commission
                app = current_app._get_current_object()
                distribute_referral_commission(user, amount, app)
                existing = Transaction.query.filter_by(user_id=user.id, type='deposit', status='completed').count()
                if existing == 1:
                    from services.rewards import grant_first_deposit_reward
                    grant_first_deposit_reward(user, amount, app)
            except Exception as e:
                current_app.logger.error(f'Post-deposit processing error: {e}')
            current_app.logger.info(f'User {user.username} auto-deposited ${amount} via Trust Wallet (TXID: {txid[:20]}...)')
            flash(f'Deposit of ${amount:.2f} confirmed and credited!', 'success')
            return redirect(url_for('user.dashboard'))

        pm = db.session.get(PaymentMethod, pm_id) if pm_id else None
        pm_label = pm.label if pm else 'N/A'
        tx = Transaction(user_id=current_user.id, type='deposit', amount=amount, status='pending', note=f'Deposit via {pm_label}')
        db.session.add(tx)
        db.session.commit()
        current_app.logger.info(f'User {current_user.username} submitted deposit request ${amount} via {pm_label}')
        flash('Deposit request submitted. Awaiting admin approval.', 'success')
        return redirect(url_for('user.dashboard'))
    payment_methods = PaymentMethod.query.filter_by(is_active=True).all()
    wallet = current_app.config.get('PLATFORM_USDT_TRC20', '')
    return render_template('investment/deposit.html', payment_methods=payment_methods, wallet_address=wallet)

@investment_bp.route('/withdraw', methods=['GET', 'POST'])
@login_required
@verified_required
def withdraw():
    if request.method == 'POST':
        amount = float(request.form.get('amount', 0))
        if amount <= 0 or amount > current_user.balance:
            flash('Invalid amount or insufficient balance', 'danger')
            return redirect(url_for('investment.withdraw'))

        if current_user.total_deposits <= 0:
            flash('You must make a deposit before withdrawing.', 'warning')
            return redirect(url_for('investment.withdraw'))
        if current_user.first_deposit_date:
            days_since = (datetime.utcnow() - current_user.first_deposit_date).days
            if days_since < 15:
                flash(f'Withdrawal available after 15 days from first deposit. {15 - days_since} days remaining.', 'warning')
                return redirect(url_for('investment.withdraw'))

        withdraw_method = request.form.get('withdraw_method', '').strip()
        withdraw_network = request.form.get('withdraw_network', '').strip()
        withdraw_address = request.form.get('withdraw_address', '').strip()

        if not withdraw_method or not withdraw_address:
            flash('Please select a payment method and enter your wallet address', 'danger')
            return redirect(url_for('investment.withdraw'))

        tx = Transaction(
            user_id=current_user.id, type='withdraw', amount=amount,
            status='pending', note='Withdrawal request',
            withdraw_method=withdraw_method, withdraw_network=withdraw_network,
            withdraw_address=withdraw_address
        )
        db.session.add(tx)
        db.session.commit()
        current_app.logger.info(f'User {current_user.username} requested withdrawal of ${amount} via {withdraw_method} ({withdraw_network}) to {withdraw_address[:12]}...')
        flash('Withdrawal request submitted. Awaiting admin approval.', 'success')
        return redirect(url_for('user.dashboard'))
    payment_methods = PaymentMethod.query.filter_by(is_active=True).all()
    return render_template('investment/withdraw.html', payment_methods=payment_methods, network_options=NETWORK_OPTIONS)

@investment_bp.route('/history')
@login_required
def history():
    investments = Investment.query.filter_by(user_id=current_user.id).order_by(Investment.start_date.desc()).all()
    return render_template('investment/history.html', investments=investments)
