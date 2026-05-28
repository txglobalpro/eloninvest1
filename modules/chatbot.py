import re
from difflib import SequenceMatcher

GREETINGS = {
    'en': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good evening', 'howdy', 'what\'s up', 'yo'],
    'ar': ['السلام عليكم', 'مرحبا', 'اهلا', 'هاي', 'هلا', 'صباح الخير', 'مساء الخير', 'تحياتي'],
}

FALLBACK = {
    'en': "I'm not sure I understand. Try asking about: investment plans, deposits, withdrawals, referral rewards, payment methods, or account settings.",
    'ar': 'لم أفهم سؤالك تماماً. جرب أن تسأل عن: خطط الاستثمار، الإيداع، السحب، مكافآت الإحالة، طرق الدفع، أو إعدادات الحساب.',
}

GREETING_RESPONSE = {
    'en': "Hello! 👋 Welcome to ElonInvest. How can I help you today? You can ask me about our investment plans, how to deposit, withdraw, referral system, and more!",
    'ar': 'مرحباً بك في ElonInvest! 👋 كيف يمكنني مساعدتك اليوم؟ يمكنك سؤالي عن خطط الاستثمار، طريقة الإيداع، السحب، نظام الإحالة، والمزيد!',
}

TOPICS = {
    'en': {
        'investment|plan|invest|roi|profit|return|daily': {
            'response': "We offer **5 investment plans** with daily returns:\n\n• **Tesla Starter** — $10–$100 | 2% daily\n• **SpaceX Voyager** — $50–$500 | 3.5% daily\n• **Neuralink Pioneer** — $100–$1000 | 5% daily\n• **X Premium** — $200–$2000 | 6.5% daily\n• **Boring Elite** — $500–$5000 | 8% daily\n\nProfits are distributed automatically every 24 hours.",
            'keywords': ['plan', 'investment', 'invest', 'roi', 'profit', 'return', 'daily', 'interest', 'rate', 'tesla', 'spacex', 'neuralink', 'boring', 'premium'],
        },
        'deposit|fund|add money|credit|payment': {
            'response': "To make a **deposit**:\n\n1. Go to your Dashboard and click 'Deposit'\n2. Select your preferred payment method (USDT, BTC, etc.)\n3. Copy the wallet address shown\n4. Send the exact amount from your wallet\n5. Submit the deposit request\n\nOur admin will verify and approve it. Once approved, the amount is credited to your balance instantly!",
            'keywords': ['deposit', 'fund', 'add money', 'credit', 'payment', 'send', 'top up', 'charge'],
        },
        'withdraw|withdrawal|cash out|payout': {
            'response': "To make a **withdrawal**:\n\n1. Go to the Withdraw page\n2. Choose your payment method and enter your wallet address\n3. Enter the amount (max your current balance)\n4. Submit the request\n\nNote: Withdrawals are available 15 days after your first deposit. Our admin will review and approve your request.",
            'keywords': ['withdraw', 'withdrawal', 'cash out', 'payout', 'take out', 'get money'],
        },
        'referral|refer|invite|commission|bonus|friend': {
            'response': "Our **3-Level Referral System**:\n\n• **Level 1** — 5% commission on their deposits\n• **Level 2** — 3% commission\n• **Level 3** — 2% commission\n\nShare your referral link from the Referral page and earn commissions instantly when your referrals deposit!",
            'keywords': ['referral', 'refer', 'invite', 'commission', 'bonus', 'friend', 'link', 'share'],
        },
        'reward|bonus|streak|gift|welcome': {
            'response': "Available **Rewards**:\n\n🎁 **Welcome Bonus** — Get a bonus on your first deposit\n🔥 **Daily Streak** — Log in daily for consecutive day rewards\n🏆 **Loyalty Bonus** — Extra reward every 30 days\n\nCheck the Rewards page for your current progress!",
            'keywords': ['reward', 'bonus', 'streak', 'gift', 'welcome', 'loyalty', 'daily reward'],
        },
        'payment method|crypto|usdt|btc|bitcoin|eth|wallet|address': {
            'response': "We support **cryptocurrency** payment methods:\n\n• **USDT** (TRC-20, ERC-20, BEP-20)\n• **BTC** (Bitcoin network)\n• **ETH** (ERC-20)\n• **SOL** (Solana)\n• **BNB** (BEP-20)\n• And more!\n\nFind all available addresses in the Payment Methods page (Admin panel).",
            'keywords': ['payment', 'crypto', 'usdt', 'btc', 'bitcoin', 'eth', 'wallet', 'address', 'coin', 'token', 'trc', 'erc', 'bep'],
        },
        'account|profile|setting|password|email|verify|login': {
            'response': "**Account Management**:\n\n• **Profile** — Update your name, payment info\n• **Password** — Change it from Profile settings\n• **Email** — Contact support to change email\n• **Verification** — Verify your email to unlock all features\n\nNeed help with anything specific?",
            'keywords': ['account', 'profile', 'setting', 'password', 'email', 'verify', 'login', 'logout', 'username'],
        },
        'admin|support|contact|help|question|issue|problem': {
            'response': "Need **help**? Here's how to reach us:\n\n• 📧 **Email**: support@eloninvest.com\n• 💬 **Telegram**: Join our official channel for news\n• 👤 **Admin**: Contact the platform administrator\n\nFor urgent issues, please email us directly.",
            'keywords': ['admin', 'support', 'contact', 'help', 'question', 'issue', 'problem', 'complaint', 'ticket'],
        },
        'balance|money|dollar|usd|amount|wallet': {
            'response': "Your **balance** and all transactions are visible on your Dashboard. You can:\n\n• View current balance\n• Check pending deposits/withdrawals\n• See investment profits\n• Track referral earnings\n\nGo to Dashboard for a complete overview!",
            'keywords': ['balance', 'money', 'dollar', 'usd', 'fund', 'wallet', 'amount', 'total'],
        },
        'plan|company|tesla|spacex|neuralink|x|boring|portfolio': {
            'response': "Our **Investment Plans** are tied to Elon Musk's companies:\n\n🚗 **Tesla** — Electric vehicles & energy\n🚀 **SpaceX** — Space exploration & Starlink\n🧠 **Neuralink** — Brain-computer interfaces\n💬 **X** — Social media & AI\n🕳️ **Boring Company** — Infrastructure & tunneling\n\nEach plan has different minimums and daily returns!",
            'keywords': ['plan', 'company', 'tesla', 'spacex', 'neuralink', 'boring', 'elon', 'musk', 'portfolio'],
        },
    },
    'ar': {
        'استثمار|خطة|ربح|عائد|أرباح|عوائد|يومي': {
            'response': 'نقدم **5 خطط استثمارية** بعوائد يومية:\n\n• **تسلا الأساسية** — 10–100 دولار | عائد 2% يومياً\n• **سبيس إكس** — 50–500 دولار | عائد 3.5% يومياً\n• **نيورالينك** — 100–1000 دولار | عائد 5% يومياً\n• **إكس بريميوم** — 200–2000 دولار | عائد 6.5% يومياً\n• **بورينج النخبة** — 500–5000 دولار | عائد 8% يومياً\n\nيتم توزيع الأرباح تلقائياً كل 24 ساعة.',
            'keywords': ['استثمار', 'خطة', 'ربح', 'عائد', 'أرباح', 'عوائد', 'يومي', 'تسلا', 'سبيس', 'نيورالينك', 'بورينج'],
        },
        'إيداع|شحن|إضافة|دفع|تحويل': {
            'response': 'لـ **الإيداع**:\n\n1. اذهب إلى لوحة التحكم واضغط "إيداع"\n2. اختر طريقة الدفع (USDT، BTC، إلخ)\n3. انسخ عنوان المحفظة الظاهر\n4. أرسل المبلغ المحدد من محفظتك\n5. قدم طلب الإيداع\n\nسيتحقق المسؤول ويوافق على الطلب. بعد الموافقة، يضاف المبلغ إلى رصيدك فوراً!',
            'keywords': ['إيداع', 'شحن', 'إضافة', 'دفع', 'تحويل', 'إيد', 'تمويل'],
        },
        'سحب|انسحاب|صرف|استلام': {
            'response': 'لـ **السحب**:\n\n1. اذهب إلى صفحة السحب\n2. اختر وسيلة الدفع وأدخل عنوان محفظتك\n3. أدخل المبلغ (الحد الأقصى هو رصيدك الحالي)\n4. قدم الطلب\n\nملاحظة: السحب متاح بعد 15 يوماً من أول إيداع. سيراجع المسؤول طلبك ويوافق عليه.',
            'keywords': ['سحب', 'انسحاب', 'صرف', 'استلام', 'سح','],
        },
        'إحالة|دعوة|عمولة|مكافأة|صديق|رابط': {
            'response': '**نظام الإحالة** ثلاثي المستويات:\n\n• **المستوى 1** — 5% عمولة على إيداعاتهم\n• **المستوى 2** — 3% عمولة\n• **المستوى 3** — 2% عمولة\n\nشارك رابط الإحالة الخاص بك من صفحة الإحالة واربح عمولات فوراً عندما يودع المدعوون!',
            'keywords': ['إحالة', 'دعوة', 'عمولة', 'مكافأة', 'صديق', 'رابط', 'شير'],
        },
        'مكافأة|مكافآت|هدية|ترحيب|ولاء|يومي': {
            'response': '**المكافآت المتاحة**:\n\n🎁 **مكافأة ترحيبية** — احصل على مكافأة عند أول إيداع\n🔥 **المتابعة اليومية** — سجل الدخول يومياً لمكافآت الأيام المتتالية\n🏆 **مكافأة الولاء** — مكافأة إضافية كل 30 يوماً\n\nتفقد صفحة المكافآت لتقدمك الحالي!',
            'keywords': ['مكافأة', 'مكافآت', 'هدية', 'ترحيب', 'ولاء', 'يومي', 'تحدي'],
        },
        'طريقة دفع|عملة|usdt|btc|بيتكوين|محفظة|عنوان': {
            'response': 'ندعم **العملات الرقمية** كطرق دفع:\n\n• **USDT** (TRC-20, ERC-20, BEP-20)\n• **BTC** (شبكة بيتكوين)\n• **ETH** (ERC-20)\n• **SOL** (سولانا)\n• **BNB** (BEP-20)\n• والمزيد!\n\nجميع العناوين متاحة في صفحة وسائل الدفع.',
            'keywords': ['طريقة دفع', 'عملة', 'usdt', 'btc', 'بيتكوين', 'محفظة', 'عنوان', 'شبكة'],
        },
        'حساب|ملف|إعدادات|كلمة مرور|بريد|تسجيل|دخول': {
            'response': '**إدارة الحساب**:\n\n• **الملف الشخصي** — تحديث الاسم ومعلومات الدفع\n• **كلمة المرور** — تغييرها من إعدادات الملف\n• **البريد الإلكتروني** — تواصل مع الدعم لتغييره\n• **التوثيق** — وثق بريدك الإلكتروني لفتح جميع الميزات\n\nهل تحتاج مساعدة في شيء محدد؟',
            'keywords': ['حساب', 'ملف', 'إعدادات', 'كلمة مرور', 'بريد', 'تسجيل', 'دخول'],
        },
        'مسؤول|دعم|اتصال|مساعدة|استفسار|مشكلة|شكوى': {
            'response': 'للـ **مساعدة**:\n\n• 📧 **البريد الإلكتروني**: support@eloninvest.com\n• 💬 **تلغرام**: انضم لقناتنا الرسمية للأخبار\n• 👤 **المسؤول**: تواصل مع مسؤول المنصة\n\nللاستفسارات العاجلة، راسلنا عبر البريد الإلكتروني مباشرة.',
            'keywords': ['مسؤول', 'دعم', 'اتصال', 'مساعدة', 'استفسار', 'مشكلة', 'شكوى', 'تواصل'],
        },
        'رصيد|مبلغ|دولار|محفظة|إجمالي': {
            'response': '**الرصيد** وجميع المعاملات ظاهرة في لوحة التحكم. يمكنك:\n\n• عرض الرصيد الحالي\n• التحقق من الإيداعات/السحوبات المعلقة\n• مشاهدة أرباح الاستثمار\n• تتبع أرباح الإحالة\n\nاذهب إلى لوحة التحكم للنظرة الكاملة!',
            'keywords': ['رصيد', 'مبلغ', 'دولار', 'محفظة', 'إجمالي', 'باقي'],
        },
    },
}

def detect_lang(text):
    if re.search(r'[\u0600-\u06ff\u0750-\u077f]', text):
        return 'ar'
    return 'en'

def is_greeting(text, lang):
    text = text.strip().lower()
    for g in GREETINGS.get(lang, []):
        if text == g or text.startswith(g) or SequenceMatcher(None, text[:len(g)], g).ratio() > 0.8:
            return True
    return False

def find_best_match(text, lang):
    text_lower = text.lower()
    topics = TOPICS.get(lang, {})
    best_score = 0
    best_response = None
    for pattern, data in topics.items():
        if re.search(pattern, text_lower):
            kw = data.get('keywords', [])
            score = sum(1 for k in kw if k in text_lower)
            if score > best_score:
                best_score = score
                best_response = data['response']
            if score >= 2:
                break
    if best_response:
        return best_response
    # fallback: check individual keywords
    for pattern, data in topics.items():
        for kw in data.get('keywords', []):
            if kw in text_lower:
                return data['response']
    return None

def get_response(message):
    lang = detect_lang(message)
    if is_greeting(message, lang):
        return GREETING_RESPONSE[lang]
    response = find_best_match(message, lang)
    if response:
        return response
    return FALLBACK[lang]
