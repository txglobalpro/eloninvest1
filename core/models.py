import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from core.extensions import db, login_manager

def gen_uuid():
    return uuid.uuid4().hex[:16]

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    total_profit = db.Column(db.Float, default=0.0)
    total_deposits = db.Column(db.Float, default=0.0)
    total_withdrawn = db.Column(db.Float, default=0.0)
    total_invested = db.Column(db.Float, default=0.0)
    email_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(64), nullable=True)
    referral_code = db.Column(db.String(16), unique=True, default=gen_uuid)
    referred_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    first_deposit_date = db.Column(db.DateTime, nullable=True)
    daily_streak = db.Column(db.Integer, default=0)
    last_daily_claim = db.Column(db.Date, nullable=True)
    lang = db.Column(db.String(2), default='en')
    payment_method = db.Column(db.Text, default='')
    kyc_status = db.Column(db.String(20), default='none')
    kyc_country = db.Column(db.String(100), default='')
    kyc_dob = db.Column(db.String(10), default='')
    kyc_age = db.Column(db.Integer, nullable=True)
    kyc_phone = db.Column(db.String(30), default='')
    kyc_id_path = db.Column(db.String(255), default='')
    kyc_submitted_at = db.Column(db.DateTime, nullable=True)
    kyc_reviewed_at = db.Column(db.DateTime, nullable=True)
    kyc_review_notes = db.Column(db.Text, default='')
    last_login_ip = db.Column(db.String(45), default='')
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())
    last_login = db.Column(db.DateTime, default=lambda: datetime.utcnow())

    referred_by = db.relationship('User', remote_side=[id], backref='referrals')

    @property
    def is_active(self):
        return not self.is_banned

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(80), nullable=False)
    min_amount = db.Column(db.Float, nullable=False)
    max_amount = db.Column(db.Float, nullable=False)
    daily_roi = db.Column(db.Float, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, default='')

NETWORK_OPTIONS = {
    'USDT': ['TRC-20', 'ERC-20', 'BEP-20'],
    'BTC': ['Bitcoin (BTC)'],
    'ETH': ['ERC-20'],
    'LTC': ['Litecoin'],
    'BNB': ['BEP-20', 'BEP-2'],
    'XRP': ['XRP Ledger'],
    'SOL': ['Solana'],
    'TRX': ['TRC-20'],
    'USDC': ['ERC-20', 'TRC-20', 'BEP-20'],
    'ADA': ['Cardano'],
    'DOT': ['Polkadot'],
    'DOGE': ['Dogecoin'],
    'MATIC': ['Polygon'],
    'AVAX': ['Avalanche C-Chain'],
}

CRYPTO_CURRENCIES = sorted(NETWORK_OPTIONS.keys())

class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30), nullable=False)
    label = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, default='')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, default=lambda: datetime.utcnow())
    end_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='active')

    user = db.relationship('User', backref='investments')
    plan = db.relationship('Plan', backref='investments')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    note = db.Column(db.String(255), default='')
    withdraw_method = db.Column(db.String(50), nullable=True)
    withdraw_network = db.Column(db.String(50), nullable=True)
    withdraw_address = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())

    user = db.relationship('User', backref='transactions')

class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referred_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    commission = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())

    referrer = db.relationship('User', foreign_keys=[referrer_id])
    referred = db.relationship('User', foreign_keys=[referred_id])

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    claimed_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())

    user = db.relationship('User', backref='rewards')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
