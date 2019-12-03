from fii_ai_api.utils.response import fii_api_handler
from .dbio import DemoMySQLIO
from .ai_models import demo_ai_model


# -------------------- #
# AI Model Results API
# -------------------- #
@fii_api_handler(['get'])
def demo_ai_view(request, debug, api_version,  # these three parameters always place at index 0:2
                 value):  # Add your parameters here
    db = DemoMySQLIO(debug=debug, api_version=api_version)

    result = demo_ai_model(db, value)

    return result


# -------------------- #
# DataBase CRUD API
# -------------------- #
@fii_api_handler(['get'])
def api_demo_read(request, debug, api_version,  # these three parameters always place at index 0:2
                    value):  # Add your parameters here
    db = DemoMySQLIO(debug=debug, api_version=api_version)

    return db.user_info(value)


@fii_api_handler(['get'])
def api_ecn_read(request, debug, api_version):  # Add your parameters here
    db = DemoMySQLIO(debug=debug, api_version=api_version)

    return db.ecn_info()


@fii_api_handler(['get'])
def api_cert_count(request, debug, api_version,
                    value):  # Add your parameters here
    db = DemoMySQLIO(debug=debug, api_version=api_version)

    return db.site_cert_amount(value)
