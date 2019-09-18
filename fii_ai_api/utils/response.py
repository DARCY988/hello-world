from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import six
import pandas as pd
import time

# Api Version Control List
from fii_ai_api.config import __API_VERSION__


def fii_api_handler(http_method_names=None):
    """
    Decorator that converts a function-based view into a ``FiiResponse`` Standard Formate.

    Parameters
    --------------
    http_method_names: list
        Takes a list of allowed methods for the view as an argument.
        Example. Enable your view with request.methods: [GET, POST, PUT]
        ```
            @fii_response_handler(['get', 'post', 'put'])
            def AI_algorithm(...):
                # Do your algorithm...
                return results
        ```

    NOTE: Please check your data type of ``results`` are acceptable.
        - list
        - dict
        - pandas.DataFrame
    """

    def decorator(func):
        WrappedResponse = type(
            six.PY3 and 'WrappedResponse' or b'WrappedResponse', (FiiResponse,), {'__doc__': func.__doc__}
        )
        WrappedResponse.__name__ = func.__name__

        @api_view(http_method_names)
        def handler(*args, **kwargs):
            data = func(*args, **kwargs)
            return WrappedResponse(*args, **kwargs, data=data)

        return handler

    return decorator


class FiiResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    This is a Response Template Format (RTF) for ``Fii IAI Team``,
    to easily document the api usage and comunicate with front-end Teams.

    There are three status of the Templates:
    1. [HTTP_200_OK] Formated Data
    2. [HTTP_400_BAD_REQUEST] NULL Data Error
    3. [HTTP_505_HTTP_VERSION_NOT_SUPPORTED] API Version Error
    """

    def __init__(
        self, request, data=None, headers=None, content_type=None, debug=False, api_version=None, *args, **kwargs
    ):

        # check results data type, and convert as JSONable(value, dict, list(dict, list)) types.
        if isinstance(data, pd.DataFrame):
            self.data = data.to_dict('record')
        elif isinstance(data, (dict, list)):
            self.data = data
        elif data:
            self.data = data
        else:
            self.data = None

        self.content_type = content_type
        self.api_version = api_version if api_version else 'latest'
        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value

        if self.api_version in __API_VERSION__:
            start_time = time.time()
            if self.data is not None:
                cost_time = time.time() - start_time
                super().__init__(
                    {
                        'api-mode': '[%s] %s' % (self.api_version, 'Debug Mode' if debug else 'Production Mode'),
                        'status': status.HTTP_200_OK,
                        'payload': {
                            'message': '%s data successfully' % (request.method),
                            'time': 'Request time %.4fs.' % (cost_time),
                            'data': self.data,
                        },
                    }
                )
            else:
                super().__init__(
                    {
                        'api-mode': '[%s] %s' % (self.api_version, 'Debug Mode' if debug else 'Production Mode'),
                        'status': status.HTTP_400_BAD_REQUEST,
                        'payload': {'msg': 'BAD REQUEST: %s data failure' % (request.method)},
                    }
                )

        # Wrong API version
        else:
            super().__init__(
                {
                    'api-mode': '[%s] %s' % (self.api_version, 'Debug Mode' if debug else 'Production Mode'),
                    'status': status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
                    'payload': {
                        'msg': 'VDX API Version(%s) will be available soon! Please be patient :)!' % (self.api_version)
                    },
                }
            )
