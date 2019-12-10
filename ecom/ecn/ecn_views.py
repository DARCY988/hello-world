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


@fii_api_handler(['get'])
def category_cert_view(request, debug, api_version):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    data = db.cert_amount('category')

    # TODO: Check Agile system and get the status

    result = {}
    for row in range(0, len(data.index)):
        result['%s' % data.iloc[row]['category']] = {'value': data.iloc[row]['amount'], 'status': 'Not Ready.'}

    return result


@fii_api_handler(['get'])
def site_cert_view(request, debug, api_version, category):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    location_dict = {
        "FCZ": [49.9493036, 15.2120232],
        "FTX": [44.8204983, -94.0602476],
        "FJZ": [31.6859596, -106.543702],
        "FOC": [22.7198832, 114.0491412],
        "FOL": [22.6764474, 113.899891],
    }

    data = db.cert_amount('site', category)

    # TODO: Check Agile system and get the status

    result = []
    for row in range(0, len(data.index)):
        coord = location_dict['%s' % data.iloc[row]['site']]
        result.append(
            {
                'location': data.iloc[row]['site'],
                'coord': coord,
                'value': data.iloc[row]['amount'],
                'status': 'Not Ready.'
            }
        )

    return result


@fii_api_handler(['get'])
def ccl_cert_view(request, debug, api_version, category, site):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    data = db.ccl_cert_amount(category, site)

    # TODO: Check Agile system and get the status

    result = {}
    for row in range(0, len(data.index)):
        result['%s' % data.iloc[row]['CCL']] = {'value': data.iloc[row]['amount'], 'status': 'Not Ready.'}

    return result


@fii_api_handler(['get'])
def all_cert_view(request, debug, api_version, category, site, ccl):

    db = ECNMySQLIO(debug=debug, api_version=api_version)

    data = db.ecn_info(category, site, ccl)

    # TODO: Check Agile system and get the status

    result = []
    for row in range(0, len(data.index)):
        result.append(
            {
                'Site': data.iloc[row]['site'],
                'Category': data.iloc[row]['category'],
                'Certificate No.': data.iloc[row]['cert_no'],
                'Product PID': data.iloc[row]['pid'],
                'CCL': data.iloc[row]['CCL'],
                'CCL Supplier': data.iloc[row]['supplier'],
                'CCL Model': data.iloc[row]['model'],
                'CCL Spec.': data.iloc[row]['spec'],
                'CCL PN': data.iloc[row]['PN'],
                'CCL Model compare': data.iloc[row]['model_compare'],
                'CCL PN compare': data.iloc[row]['PN_compare'],
            }
        )

    return result


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
