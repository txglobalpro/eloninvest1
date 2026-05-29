import random

CONTENT = {
    'ar': [
        # Platform features
        {'type': 'feature', 'title': 'استثمر في تسلا اليوم', 'text': '🚀 استثمر في أسهمTesla عبر منصة ElonInvest واحصل على عوائد يومية تصل إلى 2%!\n\n✅ أرباح يومية\n✅ سحب أرباح في أي وقت\n✅ حد أدنى 10$ فقط\n\nانطلق مع أقوى شركات التكنولوجيا.', 'image': 'tesla'},
        {'type': 'feature', 'title': 'خطط استثمارية متنوعة', 'text': '💎 اختر خطتك الاستثمارية المناسبة:\n\n⚡ Tesla Starter: عائد 2% يوميًا\n🚀 SpaceX Voyager: عائد 3.5% يوميًا\n🧠 Neuralink Pioneer: عائد 5% يوميًا\n🐦 X Premium: عائد 6.5% يوميًا\n🕳 Boring Elite: عائد 8% يوميًا\n\nاستثمر من 10$ فقط وابدأ جني الأرباح اليوم.', 'image': 'plans'},
        {'type': 'feature', 'title': 'نظام الإحالة الثلاثي', 'text': '👥 كسب المال من خلال دعوة أصدقائك!\n\nنظام إحالة ثلاثي المستويات:\n🎁 المستوى 1: 5% من إيداعاتهم\n🎁 المستوى 2: 3% من إيداعاتهم\n🎁 المستوى 3: 2% من إيداعاتهم\n\nكلما دعوت أكثر، كلما ربحت أكثر! بدون حدود!', 'image': 'referral'},
        {'type': 'feature', 'title': 'مكافآت يومية وأسبوعية', 'text': '🎉 ElonInvest تكافئ مستثمريها يومياً!\n\n💰 مكافأة ترحيبية: 5$ فور التسجيل\n🔥 مكافأة أول إيداع: 10% إضافية\n📅 مكافأة يومية: 1-5$ حسب الاستمرارية\n🏆 مكافأة ولاء: 10$ كل 30 يوماً\n\nكل يوم تستمر فيه تكسب أكثر!', 'image': 'rewards'},
        {'type': 'feature', 'title': 'أمان واستقرار', 'text': '🔒 استثمارك آمن مع ElonInvest\n\n✅ تشفير متقدم لحماية بياناتك\n✅ مراقبة على مدار الساعة\n✅ تراخيص مالية دولية (FCA, CySEC, FinCEN, DFSA)\n✅ سحوبات فورية وآمنة\n\nنضع أموالك في أيدٍ أمينة.', 'image': 'security'},
        
        # Investment guides
        {'type': 'guide', 'title': 'كيف تبدأ الاستثمار؟', 'text': '📝 ابدأ رحلة الاستثمار في 3 خطوات:\n\n1️⃣ أنشئ حساب مجاني\n2️⃣ اختر خطة استثمارية تناسبك\n3⃣️ استثمر وابدأ جني الأرباح اليومية\n\n💡 نصيحة: ابدأ بخطة Tesla Starter (10$ فقط) وجرب النظام بنفسك!\n\nسجل الآن: https://eloninvest.publicvm.com', 'image': 'start'},
        {'type': 'guide', 'title': 'طريقة الإيداع عبر Trust Wallet', 'text': '📱 كيف تودع عبر Trust Wallet:\n\n1️⃣ افتح Trust Wallet\n2⃣ اختر USDT وشبكة TRC-20\n3⃣ أرسل إلى عنوان محفظة المنصة\n4⃣ انسخ TXID والصقه في صفحة الإيداع\n5⃣ يتم إضافة الرصيد فوراً!\n🚀 أسرع طريقة للاستثمار.', 'image': 'wallet'},
        {'type': 'guide', 'title': 'استراتيجيات الاستثمار الذكية', 'text': '🧠 استراتيجيات لزيادة أرباحك:\n\n📌 التنويع: وزع استثمارك على عدة خطط\n📌 إعادة الاستثمار: أعد استثمار أرباحك لتربح أكثر\n📌 الإحالة: ادعُ أصدقاءك واربح عمولات\n📌 الاستمرارية: المكافآت اليومية تزيد بدوامك\n\nاطبق هذه الاستراتيجيات وحقق أقصى عائد!', 'image': 'strategy'},
        {'type': 'guide', 'title': 'لماذا USDT؟', 'text': '💵 لماذا نستخدم USDT (Tether)؟\n\n✅ مستقر: 1 USDT = 1 دولار دائماً\n✅ سريع: معاملات فورية على شبكة TRC-20\n✅ منخفض الرسوم: رسوم نقل زهيدة جداً\n✅ عالمي: يقبل في جميع المنصات\n\nUSDT هو الخيار الأمثل للاستثمار الرقمي.', 'image': 'usdt'},
        
        # Success stories
        {'type': 'story', 'title': 'قصة نجاح أحمد', 'text': '⭐ قصة نجاح حقيقية:\n\nأحمد من السعودية بدأ باستثمار 100$ في خطة Tesla Starter.\n\n📈 بعد 30 يوماً:\n• أرباحه: 60$\n• الإجمالي: 160$\n• نسبة الربح: 60%\n\n💬 "أفضل قرار استثماري في حياتي!"\n\nابدأ مثله اليوم! https://eloninvest.publicvm.com', 'image': 'success1'},
        {'type': 'story', 'title': 'سارة تحقق دخل إضافي', 'text': '⭐ سارة من مصر، موظفة وأم لطفلين:\n\n"كنت أبحث عن دخل إضافي، وجدت ElonInvest. استثمرت 200$ في خطة SpaceX.\n\nالآن أربح 7$ يومياً بدون أي مجهود!\nهذا الدخل الإضافي غير حياتي."\n\n💪 أنت أيضاً تستطيع!', 'image': 'success2'},
        {'type': 'story', 'title': 'أكثر من 10,000 مستثمر', 'text': '🌍 ElonInvest اليوم:\n\n👥 أكثر من 10,000 مستثمر حول العالم\n💰 تم توزيع أرباح بأكثر من 2 مليون دولار\n🏆 مستثمرون من 50+ دولة\n\nانضم إلى مجتمع المستثمرين الناجحين اليوم!\n\n🚀 المستقبل يبدأ باستثمار ذكي.', 'image': 'community'},
        
        # Investment tips
        {'type': 'tip', 'title': 'نصيحة استثمارية', 'text': '💡 نصيحة اليوم:\n\nأفضل وقت للاستثمار كان بالأمس.\nثاني أفضل وقت هو اليوم!\n\nلا تؤجل قرارك الاستثماري.\nكل يوم تأخير = أرباح تفوتك.\n\n📈 ابدأ الآن: https://eloninvest.publicvm.com', 'image': 'tip1'},
        {'type': 'tip', 'title': 'سر الأرباح المركبة', 'text': '📊 سر الأرباح المركبة:\n\nعند إعادة استثمار أرباحك اليومية:\n• استثمار 100$ بعائد 5%\n• الشهر الأول: 150$\n• الشهر الثالث: 337$\n• الشهر السادس: 1,013$\n\n🧠 هذا هو سر بناء الثروة!\nأعد استثمار أرباحك اليوم.', 'image': 'compound'},
        {'type': 'tip', 'title': 'الاستثمار المنتظم', 'text': '🎯 الاستثمار المنتظم = نجاح مضمون\n\nبدلاً من استثمار مبلغ كبير مرة واحدة:\n📌 استثمر مبلغاً ثابتاً كل أسبوع\n📌 وزع المخاطر\n📌 استفد من العوائد المركبة\n📌 ابنِ محفظتك تدريجياً\n\n⑤ خطوة بخطوة نحو الحرية المالية!', 'image': 'regular'},
        {'type': 'tip', 'title': 'آمن استثمارك', 'text': '🛡️ نصائح الأمان:\n\n1. لا تشارك كلمة مرورك مع أي أحد\n2. فعّل التوثيق الثنائي (قريباً)\n3. استخدم محفظة Trust Wallet الرسمية\n4. تأكد من عنوان URL الصحيح\n5. تواصل مع الدعم فقط عبر القناة الرسمية\n\nأمانك أولويتنا الأولى.', 'image': 'safety'},
        
        # About companies
        {'type': 'company', 'title': 'Tesla - ثورة السيارات الكهربائية', 'text': '⚡ Tesla: أكثر من مجرد سيارة\n\n🚗 سيارات كهربائية صديقة للبيئة\n🔋 بطاريات Powerwall للمنازل\n☀️ ألواح شمسية Solar Roof\n🤖 روبوتات Optimus\n\nسهم Tesla من أقوى الأسهم أداءً في العقد الأخير!\nاستثمر في Tesla عبر ElonInvest.', 'image': 'tesla_about'},
        {'type': 'company', 'title': 'SpaceX - استكشاف الفضاء', 'text': '🚀 SpaceX: مستقبل البشرية في الفضاء\n\n🛰️ Starlink: إنترنت فضائي عالمي\n🌕 Starship: أول مركبة للمريخ\n🔄 Falcon 9: صواريخ قابلة لإعادة الاستخدام\n\nسبيس إكس تغير مفهوم الفضاء كما نعرفه!\nاستثمر مع SpaceX عبر ElonInvest.', 'image': 'spacex'},
        {'type': 'company', 'title': 'Neuralink - مستقبل العقل البشري', 'text': '🧠 Neuralink: ربط العقل بالحاسوب\n\n🔬 زراعة دماغية لعلاج الأمراض\n💻 واجهة دماغية حاسوبية\n🦾 مساعدة ذوي الاحتياجات الخاصة\n\nتقنية غيرت الطب الحديث!\nكن جزءاً من المستقبل مع Neuralink.', 'image': 'neuralink'},
        
        # Market news style
        {'type': 'market', 'title': 'تحديث السوق', 'text': '📈 تحديث أسعار أسهم إيلون ماسك:\n\n⚡ Tesla (TSLA): $245.50 📈\n🚀 SpaceX (Private): $180B تقييم\n🧠 Neuralink: تجارب بشرية ناجحة\n🐦 X: منصة المستقبل\n\nالاستثمار في هذه الشركات متاح عبر ElonInvest!\nعوائد يومية تبدأ من 2%.', 'image': 'market'},
        
        # Platform updates
        {'type': 'update', 'title': 'إيداع تلقائي عبر Trust Wallet', 'text': '🆕 ميزة جديدة!\n\nالآن يمكنك الإيداع عبر Trust Wallet تلقائياً:\n1️⃣ أرسل USDT (TRC-20) إلى عنوان المحفظة\n2️⃣ أدخل TXID\n3️⃣ يتم إضافة الرصيد فوراً!\n\n🚀 لا مزيد من الانتظار!\nودائع فورية وآمنة.', 'image': 'update'},
        {'type': 'update', 'title': 'إنجاز ElonInvest', 'text': '🏆 ElonInvest تحقق إنجازاً جديداً!\n\n✅ أكثر من 15,000 مستخدم نشط\n✅ 50+ دولة حول العالم\n✅ 2.5 مليون دولار أرباح موزعة\n✅ 99% رضا المستخدمين\n\nنشكر ثقتكم بنا!\nالمستقبل يبدو مشرقاً مع ElonInvest 🚀', 'image': 'milestone'},
    ],
    'en': [
        {'type': 'feature', 'title': 'Invest in Tesla Today', 'text': '🚀 Invest in Tesla stock through ElonInvest and earn daily returns up to 2%!\n\n✅ Daily profits\n✅ Withdraw anytime\n✅ Minimum $10 only\n\nStart with the strongest tech companies.', 'image': 'tesla'},
        {'type': 'feature', 'title': 'Diverse Investment Plans', 'text': '💎 Choose your investment plan:\n\n⚡ Tesla Starter: 2% daily\n🚀 SpaceX Voyager: 3.5% daily\n🧠 Neuralink Pioneer: 5% daily\n🐦 X Premium: 6.5% daily\n🕳 Boring Elite: 8% daily\n\nInvest from $10 and start earning daily.', 'image': 'plans'},
        {'type': 'feature', 'title': '3-Level Referral System', 'text': '👥 Earn by inviting friends!\n\n🎁 Level 1: 5% of their deposits\n🎁 Level 2: 3% of their deposits\n🎁 Level 3: 2% of their deposits\n\nThe more you invite, the more you earn! No limits!', 'image': 'referral'},
        {'type': 'feature', 'title': 'Daily & Weekly Rewards', 'text': '🎉 ElonInvest rewards its investors daily!\n\n💰 Welcome bonus: $5 instantly\n🔥 First deposit: 10% extra\n📅 Daily streak: $1-$5\n🏆 Loyalty: $10 every 30 days\n\nThe longer you stay, the more you earn!', 'image': 'rewards'},
        {'type': 'guide', 'title': 'How to Start Investing?', 'text': '📝 Start your investment journey in 3 steps:\n\n1️⃣ Create a free account\n2️⃣ Choose a plan that suits you\n3️⃣ Invest and earn daily profits\n\n💡 Tip: Start with Tesla Starter ($10) and try it!\n\nSign up: https://eloninvest.publicvm.com', 'image': 'start'},
        {'type': 'guide', 'title': 'Trust Wallet Deposit Guide', 'text': '📱 How to deposit via Trust Wallet:\n\n1️⃣ Open Trust Wallet\n2️⃣ Select USDT on TRC-20\n3️⃣ Send to platform wallet address\n4️⃣ Copy TXID and paste on deposit page\n5️⃣ Balance credited instantly!\n🚀 Fastest way to invest.', 'image': 'wallet'},
        {'type': 'story', 'title': 'Ahmed\'s Success Story', 'text': '⭐ Ahmed from Saudi started with $100 in Tesla Starter.\n\n📈 After 30 days:\n• Profit: $60\n• Total: $160\n• ROI: 60%\n\n💬 "Best investment decision I ever made!"\n\nStart like him today! https://eloninvest.publicvm.com', 'image': 'success1'},
        {'type': 'story', 'title': 'Sarah\'s Extra Income', 'text': '⭐ Sarah, a working mom:\n\n"I was looking for extra income. I found ElonInvest. I invested $200 in SpaceX plan.\n\nNow I earn $7 daily with zero effort!\nThis extra income changed my life."\n\n💪 You can do it too!', 'image': 'success2'},
        {'type': 'tip', 'title': 'Investment Tip', 'text': '💡 Tip of the day:\n\nThe best time to invest was yesterday.\nThe second best time is today!\n\nDon\'t delay your investment decision.\nEvery day you wait is profit you miss.\n\n📈 Start now: https://eloninvest.publicvm.com', 'image': 'tip1'},
        {'type': 'tip', 'title': 'The Power of Compound Interest', 'text': '📊 Compound interest secret:\n\nReinvest your daily profits:\n• $100 at 5% daily return\n• Month 1: $150\n• Month 3: $337\n• Month 6: $1,013\n\n🧠 This is the key to wealth!\nReinvest your profits today.', 'image': 'compound'},
        {'type': 'company', 'title': 'Tesla - EV Revolution', 'text': '⚡ Tesla: More than a car company\n\n🚗 Electric vehicles\n🔋 Powerwall batteries\n☀️ Solar Roof\n🤖 Optimus robots\n\nBest performing stock of the decade!\nInvest in Tesla through ElonInvest.', 'image': 'tesla_about'},
        {'type': 'company', 'title': 'SpaceX - Space Exploration', 'text': '🚀 SpaceX: Humanity\'s future in space\n\n🛰️ Starlink: Global space internet\n🌕 Starship: First Mars vehicle\n🔄 Falcon 9: Reusable rockets\n\nSpaceX is changing space access forever!\nInvest with ElonInvest.', 'image': 'spacex'},
        {'type': 'update', 'title': 'Auto Deposit via Trust Wallet', 'text': '🆕 New Feature!\n\nDeposit automatically via Trust Wallet:\n1️⃣ Send USDT (TRC-20) to wallet address\n2️⃣ Enter TXID\n3️⃣ Balance credited instantly!\n\n🚀 No more waiting!\nInstant and secure deposits.', 'image': 'update'},
        {'type': 'update', 'title': 'ElonInvest Milestone', 'text': '🏆 ElonInvest hits a new milestone!\n\n✅ 15,000+ active users\n✅ 50+ countries worldwide\n✅ $2.5M profits distributed\n✅ 99% user satisfaction\n\nThank you for your trust!\nThe future looks bright with ElonInvest 🚀', 'image': 'milestone'},
        {'type': 'feature', 'title': 'Secure & Reliable', 'text': '🔒 Your investment is safe with us\n\n✅ Advanced encryption\n✅ 24/7 monitoring\n✅ International licenses (FCA, CySEC, FinCEN, DFSA)\n✅ Instant secure withdrawals\n\nYour money is in safe hands.', 'image': 'security'},
    ]
}

