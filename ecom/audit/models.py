from pandas import DataFrame
from datetime import datetime, timezone, timedelta
from fii_ai_api.settings import STATIC_ROOT
from ecom.config import __CATEGORIES__, __LOCATIONS__
from .fileio import FileFormIO
from .notify import MailCenter
import os


# Build path in this module like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.join(os.path.join(STATIC_ROOT, 'ecom'), 'audit')


def info_upload(request, dbio):
    f_type = request.POST.get('file_type')
    uploader = request.POST.get('user')
    type_dict = {
        'ISO9001 Certificate': 1,
        'Business License': 2,
        'ODM/OEM Agreement': 3,
        'Factory Introduction': 4,
        'Company Org': 5,
        'CNAS Certificate': 6,
    }

    if f_type in type_dict.keys():  # Check whether file_type is in formatted list.
        upload_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        mod_path = os.path.join(BASE_DIR, 'info')
        site = request.POST.get('site')

        # Handle files
        fileio = FileFormIO(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')  # getlist() attribute name must be tha same as the front-form
        if fileio.is_valid():
            finish = []
            for f in files:
                # Save file
                path = os.path.join(mod_path, site)
                fileio.save(f, path)
                # Insert into db
                dbio.create_file('FAInfo_upload', 'site', site, f.name, path, uploader, upload_time, type_dict[f_type])

                finish.append(f.name)

        result = {
            'message': 'File "%s" uploaded successfully.' % ', '.join(finish)
        }

    else:
        result = {
            'message': 'Type not existed.'
        }

    return result


def report_upload(request, dbio):
    f_type = request.POST.get('file_type')
    uploader = request.POST.get('user')
    type_dict = {
        'Audit Report/Self-inspection Report': 1,
        'CAR': 2,
    }

    if f_type in type_dict.keys():  # Check whether file_type is in formatted list.
        # Keys to get seq
        site = request.POST.get('site')
        category = request.POST.get('category')

        upload_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        mod_path = os.path.join(BASE_DIR, 'report')
        report_seq = dbio.get_seq('FAReport', site=site, category=category)

        # Handle files
        fileio = FileFormIO(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')  # getlist() attribute name must be tha same as the front-form
        if fileio.is_valid():
            finish = []
            for f in files:
                # Save file
                path = os.path.join(mod_path, report_seq)
                fileio.save(f, path)
                # Insert into db
                dbio.create_file('FAReport_upload', 'FAReport_seq', report_seq,
                                 f.name, path, uploader, upload_time, type_dict[f_type])

                finish.append(f.name)

        result = {
            'message': 'File "%s" uploaded successfully.' % ', '.join(finish)
        }

    else:
        result = {
            'message': 'Type not existed.'
        }

    return result


def check_upload(request, dbio):
    f_type = request.POST.get('file_type')
    uploader = request.POST.get('user')
    type_dict = {
        'Validation Report': 1,
        'PMP': 2,
        'SOP': 3,
        'SIP': 4,
        'CCL Certificate': 5,
        'In-coming Inspection Report': 6,
        'Internal Audit Report': 7,
        'Other': 8,
    }

    if f_type in type_dict.keys():  # Check whether file_type is in formatted list.
        # Keys to get seq
        site = request.POST.get('site')
        category = request.POST.get('category')
        sample_category = request.POST.get('sample_category')
        sample_pid = request.POST.get('sample_pid')

        upload_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        mod_path = os.path.join(BASE_DIR, 'check')
        check_seq = dbio.get_seq('FACheck', site=site, category=category,
                                 sample_category=sample_category, sample_pid=sample_pid)

        # Handle files
        fileio = FileFormIO(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')  # getlist() attribute name must be tha same as the front-form
        if fileio.is_valid():
            finish = []
            for f in files:
                # Save file
                path = os.path.join(mod_path, check_seq)
                fileio.save(f, path)
                # Insert into db
                dbio.create_file('FACheck_upload', 'FACheck_seq', check_seq,
                                 f.name, path, uploader, upload_time, type_dict[f_type])

                finish.append(f.name)

        result = {
            'message': 'File "%s" uploaded successfully.' % ', '.join(finish)
        }

    else:
        result = {
            'message': 'Type not existed.'
        }

    return result
