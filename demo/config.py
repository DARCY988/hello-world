# Add your name into the list
__CONTRIBUTORS__ = ['Bean']

# API version
__API_VERSION__ = ['latest', 'v1.0']

# test adding one line
# -------------------- #
# DB Information
# -------------------- #
# Production Table
MYSQL_product_table = {
    'demo': 'usr_info'
}

# Testing Table
MYSQL_test_table = {
    'demo': 'usr_info_copy1'
}

# MySQL login accout and password
MYSQL_login_info = {
    'username': 'api',
    'password': 'Develop123!@#',
    'hostname': '10.124.131.87',
    'port': 8871,
    'db_name': 'demo',
    'prod_table': MYSQL_product_table,
    'test_table': MYSQL_test_table
}

# # Local MySQL login accout and password
# MYSQL_login_info = {
#     'username': 'api',
#     'password': 'foxconn168!!',
#     'hostname': 'localhost',
#     'port': 3306,
#     'db_name': 'demo',
#     'prod_table': MYSQL_product_table,
#     'test_table': MYSQL_test_table
# }

# !!!!!! ONLY FOR 10/12 tutorial !!!!!!
# MYSQL_login_info = {
#     'username': 'sql12308246',
#     'password': 'kSzgZteUSX',
#     'hostname': 'sql12.freemysqlhosting.net',
#     'port': 3306,
#     'db_name': 'sql12308246',
#     'prod_table': MYSQL_product_table,
#     'test_table': MYSQL_test_table
# }
