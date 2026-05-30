import random

YOUTUBE_VIDEOS = [
    {'id': 'Nov_f7VK99o', 'title_ar': 'كيف تصبح مليونير', 'title_en': 'How to Become a Millionaire'},
    {'id': '4sD_dK0IZ0k', 'title_ar': 'عقلية المليونير', 'title_en': 'Millionaire Mindset'},
    {'id': '5_SzE6xryA0', 'title_ar': 'أسرار الأثرياء', 'title_en': 'Secrets of the Rich'},
    {'id': 'eG-Gz3P6Lkk', 'title_ar': 'قوانين المال الخمسين', 'title_en': '50 Laws of Money'},
    {'id': 's4hUFjV6y6U', 'title_ar': 'الاستثمار للمبتدئين', 'title_en': 'Investing for Beginners'},
    {'id': 'w8Qv4h58N1M', 'title_ar': 'كيف تبني ثروة', 'title_en': 'How to Build Wealth'},
    {'id': 'sEFl72IwXKI', 'title_ar': 'الحرية المالية', 'title_en': 'Financial Freedom'},
    {'id': '9i8K7yPpFkE', 'title_ar': 'قصة نجاح إيلون ماسك', 'title_en': 'Elon Musk Success Story'},
    {'id': 'zhWd9tAq3iM', 'title_ar': 'الاستثمار في الأسهم', 'title_en': 'Stock Market Investing'},
    {'id': 'FfN_3aIKoXg', 'title_ar': 'الدخل السلبي', 'title_en': 'Passive Income'},
]

STORY_TEMPLATES_AR = [
    # Stories about regular people starting small
    '⭐ {name} من {country}:\n\n"قررت أجرب الاستثمار بمبلغ {amount}$ في خطة {plan}.\nبعد {days} يوماً:\n• إجمالي الأرباح: {profit}$\n• إجمالي المحفظة: {total}$\n• العائد اليومي: {daily}$\n\n{quote}"\n\n🚀 {name} بدأ بـ {amount}$ فقط!\nوانت أيضاً تقدر تبدأ اليوم!',
    '⭐ قصة نجاح {name} من {country}:\n\n"سمعت عن ElonInvest من صديق.\nاستثمرت {amount}$ في {plan}.\nالآن بعد {days} يوماً:\n• أرباحي: {profit}$\n• المحفظة: {total}$\n• دخل يومي: {daily}$\n\n{quote}"\n\n💎 ابدأ رحلتك الاستثمارية اليوم!',
    '⭐ {name} من {country} يحقق حلمه:\n\n"كنت أحلم بدخل إضافي. وجدت ElonInvest.\nاستثمرت {amount}$ فقط.\nبعد {days} يوم:\n• الأرباح: {profit}$\n• الإجمالي: {total}$\n• أرباح يومية: {daily}$\n\n{quote}"\n\n🔥 الفرصة بين يديك! ابدأ الآن.',
    '⭐ {name} من {country}:\n\n"صراحة ما كنت متأكد في البداية.\nلكن بعد ما شفت أرباح أول أسبوع:\nاستثمار: {amount}$\nالخطة: {plan}\nالمدة: {days} يوم\nالأرباح: {profit}$\nالمجموع: {total}$\n\nالحمدلله على هالقرار."\n\n📈 لا تتردد! ابدأ واستثمر اليوم.',
    '⭐ تجربة {name} من {country}:\n\n"جربت منصة ElonInvest بناءً على توصية.\nاستثمار: {amount}$\nالخطة: {plan}\n• المدة: {days} يوم\n• صافي الربح: {profit}$\n• الرصيد الحالي: {total}$\n\n{quote}"\n\n💪 المستقبل يبدأ بقرار!',
    '⭐ {name} من {country} يشاركنا قصته:\n\n"من وقت ما بدأت مع ElonInvest:\nرأس المال: {amount}$\nالخطة: {plan}\nعدد الأيام: {days}\nالأرباح المتحققة: {profit}$\nقيمة المحفظة: {total}$\n\n{quote}\nأنصح الكل بتجربة المنصة!"\n\n🚀 انطلق نحو مستقبلك المالي!',
    '⭐ {name} من {country}:\n\n"أخيراً لقيت منصة استثمارية صادقة!\n\nالمبلغ: {amount}$\nخطة: {plan}\nالمدة: {days} يوم\nالأرباح: {profit}$\nالإجمالي: {total}$\nالعائد اليومي: {daily}$\n\n{quote}"\n\n💰 ابدأ بصقل مهاراتك الاستثمارية!',
]

