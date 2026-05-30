import logging
import random
import requests
from datetime import datetime
from services.content_library import get_random_content, IMAGE_KEYWORDS

logger = logging.getLogger(__name__)

UNSPLASH_ACCESS_KEY = None  # Optional: set in config for higher quality images

def get_image_url(keyword):
    kw = IMAGE_KEYWORDS.get(keyword, 'wealthy+success+money')
    if UNSPLASH_ACCESS_KEY:
        try:
            r = requests.get(
                f'https://api.unsplash.com/photos/random?query={kw}&orientation=landscape&w=800',
                headers={'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'},
                timeout=8
            )
            if r.status_code == 200:
                return r.json()['urls']['regular']
        except Exception as e:
            logger.warning(f'Unsplash failed: {e}')
    try:
        kw_clean = kw.replace('+', ',')
        r = requests.get(f'https://loremflickr.com/800/400/{kw_clean}', timeout=8, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 1000:
            return r.url
    except Exception as e:
        logger.warning(f'LoremFlickr failed: {e}')
    return f'https://picsum.photos/seed/{keyword}{random.randint(1,9999)}/800/400'

def post_to_telegram(message, token, channel_id, image_url=None):
    if not token or not channel_id:
        logger.warning('Telegram not configured')
        return False
    try:
        if image_url:
            resp = requests.post(
                f'https://api.telegram.org/bot{token}/sendPhoto',
                json={
                    'chat_id': channel_id,
                    'photo': image_url,
                    'caption': message,
                    'parse_mode': 'Markdown',
                }, timeout=20
            )
        else:
            resp = requests.post(
                f'https://api.telegram.org/bot{token}/sendMessage',
                json={
                    'chat_id': channel_id,
                    'text': message,
                    'parse_mode': 'Markdown',
                    'disable_web_page_preview': False,
                }, timeout=15
            )
        if resp.status_code == 200:
            logger.info('Telegram post OK')
            return True
        logger.error(f'Telegram API {resp.status_code}: {resp.text}')
        return False
    except Exception as e:
        logger.error(f'Telegram post failed: {e}')
        return False

def run_auto_poster(app):
    with app.app_context():
        token = app.config.get('TELEGRAM_BOT_TOKEN', '')
        channel = app.config.get('TELEGRAM_CHANNEL_ID', '')
        if not token or not channel:
            logger.info('Telegram bot not configured, skipping auto post')
            return

        lang = random.choice(['ar', 'en'])
        content = get_random_content(lang)
        msg = f"*{content['title']}*\n\n{content['text']}"
        msg += f"\n\n🌐 [ElonInvest](https://eloninvest.onrender.com)"

        if content['type'] == 'video':
            post_to_telegram(msg, token, channel)
        else:
            image_url = get_image_url(content['image'])
            post_to_telegram(msg, token, channel, image_url)

def run_daily_news(app):
    run_auto_poster(app)
