# services/mail.py

# https://hackmd.io/c/HJiZtEngG/https%3A%2F%2Fhackmd.io%2Fs%2FBkYRYDmBf

from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from caten_worship import models

mail = models.mail

def send_mail(sender, recipients, subject, template, **kwargs):
    # sender: 寄件者
    # recipients: 收件者, list
    # subject: 主旨
    # template: 模板名稱
    # **kwargs: 要傳入template的參數

    app = current_app._get_current_object()
    mailcontent.html = render_template(template, **kwargs)

    # 多線程
    thread = Thread(target=send_async_email, args=[app, mailcontent])
    thread.start()

    return thread
