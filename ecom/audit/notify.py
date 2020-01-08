from email.mime.text import MIMEText
from fii_ai_api.utils.mail import MailService
from ecom.config import MAIL_connect_info
import smtplib


class MailCenter(MailService):
    def __init__(self, debug=False, custom_login_info={}, **kwargs):
        super().__init__(debug=debug, login_info=MAIL_connect_info, **kwargs)

    def send_alarm(self, subject, message, from_email='', recipient_list=[], cc=None, **kwargs):
        result = self.send_mail(subject=subject, message=message, from_email=from_email,
                                recipient_list=recipient_list, cc=cc, **kwargs)

        return result

    def send_fii_alarm(self, subject, message, from_mail='', recipient_list=[]):
        result = self.send_fii_mail(subject=subject, message=message, from_mail=from_mail,
                                    recipient_list=recipient_list)

        return result
