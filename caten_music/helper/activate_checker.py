# helper/activate_checker.py

from flask import current_app
from itsdangerous import URLSafeTimedSerializer as sign
from itsdangerous import SignatureExpired, BadSignature


def checkActivateToken(token: str, hours=2) -> bool:
    time = hours * 3600

    tokenGenerator = sign(current_app.config['SECRET_KEY'])

    try:
        check_result = tokenGenerator.loads(token, max_age=time)  # 驗證

    except SignatureExpired:
        #  當時間超過的時候就會引發SignatureExpired錯誤
        return False

    except BadSignature:
        #  當驗證錯誤的時候就會引發BadSignature錯誤
        return False

    return check_result