STORY_TEMPLATES_EN = [
    '⭐ {name} from {country}:\n\n"I decided to try investing {amount}$ in {plan}.\nAfter {days} days:\n• Total profit: {profit}$\n• Portfolio: {total}$\n• Daily return: {daily}$\n\n{quote}"\n\n🚀 {name} started with just {amount}$!\nYou can start today too!',
    '⭐ Success story: {name} from {country}:\n\n"I heard about ElonInvest from a friend.\nI invested {amount}$ in {plan}.\nNow after {days} days:\n• Profit: {profit}$\n• Portfolio: {total}$\n• Daily income: {daily}$\n\n{quote}"\n\n💎 Start your investment journey today!',
    '⭐ {name} from {country} achieving his dream:\n\n"I dreamed of extra income. I found ElonInvest.\nI invested just {amount}$.\nAfter {days} days:\n• Profit: {profit}$\n• Total: {total}$\n• Daily earnings: {daily}$\n\n{quote}"\n\n🔥 The opportunity is here! Start now.',
    '⭐ {name} from {country}:\n\n"Honestly I wasn\'t sure at first.\nBut after seeing my first week profits:\nInvestment: {amount}$\nPlan: {plan}\nPeriod: {days} days\nProfit: {profit}$\nTotal: {total}$\n\nBest decision ever!"\n\n📈 Don\'t hesitate! Invest today.',
    '⭐ {name} from {country} shares:\n\n"Tried ElonInvest based on a recommendation.\nInvestment: {amount}$\nPlan: {plan}\n• Period: {days} days\n• Net profit: {profit}$\n• Current balance: {total}$\n\n{quote}"\n\n💪 The future starts with a decision!',
]

NAMES_AR = ['أحمد', 'محمد', 'سارة', 'نورة', 'خالد', 'فاطمة', 'عبدالله', 'مريم', 'عمر', 'لينا',
            'يوسف', 'حصة', 'إبراهيم', 'دلال', 'سعود', 'هند', 'فيصل', 'أمل', 'ماجد', 'نوف',
            'حسن', 'لولوة', 'علي', 'منال', 'سلطان', 'موضي', 'بدر', ' الجازي', 'تركي', 'شيماء',
            'نايف', 'حنان', 'سامي', 'وجدان', 'مشعل', 'عفاف', 'ناصر', 'تهاني', 'فواز', 'فردوس']

NAMES_EN = ['Ahmed', 'Mohammed', 'Sarah', 'Nora', 'Khalid', 'Fatima', 'Abdullah', 'Maryam', 'Omar', 'Layla',
            'Yousef', 'Hessa', 'Ibrahim', 'Dalal', 'Saud', 'Hind', 'Faisal', 'Amal', 'Majed', 'Nouf',
            'Hassan', 'Lulwa', 'Ali', 'Manal', 'Sultan', 'Moudi', 'Badr', 'Al-Jazi', 'Turki', 'Shaima',
            'Naif', 'Hanan', 'Sami', 'Wijdan', 'Mishal', 'Afaf', 'Naser', 'Tehani', 'Fawaz', 'Firdous']

COUNTRIES_AR = ['السعودية', 'الإمارات', 'الكويت', 'قطر', 'عمان', 'البحرين', 'مصر', 'الأردن', 'العراق', 'تونس',
                'الجزائر', 'المغرب', 'ليبيا', 'السودان', 'اليمن', 'سوريا', 'فلسطين', 'لبنان', 'موريتانيا', 'الصومال']
