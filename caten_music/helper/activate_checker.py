# helper/activate_checker.py

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as sign
from itsdangerous import SignatureExpired, BadSignature


def checkActivateToken(token):

    tokenGenerator = sign(current_app.config['SECRET_KEY'])

    try:
        check_result = tokenGenerator.loads(token)  # 驗證

    except SignatureExpired:
        #  當時間超過的時候就會引發SignatureExpired錯誤
        return False

    except BadSignature:
        #  當驗證錯誤的時候就會引發BadSignature錯誤
        return False

    return check_result
