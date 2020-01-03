from fii_ai_api.utils.response import fii_api_handler
from .dbio import DataCenterMySQLIO
from .fileio import FileFormIO
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
from . import models
from fii_ai_api.settings import STATIC_ROOT
import pandas as pd
from pandas import DataFrame, read_excel
from fii_ai_api.utils.files import FileHandler
import datetime

# Build path in this module like this: os.path.join(BASE_DIR, ...)
BASE_DIR = STATIC_ROOT
db = DataCenterMySQLIO(debug=True)
# -------------------- #
# AI Model Results API
# -------------------- #


@fii_api_handler(['post'])
def api_checking_status_by_category(request, debug, api_version  # these three parameters always place at index 0:2
                                    ):  # Add your parameters here

    result = models.checking_status_by_category('category', select_site=request.POST.get('select_site'))

    return result


@fii_api_handler(['post'])
def api_checking_status_by_site(request, debug, api_version  # these three parameters always place at index 0:2
                                ):  # Add your parameters here

    result = models.checking_status_by_site('site', select_category=request.POST.get('select_category'))

    return result


@fii_api_handler(['post'])
def api_get_all_data(request, debug, api_version  # these three parameters always place at index 0:2
                     ):  # Add your parameters here

    result = models.checking_expire(select_site=request.POST.get('select_site'),
                                    select_category=request.POST.get('select_category'))
    #  input site , and one of category ,if category = none , return all category
    #  或者 category ,以及其中一項site, 若site is none也可

    result.sort(key=lambda row: row['exp_date'])
    #  依照日期做排序 取出每一列的exp_data做升冪排序
    return result


@fii_api_handler(['post'])
def dc_upload(request, debug, api_version  # these three parameters always place at index 0:2
              ):  # Add your parameters here

    result = db.insert_dc_upload(path=BASE_DIR, file=request.FILES['file'],
                                 name=request.FILES['file'].name,
                                 cert_no=request.POST.get('cert_no'),
                                 upload=request.POST.get('upload'),
                                 upload_type=request.POST.get('upload_type'))

    return result


@fii_api_handler(['post'])
def get_path_by_cert(request, debug, api_version  # these three parameters always place at index 0:2
                     ):  # Add your parameters here

    result = db.select_cert_files(request.POST.get('cert_no'))
    return result


@fii_api_handler(['post'])
def delete_by_path(request, debug, api_version  # these three parameters always place at index 0:2
                   ):  # Add your parameters here

    result = db.delete_cert_files(path=request.POST.get('path'))

    return result


@api_view(['post'])
def preview_by_path(request, debug, api_version  # these three parameters always place at index 0:2
                    ):  # Add your parameters here

    result = db.preview_files(request.POST.get('path'))
    return result


@api_view(['post'])
def download_by_path(request, debug, api_version  # these three parameters always place at index 0:2
                     ):  # Add your parameters here

    result = db.download_files(request.POST.get('path'))

    return result


@fii_api_handler(['post'])
def upload_excel(request, debug, api_version  # these three parameters always place at index 0:2
                 ):  # Add your parameters here

    data = request.FILES['file']
    datacente_df = pd.read_excel(data, sheet_name='Data Center')
    result_list = []
    for i in range(len(datacente_df)):
        sql_dict = {}
        sql_dict['site'] = datacente_df.iloc[i][0]
        sql_dict['category'] = datacente_df.iloc[i][1]
        sql_dict['cert_no'] = datacente_df.iloc[i][2]
        sql_dict['applicant'] = datacente_df.iloc[i][3]
        sql_dict['pid'] = datacente_df.iloc[i][4]
        sql_dict['issue_date'] = datacente_df.iloc[i][5]
        sql_dict['exp_date'] = datacente_df.iloc[i][6]
        sql_dict['status'] = datacente_df.iloc[i][7]
        sql_dict['upload'] = 'null'
        sql_dict['create_time'] = datetime.datetime.now()
        try:
            result = db.insert_datacenter(sql_dict)
            if result:
                result = 'upload row %d success' % i
            else:
                result = 'upload row %d fail, Duplicate entry pid' % i
            result_list.append(result)
        except Exception:
            result = 'upload row %i error' % i
            result_list.append(result)

    return result_list