COUNTRIES_EN = ['Saudi Arabia', 'UAE', 'Kuwait', 'Qatar', 'Oman', 'Bahrain', 'Egypt', 'Jordan', 'Iraq', 'Tunisia',
                'Algeria', 'Morocco', 'Libya', 'Sudan', 'Yemen', 'Syria', 'Palestine', 'Lebanon', 'Mauritania', 'Somalia']

PLANS = ['Tesla Starter', 'SpaceX Voyager', 'Neuralink Pioneer', 'X Premium', 'Boring Elite']
PLANS_AR = ['Tesla Starter', 'SpaceX Voyager', 'Neuralink Pioneer', 'X Premium', 'Boring Elite']

QUOTES_AR = [
    'أفضل قرار استثماري في حياتي!',
    'الفرصة الحقيقية لا تأتي مرتين.',
    'الحمدلله على هذه النعمة.',
    'الاستثمار الذكي يغير الحياة.',
    'أنصح الجميع بتجربة المنصة.',
    'أشعر بالأمان المالي لأول مرة.',
    'هذا هو المستقبل بكل تأكيد.',
    'نمت واستيقظت على أرباح!',
    'عملت بجد والآن المال يعمل لأجلي.',
    'أفضل من الوظيفة بكثير.',
    'الآن أفهم معنى الحرية المالية.',
    'قرار غيّر مسار حياتي للأبد.',
    'بفضل الله ثم ElonInvest.',
    'تجربة لا تنسى وأرباح خيالية.',
    'كل يوم أرباح جديدة!',
    'من أفضل المنصات الاستثمارية.',
    'أتمنى لو بدأت من زمان!',
    'الاستثمار الأمثل في وقتي.',
    'مستقبل أولادي في أمان.',
    'أرباح تفوق التوقعات!',
]
QUOTES_EN = [
    'Best investment decision I ever made!',
    'Real opportunity doesn\'t come twice.',
    'Smart investing changes lives.',
    'I feel financially secure for the first time.',
    'I highly recommend this platform.',
    'This is definitely the future.',
    'I slept and woke up to profits!',
    'I worked hard, now money works for me.',
    'Much better than a regular job.',
    'Now I understand what financial freedom means.',
    'A decision that changed my life forever.',
    'An unforgettable experience with incredible profits.',
    'Every day brings new profits!',
    'One of the best investment platforms.',
    'I wish I had started earlier!',
    'The best investment of my time.',
    'My children\'s future is secure.',
    'Profits beyond expectations!',
]

def _fill_story(templates, names, countries, plans, quotes, daily_roi_map, amounts=None):
    t = random.choice(templates)
    name = random.choice(names)
    country = random.choice(countries)
    plan = random.choice(plans)
    roi = daily_roi_map.get(plan, 0.05)
    if amounts:
        amount = random.choice(amounts)
    else:
        amount = random.choice([10, 25, 50, 100, 150, 200, 250, 300, 500, 750, 1000, 1500, 2000])
    days = random.choice([15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 75, 90])
    profit = round(amount * roi * days)
    total = amount + profit
    daily = round(amount * roi, 2)
    quote = random.choice(quotes)
    return t.format(name=name, country=country, amount=amount, plan=plan, days=days,
                    profit=profit, total=total, daily=daily, quote=quote)

DAILY_ROI_MAP = {'Tesla Starter': 0.02, 'SpaceX Voyager': 0.035, 'Neuralink Pioneer': 0.05, 'X Premium': 0.065, 'Boring Elite': 0.08}

def generate_story(lang='ar'):
    if lang == 'ar':
        return _fill_story(STORY_TEMPLATES_AR, NAMES_AR, COUNTRIES_AR, PLANS_AR, QUOTES_AR, DAILY_ROI_MAP)
    return _fill_story(STORY_TEMPLATES_EN, NAMES_EN, COUNTRIES_EN, PLANS, QUOTES_EN, DAILY_ROI_MAP)

