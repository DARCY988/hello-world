from fii_ai_api.utils.response import fii_api_handler
from .dbio import ECNMySQLIO


# -------------------- #
# AI Model Results API
# -------------------- #


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
