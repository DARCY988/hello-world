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
        host = '10.134.34.241'
        port = 587
        ehlo = 'ismetoad'  # This is how we get authentication

        message = MIMEText(message, 'plain', 'utf-8')
        message['Subject'] = subject
        message['From'] = from_mail
        message['To'] = ', '.join(recipient_list)

        try:
            smtp = smtplib.SMTP(host, port)
            # Authenticate
            smtp.ehlo(ehlo)
            smtp.starttls()
            smtp.helo(ehlo)
            # Set the debug output level
            smtp.set_debuglevel(0)
            # Send mail
            smtp.sendmail(from_mail, recipient_list, message.as_string())
            # Close connection
            smtp.quit()
            result = 'Alarm has been sent.'
        except smtplib.SMTPException as e:
            print(e)
            result = 'Fail to send mail.'

        return result