FEATURE_POSTS = {
    'ar': [
        {'title': 'استثمر في تسلا اليوم', 'text': '🚀 استثمر في أسهمTesla عبر منصة ElonInvest واحصل على عوائد يومية تصل إلى 2%!\n\n✅ أرباح يومية\n✅ سحب أرباح في أي وقت\n✅ حد أدنى 10$ فقط\n\nانطلق مع أقوى شركات التكنولوجيا.', 'image': 'tesla'},
        {'title': 'خطط استثمارية متنوعة', 'text': '💎 اختر خطتك الاستثمارية المناسبة:\n\n⚡ Tesla Starter: عائد 2% يوميًا\n🚀 SpaceX Voyager: عائد 3.5% يوميًا\n🧠 Neuralink Pioneer: عائد 5% يوميًا\n🐦 X Premium: عائد 6.5% يوميًا\n🕳 Boring Elite: عائد 8% يوميًا\n\nاستثمر من 10$ فقط وابدأ جني الأرباح اليوم.', 'image': 'plans'},
        {'title': 'نظام الإحالة الثلاثي', 'text': '👥 كسب المال من خلال دعوة أصدقائك!\n\nنظام إحالة ثلاثي المستويات:\n🎁 المستوى 1: 5% من إيداعاتهم\n🎁 المستوى 2: 3% من إيداعاتهم\n🎁 المستوى 3: 2% من إيداعاتهم\n\nكلما دعوت أكثر، كلما ربحت أكثر! بدون حدود!', 'image': 'referral'},
        {'title': 'مكافآت يومية وأسبوعية', 'text': '🎉 ElonInvest تكافئ مستثمريها يومياً!\n\n💰 مكافأة ترحيبية: 5$ فور التسجيل\n🔥 مكافأة أول إيداع: 10% إضافية\n📅 مكافأة يومية: 1-5$ حسب الاستمرارية\n🏆 مكافأة ولاء: 10$ كل 30 يوماً\n\nكل يوم تستمر فيه تكسب أكثر!', 'image': 'rewards'},
        {'title': 'أمان واستقرار', 'text': '🔒 استثمارك آمن مع ElonInvest\n\n✅ تشفير متقدم لحماية بياناتك\n✅ مراقبة على مدار الساعة\n✅ تراخيص مالية دولية (FCA, CySEC, FinCEN, DFSA)\n✅ سحوبات فورية وآمنة\n\nنضع أموالك في أيدٍ أمينة.', 'image': 'security'},
        {'title': 'كيف تبدأ الاستثمار؟', 'text': '📝 ابدأ رحلة الاستثمار في 3 خطوات:\n\n1️⃣ أنشئ حساب مجاني\n2️⃣ اختر خطة استثمارية تناسبك\n3⃣️ استثمر وابدأ جني الأرباح اليومية\n\n💡 نصيحة: ابدأ بخطة Tesla Starter (10$ فقط) وجرب النظام بنفسك!', 'image': 'start'},
        {'title': 'طريقة الإيداع عبر Trust Wallet', 'text': '📱 كيف تودع عبر Trust Wallet:\n\n1️⃣ افتح Trust Wallet\n2⃣ اختر USDT وشبكة TRC-20\n3⃣ أرسل إلى عنوان محفظة المنصة\n4⃣ انسخ TXID والصقه في صفحة الإيداع\n5⃣ يتم إضافة الرصيد فوراً!\n🚀 أسرع طريقة للاستثمار.', 'image': 'wallet'},
        {'title': 'استراتيجيات الاستثمار الذكية', 'text': '🧠 استراتيجيات لزيادة أرباحك:\n\n📌 التنويع: وزع استثمارك على عدة خطط\n📌 إعادة الاستثمار: أعد استثمار أرباحك لتربح أكثر\n📌 الإحالة: ادعُ أصدقاءك واربح عمولات\n📌 الاستمرارية: المكافآت اليومية تزيد بدوامك\n\nاطبق هذه الاستراتيجيات وحقق أقصى عائد!', 'image': 'strategy'},
        {'title': 'لماذا USDT؟', 'text': '💵 لماذا نستخدم USDT (Tether)؟\n\n✅ مستقر: 1 USDT = 1 دولار دائماً\n✅ سريع: معاملات فورية على شبكة TRC-20\n✅ منخفض الرسوم: رسوم نقل زهيدة جداً\n✅ عالمي: يقبل في جميع المنصات\n\nUSDT هو الخيار الأمثل للاستثمار الرقمي.', 'image': 'usdt'},
        {'title': 'Tesla - ثورة السيارات الكهربائية', 'text': '⚡ Tesla: أكثر من مجرد سيارة\n\n🚗 سيارات كهربائية صديقة للبيئة\n🔋 بطاريات Powerwall للمنازل\n☀️ ألواح شمسية Solar Roof\n🤖 روبوتات Optimus\n\nسهم Tesla من أقوى الأسهم أداءً في العقد الأخير!', 'image': 'tesla_about'},
        {'title': 'SpaceX - استكشاف الفضاء', 'text': '🚀 SpaceX: مستقبل البشرية في الفضاء\n\n🛰️ Starlink: إنترنت فضائي عالمي\n🌕 Starship: أول مركبة للمريخ\n🔄 Falcon 9: صواريخ قابلة لإعادة الاستخدام\n\nسبيس إكس تغير مفهوم الفضاء كما نعرفه!', 'image': 'spacex'},
        {'title': 'Neuralink - مستقبل العقل البشري', 'text': '🧠 Neuralink: ربط العقل بالحاسوب\n\n🔬 زراعة دماغية لعلاج الأمراض\n💻 واجهة دماغية حاسوبية\n🦾 مساعدة ذوي الاحتياجات الخاصة\n\nتقنية غيرت الطب الحديث!', 'image': 'neuralink'},
        {'title': 'تحديث السوق', 'text': '📈 تحديث أسعار أسهم إيلون ماسك:\n\n⚡ Tesla (TSLA): $245.50 📈\n🚀 SpaceX (Private): $180B تقييم\n🧠 Neuralink: تجارب بشرية ناجحة\n🐦 X: منصة المستقبل\n\nالاستثمار في هذه الشركات متاح عبر ElonInvest!', 'image': 'market'},
        {'title': 'إيداع تلقائي عبر Trust Wallet', 'text': '🆕 ميزة جديدة!\n\nالآن يمكنك الإيداع عبر Trust Wallet تلقائياً:\n1️⃣ أرسل USDT (TRC-20) إلى عنوان المحفظة\n2️⃣ أدخل TXID\n3️⃣ يتم إضافة الرصيد فوراً!\n\n🚀 لا مزيد من الانتظار!\nودائع فورية وآمنة.', 'image': 'update'},
        {'title': 'إنجاز ElonInvest', 'text': '🏆 ElonInvest تحقق إنجازاً جديداً!\n\n✅ أكثر من 15,000 مستخدم نشط\n✅ 50+ دولة حول العالم\n✅ 2.5 مليون دولار أرباح موزعة\n✅ 99% رضا المستخدمين\n\nنشكر ثقتكم بنا!\nالمستقبل يبدو مشرقاً مع ElonInvest 🚀', 'image': 'milestone'},
        {'title': 'سر الأرباح المركبة', 'text': '📊 سر الأرباح المركبة:\n\nعند إعادة استثمار أرباحك اليومية:\n• استثمار 100$ بعائد 5%\n• الشهر الأول: 150$\n• الشهر الثالث: 337$\n• الشهر السادس: 1,013$\n\n🧠 هذا هو سر بناء الثروة!\nأعد استثمار أرباحك اليوم.', 'image': 'compound'},
        {'title': 'الاستثمار المنتظم', 'text': '🎯 الاستثمار المنتظم = نجاح مضمون\n\nبدلاً من استثمار مبلغ كبير مرة واحدة:\n📌 استثمر مبلغاً ثابتاً كل أسبوع\n📌 وزع المخاطر\n📌 استفد من العوائد المركبة\n📌 ابنِ محفظتك تدريجياً\n\n⑤ خطوة بخطوة نحو الحرية المالية!', 'image': 'regular'},
        {'title': 'آمن استثمارك', 'text': '🛡️ نصائح الأمان:\n\n1. لا تشارك كلمة مرورك مع أي أحد\n2. فعّل التوثيق الثنائي (قريباً)\n3. استخدم محفظة Trust Wallet الرسمية\n4. تأكد من عنوان URL الصحيح\n5. تواصل مع الدعم فقط عبر القناة الرسمية\n\nأمانك أولويتنا الأولى.', 'image': 'safety'},
    ],
    'en': [
        {'title': 'Invest in Tesla Today', 'text': '🚀 Invest in Tesla through ElonInvest and earn daily returns up to 2%!\n\n✅ Daily profits\n✅ Withdraw anytime\n✅ Minimum $10 only\n\nStart with the strongest tech companies.', 'image': 'tesla'},
        {'title': 'Diverse Investment Plans', 'text': '💎 Choose your investment plan:\n\n⚡ Tesla Starter: 2% daily\n🚀 SpaceX Voyager: 3.5% daily\n🧠 Neuralink Pioneer: 5% daily\n🐦 X Premium: 6.5% daily\n🕳 Boring Elite: 8% daily\n\nInvest from $10 and start earning daily.', 'image': 'plans'},
        {'title': '3-Level Referral System', 'text': '👥 Earn by inviting friends!\n\n🎁 Level 1: 5% of their deposits\n🎁 Level 2: 3% of their deposits\n🎁 Level 3: 2% of their deposits\n\nThe more you invite, the more you earn! No limits!', 'image': 'referral'},
        {'title': 'Daily Rewards', 'text': '🎉 ElonInvest rewards its investors daily!\n\n💰 Welcome bonus: $5 instantly\n🔥 First deposit: 10% extra\n📅 Daily streak: $1-$5\n🏆 Loyalty: $10 every 30 days\n\nThe longer you stay, the more you earn!', 'image': 'rewards'},
        {'title': 'How to Start Investing?', 'text': '📝 Start your investment journey in 3 steps:\n\n1️⃣ Create a free account\n2️⃣ Choose a plan that suits you\n3️⃣ Invest and earn daily profits\n\n💡 Tip: Start with Tesla Starter ($10) and try it!', 'image': 'start'},
        {'title': 'Trust Wallet Deposit Guide', 'text': '📱 How to deposit via Trust Wallet:\n\n1️⃣ Open Trust Wallet\n2️⃣ Select USDT on TRC-20\n3️⃣ Send to platform wallet address\n4️⃣ Copy TXID and paste on deposit page\n5️⃣ Balance credited instantly!\n🚀 Fastest way to invest.', 'image': 'wallet'},
        {'title': 'Investment Tip of the Day', 'text': '💡 The best time to invest was yesterday.\nThe second best time is today!\n\nDon\'t delay your investment decision.\nEvery day you wait is profit you miss.', 'image': 'tip1'},
        {'title': 'The Power of Compound Interest', 'text': '📊 Compound interest secret:\n\nReinvest your daily profits:\n• $100 at 5% daily return\n• Month 1: $150\n• Month 3: $337\n• Month 6: $1,013\n\n🧠 This is the key to wealth!', 'image': 'compound'},
        {'title': 'Tesla - EV Revolution', 'text': '⚡ Tesla: More than a car company\n\n🚗 Electric vehicles\n🔋 Powerwall batteries\n☀️ Solar Roof\n🤖 Optimus robots\n\nBest performing stock of the decade!', 'image': 'tesla_about'},
        {'title': 'SpaceX - Space Exploration', 'text': '🚀 SpaceX: Humanity\'s future in space\n\n🛰️ Starlink: Global space internet\n🌕 Starship: First Mars vehicle\n🔄 Falcon 9: Reusable rockets\n\nSpaceX is changing space access forever!', 'image': 'spacex'},
        {'title': 'Auto Deposit via Trust Wallet', 'text': '🆕 New Feature!\n\nDeposit automatically via Trust Wallet:\n1️⃣ Send USDT (TRC-20) to wallet address\n2️⃣ Enter TXID\n3️⃣ Balance credited instantly!', 'image': 'update'},
        {'title': 'ElonInvest Milestone', 'text': '🏆 ElonInvest hits a new milestone!\n\n✅ 15,000+ active users\n✅ 50+ countries worldwide\n✅ $2.5M profits distributed\n✅ 99% user satisfaction\n\nThank you for your trust! 🚀', 'image': 'milestone'},
        {'title': 'Secure & Reliable', 'text': '🔒 Your investment is safe with us\n\n✅ Advanced encryption\n✅ 24/7 monitoring\n✅ International licenses (FCA, CySEC, FinCEN, DFSA)\n✅ Instant secure withdrawals', 'image': 'security'},
        {'title': 'Smart Investment Strategies', 'text': '🧠 Strategies to maximize your profits:\n\n📌 Diversify across multiple plans\n📌 Reinvest your profits for compound growth\n📌 Invite friends and earn commissions\n📌 Stay active for daily streak rewards', 'image': 'strategy'},
        {'title': 'Why USDT?', 'text': '💵 Why we use USDT (Tether)?\n\n✅ Stable: 1 USDT = $1 always\n✅ Fast: Instant TRC-20 transactions\n✅ Low fees: Minimal transfer costs\n✅ Global: Accepted everywhere', 'image': 'usdt'},
    ]
}

