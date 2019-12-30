from fii_ai_api.utils.response import fii_api_handler
from .dbio import ECNMySQLIO, AgileMySQLIO
from .notify import MailCenter
from .fileio import FileFormIO
from .models import (
    count_by_category, count_by_site, list_all_cert, edit_cert_table,
    list_all_ecn
)
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
    # mail = MailCenter(debug=debug, api_version=api_version)

    result = count_by_category(db, site)

    return Response(result)


@api_view(['get'])
def site_cert_view(request, debug, api_version, category):

    db = ECNMySQLIO(debug=debug, api_version=api_version)
    # mail = MailCenter(debug=debug, api_version=api_version)

    result = count_by_site(db, category)

    return Response(result)


@api_view(['get'])
def all_cert_view(request, debug, api_version):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    category = request.GET.get('category', None)
    site = request.GET.get('site', None)

    result = list_all_cert(db, category, site)

    return Response(result)


@api_view(['post', 'put'])
def edit_cert_view(request, debug, api_version):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    if request.method in ['POST', 'PUT']:
        site = request.POST.get('site')
        category = request.POST.get('category')
        cert_no = request.POST.get('cert_no')
        pid = request.POST.get('pid')
        ccl = request.POST.get('ccl')
        supplier = request.POST.get('supplier')
        model = request.POST.get('model')
        spec = request.POST.get('spec')
        pn = request.POST.get('pn')
        updater = request.POST.get('updater')
        new_pn = request.POST.get('new_pn', None)
        new_supplier = request.POST.get('new_supplier', None)
        new_model = request.POST.get('new_model', None)
        new_spec = request.POST.get('new_spec', None)

        result = edit_cert_table(db, site, category, cert_no, pid, ccl, supplier, model, spec, pn, updater,
                                 new_pn, new_supplier, new_model, new_spec)

    return Response(result)

# Agile Tab
@api_view(['get'])
def all_ecn_view(request, debug, api_version, site=None):
    agile_db = AgileMySQLIO(debug=debug, api_version=api_version)
    ecn_db = ECNMySQLIO(debug=debug, api_version=api_version)

    result = list_all_ecn(agile_db, ecn_db, site)

    return Response(result)


# -------------------- #
# DataBase CRUD API
# -------------------- #
@fii_api_handler(['get'])
def api_ecn_read(request, debug, api_version):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    return db.read_cert_info()


@fii_api_handler(['get'])
def api_cert_count(request, debug, api_version, key):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    return db.cert_amount(key)


@api_view(['post'])
def api_file_upload(request, debug, api_version):

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
def api_file_download(request, debug, api_version, file_name):

    path = os.path.join(BASE_DIR, 'doc')

    # Do download method.
    fileio = FileFormIO()
    result = fileio.download(path, file_name)

    return result


@api_view(['get'])
def api_file_preview(request, debug, api_version, file_name):

    path = os.path.join(BASE_DIR, 'doc')

    # Do preview method.
    fileio = FileFormIO()
    result = fileio.preview(path, file_name)

    return result


@api_view(['delete'])
def api_file_delete(request, debug, api_version, file_name):

    path = os.path.join(BASE_DIR, 'doc')
    if request.method == 'DELETE':
        # Do delete method.
        fileio = FileFormIO()
        result = fileio.delete(path, file_name)

    return result
