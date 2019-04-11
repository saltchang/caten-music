# https://hackmd.io/c/HJiZtEngG/https%3A%2F%2Fhackmd.io%2Fs%2FBkYRYDmBf

from caten_worship import mail
from flask_mail import Message
from flask import render_template, current_app
from threading import Thread


def send_mail(sender, recipients, subject, template, **kwargs):
    """
    sender:的部份可以考慮透過設置default
    recipients:記得要list格式
    subject:是郵件主旨
    template:樣板名稱
    **kwargs:參數
    """
    app = current_app._get_current_object()
    msg = Message(subject,
                  sender=sender,
                  recipients=recipients)
    msg.html = render_template(template, **kwargs)

    #  使用多線程
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_async_email(app, msg):
    """
    利用多執行緒來處理郵件寄送，因為使用另一執行緒來寄信，
    所以需要利用app_context來處理。
    :param app: 實作Flask的app
    :param msg: 實作Message的msg
    :return:
    """
    with app.app_context():
        mail.send(msg)