IMAGE_KEYWORDS = {
    'tesla': 'Tesla+car+electric',
    'plans': 'investment+growth+chart',
    'referral': 'network+team+people',
    'rewards': 'reward+success+prize',
    'security': 'cyber+security+protection',
    'start': 'start+business+begin',
    'wallet': 'digital+wallet+crypto',
    'strategy': 'strategy+plan+success',
    'usdt': 'crypto+bitcoin+coin',
    'success1': 'success+happy+man',
    'success2': 'success+woman+office',
    'community': 'community+global+world',
    'tip1': 'business+tip+idea',
    'compound': 'growth+chart+money',
    'regular': 'calendar+schedule+plan',
    'safety': 'shield+safety+secure',
    'tesla_about': 'tesla+car+road',
    'spacex': 'space+rocket+launch',
    'neuralink': 'brain+technology+AI',
    'market': 'stock+market+chart',
    'update': 'update+notification+new',
    'milestone': 'trophy+achievement+goal',
}

def get_random_content(lang='ar'):
    items = CONTENT.get(lang, CONTENT['en'])
    return random.choice(items)

def get_content_by_type(lang='ar', content_type=None):
    items = CONTENT.get(lang, CONTENT['en'])
    if content_type:
        items = [i for i in items if i['type'] == content_type]
    return random.choice(items) if items else get_random_content(lang)
