from fii_ai_api.utils.response import fii_api_handler
from .dbio import ECNMySQLIO
from .models import (
    upload_files, list_files, delete_files, count_by_category, count_by_site
)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta, timezone


# -------------------- #
# AI Model Results API
# -------------------- #
# ----- Module 1 ----- #
@api_view(['get'])
def category_cert_view(request, debug, api_version, site=None):

    db = ECNMySQLIO(debug=debug, api_version=api_version)
    # mail = MailCenter(debug=debug, api_version=api_version)

    result = count_by_category(db, site)

    return Response(result)
# ----- Module 2 ----- #
@api_view(['get'])
def site_cert_view(request, debug, api_version, category):

    db = ECNMySQLIO(debug=debug, api_version=api_version)
    # mail = MailCenter(debug=debug, api_version=api_version)

    result = count_by_site(db, category)

    return Response(result)
# ----- Module 3 ----- #
# ----- Module 4 ----- #
@api_view(['get', 'delete'])
def info_view(request, debug, api_version):  # Create method is include in upload method.

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    # List all report
    if request.method == 'GET':
        result = list_files(request, db, 'info')

    if request.method == 'DELETE':
        result = {}

    return Response(result)


@api_view(['get', 'post', 'put', 'delete'])
def report_view(request, debug, api_version):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    # List all report
    if request.method == 'GET':
        site = request.POST.get('site')
        category = request.POST.get('category')
        result = db.read_report(site=site, category=category)

    # Add new record
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

    # Edit report
    if request.method == 'PUT':
        # Keys
        site = request.POST.get('site')
        category = request.POST.get('category')

        # Edit items
        new_class = request.POST.get('new_class')
        new_date = request.POST.get('new_audit_date')

        new_result = request.POST.get('new_result')
        result_dict = {
            'Pass A': 1,
            'Pass B': 2,
            'Pass C': 3,
            'Fail': 4,
        }
        if new_result in result_dict.keys():
            new_result = result_dict[new_result]

        new_nexttime = datetime.strptime(new_date, '%Y/%m/%d').date() + timedelta(days=365)  # 1 year for 'CCC'
        uploader = request.POST.get('uploader')
        update_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")

        # Update db
        db.update_report(site, category, new_class, new_date, new_result, new_nexttime, uploader, update_time)

        result = {
            'message': 'Update report successfully.'
        }

    # # Delete report
    # if request.method == 'DELETE':
    #     site = request.POST.get('site')
    #     category = request.POST.get('category')

    #     db.delete_report(site, category)
    #     db.delete_file()

    return Response(result)


@api_view(['get', 'post', 'put', 'delete'])
def check_view(request, debug, api_version):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    conform_status = {
        'OK': 1,
    }

    # List all report
    if request.method == 'GET':
        site = request.POST.get('site')
        category = request.POST.get('category')
        sample_category = request.POST.get('sample_category')
        sample_pid = request.POST.get('sample_pid')
        result = db.read_check(site=site, category=category, sample_category=sample_category, sample_pid=sample_pid)

    # Add new record
    if request.method == 'POST':
        # Get data
        site = request.POST.get('site')
        category = request.POST.get('category')
        audit_date = request.POST.get('audit_date')
        sample_category = request.POST.get('sample_category')
        sample_pid = request.POST.get('sample_pid')
        sample_applicant = request.POST.get('sample_applicant')
        sample_conform = request.POST.get('sample_conform')

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

    # Edit check
    if request.method == 'PUT':
        # Keys
        site = request.POST.get('site')
        category = request.POST.get('category')
        sample_category = request.POST.get('sample_category')
        sample_pid = request.POST.get('sample_pid')

        # Edit items
        new_date = request.POST.get('new_audit_date')
        new_applicant = request.POST.get('new_applicant')
        new_conform = request.POST.get('new_conform')

        if new_conform in conform_status.keys():
            new_conform = conform_status[new_conform]

        uploader = request.POST.get('uploader')
        update_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")

        # Update db
        db.update_check(site, category, sample_category, sample_pid, new_date, new_applicant, new_conform,
                        uploader, update_time)

        result = {
            'message': 'Update check successfully.'
        }

    return Response(result)


# -------------------- #
# DataBase CRUD API
# -------------------- #
@api_view(['get', 'post', 'delete'])
def api_file_io(request, debug, api_version, module):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    mod_list = ['info', 'report', 'check']

    if module in mod_list:
        if request.method == 'GET':
            result = list_files(request, db, module)

        if request.method == 'POST':
            result = upload_files(request, db, module)

        if request.method == 'DELETE':
            name = request.POST.get('name')
            path = request.POST.get('path')

            result = delete_files(db, module, name, path)

    return result
