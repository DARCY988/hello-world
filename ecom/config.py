# Add your name into the list
__CONTRIBUTORS__ = ['BonJu', 'Leo']

# API version
__API_VERSION__ = ['latest', 'v2.2']


# -------------------- #
# Common Information
# -------------------- #
# Category list
__CATEGORIES__ = [
    'CCC',
    'CSA',
    'ETL',
    'IECEx',
    'MET',
    'Nemko',
    'TUV',
    'UL',
]

# Site list
__LOCATIONS__ = {
    "FCZ": [15.2120232, 49.9493036],
    "FOC": [115.0491412, 27.7198832],
    "FOL": [113.899891, 18.6764474],
    "FTX": [-94.0602476, 44.8204983],
    "FJZ": [-106.543702, 31.6859596],
}


# -------------------- #
# DB Information
# -------------------- #
# Production Table
MYSQL_product_table = {
    'ECN': 'ECN',
    'ECN_CCL': 'ECN_CCL',
    'ECN_model': 'ECN_model',
    'DataCenter' : 'DataCenter',
    'DC_upload' : 'DC_upload',
    'FACheck' : 'FACheck',
    'FACheck_upload' : 'FACheck_upload',
    'FAInfo_upload' : 'FAInfo_upload',
    'FAReport' : 'FAReport',
    'FAReport_upload' : 'FAReport_upload',
    'ODM' : 'ODM',
    'ODM_upload' : 'ODM_upload',
    'PVTComp' : 'PVTComp',
    'PVTComp_upload' : 'PVTComp_upload',
    'PVTGoods' : 'PVTGoods',
    'PVTGoods_upload' : 'PVTGoods_upload',
}

AGILE_product_table = {
    'ECN': 'ECN',
    'PN': 'PN',
}

# Testing Table(LOCAL ONLY)
MYSQL_test_table = {
    'ECN': 'ECN_copy1',
    'ECN_CCL': 'ECN_CCL_copy1',
    'ECN_model': 'ECN_model_copy1',
    'DataCenter' : 'DataCenter_test',
    'DC_upload' : 'DC_upload',
<<<<<<< HEAD
    'PVTGoods' : 'PVTGoods',
    'PVTGoods_upload' : 'PVTGoods_upload',
    'PVTComp' : 'PVTComp',
    'PVTComp_upload' : 'PVTComp_upload',
=======
    'FACheck' : 'FACheck_copy1',
    'FACheck_upload' : 'FACheck_upload_copy1',
    'FAInfo_upload' : 'FAInfo_upload_copy1',
    'FAReport' : 'FAReport_copy1',
    'FAReport_upload' : 'FAReport_upload_copy1',
    'ODM' : 'ODM_copy1',
    'ODM_upload' : 'ODM_upload_copy1',
    'PVTComp' : 'PVTComp_copy1',
    'PVTComp_upload' : 'PVTComp_upload_copy1',
    'PVTGoods' : 'PVTGoods_copy1',
    'PVTGoods_upload' : 'PVTGoods_upload_copy1',
>>>>>>> master
}

AGILE_test_table = {
    'ECN': 'ECN',
    'PN': 'PN',
}

# MySQL login accout and password
MYSQL_login_info = {
    'username': 'EUser',
    'password': 'Efoxconn88',
    'hostname': '10.124.131.81',
    'port': 8872,
    'db_name': 'ECompliance',
    'prod_table': MYSQL_product_table,
    'test_table': MYSQL_test_table
}

# Agile MySQL login account and password
AGILE_login_info = {
    'username': 'mqait',
    'password': 'foxconnmqait',
    'hostname': '10.124.132.81',
    'port': 8878,
    'db_name': 'mqadb',
    'prod_table': AGILE_product_table,
    'test_table': AGILE_test_table
}

# # bonju0102 local MySQL login accout and password
# MYSQL_login_info = {
#     'username': 'api',
#     'password': 'foxconn168!!',
#     'hostname': 'localhost',
#     'port': 3306,
#     'db_name': 'ECompliance',
#     'prod_table': MYSQL_product_table,
#     'test_table': MYSQL_test_table
# }


#  leolee loacl MySQL login accout and password
MYSQL_login_info = {
    'username': 'root',
    'password': '55665566',
    'hostname': '127.0.0.1',
    'port': 3306,
    'db_name': 'test',
    'prod_table': MYSQL_product_table,
    'test_table': MYSQL_test_table
}


# -------------------- #
# Mail Information
# -------------------- #
# Production settings
MAIL_product_setting = {
    'use_ssl': True,
    'use_tls': False,
    'host': 'smtp.163.com',
    'port': 465,
    'username': 'iai_reply@163.com',
    'password': 'foxconn88',  # password: foxconn168!!
    'from_mail': 'IAI Alarm Center <iai_reply@163.com>',
    'recipient_list': [
        'BonJu <bonju.huang@gmail.com>',
    ],
}

# Test settings
MAIL_test_setting = {
    'use_ssl': True,
    'use_tls': False,
    'host': 'smtp.163.com',
    'port': 465,
    'username': 'iai_reply@163.com',
    'password': 'foxconn88',  # password: foxconn168!!
    'from_mail': 'IAI Alarm Center <iai_reply@163.com>',
    'recipient_list': [
        'BonJu <bonju.huang@gmail.com>',
    ],
}

MAIL_connect_info = {
    'prod_setting': MAIL_product_setting,
    'test_setting': MAIL_test_setting
}
