# routes/invitation.py

from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from caten_music import helper, models

InvitationCode = models.InvitationCode

invitation_admin_bp = Blueprint('invitation_admin_bp', __name__, template_folder='templates')
invitation_api_bp = Blueprint('invitation_api_bp', __name__, template_folder='templates')


@invitation_admin_bp.route('/admin/invitation', methods=['GET'])
@login_required
def invitation_admin():
    if current_user.is_authenticated:
        current_user.login_update()

    if not current_user.is_admin:
        flash('很抱歉，您並沒有管理邀請碼的權限。', 'danger')
        return redirect('/')

    invitation_codes = InvitationCode.query.order_by(InvitationCode.created_at.desc()).all()

    admins = models.UserModel.query.filter_by(is_admin=True).all()
    admin_dict = {admin.id: admin.displayname for admin in admins}

    now = datetime.now()

    return render_template(
        'admin/invitation.html',
        invitation_codes=invitation_codes,
        admin_dict=admin_dict,
        now=now,
    )


@invitation_api_bp.route('/api/invitation/toggle-code/<int:code_id>', methods=['POST'])
@login_required
def toggle_invitation_code(code_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': '您沒有權限執行此操作'}), 403

    data = request.get_json()
    is_disabled = data.get('is_disabled', False)

    success, result = helper.toggle_invitation_code(code_id, is_disabled)

    if success:
        return jsonify({'success': True, 'message': '邀請碼已' + ('停用' if is_disabled else '啟用')})
    else:
        return jsonify({'success': False, 'message': result})


@invitation_api_bp.route('/api/invitation/generate', methods=['POST'])
@login_required
def generate_invitation():
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': '您沒有權限執行此操作'}), 403

    invitation = helper.create_invitation_code(current_user.id)

    invitation_link = url_for('register_bp.register', invitation_code=invitation.code, _external=True)

    return jsonify(
        {
            'success': True,
            'code': invitation.code,
            'expires_at': invitation.expires_at.strftime('%Y-%m-%d %H:%M:%S'),
            'link': invitation_link,
        }
    )


@invitation_api_bp.route('/api/invitation/validate/<code>', methods=['GET'])
def validate_invitation(code):
    is_valid, result = helper.validate_invitation_code(code)

    if is_valid and isinstance(result, InvitationCode):
        return jsonify(
            {'success': True, 'message': '有效的邀請碼', 'expires_at': result.expires_at.strftime('%Y-%m-%d %H:%M:%S')}
        )
    else:
        return jsonify({'success': False, 'message': result})
