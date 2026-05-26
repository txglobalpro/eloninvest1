from datetime import datetime
import secrets, threading
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from core.extensions import db, mail
from core.models import User, Referral, Reward, Transaction
from core.forms import LoginForm, RegisterForm
from services.rewards import grant_welcome_reward

auth_bp = Blueprint('auth', __name__, template_folder='../../templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            user.last_login = datetime.utcnow()
            user.last_login_ip = request.remote_addr or ''
            db.session.commit()
            current_app.logger.info(f'User {user.username} logged in')
            if not user.email_verified:
                flash('Please verify your email address to access all features.', 'warning')
            return redirect(url_for('user.dashboard'))
        flash('Invalid email or password', 'danger')
    return render_template('auth/login.html', form=form)

def _verification_html_email(user, verify_url):
    return f'''<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  body{{margin:0;padding:0;background-color:#070b1a;font-family:'Segoe UI',Arial,sans-serif}}
  table{{border-spacing:0}}
  td{{padding:0}}
  img{{border:0;display:block}}
  .wrapper{{width:100%;table-layout:fixed;background-color:#070b1a;padding-bottom:40px}}
  .main{{background-color:#0f1729;margin:0 auto;width:100%;max-width:560px;border-spacing:0;border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,0.06)}}
  .header-cell{{padding:32px 32px 24px;text-align:center;background:linear-gradient(135deg,#0f1729 0%,#162a50 100%)}}
  .logo{{font-size:26px;font-weight:800;letter-spacing:1px;color:#f0b90b;text-decoration:none}}
  .body-cell{{padding:0 32px 32px}}
  h1{{font-size:22px;font-weight:700;color:#e2e8f0;margin:0 0 8px;text-align:center}}
  p{{font-size:15px;line-height:1.6;color:#94a3b8;margin:0 0 20px;text-align:center}}
  .btn{{display:inline-block;padding:14px 40px;background:linear-gradient(135deg,#f0b90b,#f5c842);color:#070b1a;font-size:16px;font-weight:700;text-decoration:none;border-radius:10px;letter-spacing:0.5px;margin:8px 0 24px}}
  .divider{{height:1px;background:rgba(255,255,255,0.06);margin:24px 0}}
  .note{{font-size:12px;color:rgba(255,255,255,0.35);line-height:1.5;margin:0;text-align:center}}
  .footer-text{{font-size:12px;color:rgba(255,255,255,0.3);text-align:center;padding:16px 32px 0}}
  .footer-text a{{color:rgba(255,255,255,0.3);text-decoration:underline}}
</style>
</head>
<body><table class="wrapper" cellpadding="0" cellspacing="0"><tr><td>
<table class="main" cellpadding="0" cellspacing="0">
  <tr><td class="header-cell">
    <a class="logo" href="{url_for('index', _external=True)}">⚡ ElonInvest</a>
  </td></tr>
  <tr><td class="body-cell">
    <h1>Verify Your Email Address</h1>
    <p>Thanks for joining ElonInvest! Please confirm your email address by clicking the button below to activate your account and unlock all features.</p>
    <table cellpadding="0" cellspacing="0" style="margin:0 auto"><tr><td style="text-align:center">
      <a class="btn" href="{verify_url}">Verify Email Address</a>
    </td></tr></table>
    <div class="divider"></div>
    <p class="note">If you didn't create this account, you can safely ignore this email.<br>
    This link expires once used. Need help? Contact our support team.</p>
  </td></tr>
</table>
<p class="footer-text">&copy; 2015 ElonInvest &mdash; All rights reserved.<br>
<a href="{url_for('index', _external=True)}">ElonInvest</a></p>
</td></tr></table></body>
</html>'''

def send_verification_email(user):
    token = user.verification_token or secrets.token_urlsafe(32)
    user.verification_token = token
    db.session.commit()
    verify_url = url_for('auth.verify_email', token=token, _external=True)
    app = current_app._get_current_object()
    try:
        msg = Message('Verify your email - ElonInvest',
                      recipients=[user.email])
        msg.body = f'''Welcome to ElonInvest!

Please verify your email address by clicking the link below:

{verify_url}

If you did not create an account, please ignore this email.

- ElonInvest Team'''
        msg.html = _verification_html_email(user, verify_url)
        threading.Thread(target=_send_email_async, args=(app, msg), daemon=True).start()
    except Exception as e:
        current_app.logger.error(f'Failed to create verification email: {e}')
    return verify_url

def _send_email_async(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            app.logger.info(f'Verification email sent')
        except Exception as e:
            app.logger.error(f'Async email failed: {e}')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    form = RegisterForm()
    current_app.logger.info('REGISTER: form created')
    ref_code = request.args.get('ref')
    if ref_code:
        form.referral_code.data = ref_code
    if request.method == 'POST':
        current_app.logger.info('REGISTER: POST received')
    if form.validate_on_submit():
        current_app.logger.info('REGISTER: form valid')
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.email_verified = True
        current_app.logger.info('REGISTER: password set')
        if form.referral_code.data:
            referrer = User.query.filter_by(referral_code=form.referral_code.data).first()
            if referrer:
                user.referred_by_id = referrer.id
        current_app.logger.info('REGISTER: referral set')
        db.session.add(user)
        db.session.commit()
        current_app.logger.info('REGISTER: user committed')
        if user.referred_by_id:
            ref = Referral(referrer_id=user.referred_by_id, referred_id=user.id, level=1, commission=0)
            db.session.add(ref)
            db.session.commit()
        current_app.logger.info('REGISTER: referral record created')
        try:
            user.balance = round(user.balance + 5.0, 2)
            reward = Reward(user_id=user.id, type='welcome', amount=5.0)
            tx = Transaction(user_id=user.id, type='reward', amount=5.0, status='completed', note='Welcome reward')
            db.session.add(reward)
            db.session.add(tx)
            db.session.commit()
            current_app.logger.info('REGISTER: welcome reward granted')
        except Exception as e:
            current_app.logger.error(f'REGISTER: reward error: {e}')
        current_app.logger.info(f'REGISTER: new user created: {user.username}')
        flash('Registration successful! Welcome to ElonInvest.', 'success')
        login_user(user)
        current_app.logger.info('REGISTER: user logged in')
        return redirect(url_for('user.dashboard'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/verify/<token>')
def verify_email(token):
    user = User.query.filter_by(verification_token=token).first()
    if not user:
        return render_template('auth/verify_failed.html', reason='invalid')
    user.email_verified = True
    user.verification_token = None
    db.session.commit()
    current_app.logger.info(f'Email verified for user: {user.username}')
    return render_template('auth/verify_success.html')

@auth_bp.route('/resend-verification')
@login_required
def resend_verification():
    if current_user.email_verified:
        flash('Your email is already verified.', 'info')
        return redirect(url_for('user.dashboard'))
    send_verification_email(current_user)
    flash('A new verification link has been sent to your email.', 'info')
    return redirect(url_for('user.profile'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
