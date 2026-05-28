import re
import random
import time
from difflib import SequenceMatcher

GREETINGS = {
    'en': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good evening', 'howdy', 'what\'s up', 'yo', 'sup'],
    'ar': ['السلام عليكم', 'مرحبا', 'اهلا', 'هاي', 'هلا', 'صباح الخير', 'مساء الخير', 'تحياتي', 'الو'],
}

FALLBACK = {
    'en': "I'm sorry, I didn't quite get that. Could you rephrase? You can ask me about our investment plans, how deposits work, withdrawals, referral rewards, or anything else about the platform and I'll be happy to help! 😊",
    'ar': 'عذراً، لم أفهم تماماً. هل يمكنك إعادة الصياغة؟ يمكنك سؤالي عن خطط الاستثمار، كيفية الإيداع، السحب، مكافآت الإحالة، أو أي شيء آخر عن المنصة وسأكون سعيدة بمساعدتك! 😊',
}

GREETING_RESPONSES = {
    'en': [
        "Hello! 👋 Welcome to ElonInvest! I'm Sarah, how can I help you today? Feel free to ask me about anything!",
        "Hi there! 😊 Great to see you! What can I help you with today?",
        "Hey! Welcome! 🎉 I'm here if you have any questions about investing, deposits, or anything else!",
    ],
    'ar': [
        'مرحباً! 👋 أهلاً بك في ElonInvest! أنا سارة، كيف يمكنني مساعدتك اليوم؟',
        'أهلاً وسهلاً! 😊 يسعدني رؤيتك! كيف أقدر أخدمك اليوم؟',
        'مرحبتين! 🎉 أنا هنا إذا كان عندك أي استفسار عن الاستثمار أو الإيداع أو أي شيء ثاني!',
    ],
}

