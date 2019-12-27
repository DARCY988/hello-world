from django.db import models
from fii_ai_api.utils.dbio.mysql import MySQL
from ecom.config import MYSQL_login_info


class DataCenterMySQLIO(MySQL):
    def __init__(self, debug=False, db_tables={}, custom_login_info={}, **kwargs):
        super().__init__(debug=debug, db_tables=db_tables, login_info=MYSQL_login_info, **kwargs)

    def get_all_data(self, **kwargs):
        #  將kwargs 寫入變數
        try:
            select_site = ' WHERE ' + 'site' + ' = ' + '\'' + kwargs['select_site'] + '\''
        except Exception:
            select_site = ''
        try:
            select_category = ' WHERE ' + 'category' + ' = ' + '\'' + kwargs['select_category'] + '\''
        except Exception:
            select_category = ''

        if select_site and select_category :
            select_category = ' AND ' + 'category' + ' = ' + '\'' + kwargs['select_category'] + '\''

        get_column = 'site, category, cert_no, applicant, pid, issue_date, exp_date, status,upload, upload Date'
        #  get_column 要顯示的欄位

        sql = '''
        SELECT %(get_column)s
        FROM %(DataCenter_table)s
        %(select_site)s %(select_category)s
        ''' % (
            {'DataCenter_table' : self.db_tables['DataCenter'], 'get_column' : get_column,
             'select_category' : select_category, 'select_site' : select_site
             }
        )

        return self.manipulate_db(sql, dtype='dict')

    def get_count(self, column, value, **kwargs):
        #  傳入必要參數column及可附加條件kwargs計算數量
        #  EX column = site ,  value = FOL
        #  EX column = category ,  value = CCC
        #  應該可以改寫迴圈
        try:
            status_value = ' AND ' + 'status' + ' = ' + '\'' + kwargs['status_value'] + '\''
        except Exception:
            status_value = ''
        try:
            select_site = ' AND ' + 'site' + ' = ' + '\'' + kwargs['select_site'] + '\''
        except Exception:
            select_site = ''
        try:
            select_category = ' AND ' + 'category' + ' = ' + '\'' + kwargs['select_category'] + '\''
        except Exception:
            select_category = ''
        #  改寫為迴圈
        sql = '''
        SELECT COUNT(%(column)s)
        FROM %(DataCenter_table)s
        WHERE  %(column)s = '%(value)s' %(status_value)s %(select_site)s %(select_category)s
        ''' % (
            {'DataCenter_table' : self.db_tables['DataCenter'], 'column' : column,
             'value' : value , 'status_value' : status_value, 'select_category' : select_category,
             'select_site' : select_site
             }
        )

        return self.manipulate_db(sql, dtype='list')
