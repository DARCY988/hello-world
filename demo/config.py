# Add your name into the list
__CONTRIBUTORS__ = []

# API version
__API_VERSION__ = ['latest', 'v1.0']


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
    'hostname': 'localhost',
    'db_name': 'demo',
    'prod_table': MYSQL_product_table,
    'test_table': MYSQL_test_table
}
