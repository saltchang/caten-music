# services/mail_server.py

# https://hackmd.io/c/HJiZtEngG/https%3A%2F%2Fhackmd.io%2Fs%2FBkYRYDmBf

import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread

from flask import render_template


def send_mail(sender, recipients, subject, template, **kwargs):
    """
    sender: 寄件者\n
    recipients: 收件者, list \n
    subject: 主旨\n
    template: 模板名稱\n
    **kwargs: 要傳入template的參數\n
    """

    html_content = render_template(template, **kwargs)

    # Create email message
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = os.environ.get('SMTP_USERNAME', '')
    message['To'] = ', '.join(recipients) if isinstance(recipients, list) else recipients

    # Add HTML content
    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)

    # SMTP configuration
    smtp_config = {
        'host': os.environ.get('SMTP_HOST', 'smtp.mailgun.org'),
        'port': os.environ.get('SMTP_PORT', 465),
        'username': os.environ.get('SMTP_USERNAME', ''),
        'password': os.environ.get('SMTP_PASSWORD', ''),
        'use_ssl': os.environ.get('SMTP_USE_SSL', True),
    }

    # multi-thread
    thread = Thread(target=send_mail_thread, args=[smtp_config, message, recipients])
    thread.start()

    return thread


def send_mail_thread(smtp_config, message, recipients):
    """
    使用多執行緒來寄送郵件
    """
    try:
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_config['host'], smtp_config['port'], context=context) as server:
            server.login(smtp_config['username'], smtp_config['password'])

            server.send_message(message, to_addrs=recipients)

        print(f'Email sent successfully to {recipients}')

    except Exception as e:
        print(f'Failed to send email: {str(e)}')
