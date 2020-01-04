from fii_ai_api.utils.response import fii_api_handler
from .dbio import ECNMySQLIO
from .models import (
    info_upload, report_upload, check_upload
)
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os


# -------------------- #
# AI Model Results API
# -------------------- #


# -------------------- #
# DataBase CRUD API
# -------------------- #
@fii_api_handler(['post'])
def api_file_io(request, debug, api_version, module):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    if request.method == 'POST':
        modules = {
            'info': info_upload(request, db, request.POST.get('user')),
            'report': report_upload(request, db, request.POST.get('user')),
            'check': check_upload(request, db, request.POST.get('user')),
        }
        if module in modules.keys():
            result = modules[module]

    return result