IMAGE_KEYWORDS = {
    'tesla': 'wealthy+businessman+car',
    'plans': 'rich+investor+money',
    'referral': 'success+team+celebration',
    'rewards': 'winner+gold+trophy+luxury',
    'security': 'confident+businessman+suit',
    'start': 'success+journey+begin',
    'wallet': 'crypto+money+digital+wealth',
    'strategy': 'wealthy+investor+planning',
    'usdt': 'crypto+profit+rich+coin',
    'success1': 'wealthy+man+success+luxury',
    'success2': 'successful+woman+office+wealth',
    'community': 'global+success+community+wealthy',
    'tip1': 'rich+advisor+wealth+advice',
    'compound': 'wealth+money+growth+rich',
    'regular': 'success+schedule+wealth+plan',
    'safety': 'confident+secure+wealthy',
    'tesla_about': 'wealthy+modern+tech+success',
    'spacex': 'success+rocket+ambition+wealthy',
    'neuralink': 'wealthy+tech+brain+success',
    'market': 'wealthy+market+profit+rich',
    'update': 'success+update+wealthy+notification',
    'milestone': 'winner+champion+gold+trophy',
    'story': 'wealthy+success+rich+winner',
    'video': 'motivation+success+winner+goal',
}

def get_random_content(lang='ar'):
    post_type = random.choices(
        ['story', 'story', 'story', 'feature', 'feature', 'video'],
        weights=[40, 40, 40, 15, 15, 10]
    )[0]
    
    if post_type == 'story':
        title = f"⭐ {random.choice(NAMES_AR) if lang == 'ar' else random.choice(NAMES_EN)}: {random.choice(QUOTES_AR) if lang == 'ar' else random.choice(QUOTES_EN)}"
        text = generate_story(lang)
        return {'title': title, 'text': text, 'type': 'story', 'image': 'story'}
    
    elif post_type == 'video':
        video = random.choice(YOUTUBE_VIDEOS)
        if lang == 'ar':
            title = f"🎬 {video['title_ar']}"
            text = f"🎥 شاهد هذا الفيديو التحفيزي:\n\n{video['title_ar']}\n\n📺 https://youtu.be/{video['id']}\n\nبعد المشاهدة، تذكر أن الاستثمار الذكي هو طريقك للحرية المالية! 💪"
        else:
            title = f"🎬 {video['title_en']}"
            text = f"🎥 Watch this motivational video:\n\n{video['title_en']}\n\n📺 https://youtu.be/{video['id']}\n\nRemember, smart investing is your path to financial freedom! 💪"
        return {'title': title, 'text': text, 'type': 'video', 'image': 'video'}
    
    else:
        features = FEATURE_POSTS.get(lang, FEATURE_POSTS['en'])
        item = random.choice(features)
        return {'title': item['title'], 'text': item['text'], 'type': 'feature', 'image': item['image']}
