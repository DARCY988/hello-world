from pandas import DataFrame
from datetime import datetime, timezone, timedelta
from fii_ai_api.settings import STATIC_ROOT
from ecom.config import __CATEGORIES__, __LOCATIONS__
from .fileio import FileFormIO
from .notify import MailCenter
import os


# Build path in this module like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.join(STATIC_ROOT, 'audit')


def info_upload(request, dbio, uploader):
    upload_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    path = os.path.join(BASE_DIR, 'info')
    site = request.POST.get('site')

    # Handle files
    fileio = FileFormIO(request.POST, request.FILES)
    files = request.FILES.getlist('file_field')  # getlist() attribute name must be tha same as the front-form
    if fileio.is_valid():
        for f in files:
            # Insert into db
            dbio.create_file('FAInfo_upload', 'site', site, f.name, path, uploader, upload_time)
            # Save file
            path = os.path.join(path, site)
            fileio.save(f, path)

    return path


def report_upload(request, dbio, uploader):
    # Keys to get seq
    site = request.POST.get('site')
    category = request.POST.get('category')

    upload_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    path = os.path.join(BASE_DIR, 'report')
    report_seq = dbio.get_seq('FAReport', site=site, category=category)
    f_type = request.POST.get('type')

    # Handle files
    fileio = FileFormIO(request.POST, request.FILES)
    files = request.FILES.getlist('file_field')  # getlist() attribute name must be tha same as the front-form
    if fileio.is_valid():
        for f in files:
            # Insert into db
            dbio.create_file('FAReport_upload', 'FAReport_seq', report_seq, f.name, path, uploader, upload_time, f_type)
            # Save file
            path = os.path.join(path, report_seq)
            fileio.save(f, path)

    return path


def check_upload(request, dbio, uploader):
    # Keys to get seq
    site = request.POST.get('site')
    category = request.POST.get('category')
    sample_category = request.POST.get('sample_category')
    sample_pid = request.POST.get('sample_pid')

    upload_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    path = os.path.join(BASE_DIR, 'check')
    check_seq = dbio.get_seq('FACheck', site=site, category=category,
                             sample_category=sample_category, sample_pid=sample_pid)
    f_type = request.POST.get('type')

    # Handle files
    fileio = FileFormIO(request.POST, request.FILES)
    files = request.FILES.getlist('file_field')  # getlist() attribute name must be tha same as the front-form
    if fileio.is_valid():
        for f in files:
            # Insert into db
            dbio.create_file('FACheck_upload', 'FACheck_seq', check_seq, f.name, path, uploader, upload_time, f_type)
            # Save file
            path = os.path.join(path, check_seq)
            fileio.save(f, path)

    return path
