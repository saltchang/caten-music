import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread

ACTIVATION_EMAIL_TEMPLATE = """\
<html><body>
<h2>帳號註冊認證信</h2>
<p>{username}，歡迎你，請點擊下面連結來啟用您的帳號</p>
<p><a href="{activation_url}">點此啟用您的帳號</a></p>
</body></html>
"""

PASSWORD_RESET_EMAIL_TEMPLATE = """\
<html><body>
<h2>密碼重設認證</h2>
<p>{username}，您好，請點擊下面連結以重設您的密碼</p>
<p><a href="{reset_url}">點此重設</a></p>
</body></html>
"""


class SmtpMailService:
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        smtp_use_ssl: bool = True,
    ):
        self._host = smtp_host
        self._port = smtp_port
        self._username = smtp_username
        self._password = smtp_password
        self._use_ssl = smtp_use_ssl

    def _send_in_thread(self, message: MIMEMultipart, recipients: list[str]) -> None:
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self._host, self._port, context=context) as server:
                server.login(self._username, self._password)
                server.send_message(message, to_addrs=recipients)
        except Exception as e:
            print(f'Failed to send email: {e}')

    def _build_message(self, recipients: list[str], subject: str, html_content: str) -> MIMEMultipart:
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = self._username
        message['To'] = ', '.join(recipients)
        message.attach(MIMEText(html_content, 'html'))
        return message

    def send_activation_email(self, email: str, username: str, activation_url: str) -> None:
        html = ACTIVATION_EMAIL_TEMPLATE.format(username=username, activation_url=activation_url)
        message = self._build_message([email], 'Caten music 帳號註冊認證信', html)
        Thread(target=self._send_in_thread, args=[message, [email]]).start()

    def send_password_reset_email(self, email: str, username: str, reset_url: str) -> None:
        html = PASSWORD_RESET_EMAIL_TEMPLATE.format(username=username, reset_url=reset_url)
        message = self._build_message([email], 'Caten music 密碼重設認證', html)
        Thread(target=self._send_in_thread, args=[message, [email]]).start()
