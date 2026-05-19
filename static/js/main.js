document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(el) { return new bootstrap.Tooltip(el); });

    var themeToggle = document.getElementById('themeToggle');
    var themeIcon = document.getElementById('themeIcon');
    var savedTheme = localStorage.getItem('eloninvest_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    if (themeIcon) {
        themeIcon.className = savedTheme === 'dark' ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
    }
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            var current = document.documentElement.getAttribute('data-theme');
            var next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('eloninvest_theme', next);
            if (themeIcon) {
                themeIcon.className = next === 'dark' ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
            }
        });
    }

    var lang = document.documentElement.lang || 'en';

    // === Top Notification Bar ===
    var topNotifications = [
        { en: 'Ahmed withdrew $2,500 from Tesla plan', ar: 'أحمد سحب 2,500 دولار من خطة تيسلا' },
        { en: 'Sarah deposited $5,000 to SpaceX plan', ar: 'سارة أودعت 5,000 دولار في خطة سبيس إكس' },
        { en: 'Mohamed earned $1,200 profit from Neuralink', ar: 'محمد حقق ربح 1,200 دولار من نيورالينك' },
        { en: 'Layla joined with $10,000 investment', ar: 'ليلى انضمت باستثمار 10,000 دولار' },
        { en: 'Omar withdrew $3,000 profit from X plan', ar: 'عمر سحب 3,000 دولار ربح من خطة إكس' },
        { en: 'Nora earned $850 today in daily profits', ar: 'نورة حققت 850 دولاراً أرباحاً يومية اليوم' },
        { en: 'Khalid deposited $15,000 into Boring Company', ar: 'خالد أودع 15,000 دولار في خطة بورينج' },
        { en: 'Hind referred 5 new investors this week', ar: 'هند أحالت 5 مستثمرين جدد هذا الأسبوع' },
        { en: 'Faisal received $2,200 referral bonus', ar: 'فيصل استلم مكافأة إحالة 2,200 دولار' },
        { en: 'Amina traded $7,500 profit on market today', ar: 'أمينة حققت ربح 7,500 دولار في السوق اليوم' },
        { en: 'Saeed upgraded to Neuralink premium plan', ar: 'سعيد ترقى إلى خطة نيورالينك المميزة' },
        { en: 'Mona completed 30-day loyalty bonus $500', ar: 'منى أكملت مكافأة الولاء 30 يوماً 500 دولار' }
    ];

    var notificationSpan = document.getElementById('notificationText');
    if (notificationSpan) {
        var idx = 0;
        setInterval(function() {
            var notif = topNotifications[idx % topNotifications.length];
            notificationSpan.textContent = notif[lang] || notif['en'];
            notificationSpan.style.animation = 'none';
            void notificationSpan.offsetHeight;
            notificationSpan.style.animation = 'fadeInUp 0.5s ease';
            idx++;
        }, 5000);
    }

    // === Floating Toast Notifications (bottom-left) ===
    var toastNotifications = [
        { name: 'Ahmed M.', action: 'deposit', amount: 2500, plan: 'Tesla', en: 'deposited {amt} to Tesla plan', ar: 'أودع {amt} في خطة تيسلا' },
        { name: 'Sarah K.', action: 'withdraw', amount: 4800, plan: 'SpaceX', en: 'withdrew {amt} from SpaceX', ar: 'سحب {amt} من سبيس إكس' },
        { name: 'Mohamed A.', action: 'deposit', amount: 3200, plan: 'Neuralink', en: 'deposited {amt} to Neuralink', ar: 'أودع {amt} في نيورالينك' },
        { name: 'Layla H.', action: 'profit', amount: 1250, plan: 'X Premium', en: 'earned {amt} profit on X plan', ar: 'حقق ربح {amt} من خطة إكس' },
        { name: 'Omar F.', action: 'withdraw', amount: 6100, plan: 'Boring', en: 'withdrew {amt} from Boring Co.', ar: 'سحب {amt} من بورينج' },
        { name: 'Nora S.', action: 'deposit', amount: 5600, plan: 'Tesla', en: 'deposited {amt} to Tesla plan', ar: 'أودع {amt} في خطة تيسلا' },
        { name: 'Khalid R.', action: 'profit', amount: 2100, plan: 'SpaceX', en: 'earned {amt} profit on SpaceX', ar: 'حقق ربح {amt} من سبيس إكس' },
        { name: 'Hind W.', action: 'referral', amount: 880, plan: '', en: 'received {amt} referral bonus', ar: 'استلم مكافأة إحالة {amt}' },
        { name: 'Faisal T.', action: 'withdraw', amount: 3400, plan: 'Neuralink', en: 'withdrew {amt} from Neuralink', ar: 'سحب {amt} من نيورالينك' },
        { name: 'Amina D.', action: 'deposit', amount: 12000, plan: 'Boring', en: 'deposited {amt} to Boring Co.', ar: 'أودع {amt} في بورينج' },
        { name: 'Saeed N.', action: 'profit', amount: 4300, plan: 'X Premium', en: 'earned {amt} profit this week', ar: 'حقق ربح {amt} هذا الأسبوع' },
        { name: 'Mona L.', action: 'deposit', amount: 1900, plan: 'Tesla', en: 'deposited {amt} to Tesla plan', ar: 'أودع {amt} في خطة تيسلا' },
        { name: 'Yusuf B.', action: 'withdraw', amount: 7800, plan: 'SpaceX', en: 'withdrew {amt} from SpaceX', ar: 'سحب {amt} من سبيس إكس' },
        { name: 'Nadia J.', action: 'referral', amount: 1520, plan: '', en: 'earned {amt} from referrals', ar: 'ربح {amt} من الإحالات' },
        { name: 'Ali H.', action: 'deposit', amount: 4450, plan: 'Neuralink', en: 'deposited {amt} to Neuralink', ar: 'أودع {amt} في نيورالينك' },
    ];

    var container = document.getElementById('toast-container');
    if (container) {
        function showToast() {
            var t = toastNotifications[Math.floor(Math.random() * toastNotifications.length)];
            var amount = '$' + t.amount.toLocaleString();
            var msg = (t[lang] || t['en']).replace('{amt}', amount);
            var icons = { deposit: 'bi bi-plus-circle', withdraw: 'bi bi-send', profit: 'bi bi-graph-up-arrow', referral: 'bi bi-people' };

            var el = document.createElement('div');
            el.className = 'toast-item';
            el.innerHTML = '<div class="toast-icon ' + t.action + '"><i class="' + (icons[t.action] || 'bi bi-bell') + '"></i></div><div class="toast-content"><div class="toast-title">' + t.name + '</div><div class="toast-desc">' + msg + '</div></div><span class="toast-time">just now</span>';
            container.appendChild(el);

            if (container.children.length > 3) {
                container.removeChild(container.firstChild);
            }

            setTimeout(function() {
                el.classList.add('toast-out');
                setTimeout(function() { if (el.parentNode) el.parentNode.removeChild(el); }, 400);
            }, 4000);
        }

        showToast();
        setInterval(showToast, 8000 + Math.random() * 4000);
    }

    // === Random Testimonial Rotation ===
    var testimonials = [
        { name: 'Ahmed Al-Rashid', meta: 'Dubai, UAE · Investor since 2023', initials: 'AR', color: 'rgba(240,185,11,0.15)', textColor: 'var(--accent-gold)', quoteEn: 'I started with just $100 and now I am earning over $50 daily. This platform changed my financial future!', quoteAr: 'بدأت بمبلغ 100 دولار فقط والآن أربح أكثر من 50 دولاراً يومياً. هذه المنصة غيرت مستقبلي المالي!' },
        { name: 'Sarah Johnson', meta: 'London, UK · Investor since 2024', initials: 'SJ', color: 'rgba(59,130,246,0.15)', textColor: 'var(--accent-blue)', quoteEn: 'The referral system is amazing! I earned over $2,000 from my network in just one month.', quoteAr: 'نظام الإحالة رائع! ربحت أكثر من 2,000 دولار من شبكتي في شهر واحد فقط.' },
        { name: 'Mohamed Karim', meta: 'Casablanca, Morocco · Investor since 2022', initials: 'MK', color: 'rgba(16,185,129,0.15)', textColor: 'var(--accent-green)', quoteEn: 'Finally a platform that delivers what it promises. Daily profits, instant support, and real results!', quoteAr: 'أخيراً منصة تفي بوعودها. أرباح يومية، دعم فوري، ونتائج حقيقية!' },
        { name: 'Nora Al-Saud', meta: 'Riyadh, KSA · Investor since 2023', initials: 'NS', color: 'rgba(168,85,247,0.15)', textColor: '#a855f7', quoteEn: 'I was skeptical at first, but the daily payouts are real. My family now has a second income stream.', quoteAr: 'كنت متشككة في البداية، لكن الأرباح اليومية حقيقية. عائلتي الآن لديها مصدر دخل ثاني.' },
        { name: 'Omar Hassan', meta: 'Cairo, Egypt · Investor since 2024', initials: 'OH', color: 'rgba(249,115,22,0.15)', textColor: 'var(--accent-orange)', quoteEn: 'Withdrawals are fast and the team is professional. I have tripled my investment in 3 months!', quoteAr: 'السحوبات سريعة والفريق محترف. لقد ضاعفت استثماري ثلاث مرات في 3 أشهر!' },
        { name: 'Layla Chen', meta: 'Singapore · Investor since 2023', initials: 'LC', color: 'rgba(6,182,212,0.15)', textColor: 'var(--accent-cyan)', quoteEn: 'The 3-level referral system is genius. I am earning commissions even from people I did not directly invite.', quoteAr: 'نظام الإحالة ثلاثي المستويات عبقري. أنا أربح عمولات حتى من أشخاص لم أدعهم مباشرة.' },
        { name: 'Khalid Al-Mansouri', meta: 'Abu Dhabi, UAE · Investor since 2022', initials: 'KM', color: 'rgba(240,185,11,0.15)', textColor: 'var(--accent-gold)', quoteEn: 'I reinvest my daily profits and watch my portfolio grow. This is the future of passive income.', quoteAr: 'أعيد استثمار أرباحي اليومية وأشاهد محفظتي تنمو. هذا هو مستقبل الدخل السلبي.' },
        { name: 'Amina Diallo', meta: 'Dakar, Senegal · Investor since 2024', initials: 'AD', color: 'rgba(59,130,246,0.15)', textColor: 'var(--accent-blue)', quoteEn: 'ElonInvest made investing accessible for me. The minimum deposit is low and the returns are consistent.', quoteAr: 'ElonInvest جعلت الاستثمار في متناول يدي. الحد الأدنى للإيداع منخفض والعوائد منتظمة.' },
    ];

    var tQuote = document.getElementById('tQuote');
    var tName = document.getElementById('tName');
    var tMeta = document.getElementById('tMeta');
    var tAvatar = document.getElementById('tAvatar');
    var dotsContainer = document.getElementById('testimonialDots');

    if (tQuote && testimonials.length > 0) {
        var currentT = 0;

        function renderTestimonial(idx) {
            var t = testimonials[idx];
            tQuote.textContent = '"' + (t['quote' + (lang === 'ar' ? 'Ar' : 'En')] || t.quoteEn) + '"';
            tName.textContent = t.name;
            tMeta.textContent = t.meta;
            tAvatar.textContent = t.initials;
            tAvatar.style.background = t.color;
            tAvatar.style.color = t.textColor;
        }

        testimonials.forEach(function(_, i) {
            var dot = document.createElement('button');
            dot.className = 'testimonial-dot' + (i === 0 ? ' active' : '');
            dot.style.background = 'var(--accent-gold)';
            dot.addEventListener('click', function() {
                currentT = i;
                document.querySelectorAll('.testimonial-dot').forEach(function(d) { d.classList.remove('active'); });
                dot.classList.add('active');
                renderTestimonial(i);
            });
            dotsContainer.appendChild(dot);
        });

        renderTestimonial(0);

        setInterval(function() {
            document.querySelectorAll('.testimonial-dot').forEach(function(d) { d.classList.remove('active'); });
            currentT = (currentT + 1) % testimonials.length;
            var dots = document.querySelectorAll('.testimonial-dot');
            if (dots[currentT]) dots[currentT].classList.add('active');
            renderTestimonial(currentT);
        }, 5000);
    }

    // === Plan Cards Hover ===
    var planCards = document.querySelectorAll('.plan-card');
    planCards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.borderColor = 'rgba(240,185,11,0.3)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.borderColor = 'rgba(255,255,255,0.08)';
        });
    });

    // === Copy Address for Deposit Page ===
    window.copyAddr = function(id) {
        var input = document.getElementById(id);
        if (!input) return;
        input.select();
        input.setSelectionRange(0, 99999);
        navigator.clipboard.writeText(input.value);
        var btn = input.nextElementSibling;
        if (!btn) return;
        var orig = btn.innerHTML;
        btn.innerHTML = '<i class="bi bi-check-lg"></i>';
        setTimeout(function() { btn.innerHTML = orig; }, 2000);
    };
});
