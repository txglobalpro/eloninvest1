import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from core.extensions import db
from core.models import Investment, Transaction, Referral

user_bp = Blueprint('user', __name__, template_folder='../../templates/user')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/dashboard')
@login_required
def dashboard():
    investments = Investment.query.filter_by(user_id=current_user.id, status='active').order_by(Investment.start_date.desc()).all()
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).limit(10).all()
    pending_withdrawals = Transaction.query.filter_by(user_id=current_user.id, type='withdraw', status='pending').count()
    pending_deposits = Transaction.query.filter_by(user_id=current_user.id, type='deposit', status='pending').count()
    total_invested = current_user.total_invested or 0
    return render_template('user/dashboard.html', investments=investments, transactions=transactions, pending_withdrawals=pending_withdrawals, pending_deposits=pending_deposits, total_invested=total_invested, now=datetime.utcnow())

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.payment_method = request.form.get('payment_method', current_user.payment_method)
        current_user.lang = request.form.get('lang', current_user.lang)
        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('user.profile'))
    months_en = ['January','February','March','April','May','June','July','August','September','October','November','December']
    months_ar = ['يناير','فبراير','مارس','إبريل','مايو','يونيو','يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر']
    referrals_count = Referral.query.filter_by(referrer_id=current_user.id).count()
    investments_count = Investment.query.filter_by(user_id=current_user.id).count()
    transactions_count = Transaction.query.filter_by(user_id=current_user.id).count()
    return render_template('user/profile.html', referrals_count=referrals_count, investments_count=investments_count, transactions_count=transactions_count, months_en=months_en, months_ar=months_ar)

@user_bp.route('/profile/kyc', methods=['POST'])
@login_required
def submit_kyc():
    if current_user.kyc_status == 'pending':
        flash('KYC already under review' if current_user.lang == 'en' else 'التحقق قيد المراجعة بالفعل', 'warning')
        return redirect(url_for('user.profile'))
    if current_user.kyc_status == 'approved':
        flash('KYC already verified' if current_user.lang == 'en' else 'التحقق موثق بالفعل', 'info')
        return redirect(url_for('user.profile'))
    country = request.form.get('kyc_country', '').strip()
    gender = request.form.get('kyc_gender', '').strip()
    doc_type = request.form.get('kyc_doc_type', '').strip()
    dob_day = request.form.get('kyc_dob_day', '').strip()
    dob_month = request.form.get('kyc_dob_month', '').strip()
    dob_year = request.form.get('kyc_dob_year', '').strip()
    phone = request.form.get('kyc_phone', '').strip()
    if not country or not gender or not doc_type or not dob_day or not dob_month or not dob_year or not phone:
        flash('Please fill in all fields' if current_user.lang == 'en' else 'يرجى تعبئة جميع الحقول', 'danger')
        return redirect(url_for('user.profile'))
    if doc_type not in ('drivers_license', 'national_id', 'passport'):
        flash('Invalid document type' if current_user.lang == 'en' else 'نوع وثيقة غير صالح', 'danger')
        return redirect(url_for('user.profile'))
    try:
        dob_str = f'{dob_year}-{int(dob_month):02d}-{int(dob_day):02d}'
        dob_date = datetime.strptime(dob_str, '%Y-%m-%d')
        if dob_date > datetime.utcnow():
            flash('Date of birth cannot be in the future' if current_user.lang == 'en' else 'تاريخ الميلاد لا يمكن أن يكون في المستقبل', 'danger')
            return redirect(url_for('user.profile'))
        age = datetime.utcnow().year - dob_date.year - ((datetime.utcnow().month, datetime.utcnow().day) < (dob_date.month, dob_date.day))
        if age < 18:
            flash('You must be at least 18 years old' if current_user.lang == 'en' else 'يجب أن يكون عمرك 18 عاماً على الأقل', 'danger')
            return redirect(url_for('user.profile'))
    except ValueError:
        flash('Invalid date' if current_user.lang == 'en' else 'تاريخ غير صالح', 'danger')
        return redirect(url_for('user.profile'))
    if 'kyc_id_front' not in request.files:
        flash('Please upload the front image of your ID' if current_user.lang == 'en' else 'يرجى رفع الصورة الأمامية للوثيقة', 'danger')
        return redirect(url_for('user.profile'))
    front = request.files['kyc_id_front']
    if not front or not front.filename or not allowed_file(front.filename):
        flash('Invalid front file type. Allowed: PNG, JPG, JPEG, GIF, WebP' if current_user.lang == 'en' else 'نوع ملف الصورة الأمامية غير صالح. المسموح: PNG, JPG, JPEG, GIF, WebP', 'danger')
        return redirect(url_for('user.profile'))
    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'kyc')
    os.makedirs(upload_dir, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    ext_f = front.filename.rsplit('.', 1)[1].lower()
    front_name = f'kyc_{current_user.id}_{ts}_front.{ext_f}'
    front.save(os.path.join(upload_dir, front_name))

    back_name = ''
    if doc_type in ('drivers_license', 'national_id'):
        if 'kyc_id_back' not in request.files:
            flash('Please upload the back image of your ID' if current_user.lang == 'en' else 'يرجى رفع الصورة الخلفية للوثيقة', 'danger')
            return redirect(url_for('user.profile'))
        back = request.files['kyc_id_back']
        if not back or not back.filename or not allowed_file(back.filename):
            flash('Invalid back file type. Allowed: PNG, JPG, JPEG, GIF, WebP' if current_user.lang == 'en' else 'نوع ملف الصورة الخلفية غير صالح. المسموح: PNG, JPG, JPEG, GIF, WebP', 'danger')
            return redirect(url_for('user.profile'))
        ext_b = back.filename.rsplit('.', 1)[1].lower()
        back_name = f'kyc_{current_user.id}_{ts}_back.{ext_b}'
        back.save(os.path.join(upload_dir, back_name))

    current_user.kyc_status = 'pending'
    current_user.kyc_country = country
    current_user.kyc_gender = gender
    current_user.kyc_doc_type = doc_type
    current_user.kyc_dob = dob_str
    current_user.kyc_age = age
    current_user.kyc_phone = phone
    current_user.kyc_id_path = f'static/uploads/kyc/{front_name}'
    current_user.kyc_id_back_path = f'static/uploads/kyc/{back_name}' if back_name else ''
    current_user.kyc_submitted_at = datetime.utcnow()
    current_user.kyc_review_notes = ''
    db.session.commit()
    flash('KYC submitted successfully! Awaiting review.' if current_user.lang == 'en' else 'تم تقديم طلب التحقق بنجاح! في انتظار المراجعة.', 'success')
    return redirect(url_for('user.profile'))
