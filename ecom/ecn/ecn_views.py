from fii_ai_api.utils.response import fii_api_handler
from .dbio import ECNMySQLIO, AgileMySQLIO
from .notify import MailCenter
from .fileio import FileFormIO
from . import models
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os

# Build path in this module like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# -------------------- #
# AI Model Results API
# -------------------- #
# ECN Tab
@api_view(['get'])
def category_cert_view(request, debug, api_version, site=None):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    result = models.count_by_category(db, site)

    mail_service = MailCenter(debug=debug, api_version=api_version)

    models.alarm(
        mail_service=mail_service,
        subject='ECN Error!',
        text_content='Find ECN different.'
    )

    return Response(result)


@api_view(['get'])
def site_cert_view(request, debug, api_version, category):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    result = models.count_by_site(db, category)

    return Response(result)


@api_view(['get'])
def all_cert_view(request, debug, api_version):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    category = request.GET.get('category', None)
    site = request.GET.get('site', None)

    result = models.list_all_cert(db, category, site)

    return Response(result)


# Agile Tab
@api_view(['get'])
def all_ecn_view(request, debug, api_version, site=None):
    agile_db = AgileMySQLIO(debug=debug, api_version=api_version)
    ecn_db = ECNMySQLIO(debug=debug, api_version=api_version)

    result = models.list_all_ecn(agile_db, ecn_db, site)

    return Response(result)


# -------------------- #
# DataBase CRUD API
# -------------------- #
@fii_api_handler(['get'])
def api_ecn_read(request, debug, api_version):  # Add your parameters here

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    return db.ecn_info()


@fii_api_handler(['get'])
def api_cert_count(request, debug, api_version, key):  # Add your parameters here

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    return db.cert_amount(key)


@api_view(['post'])
def api_file_upload(request, debug, api_version):  # Add your parameters here

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    # path = os.path.join(BASE_DIR, 'doc')
    # status = {}
    if request.method == 'POST':
        fileio = FileFormIO(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')  # getlist() attribute name must be tha same as the front-form
        if fileio.is_valid():
            for f in files:
                # Save file
                # status[f.name] = {
                #     'status': fileio.save(f, path)
                # }
                # Read file and save to db
                result = fileio.read_ecn(f, db, request.POST.get('user'))

    return Response(result)


@api_view(['get'])
def api_file_download(request, debug, api_version, file_name):  # Add your parameters here

    path = os.path.join(BASE_DIR, 'doc')
    if request.method == 'GET':
        # Do download method.
        fileio = FileFormIO()
        result = fileio.download(path, file_name)

    return result


@api_view(['get'])
def api_file_preview(request, debug, api_version, file_name):  # Add your parameters here

    path = os.path.join(BASE_DIR, 'doc')
    if request.method == 'GET':
        # Do preview method.
        fileio = FileFormIO()
        result = fileio.preview(path, file_name)

    return result


@api_view(['delete'])
def api_file_delete(request, debug, api_version, file_name):  # Add your parameters here

    path = os.path.join(BASE_DIR, 'doc')
    if request.method == 'DELETE':
        # Do delete method.
        fileio = FileFormIO()
        result = fileio.delete(path, file_name)

    return result
