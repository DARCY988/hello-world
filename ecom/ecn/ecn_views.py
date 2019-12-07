from fii_ai_api.utils.response import fii_api_handler
from .dbio import ECNMySQLIO
from .upload import UploadFileForm
from django.http import HttpResponseRedirect

# -------------------- #
# AI Model Results API
# -------------------- #
@fii_api_handler(['post'])
def upload_file(request, debug, api_version):  # Add your parameters here

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save file
            # result = form.save_upload_file(request.FILES['file'], str(request.FILES.get('file')))
            # Read file
            result = form.read_upload_file(request.FILES.get('file'), db, request.POST.get('user'))

    return result


# -------------------- #
# DataBase CRUD API
# -------------------- #
@fii_api_handler(['get'])
def api_ecn_read(request, debug, api_version):  # Add your parameters here

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    return db.ecn_info()


@fii_api_handler(['get'])
def api_cert_count(request, debug, api_version, value):  # Add your parameters here

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    return db.site_cert_amount(value)
