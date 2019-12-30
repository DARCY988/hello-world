from fii_ai_api.utils.mail import MailService
from ecom.config import MAIL_connect_info


class MailCenter(MailService):
    def __init__(self, debug=False, custom_login_info={}, **kwargs):
        super().__init__(debug=debug, login_info=MAIL_connect_info, **kwargs)

    def send_alarm(self, subject, message, from_email='', recipient_list=[], cc=None, **kwargs):
        result = self.send_mail(subject=subject, message=message, from_email=from_email,
                                recipient_list=recipient_list, cc=cc, **kwargs)

        return result
