from fii_ai_api.utils.response import fii_api_handler
from .models import demo_db


@fii_api_handler(['get'])
def demo_response(request, debug, api_version,  # these three parameters always place at index 0:2
                  value):  # Add your parameters here
    return demo_db.test(value)
