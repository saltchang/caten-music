# helper/invitation.py

import random
import string
from datetime import datetime, timedelta

from caten_music.models import InvitationCode


def generate_invitation_code(length=12):
    """Generate a random invitation code of specified length"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def create_invitation_code(admin_id, expiration_hours=48):
    """Create a new invitation code with expiration time"""
    code = generate_invitation_code()
    expires_at = datetime.now() + timedelta(hours=expiration_hours)

    invitation = InvitationCode()
    invitation.code = code
    invitation.expires_at = expires_at
    invitation.created_by = admin_id
    invitation.is_disabled = False
    invitation.usage_count = 0
    invitation.save()

    return invitation


def validate_invitation_code(code):
    """Validate if an invitation code is valid"""
    invitation = InvitationCode.query.filter_by(code=code).first()
    if not invitation:
        return False, '無效的邀請碼'

    if invitation.is_disabled:
        return False, '邀請碼已被停用'

    if datetime.now() > invitation.expires_at:
        return False, '邀請碼已過期'

    return True, invitation


def toggle_invitation_code(code_id, is_disabled):
    """Enable or disable an invitation code"""
    invitation = InvitationCode.query.get(code_id)
    if not invitation:
        return False, '邀請碼不存在'

    if is_disabled:
        invitation.disable()
    else:
        invitation.enable()

    return True, invitation
