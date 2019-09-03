from rest_framework.response import Response
from rest_framework import status
from django.utils import six
import time

# Api Version Control List
from .config import __API_VERSION__


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

    def __init__(self, request, data=None, headers=None, content_type=None, debug=False, api_version=None):

        self._request = request
        self.data = data
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
                            'message': '%s data successfully' % (self._request.method),
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
                        'payload': {'msg': 'BAD REQUEST: %s data failure' % (self._request.method)},
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
