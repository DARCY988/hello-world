"""
Mail service class.
"""
from django.core.mail import get_connection, EmailMultiAlternatives
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

    def send_mail(self, subject, message, from_email, recipient_list, cc, attachments=None,
                  fail_silently=False, connection=None, html_message=None):
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
