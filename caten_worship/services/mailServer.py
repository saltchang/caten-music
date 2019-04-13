# services/mail.py

# https://hackmd.io/c/HJiZtEngG/https%3A%2F%2Fhackmd.io%2Fs%2FBkYRYDmBf

from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from caten_worship import models

mail = models.mail

def send_mail(sender, recipients, subject, template, **kwargs):
    """
    sender: 寄件者\n
    recipients: 收件者, list \n
    subject: 主旨\n
    template: 模板名稱\n
    **kwargs: 要傳入template的參數\n
    """

    app = current_app._get_current_object()
    mailcontent = Message(subject,
                          sender=sender,
                          recipients=recipients)
    mailcontent.html = render_template(template, **kwargs)

    # 多線程
    thread = Thread(target=send_mail_thread, args=[app, mailcontent])
    thread.start()

    return thread

def send_mail_thread(app, mailcontent):
    """
    使用多執行緒來寄送郵件
    """
    with app.app_context():
        mail.send(mailcontent)
