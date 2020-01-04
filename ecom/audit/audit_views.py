from fii_ai_api.utils.response import fii_api_handler
from .dbio import ECNMySQLIO
from .models import (
    info_upload, report_upload, check_upload
)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta, timezone


# -------------------- #
# AI Model Results API
# -------------------- #
@fii_api_handler(['get'])
def info_view(request, debug, api_version):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    # List all report
    if request.method == 'GET':
        site = request.GET.get('site', None)
        result = db.read_info(site)

    return result


@fii_api_handler(['get', 'post'])
def report_view(request, debug, api_version):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    # List all report
    if request.method == 'GET':
        site = request.GET.get('site', None)
        category = request.GET.get('category', None)
        result = db.read_report(site, category)

    if request.method == 'POST':
        # Get data
        site = request.POST.get('site')
        category = request.POST.get('category')
        r_class = request.POST.get('class')
        audit_date = request.POST.get('audit_date')

        audit_result = request.POST.get('audit_result')
        result_dict = {
            'Pass A': 1,
            'Pass B': 2,
            'Pass C': 3,
            'Fail': 4,
        }
        if audit_result in result_dict.keys():
            audit_result = result_dict[audit_result]

        nextaudittime = datetime.strptime(audit_date, '%Y/%m/%d').date() + timedelta(days=365)  # 1 year for 'CCC'
        uploader = request.POST.get('uploader')
        create_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")

        # Insert into db
        db.create_report(site, category, r_class, audit_date, audit_result, nextaudittime, uploader, create_time)

        result = {
            'message': 'Create report successfully.'
        }

    return result


@fii_api_handler(['get', 'post'])
def check_view(request, debug, api_version):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    # List all report
    if request.method == 'GET':
        site = request.GET.get('site', None)
        category = request.GET.get('category', None)
        sample_category = request.GET.get('sample_category', None)
        sample_pid = request.GET.get('sample_pid', None)
        result = db.read_check(site, category, sample_category, sample_pid)

    if request.method == 'POST':
        # Get data
        site = request.POST.get('site')
        category = request.POST.get('category')
        audit_date = request.POST.get('audit_date')
        sample_category = request.POST.get('sample_category')
        sample_pid = request.POST.get('sample_pid')
        sample_applicant = request.POST.get('sample_applicant')

        sample_conform = request.POST.get('sample_conform')
        conform_status = {
            'OK': 1,
        }
        if sample_conform in conform_status.keys():
            sample_conform = conform_status[sample_conform]

        uploader = request.POST.get('uploader')
        create_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")

        # Insert into db
        db.create_check(site, category, audit_date, sample_category, sample_pid,
                        sample_applicant, sample_conform, uploader, create_time)

        result = {
            'message': 'Create check successfully.'
        }

    return result


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
