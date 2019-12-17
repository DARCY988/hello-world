# Add your name into the list
__CONTRIBUTORS__ = ['BonJu']

# API version
__API_VERSION__ = ['latest', 'v1.1']


# -------------------- #
# DB Information
# -------------------- #
# Production Table
MYSQL_product_table = {
    'ECN': 'ECN',
    'ECN_CCL': 'ECN_CCL',
    'ECN_model': 'ECN_model',
}

# Testing Table(LOCAL ONLY)
MYSQL_test_table = {
    'ECN': 'ECN_copy1',
    'ECN_CCL': 'ECN_CCL_copy1',
    'ECN_model': 'ECN_model_copy1',
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

# # Local MySQL login accout and password
# MYSQL_login_info = {
#     'username': 'api',
#     'password': 'foxconn168!!',
#     'hostname': 'localhost',
#     'port': 3306,
#     'db_name': 'ECompliance',
#     'prod_table': MYSQL_product_table,
#     'test_table': MYSQL_test_table
# }
