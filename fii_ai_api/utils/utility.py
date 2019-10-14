import os
import time
import pytz
import inspect
from datetime import datetime
import platform
import logging.handlers
from functools import wraps

from django.utils.deprecation import MiddlewareMixin


if platform.system() == 'Linux':
    LOG = logging.getLogger(__name__)
    LOG.setLevel(logging.DEBUG)
    rotating_file_handler = logging.handlers.RotatingFileHandler(
        filename=r'./.uwsgi/logs/fii_api_server.log', mode='a', maxBytes=1024 * 1024, backupCount=20
    )
    formatter = logging.Formatter(fmt='%(asctime)s: %(message)s', datefmt='%a %d %b %Y %H:%M:%S')
    rotating_file_handler.setFormatter(formatter)
    LOG.addHandler(rotating_file_handler)


def log(msg):
    """
    For user to print msg or save in PROD server. DEBUG use only.
    :param msg:
    :return:
    """
    user_platform = platform.system()
    if user_platform == 'Linux':
        print(msg)
        return LOG.info(msg)
    else:
        return print(msg)


def fii_cronlog_handler(func):
    """
    For ``Fii IAI Team`` easily implement into your own cron jobs,
    we create a Decorator to record the execution status and feedback,
    and save as a summary log (usually save at '/opt/logs/fii_iai.log')

    Example.
    ```
        from fii_ai_api.utils.utility import fii_cronlog_handler
        @fii_cron_handler
        def my_cron_job_demo():
            # Do your magic...
            return 'Hello Fii IAI cron job.'
    ```
    NOTE: This handler is only show your function's execution status
          and feedback (ex. '|YYYY-MM-DD hh:mm:ss|[CRON Sucess]
          `my_cron_job_demo` (0.001s)').
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        app_name = os.path.split(os.path.dirname(inspect.getfile(func)))[-1]
        try:
            results = func(*args, **kwargs)
            cost_time = time.time() - start_time
            if results is not None:
                log(
                    datetime.now().strftime("|%Y/%m/%d %H:%M:%S|")
                    + '<%s>[CRON Sucess]`%s` (%.3fs)' % (app_name, func.__name__, cost_time)
                )
                return results
            else:
                log(datetime.now().strftime("|%Y/%m/%d %H:%M:%S|") + '<%s>[CRON Fail]`%s`' % (app_name, func.__name__))

        except Exception as err:
            log(
                datetime.now().strftime("|%Y/%m/%d %H:%M:%S|")
                + '<%s>[CRON Error]`%s`: %s' % (app_name, func.__name__, err)
            )
        return results

    return wrapper


def timeit(func):
    """ Decorator to calc the time cost
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()
        log('[{}] costs [{}]secs'.format(func.__name__, end_time - start_time))
        return result

    return wrapper


class TimeitMiddleware(MiddlewareMixin):
    """
    Caculate the usage time for the API requests.
    NOTE: Need to inheritance class `MiddlewareMixin`,
        add it in settings.MIDDLEWARE
    """

    start_time = None

    def process_request(self, request):
        # request 开始处理的时间
        self.start_time = time.time()

    def process_response(self, request, response):
        method = request.method
        path = request.path

        # get requests parameters
        parameters = request.environ['QUERY_STRING']
        if parameters:
            parameters = '?' + parameters
        end_time = time.time()
        cost_time = end_time - self.start_time
        if cost_time > 5:
            log('[{} {}] costs [{}]secs...'.format(method.upper(), path + parameters, cost_time))

        return response