TOPICS = {
    'en': {
        'investment|plan|invest|roi|profit|return|daily|interest|rate': {
            'response': [
                "Great question! 😊 We offer **5 investment plans** with daily returns:\n\n• **Tesla Starter** — $10–$100 | 2% daily\n• **SpaceX Voyager** — $50–$500 | 3.5% daily\n• **Neuralink Pioneer** — $100–$1000 | 5% daily\n• **X Premium** — $200–$2000 | 6.5% daily\n• **Boring Elite** — $500–$5000 | 8% daily\n\nProfits are distributed automatically every 24 hours. Would you like me to explain how to get started?",
                "Sure! Here are our plans 💼\n\n• Tesla Starter: $10–100 | 2% daily\n• SpaceX Voyager: $50–500 | 3.5% daily\n• Neuralink Pioneer: $100–1000 | 5% daily\n• X Premium: $200–2000 | 6.5% daily\n• Boring Elite: $500–5000 | 8% daily\n\nThe returns are credited daily. Let me know if you want more details on any plan!",
            ],
            'keywords': ['plan', 'investment', 'invest', 'roi', 'profit', 'return', 'daily', 'interest', 'rate'],
        },
        'deposit|fund|add money|credit|payment|send|top up|charge': {
            'response': [
                "Of course! Here's how to make a deposit 💰\n\n1️⃣ Go to your Dashboard and click 'Deposit'\n2️⃣ Pick your payment method (USDT, BTC, etc.)\n3️⃣ Copy the wallet address shown\n4️⃣ Send the exact amount from your wallet\n5️⃣ Submit the deposit request\n\nOur team will verify it and once approved, the funds are added to your balance right away! Let me know if you run into any issues.",
                "Making a deposit is easy! 🎯\n\nJust head to the Deposit page, choose your preferred crypto (USDT, BTC, ETH, etc.), copy the address, send the amount, and submit the form. Our admin will approve it shortly after.\n\nAny questions about the process?",
            ],
            'keywords': ['deposit', 'fund', 'add money', 'credit', 'payment', 'send', 'top up', 'charge'],
        },
        'withdraw|withdrawal|cash out|payout|take out': {
            'response': [
                "For withdrawals 💸\n\n1️⃣ Go to the Withdraw page\n2️⃣ Select your payment method and enter your wallet address\n3️⃣ Enter the amount (up to your current balance)\n4️⃣ Submit the request\n\nJust a heads up — withdrawals are available 15 days after your first deposit. Our admin will review and approve it. Let me know if you need anything else!",
                "Sure! Here's how withdrawals work 🔄\n\nYou can request a withdrawal from the Withdraw page. Just pick your method, enter the address and amount, and submit.\n\nNote: There's a 15-day waiting period after your first deposit before withdrawals are enabled. This is for security purposes.\n\nAnything else I can help with?",
            ],
            'keywords': ['withdraw', 'withdrawal', 'cash out', 'payout', 'take out'],
        },
        'referral|refer|invite|commission|bonus|friend|link|share': {
            'response': [
                "Our referral system is awesome! 🎉\n\n• **Level 1** — 5% commission on their deposits\n• **Level 2** — 3% commission\n• **Level 3** — 2% commission\n\nJust share your unique referral link from the Referral page and earn commissions whenever your referrals deposit! It's that simple 😊",
                "You can earn extra income by referring friends! 🤝\n\nGet 5% from direct referrals, 3% from their referrals, and 2% from the third level. Your referral link is available on the Referral page.\n\nStart sharing and watch your commissions grow! 🚀",
            ],
            'keywords': ['referral', 'refer', 'invite', 'commission', 'bonus', 'friend', 'link', 'share'],
        },
        'reward|bonus|streak|gift|welcome|loyalty': {
            'response': [
                "We love rewarding our members! 🎁\n\n🎊 **Welcome Bonus** — Get a bonus on your first deposit\n🔥 **Daily Streak** — Log in daily for consecutive day rewards\n🏆 **Loyalty Bonus** — Extra reward every 30 days\n\nCheck the Rewards page to see your progress and claim your bonuses!",
                "Here are the rewards you can get 🌟\n\n• Welcome bonus on your first deposit\n• Daily streak rewards for logging in\n• Loyalty bonus every 30 days\n\nHead to the Rewards page to claim yours! 😊",
            ],
            'keywords': ['reward', 'bonus', 'streak', 'gift', 'welcome', 'loyalty'],
        },
        'payment method|crypto|usdt|btc|bitcoin|eth|wallet|address|coin|token|trc|erc|bep': {
            'response': [
                "We support various cryptocurrencies 💳\n\n• **USDT** (TRC-20, ERC-20, BEP-20)\n• **BTC** (Bitcoin network)\n• **ETH** (ERC-20)\n• **SOL** (Solana)\n• **BNB** (BEP-20)\n• And more!\n\nYou can find all available addresses in the Payment Methods section in the Admin panel. Need help with a specific one?",
                "Here are the crypto options we accept 🔄\n\nUSDT, BTC, ETH, SOL, BNB, XRP, ADA, and more! Each has its own network so make sure you select the right one when sending.\n\nIf you're unsure which to use, USDT (TRC-20) is usually the fastest and cheapest! 😊",
            ],
            'keywords': ['payment', 'crypto', 'usdt', 'btc', 'bitcoin', 'eth', 'wallet', 'address', 'coin', 'token'],
        },
        'account|profile|setting|password|email|verify|login|logout': {
            'response': [
                "Let me help with your account! 🔐\n\n• **Profile** — You can update your name and payment info\n• **Password** — You can change it from your Profile settings\n• **Email** — Contact our support to update your email\n• **Verification** — Make sure to verify your email to unlock all features\n\nIs there something specific you need help with?",
                "Your account is easy to manage! ⚙️\n\nHead to your Profile to update personal details, change your password, or manage your payment information.\n\nDon't forget to verify your email if you haven't already — it unlocks full access! 😊",
            ],
            'keywords': ['account', 'profile', 'setting', 'password', 'email', 'verify', 'login', 'logout'],
        },
        'admin|support|contact|help|question|issue|problem|complaint|ticket': {
            'response': [
                "I'm here to help! 😊 If you need further assistance:\n\n📧 **Email**: support@eloninvest.com\n💬 **Telegram**: Join our channel for updates\n👤 **Admin**: The platform admin can also help\n\nFeel free to reach out anytime!",
                "Need to talk to someone? Here are the ways to reach us 📬\n\n• Email: support@eloninvest.com\n• Telegram: @eloniinvest\n\nI can also help with most questions right here! Just ask 😊",
            ],
            'keywords': ['admin', 'support', 'contact', 'help', 'question', 'issue', 'problem'],
        },
        'balance|money|dollar|usd|fund|wallet|total': {
            'response': [
                "Your balance and all transactions are shown on your Dashboard 📊\n\nYou can see:\n• Current available balance\n• Pending deposits and withdrawals\n• Investment profits\n• Referral earnings\n\nEverything is updated in real-time! Is there a specific number you're looking for?",
                "Check your Dashboard for a complete overview of your finances 💰\n\nYou'll find your balance, earnings from investments, referral commissions, and your transaction history all in one place.\n\nLet me know if you need help reading any of it! 😊",
            ],
            'keywords': ['balance', 'money', 'dollar', 'usd', 'fund', 'wallet', 'total'],
        },
        'plan|company|tesla|spacex|neuralink|x|boring|elon|musk|portfolio': {
            'response': [
                "Our investment plans are tied to innovative tech companies 🚀\n\n🚗 **Tesla** — Electric vehicles & clean energy\n🚀 **SpaceX** — Space exploration & Starlink\n🧠 **Neuralink** — Brain-computer interfaces\n💬 **X** — AI & social media\n🕳️ **Boring Company** — Infrastructure\n\nEach plan has different minimums and daily returns. Which one interests you?",
                "We offer plans based on leading tech companies 💼\n\nFrom Tesla and SpaceX to Neuralink and X — each plan has its own investment range and daily return rate.\n\nWould you like me to explain the details of a specific plan? 😊",
            ],
            'keywords': ['plan', 'company', 'tesla', 'spacex', 'neuralink', 'boring', 'elon', 'musk'],
        },
    },
    'ar': {
        'استثمار|خطة|ربح|عائد|أرباح|عوائد|يومي|تسلا|سبيس': {
            'response': [
                'أهلاً! عندنا **5 خطط استثمارية** بعوائد يومية 💼\n\n• **تسلا الأساسية** — 10–100$ | 2% يومياً\n• **سبيس إكس** — 50–500$ | 3.5% يومياً\n• **نيورالينك** — 100–1000$ | 5% يومياً\n• **إكس بريميوم** — 200–2000$ | 6.5% يومياً\n• **بورينج النخبة** — 500–5000$ | 8% يومياً\n\nالأرباح توزع تلقائياً كل 24 ساعة. تحب أشرح لك كيف تبدأ؟ 😊',
                'طبعاً! هذه خططنا 📊\n\n• تسلا: 10–100$ | عائد 2% يومي\n• سبيس إكس: 50–500$ | عائد 3.5%\n• نيورالينك: 100–1000$ | عائد 5%\n• إكس بريميوم: 200–2000$ | عائد 6.5%\n• بورينج النخبة: 500–5000$ | عائد 8%\n\nالعوائد تضاف لحسابك كل يوم. إذا تبغى تفاصيل أكثر عن أي خطة، أنا هنا! 😊',
            ],
            'keywords': ['استثمار', 'خطة', 'ربح', 'عائد', 'أرباح', 'عوائد', 'يومي', 'تسلا', 'سبيس', 'نيورالينك', 'بورينج'],
        },
        'إيداع|شحن|إضافة|دفع|تحويل|تمويل': {
            'response': [
                'طريقة الإيداع سهلة جداً 💰\n\n1️⃣ اذهب إلى لوحة التحكم واضغط "إيداع"\n2️⃣ اختر طريقة الدفع (USDT، BTC، إلخ)\n3️⃣ انسخ عنوان المحفظة\n4️⃣ أرسل المبلغ المحدد من محفظتك\n5️⃣ قدم طلب الإيداع\n\nبعد ما ترسل، المسؤول يوافق على الطلب ويضاف المبلغ لحسابك فوراً! 🎉\n\nإذا احتجت مساعدة في أي خطوة، أخبرني!',
                'للايداع، اتبع هالخطوات ✨\n\nروح لصفحة الإيداع، اختر العملة، انسخ العنوان، أرسل المبلغ، وقدم الطلب.\n\nبسيطة صح؟ 😊 إذا واجهتك أي مشكلة أنا هنا!',
            ],
            'keywords': ['إيداع', 'شحن', 'إضافة', 'دفع', 'تحويل'],
        },
        'سحب|انسحاب|صرف|استلام': {
            'response': [
                'للسحب 💸\n\n1️⃣ اذهب إلى صفحة السحب\n2️⃣ اختر وسيلة الدفع وأدخل عنوان محفظتك\n3️⃣ أدخل المبلغ (أقصاه رصيدك الحالي)\n4️⃣ قدم الطلب\n\n📌 ملاحظة: السحب متاح بعد 15 يوم من أول إيداع (هذا للإجراءات الأمنية).\n\nالمسؤول يراجع طلبك ويوافق عليه. هل عندك أي استفسار ثاني؟',
                'طريقة السحب بسيطة 🔄\n\nروح لصفحة السحب، اختر الطريقة، أدخل العنوان والمبلغ، وقدم. \n\nفيه حد أدنى 15 يوم من أول إيداع قبل ما تقدر تسحب. هذا لحماية الجميع 😊\n\nأي شيء ثاني؟',
            ],
            'keywords': ['سحب', 'انسحاب', 'صرف', 'استلام'],
        },
        'إحالة|دعوة|عمولة|مكافأة|صديق|رابط|شير': {
            'response': [
                'نظام الإحالة ممتاز! 🎉\n\n• **المستوى 1** — 5% عمولة على إيداعاتهم\n• **المستوى 2** — 3% عمولة\n• **المستوى 3** — 2% عمولة\n\nشارك رابطك من صفحة الإحالة واربح عمولات كل ما أحد يودع! سهل صح؟ 😊',
                'تقدر تكسب دخل إضافي بدعوة أصدقائك! 🤝\n\nتاخذ 5% من اللي تدعوهم، و3% من اللي يدعونهم، و2% من المستوى الثالث.\n\nالرابط موجود في صفحة الإحالة. شاركه وابدأ الربح! 🚀',
            ],
            'keywords': ['إحالة', 'دعوة', 'عمولة', 'مكافأة', 'صديق', 'رابط'],
        },
        'مكافأة|مكافآت|هدية|ترحيب|ولاء': {
            'response': [
                'نحب نكافئ أعضائنا! 🎁\n\n🎊 **مكافأة ترحيبية** — أول إيداع\n🔥 **المتابعة اليومية** — سجل دخول كل يوم\n🏆 **مكافأة الولاء** — كل 30 يوم\n\nروح لصفحة المكافآت وشوف تقدمك واطلب مكافآتك! 😊',
                'فيه مكافآت كثيرة تنتظرك 🌟\n\nمكافأة ترحيبية، مكافآت يومية للمتابعة، ومكافأة ولاء كل شهر.\n\nتفقد صفحة المكافآت عشان تطالب بها!',
            ],
            'keywords': ['مكافأة', 'مكافآت', 'هدية', 'ترحيب', 'ولاء'],
        },
        'طريقة دفع|عملة|usdt|btc|بيتكوين|محفظة|عنوان|شبكة': {
            'response': [
                'ندعم عدة عملات رقمية 💳\n\n• **USDT** (TRC-20, ERC-20, BEP-20)\n• **BTC** (شبكة بيتكوين)\n• **ETH** (ERC-20)\n• **SOL** (سولانا)\n• **BNB** (BEP-20)\n• وغيرها!\n\nكل العناوين موجودة في صفحة وسائل الدفع. إذا تحتاج مساعدة بأي عملة، أخبرني!',
                'هذي العملات اللي نقبلها 🔄\n\nUSDT, BTC, ETH, SOL, BNB, XRP, وغيرها.\n\nفي العادة USDT (TRC-20) هي الأسرع والأرخص! 😊\n\nوش تفضل تستخدم؟',
            ],
            'keywords': ['طريقة دفع', 'عملة', 'usdt', 'btc', 'بيتكوين', 'محفظة', 'عنوان', 'شبكة'],
        },
        'حساب|ملف|إعدادات|كلمة مرور|بريد|تسجيل|دخول': {
            'response': [
                'خلني أساعدك في حسابك 🔐\n\n• **الملف الشخصي** — تقدر تحدث اسمك ومعلومات الدفع\n• **كلمة المرور** — تغيرها من إعدادات الملف\n• **البريد الإلكتروني** — تواصل مع الدعم لتغييره\n• **التوثيق** — وثق بريدك عشان تفتح كل المميزات\n\nتحتاج مساعدة في شي محدد؟',
                'إدارة حسابك سهلة ⚙️\n\nروح للملف الشخصي عشان تحدث معلوماتك أو تغير كلمة السر.\n\nولا تنسى توثق بريدك الإلكتروني عشان تفتح كل الصلاحيات! 😊',
            ],
            'keywords': ['حساب', 'ملف', 'إعدادات', 'كلمة مرور', 'بريد', 'تسجيل', 'دخول'],
        },
        'مسؤول|دعم|اتصال|مساعدة|استفسار|مشكلة|شكوى|تواصل': {
            'response': [
                'أنا هنا لمساعدتك! 😊 إذا تحتاج تواصل إضافي:\n\n📧 **البريد**: support@eloninvest.com\n💬 **تلغرام**: @eloniinvest\n\nتقدر تراسلني أنا كمان وأنا أساعدك في أي وقت!',
                'طرق التواصل 📬\n\n• إيميل: support@eloninvest.com\n• تلغرام: @eloniinvest\n\nأنا موجودة هنا إذا احتجت أي مساعدة. فقط اسأل! 😊',
            ],
            'keywords': ['مسؤول', 'دعم', 'اتصال', 'مساعدة', 'استفسار', 'مشكلة', 'شكوى'],
        },
        'رصيد|مبلغ|دولار|محفظة|إجمالي|باقي': {
            'response': [
                'تقدر تشوف رصيدك وكل معاملاتك في لوحة التحكم 📊\n\n• الرصيد الحالي\n• الإيداعات والسحوبات المعلقة\n• أرباح الاستثمار\n• أرباح الإحالة\n\nكل شيء محدث في الوقت الفعلي!',
                'لوحة التحكم تظهر لك كل شيء 💰\n\nالرصيد، الأرباح، العمولات، وكل المعاملات في مكان واحد.\n\nإذا احتجت مساعدة في قراءة أي رقم، أنا موجودة! 😊',
            ],
            'keywords': ['رصيد', 'مبلغ', 'دولار', 'محفظة', 'إجمالي'],
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
    best_responses = None
    for pattern, data in topics.items():
        if re.search(pattern, text_lower):
            kw = data.get('keywords', [])
            score = sum(1 for k in kw if k in text_lower)
            if score > best_score:
                best_score = score
                best_responses = data['response']
            if score >= 2:
                break
    if best_responses:
        return best_responses
    for pattern, data in topics.items():
        for kw in data.get('keywords', []):
            if kw in text_lower:
                return data['response']
    return None

def get_response(message):
    lang = detect_lang(message)
    if is_greeting(message, lang):
        return random.choice(GREETING_RESPONSES[lang])
    responses = find_best_match(message, lang)
    if responses:
        return random.choice(responses)
    return FALLBACK[lang]
