import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-secret-key-in-production')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@eloninvest.com')

    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHANNEL_ID = os.environ.get('TELEGRAM_CHANNEL_ID', '@eloniinvest')
    TELEGRAM_CHANNEL_URL = os.environ.get('TELEGRAM_CHANNEL_URL', 'https://t.me/eloniinvest')

    SOCIAL_LINKS = [
        {'key': 'telegram', 'url': os.environ.get('TELEGRAM_CHANNEL_URL', 'https://t.me/eloniinvest'), 'icon': 'bi-telegram', 'label': 'Telegram', 'color': '#08c'},
        {'key': 'facebook', 'url': os.environ.get('FACEBOOK_URL', '#'), 'icon': 'bi-facebook', 'label': 'Facebook', 'color': '#1877f2'},
        {'key': 'twitter', 'url': os.environ.get('TWITTER_URL', '#'), 'icon': 'bi-twitter-x', 'label': 'X', 'color': '#fff'},
        {'key': 'website', 'url': os.environ.get('WEBSITE_URL', 'https://eloninvest.publicvm.com'), 'icon': 'bi-globe2', 'label': 'Website', 'color': '#f0b90b'},
    ]

    WTF_CSRF_ENABLED = True
    LANGUAGES = {'en': 'English', 'ar': 'العربية'}
