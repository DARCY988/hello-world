from pandas import DataFrame
from datetime import datetime, timezone, timedelta
from rest_framework.response import Response
from fii_ai_api.settings import STATIC_ROOT
from ecom.config import __CATEGORIES__, __LOCATIONS__
from .fileio import FileFormIO
from .notify import MailCenter
import os


# Build path in this module like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.join(os.path.join(STATIC_ROOT, 'ecom'), 'audit')


# ---- Module 1/3 ---- #
def count_by_category(dbio, site):
    categories = __CATEGORIES__.copy()
    data = dbio.report_amount('category', 'site' if site else None, site)

    # alarm = MailCenter()

    result = {}
    for row in range(0, len(data.index)):
        category = data.iloc[row]['category']
        amount = data.iloc[row]['amount']
        # Pass A: 1, Pass B: 2, Pass C: 3, Fail: 4
        status = data.iloc[row]['status']

        # Pass A: 1, Pass B&C: 2, Fail: 3
        if status > 2:
            status -= 1
            # if status == 3:
            #     alarm.send_fii_alarm(subject='Factory Audit Alarm!', message='')

        result[category] = {'value': amount, 'status': status}

        # Remove none-zero category from list
        if category in categories:
            categories.remove(category)

    for empty in categories:
        result[empty] = {'value': 0, 'status': 1}

    return result


# ----- Module 2 ----- #
def count_by_site(dbio, category):
    locations = __LOCATIONS__.copy()
    data = dbio.report_amount('site', 'category' if category else None, category)

    result = []
    for row in range(0, len(data.index)):
        site = data.iloc[row]['site']
        amount = data.iloc[row]['amount']
        # Pass A: 1, Pass B: 2, Pass C: 3, Fail: 4
        status = data.iloc[row]['status']

        # Pass A: 1, Pass B&C: 2, Fail: 3
        if status > 2:
            status -= 1
            # if status == 3:
            #     alarm.send_fii_alarm(subject='Factory Audit Alarm!', message='')

        result.append(
            {
                'name': site,
                'coord': locations[site],
                'value': amount,
                'status': status
            }
        )

        # Remove none-zero site from dictionary
        if site in locations:
            del locations[site]

    for empty in locations:
        result.append(
            {
                'name': empty,
                'coord': locations[empty],
                'value': 0,
                'status': 1
            }
        )

    return result


# ----- Module 4 ----- #
# ----- Files IO ----- #
def upload_files(request, dbio, module):
    site = request.POST.get('site')
    f_type = request.POST.get('file_type')
    file_types = {
        # Info
        'ISO9001 Certificate': 1,
        'Business License': 2,
        'ODM/OEM Agreement': 3,
        'Factory Introduction': 4,
        'Company Org': 5,
        'CNAS Certificate': 6,
        # Report
        'Audit Report/Self-inspection Report': 1,
        'CAR': 2,
        # Check
        'Validation Report': 1,
        'PMP': 2,
        'SOP': 3,
        'SIP': 4,
        'CCL Certificate': 5,
        'In-coming Inspection Report': 6,
        'Internal Audit Report': 7,
        'Other': 8,
    }
    if module == 'info':
        table = 'FAInfo_upload'
        key = 'site'
        value = site

    elif module == 'report':
        category = request.POST.get('category')
        table = 'FAReport_upload'
        key = 'FAReport_seq'
        value = dbio.get_seq('FAReport', site=site, category=category).iloc[0]['seq']

    elif module == 'check':
        category = request.POST.get('category')
        s_category = request.POST.get('sample_category')
        s_pid = request.POST.get('sample_pid')
        table = 'FACheck_upload'
        key = 'FACheck_seq'
        value = dbio.get_seq('FACheck', site=site, category=category,
                             sample_category=s_category, sample_pid=s_pid).iloc[0]['seq']

    if f_type in file_types:  # Check whether file_type is in formatted list.
        uploader = request.POST.get('uploader')
        upload_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        mod_path = os.path.join(BASE_DIR, module)  # first level directory

        # Handle files
        fileio = FileFormIO(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')  # getlist() attribute name must be tha same as the front-form
        if fileio.is_valid():
            status = {}
            for f in files:
                # Save file
                try:
                    timestamp = str(datetime.now(timezone(timedelta(hours=8))).timestamp()).replace('.', '')
                    path = os.path.join(mod_path, timestamp)  # Use timestamp to generate file path
                    fileio.save(f, path)
                    # Insert into db
                    dbio.create_file(table, key, value, f.name, path, uploader, upload_time, file_types[f_type])

                    status[f.name] = 'Upload successfully.'
                except Exception as e:
                    status[f.name] = 'Error: %s' % e.__str__()

        result = {
            'message': status
        }

    else:
        result = {
            'message': 'Type not existed.'
        }

    return Response(result)


def list_files(request, dbio, module):
    site = request.POST.get('site')
    if module == 'info':
        table = 'FAInfo_upload'
        key = 'site'
        value = site

    elif module == 'report':
        category = request.POST.get('category')
        table = 'FAReport_upload'
        key = 'FAReport_seq'
        value = dbio.get_seq('FAReport', site=site, category=category).iloc[0]['seq']

    elif module == 'check':
        category = request.POST.get('category')
        s_category = request.POST.get('sample_category')
        s_pid = request.POST.get('sample_pid')
        table = 'FACheck_upload'
        key = 'FACheck_seq'
        value = dbio.get_seq('FACheck', site=site, category=category,
                             sample_category=s_category, sample_pid=s_pid).iloc[0]['seq']

    data = dbio.read_upload(table, key, value)

    result = []
    for row in range(0, len(data.index)):
        result.append(
            {
                'name': data.iloc[row][1],
                'path': data.iloc[row][2],
                'type': data.iloc[row][3],
                'upload_time': str(data.iloc[row][4]),
                'uploader': data.iloc[row][5],
            }
        )

    return Response(result)


def delete_files(dbio, module, name, path):
    tables = {
        'info': 'FAInfo_upload',
        'report': 'FAReport_upload',
        'check': 'FACheck_upload',
    }
    # Delete db record
    dbio.delete_file(tables[module], name, path)
    # Delete file
    fileio = FileFormIO()
    result = fileio.delete(path, name)

    return result
