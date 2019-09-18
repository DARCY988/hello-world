import time
import pytz
import datetime
import platform
import logging.handlers
from functools import wraps

from django.utils.deprecation import MiddlewareMixin


if platform.system() == 'Linux':
    LOG = logging.getLogger(__name__)
    LOG.setLevel(logging.DEBUG)
    rotating_file_handler = logging.handlers.RotatingFileHandler(
        filename=r'/opt/logs/fii_iai.log', mode='a', maxBytes=1024 * 1024, backupCount=20
    )
    formatter = logging.Formatter(fmt='%(asctime)s: %(message)s', datefmt='%a %d %b %Y %H:%M:%S')
    rotating_file_handler.setFormatter(formatter)
    LOG.addHandler(rotating_file_handler)


def log(msg):
    """ For user to print msg or save in PROD server. DEBUG use only.
    :return:
    """
    user_platform = platform.system()
    if user_platform == 'Windows':
        return print(msg)
    elif user_platform == 'Linux':
        print(msg)
        return LOG.info(msg)


def china_time():
    """ Return current China time.
    :return: datetime format
    """
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(tz)


def utc_time():
    """ Return current UTC time.
    :return: datetime format
    """
    return datetime.datetime.utcnow()


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
