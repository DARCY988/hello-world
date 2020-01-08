"""
Mail service class.
"""
from django.core.mail import get_connection, EmailMultiAlternatives, EmailMessage
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPException
import os
import inspect
import importlib


class BasicMail(object):
    def __init__(self, host='smtp.163.com', port=465, username='iai_reply@163.com', password='foxconn88',
                 from_email='IAI Alarm Center <iai_reply@163.com>', recipient_list=[], **kwargs):
        # Mail connection info
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.from_email = from_email
        self.recipient_list = recipient_list

        # Connect SMTP server
        self.connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            fail_silently=False,
            **kwargs
        )

    def send_fii_mail(self, subject, message, from_mail, recipient_list):
        ''' Send foxconn mail
        Parameters
        --------------
        subject: str
            Mail title. It is important for mail server to recognize whether this mail is spam or not.

        message: str
            Mail body message.

        from_mail: str
            The sender name and email shown to the recipients.
            Example:
            ```
            'Name <no-reply@example.com>'
            ```

        recipient_list: list
            A list of strings, each an email address. Each member of recipient_list
            will see the other recipients in the “To:” field of the email message.
            Example:
            ```
            ['123@example.com', '456@example.com', ...]
            ```
        Return
        --------------
        result: str
            Email sending result.
        '''
        # Mail connection info
        host = '10.134.34.241'
        port = 587
        ehlo = 'ismetoad'  # IMPORTANT: This is how we get authentication

        message = MIMEText(message, 'plain', 'utf-8')
        message['Subject'] = subject
        message['From'] = from_mail or self.from_email
        message['To'] = ', '.join(recipient_list or self.recipient_list)

        try:
            smtp = SMTP(host, port)
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
        except SMTPException as e:
            result = 'Fail to send mail. Error: %s' % (e)

        return result

    def send_mail(self, subject, message, from_email, recipient_list, cc=None, attachments=None,
                  fail_silently=False, connection=None, html_message=None):
        ''' Send mail
        Parameters
        --------------
        subject: str
            Mail title. It is important for mail server to recognize whether this mail is spam or not.

        message: str
            Mail body message.

        from_mail: str
            The sender name and email shown to the recipients.
            Example:
            ```
            'Name <no-reply@example.com>'
            ```

        recipient_list: list
            A list of strings, each an email address. Each member of recipient_list
            will see the other recipients in the “To:” field of the email message.
            Example:
            ```
            ['123@example.com', '456@example.com', ...]
            ```

        cc: list
            CC list.
            Example:
            ```
            ['admin_1@example.com', 'admin_2@example.com', ...]
            ```

        attachments: str
            The file path you want to attach. Attach single file for each time.
            Example:
            ```
            '.../documents/filename'
            ```

        fail_silently: Boolean
            When it’s False, send_mail() will raise an smtplib.SMTPException
            if an error occurs. See the smtplib docs for a list of possible
            exceptions, all of which are subclasses of SMTPException.

        connection: EmailBackend
            The optional email backend to use to send the mail. If unspecified, an
            instance of the default backend will be used. See the documentation on
            Email backends for more details.

        html_message: str
            If html_message is provided, the resulting email will be a multipart/alternative
            email with message as the text/plain content type and html_message as the
            text/html content type.

        Return
        --------------
        mail.send(): int
            The number of email messages sent.
        '''
        connection = connection or self.connection
        from_email = from_email or self.from_email
        recipient_list = recipient_list or self.recipient_list
        mail = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
            cc=cc,
            attachments=attachments,
            connection=connection)
        if html_message:
            mail.attach_alternative(html_message, 'text/html')

        return mail.send()

    def send_mass_mail(self, datatuple, fail_silently=False, connection=None):
        ''' Send multiple mails
        Parameters
        --------------
        datatuple: tuple
            Given a datatuple of (subject, message, from_email, recipient_list), send
            each message to each recipient list. Return the number of emails sent.
            If from_email is None, use the DEFAULT_FROM_EMAIL setting.

        fail_silently: Boolean
            When it’s False, send_mail() will raise an smtplib.SMTPException
            if an error occurs. See the smtplib docs for a list of possible
            exceptions, all of which are subclasses of SMTPException.

        connection: EmailBackend
            The optional email backend to use to send the mail. If unspecified, an
            instance of the default backend will be used. See the documentation on
            Email backends for more details.

        Return
        --------------
        connection.send_messages(messages): int
            The number of email messages sent.
        '''
        connection = connection or self.connection
        messages = [
            EmailMessage(subject, message, sender, recipient, connection=connection)
            for subject, message, sender, recipient in datatuple
        ]
        return connection.send_messages(messages)


class MailService(BasicMail):
    def __init__(self, debug=False, login_info={}, **kwargs):
        self._debug = True if debug == 'test/' else False
        self.app_path = self._get_caller_app_path

        if login_info:
            self.app_config = login_info
        else:
            self.app_config = self._default_config

        if self._debug is True:
            if 'test_setting' not in self.app_config:
                raise KeyError(
                    "Your dictionary lacks key '%s'. Please provide to determine"
                    "which mail server to send from." % 'test_setting'
                )
            else:
                self.mail_settings = self.app_config['test_setting']
        else:
            if 'prod_setting' not in self.app_config:
                raise KeyError(
                    "Your dictionary lacks key '%s'. Please provide to determine"
                    "which mail server to send from." % 'prod_setting'
                )
            else:
                self.mail_settings = self.app_config['prod_setting']

        super().__init__(**self.mail_settings, **kwargs)

    @property
    def get_mail_setting(self):
        '''Get mail settings'''
        return self.mail_settings

    @property
    def _if_debug(self):
        '''Check if the api mode is in debug mode'''
        return self._debug

    @property
    def get_app_name(self):
        '''Get which app is calling this function'''
        app = os.path.split(self.app_path)[-1]

        if 'urls.py' in os.listdir(self.app_path):
            url_file = importlib.import_module('{}.urls'.format(app))
            app_name = app
            if not hasattr(url_file, 'app_name'):
                raise AttributeError(" File '{}' has no attribute '{}'".format(url_file, 'app_name'))
            else:
                app_name = getattr(url_file, 'app_name')
        return app_name

    @property
    def _get_caller_app_path(self):
        stack = inspect.stack()

        # Get caller function object from `stack`
        for frame in stack:
            # Get module name
            module = inspect.getmodule(frame[0])
            module_name = module.__name__
            if module_name.endswith(('models', 'views')):
                break

        return os.path.dirname(module.__file__)

    @property
    def _default_config(self):
        app = os.path.split(self.app_path)[-1]

        if 'config.py' in os.listdir(self.app_path):
            config_file = importlib.import_module('{}.config'.format(app))

            if not hasattr(config_file, 'MAIL_connect_info'):
                raise AttributeError(" File '{}' has no attribute '{}'".format(config_file, 'MAIL_connect_info'))
            else:
                return getattr(config_file, 'MAIL_connect_info')
