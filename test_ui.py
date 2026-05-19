"""UI integration tests using one Flask test client per test group."""
import re, sys, os
from app import create_app
from datetime import datetime, timedelta

app = create_app()
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = True
failed = []

with app.app_context():
    from core.extensions import db
    from core.models import User, Transaction, Investment
    from werkzeug.security import generate_password_hash
    import uuid

    # — Seed test user (skip if exists, for idempotent re-runs) —
    pw = generate_password_hash('test123')
    existing = User.query.filter_by(email='ui@t.com').first()
    if existing:
        UID = existing.id
        print('Test user already exists, reusing UID=' + str(UID))
    else:
        ref = uuid.uuid4().hex[:16]
        u = User(
            username='uitest', email='ui@t.com', password_hash=pw,
            balance=500, total_profit=0, total_deposits=1000, total_withdrawn=200,
            total_invested=0, email_verified=True, is_admin=False, referral_code=ref,
            daily_streak=0, lang='en', payment_method='TTYdsoYhYabq9e4kByamzACpYj5PzP3Q5e',
            last_login_ip='', first_deposit_date=None, created_at=datetime.utcnow(),
            last_login=datetime.utcnow()
        )
        db.session.add(u)
        db.session.flush()
        # Seed pending transactions for admin Approve/Reject test
        db.session.add(Transaction(user_id=u.id, type='deposit', amount=250, status='pending', note='Test pending deposit'))
        db.session.add(Transaction(user_id=u.id, type='withdraw', amount=100, status='pending', note='Test pending withdraw'))
        db.session.commit()
        UID = u.id

    # — Seed unverified user for email verification tests —
    unv = User.query.filter_by(email='unverified@x.com').first()
    if unv:
        unv.email_verified = False
        unv.verification_token = 'test_verify_token_abc123'
    else:
        unv = User(
            username='unverified', email='unverified@x.com', password_hash=pw,
            balance=0, email_verified=False, is_admin=False,
            referral_code=uuid.uuid4().hex[:16], verification_token='test_verify_token_abc123',
            lang='en', created_at=datetime.utcnow(), last_login=datetime.utcnow()
        )
        db.session.add(unv)
    db.session.commit()
    UNV_UID = unv.id

    def check(body, keyword, label):
        if keyword in body:
            print(f'OK: {label}')
        else:
            print(f'FAIL: {label}')
            failed.append(label)

    def check_bool(condition, label):
        if condition:
            print(f'OK: {label}')
        else:
            print(f'FAIL: {label}')
            failed.append(label)

    def login(c, email, password):
        r = c.get('/auth/login', follow_redirects=True)
        csrf = re.search(rb'name="csrf_token".*?value="([^"]+)"', r.data)
        if not csrf:
            # might be already logged in — logout first
            c.get('/auth/logout', follow_redirects=True)
            r = c.get('/auth/login')
            csrf = re.search(rb'name="csrf_token".*?value="([^"]+)"', r.data)
        c.post('/auth/login', data={'email': email, 'password': password, 'csrf_token': csrf.group(1).decode()}, follow_redirects=True)

    with app.test_client() as c:
        # === 1. Index (anonymous) ===
        body = c.get('/').data
        for kw, lb in [
            (b'Invest in the Future', 'Index: hero title'),
            (b'license-card', 'Index: licenses'),
            (b'FCA', 'Index: FCA'),
            (b'CySEC', 'Index: CySEC'),
            (b'FinCEN', 'Index: FinCEN'),
            (b'DFSA', 'Index: DFSA'),
            (b'What Our Investors Say', 'Index: testimonials'),
            (b'toast-container', 'Index: toast-container'),
            (b'testimonial-avatar', 'Index: testimonial-avatar'),
            (b'testimonialDots', 'Index: testimonialDots'),
        ]:
            check(body, kw, lb)

        # === 2. Withdraw + Deposit (uitest) ===
        login(c, 'ui@t.com', 'test123')

        # Withdraw — new professional layout
        body = c.get('/investment/withdraw').data
        for kw, lb in [
            (b'Wallet Overview', 'Withdraw: wallet-overview'),
            (b'Available Balance', 'Withdraw: available-balance'),
            (b'Request Withdrawal', 'Withdraw: request-form'),
            (b'Withdrawal History', 'Withdraw: history'),
            (b'USDT', 'Withdraw: USDT'),
            (b'Secure Process', 'Withdraw: secure-process'),
            (b'Processing Time', 'Withdraw: processing-time'),
            (b'24/7 Support', 'Withdraw: support'),
            (b'$500.00', 'Withdraw: balance'),
            (b'$1000.00', 'Withdraw: deposits'),
            (b'$200.00', 'Withdraw: withdrawn'),
            (b'withdraw-pm-card', 'Withdraw: PM cards'),
            (b'Select Payment Method', 'Withdraw: select PM'),
            (b'Select Network', 'Withdraw: select network'),
            (b'withdraw_network', 'Withdraw: network dropdown'),
            (b'Enter Wallet Address', 'Withdraw: enter address'),
            (b'withdraw_address', 'Withdraw: address input'),
            (b'pasteAddress', 'Withdraw: paste button'),
            (b'setMaxAmount', 'Withdraw: max button'),
            (b'withdrawSummary', 'Withdraw: summary box'),
            (b'You will receive', 'Withdraw: summary text'),
            (b'validateWithdrawForm', 'Withdraw: JS validation'),
            (b'networkOptions', 'Withdraw: network options JS'),
        ]:
            check(body, kw, lb)

        # Test POST withdrawal with new fields (app uses no CSRFProtect on raw forms)
        resp = c.post('/investment/withdraw', data={
            'amount': '50',
            'withdraw_method': 'USDT',
            'withdraw_network': 'TRC-20',
            'withdraw_address': 'TTestWalletAddress1234567890',
        }, follow_redirects=True)
        check(resp.data, b'Awaiting admin approval', 'Withdraw: POST success')
        # Verify the transaction was created with details
        from core.models import Transaction as Tx2
        tx = Tx2.query.filter_by(user_id=UID, type='withdraw', amount=50.0).first()
        if tx and tx.withdraw_method == 'USDT' and tx.withdraw_network == 'TRC-20' and tx.withdraw_address == 'TTestWalletAddress1234567890':
            print('OK: Withdraw: transaction details saved')
        else:
            print(f'FAIL: Withdraw: transaction details missing — method={tx.withdraw_method if tx else None} net={tx.withdraw_network if tx else None} addr={tx.withdraw_address if tx else None}')
            failed.append('Withdraw: tx details')

        # Deposit
        dep = c.get('/investment/deposit').data
        check(dep, b'TTYdsoYhYabq9e4kByamzACpYj5PzP3Q5e', 'Deposit: USDT addr')
        check(dep, b'Deposit Address', 'Deposit: address')
        check(dep, b'TRX', 'Deposit: network')

        # === 3. Profile page — professional redesign ===
        prof = c.get('/user/profile').data
        for kw, lb in [
            (b'profile-cover', 'Profile: cover banner'),
            (b'profile-avatar', 'Profile: avatar'),
            (b'profile-stat', 'Profile: stat cards'),
            (b'profile-tabs', 'Profile: tab nav'),
            (b'Personal Info', 'Profile: personal info tab'),
            (b'Security', 'Profile: security tab'),
            (b'Payment Info', 'Profile: payment info tab'),
            (b'Referral Code', 'Profile: referral code field'),
            (b'Save Changes', 'Profile: save button'),
            (b'Email Verified', 'Profile: email verified'),
            (b'Last Login', 'Profile: last login'),
            (b'uitest', 'Profile: username'),
            (b'ui@t.com', 'Profile: email'),
            (b'profile-info-card', 'Profile: info cards'),
        ]:
            check(prof, kw, lb)

        # === 4. Email verification flow ===
        login(c, 'unverified@x.com', 'test123')
        unv_dash = c.get('/user/dashboard').data
        check(unv_dash, b'verify-bar', 'Verify: banner shown on dashboard')
        check(unv_dash, b'Verify Now', 'Verify: button text')
        # Redirected from protected routes
        dep_r = c.get('/investment/deposit', follow_redirects=True).data
        check(dep_r, b'verify your email', 'Verify: deposit redirects to profile')
        wd_r = c.get('/investment/withdraw', follow_redirects=True).data
        check(wd_r, b'verify your email', 'Verify: withdraw redirects to profile')
        ref_r = c.get('/referral/', follow_redirects=True).data
        check(ref_r, b'verify your email', 'Verify: referral redirects to profile')
        # Verify via token works
        vr = c.get('/auth/verify/test_verify_token_abc123', follow_redirects=True).data
        check(vr, b'Email Verified', 'Verify: success page')
        check(vr, b'bi-pie-chart', 'Verify: success invest icon')
        check(vr, b'bi-arrow-up-right', 'Verify: success withdraw icon')
        check(vr, b'bi-people', 'Verify: success referral icon')
        check(vr, b'bi-gift', 'Verify: success rewards icon')
        # Invalid token shows failed page
        vf = c.get('/auth/verify/invalidtoken123', follow_redirects=True).data
        check(vf, b'Verification Link Invalid', 'Verify: failed page')
        check(vf, b'bi-x-circle-fill', 'Verify: failed icon')
        # After verification, banner is gone
        dash2 = c.get('/user/dashboard').data
        if b'verify-bar' in dash2:
            print('FAIL: Verify: banner still shown after verification')
            failed.append('Verify: banner after verification')
        else:
            print('OK: Verify: banner hidden after verification')

        # === 5. Admin transactions ===
        login(c, 'admin@eloninvest.com', 'admin123')
        adm = c.get('/admin/transactions').data
        check(adm, b'Manage Transactions', 'Admin: transactions')
        check(adm, b'Approve', 'Admin: approve')
        check(adm, b'Reject', 'Admin: reject')
        check(adm, b'USDT', 'Admin: tx method shown')
        check(adm, b'TRC-20', 'Admin: tx network shown')
        check(adm, b'TTestWallet', 'Admin: tx address shown')
        check(adm, b'ui@t.com', 'Admin: tx email shown')
        check(adm, b'check-lg', 'Admin: tx deposited-before icon')
        check(adm, b'Deposited Before', 'Admin: tx deposited-before col')

        # === 6. Admin users — ban/delete buttons ===
        users_body = c.get('/admin/users').data
        check(users_body, b'Manage Users', 'Admin: users page')
        check(users_body, b'ui@t.com', 'Admin: users email')
        check(users_body, b'/ban', 'Admin: ban route in page')
        check(users_body, b'/delete', 'Admin: delete route in page')
        check(users_body, b'bi-lock', 'Admin: ban button icon')
        check(users_body, b'bi-trash', 'Admin: delete button icon')

        # === 7. Admin payment methods — professional UI ===
        pm_body = c.get('/admin/payment-methods').data
        check(pm_body, b'Add Method', 'Admin: PM add button')
        check(pm_body, b'Active', 'Admin: PM active badge')
        check(pm_body, b'USDT', 'Admin: PM USDT label')
        check(pm_body, b'Address:', 'Admin: PM parsed address')
        check(pm_body, b'Network:', 'Admin: PM parsed network')
        check(pm_body, b'btn-outline-primary', 'Admin: PM visible edit btn')
        check(pm_body, b'btn-outline-danger', 'Admin: PM visible delete btn')

        # === 8. Ban test: create banned user (skip if exists), verify login blocked ===
        if not User.query.filter_by(email='banned@x.com').first():
            banned = User(
                username='banneduser', email='banned@x.com', password_hash=pw,
                balance=0, is_admin=False, is_banned=True, referral_code=uuid.uuid4().hex[:16],
                lang='en', email_verified=True, created_at=datetime.utcnow(), last_login=datetime.utcnow()
            )
            db.session.add(banned)
            db.session.commit()
        with app.test_client() as c2:
            r = c2.get('/auth/login', follow_redirects=True)
            m = re.search(rb'name="csrf_token".*?value="([^"]+)"', r.data)
            if not m:
                c2.get('/auth/logout', follow_redirects=True)
                r = c2.get('/auth/login', follow_redirects=True)
                m = re.search(rb'name="csrf_token".*?value="([^"]+)"', r.data)
            csrf_b = m.group(1).decode() if m else ''
            resp = c2.post('/auth/login', data={'email': 'banned@x.com', 'password': 'test123', 'csrf_token': csrf_b}, follow_redirects=True)
            if b'account has been suspended' in resp.data.lower() or b'banned' in resp.data.lower() or b'suspended' in resp.data.lower() or b'Invalid email or password' in resp.data:
                print('OK: Auth: banned user blocked')
            else:
                print(f'FAIL: Auth: banned user not blocked — snippet: {resp.data[:300]}')
                failed.append('Auth: ban block')

        # === 9. JS checks ===
        js = open('static/js/main.js', 'r', encoding='utf-8').read()
        for kw, lb in [
            ('showToast', 'JS: showToast'),
            ('toastNotifications', 'JS: toastNotifications'),
            ('testimonials', 'JS: testimonials'),
            ('renderTestimonial', 'JS: renderTestimonial'),
            ('window.copyAddr', 'JS: copyAddr'),
        ]:
            check(js, kw, lb)

        # === 10. CSS checks ===
        css = open('static/css/style.css', 'r', encoding='utf-8').read()
        for kw, lb in [
            ('toast-item', 'CSS: toast-item'),
            ('toastIn', 'CSS: toastIn'),
            ('testimonial-avatar', 'CSS: testimonial-avatar'),
            ('testimonial-dot', 'CSS: testimonial-dot'),
            ('license-card', 'CSS: license-card'),
            ('license-divider', 'CSS: license-divider'),
            ('profile-cover', 'CSS: profile-cover'),
            ('profile-stat', 'CSS: profile-stat'),
            ('profile-tabs', 'CSS: profile-tabs'),
            ('profile-info-card', 'CSS: profile-info-card'),
            ('verify-bar', 'CSS: verify-bar'),
        ]:
            check(css, kw, lb)

        # === 11. Favicon ===
        svg = open('static/images/favicon.svg', 'r', encoding='utf-8').read()
        check(svg, 'f0b90b', 'Favicon: gold gradient color')
        check(svg, '070b1a', 'Favicon: dark background')
        check(svg, 'M36 4L16 36h10l-2 24 22-32H36l2-24z', 'Favicon: lightning path')
        # Favicon linked in base.html
        base = open('templates/base.html', 'r', encoding='utf-8').read()
        check(base, 'favicon.svg', 'Favicon: linked in base.html')
        check(base, 'type="image/svg+xml"', 'Favicon: SVG type declared')
        # Favicon served at /static/images/favicon.svg
        fav = c.get('/static/images/favicon.svg').data
        check(fav, b'f0b90b', 'Favicon: served by Flask')

        # === 12. PWA / Android App ===
        manifest = open('static/manifest.json', 'r', encoding='utf-8').read()
        check(manifest, '"standalone"', 'PWA: display standalone')
        check(manifest, 'icon-192.png', 'PWA: 192 icon')
        check(manifest, 'icon-512.png', 'PWA: 512 icon')
        check(manifest, '"#070b1a"', 'PWA: bg_color')
        check(manifest, '"#f0b90b"', 'PWA: theme_color')
        sw = open('static/js/sw.js', 'r', encoding='utf-8').read()
        check(sw, 'eloninvest-v1', 'SW: cache name')
        check(sw, 'install', 'SW: install event')
        check(sw, 'fetch', 'SW: fetch event')
        base = open('templates/base.html', 'r', encoding='utf-8').read()
        check(base, 'manifest.json', 'PWA: manifest linked')
        check(base, 'apple-mobile-web-app-capable', 'PWA: iOS support')
        check(base, 'serviceWorker', 'PWA: SW registration')
        check(base, 'sw.js', 'PWA: SW file')
        # Icons exist and are valid PNGs
        for s in ['192', '512']:
            ico = open(f'static/images/icon-{s}.png', 'rb').read()
            if ico[:8] == b'\x89PNG\r\n\x1a\n':
                print(f'OK: PWA: icon-{s}.png valid PNG')
            else:
                print(f'FAIL: PWA: icon-{s}.png invalid')
                failed.append(f'PWA icon-{s}')

        # === 13. Referral system comprehensive tests ===
        login(c, 'admin@eloninvest.com', 'admin123')
        from core.models import Plan as PlanModel, Referral as RefModel
        from services.referral import distribute_referral_commission
        import uuid as _uuid
        # Clear prior referral test data for idempotent re-runs
        for u in User.query.filter(User.email.like('%@x.com')).all():
            RefModel.query.filter_by(referred_id=u.id).delete()
            RefModel.query.filter_by(referrer_id=u.id).delete()
        # Create 3 users in a chain: A (root) -> B (level1) -> C (level2)
        uA = User.query.filter_by(email='refA@x.com').first()
        if not uA:
            uA = User(username='refA', email='refA@x.com', password_hash=pw, balance=100, referral_code=_uuid.uuid4().hex[:16], lang='en', email_verified=True, created_at=datetime.utcnow(), last_login=datetime.utcnow())
            db.session.add(uA); db.session.flush()
        uB = User.query.filter_by(email='refB@x.com').first()
        if not uB:
            uB = User(username='refB', email='refB@x.com', password_hash=pw, balance=100, referral_code=_uuid.uuid4().hex[:16], referred_by_id=uA.id, lang='en', email_verified=True, created_at=datetime.utcnow(), last_login=datetime.utcnow())
            db.session.add(uB); db.session.flush()
        uC = User.query.filter_by(email='refC@x.com').first()
        if not uC:
            uC = User(username='refC', email='refC@x.com', password_hash=pw, balance=0, referral_code=_uuid.uuid4().hex[:16], referred_by_id=uB.id, lang='en', email_verified=True, created_at=datetime.utcnow(), last_login=datetime.utcnow())
            db.session.add(uC); db.session.flush()
        db.session.commit()
        refA = uA.referral_code
        check(c.get('/admin/users').data, b'refA@x.com', 'Referral: users created')

        # Referral code ?ref= pre-fills the form
        c.get('/auth/logout', follow_redirects=True)
        reg_body = c.get('/auth/register?ref=' + refA).data
        kw_ref = 'value="' + refA + '"'
        check(reg_body, kw_ref.encode(), 'Referral: ref param pre-fills form')
        login(c, 'admin@eloninvest.com', 'admin123')

        # Commission distribution: C deposits $200 -> L1 (B) gets 5%, L2 (A) gets 3%
        uB_bal_before = db.session.get(User, uB.id).balance
        uA_bal_before = db.session.get(User, uA.id).balance
        distribute_referral_commission(uC, 200, app)
        db.session.commit()
        l1 = RefModel.query.filter_by(referred_id=uC.id, level=1).first()
        l2 = RefModel.query.filter_by(referred_id=uC.id, level=2).first()
        check_bool(l1 is not None and abs(l1.commission - 10.0) < 0.01, 'Referral: L1 5% commission on $200 = $10')
        check_bool(l2 is not None and abs(l2.commission - 6.0) < 0.01, 'Referral: L2 3% commission on $200 = $6')
        check_bool(abs(db.session.get(User, uB.id).balance - uB_bal_before - 10.0) < 0.01, 'Referral: L1 balance +$10')
        check_bool(abs(db.session.get(User, uA.id).balance - uA_bal_before - 6.0) < 0.01, 'Referral: L2 balance +$6')

        # No commission on zero-level (no referrer)
        uD = User.query.filter_by(email='refD@x.com').first()
        if not uD:
            uD = User(username='refD', email='refD@x.com', password_hash=pw, balance=0, referral_code=_uuid.uuid4().hex[:16], lang='en', email_verified=True, created_at=datetime.utcnow(), last_login=datetime.utcnow())
            db.session.add(uD); db.session.commit()
        distribute_referral_commission(uD, 100, app)
        db.session.commit()
        l0 = RefModel.query.filter_by(referred_id=uD.id).all()
        check_bool(len(l0) == 0, 'Referral: no commission for user without referrer')

        # Multiple deposits create multiple referral records (commission on every deposit)
        distribute_referral_commission(uC, 300, app)
        db.session.commit()
        l1b = RefModel.query.filter_by(referred_id=uC.id, level=1).count()
        l2b = RefModel.query.filter_by(referred_id=uC.id, level=2).count()
        check_bool(l1b == 2, 'Referral: 2nd deposit creates 2nd L1 record')
        check_bool(l2b == 2, 'Referral: 2nd deposit creates 2nd L2 record')

        # === 12. Daily profit comprehensive tests ===
        from services.profit import distribute_daily_profits
        # Clean up prior profit transactions and investments for uD
        Transaction.query.filter_by(user_id=uD.id, type='profit').delete()
        Investment.query.filter_by(user_id=uD.id).delete()
        db.session.commit()
        plan = PlanModel.query.first()
        inv = Investment(user_id=uD.id, plan_id=plan.id, amount=500, start_date=datetime.utcnow(), end_date=datetime.utcnow() + timedelta(days=plan.duration_days), status='active')
        db.session.add(inv)
        db.session.commit()
        INV_ID = inv.id
        bal_before = db.session.get(User, uD.id).balance
        distribute_daily_profits(app)
        bal_after = db.session.get(User, uD.id).balance
        expected_profit = round(500 * plan.daily_roi, 2)
        check_bool(abs(bal_after - bal_before - expected_profit) < 0.01, f'Profit: daily profit = ${expected_profit} on $500 at {plan.daily_roi*100}%')
        # Check Transaction created
        profit_tx = Transaction.query.filter_by(user_id=uD.id, type='profit').first()
        check_bool(profit_tx is not None and abs(profit_tx.amount - expected_profit) < 0.01, 'Profit: transaction record created')

        # Investment completion: set end_date in past, run profit
        past_inv = db.session.get(Investment, INV_ID)
        past_inv.end_date = datetime.utcnow() - timedelta(days=1)
        db.session.commit()
        distribute_daily_profits(app)
        # Should be completed now, no more profit
        check_bool(db.session.get(Investment, INV_ID).status == 'completed', 'Profit: investment completed after end_date')
        count_after = Transaction.query.filter_by(user_id=uD.id, type='profit').count()
        check_bool(count_after == 1, 'Profit: no additional profit after completion')

        # === 13. 18-page regression ===
        urls = ['/', '/auth/login', '/auth/register', '/market/', '/user/dashboard', '/user/profile',
                '/investment/plans', '/investment/deposit', '/investment/withdraw', '/investment/history',
                '/referral/', '/rewards/', '/admin/', '/admin/users', '/admin/transactions',
                '/admin/plans', '/admin/payment-methods', '/admin/user/1']
        ok = 0
        for url in urls:
            try:
                resp = c.get(url, follow_redirects=True)
                assert resp.status_code < 400, f'{resp.status_code} for {url}'
                assert b'Traceback' not in resp.data, f'Traceback in {url}'
                ok += 1
            except Exception as e:
                print(f'FAIL regression {url}: {e}')
                failed.append(f'regression_{url}')
        print(f'Regression: {ok}/{len(urls)} pages OK')

    # — Summary —
    print()
    if not failed:
        print('=== ALL TESTS PASSED ===')
    else:
        print('=== FAILED: ' + str(failed) + ' ===')
