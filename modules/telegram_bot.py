import logging
import xml.etree.ElementTree as ET
import requests
from datetime import datetime
from html import unescape

logger = logging.getLogger(__name__)

RSS_FEEDS = [
    'https://news.google.com/rss/search?q=Elon+Musk+business+deal&hl=en-US&gl=US&ceid=US:en',
    'https://news.google.com/rss/search?q=Tesla+news+financial+deal&hl=en-US&gl=US&ceid=US:en',
    'https://news.google.com/rss/search?q=SpaceX+Starlink+investment&hl=en-US&gl=US&ceid=US:en',
    'https://news.google.com/rss/search?q=xAI+Neuralink+news&hl=en-US&gl=US&ceid=US:en',
]

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def fetch_news():
    articles = []
    for url in RSS_FEEDS:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code != 200:
                continue
            root = ET.fromstring(r.content)
            for item in root.findall('.//item'):
                title = item.findtext('title', '')
                link = item.findtext('link', '')
                pub = item.findtext('pubDate', '')
                if title and link:
                    # Remove source suffix like " - Reuters" from title
                    clean = title.rsplit(' - ', 1)[0] if ' - ' in title else title
                    articles.append({'title': unescape(clean), 'link': link, 'published': pub})
        except Exception as e:
            logger.warning(f'RSS failed for {url}: {e}')
    seen = set()
    unique = []
    for a in articles:
        key = a['title'].lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(a)
    return unique[:6]

def format_message(articles, lang='en'):
    if not articles:
        return None
    if lang == 'ar':
        lines = [
            '🚀 *ملخص ElonInvest اليومي*',
            f'📅 {datetime.utcnow().strftime("%Y/%m/%d")}',
            '',
        ]
        for i, a in enumerate(articles, 1):
            t = a['title'].replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace('`', '\\`')
            lines.append(f'{i}. [{t}]({a["link"]})')
        lines.extend(['', '💡 *استثمر بذكاء مع ElonInvest*', '👉 [eloninvest.publicvm.com](https://eloninvest.publicvm.com)'])
    else:
        lines = [
            '🚀 *ElonInvest Daily Digest*',
            f'📅 {datetime.utcnow().strftime("%B %d, %Y")}',
            '',
        ]
        for i, a in enumerate(articles, 1):
            t = a['title'].replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace('`', '\\`')
            lines.append(f'{i}. [{t}]({a["link"]})')
        lines.extend(['', '💡 *Invest wisely with ElonInvest*', '👉 [eloninvest.publicvm.com](https://eloninvest.publicvm.com)'])
    return '\n'.join(lines)

def post_to_telegram(message, token, channel_id):
    if not token or not channel_id:
        logger.warning('Telegram not configured')
        return False
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        resp = requests.post(url, json={
            'chat_id': channel_id,
            'text': message,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': False,
        }, timeout=15)
        if resp.status_code == 200:
            logger.info('Telegram post OK')
            return True
        logger.error(f'Telegram API {resp.status_code}: {resp.text}')
        return False
    except Exception as e:
        logger.error(f'Telegram post failed: {e}')
        return False

def run_daily_news(app):
    with app.app_context():
        token = app.config.get('TELEGRAM_BOT_TOKEN', '')
        channel = app.config.get('TELEGRAM_CHANNEL_ID', '')
        if not token or not channel:
            logger.info('Telegram bot not configured, skipping news')
            return
        articles = fetch_news()
        # Try Arabic first, fallback to English
        msg = format_message(articles, 'ar')
        if not msg:
            msg = format_message(articles, 'en')
        if msg:
            post_to_telegram(msg, token, channel)
        else:
            logger.warning('No articles found')
