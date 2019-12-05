from fii_ai_api.utils.response import fii_api_handler
from .dbio import ECNMySQLIO
from .upload import UploadFileForm
from django.http import HttpResponseRedirect

# -------------------- #
# AI Model Results API
# -------------------- #
@fii_api_handler(['get', 'post'])
def upload_view(request, debug, api_version):  # Add your parameters here
    import os
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.handle_upload_file(request.FILES['file'], str(request.FILES.get('file')))
            # target = os.path.join(form.path, str(request.FILES.get('file')))
            # with open(target, 'wb+') as destination:
            #     for chunk in request.FILES['file']:
            #         destination.write(chunk)
            #     destination.close()

    return HttpResponseRedirect('success')


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
