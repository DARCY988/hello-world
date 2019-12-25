from django.db import models
from fii_ai_api.utils.dbio.mysql import MySQL
from ecom.config import MYSQL_login_info


class DataCenterMySQLIO(MySQL):
    def __init__(self, debug=False, db_tables={}, custom_login_info={}, **kwargs):
        super().__init__(debug=debug, db_tables=db_tables, login_info=MYSQL_login_info, **kwargs)

    def get_all_column(self, **kwargs):

        # if column == 'site':
        #     select_column = 'category'
        # else:
        #     select_column = 'site'
        # if kwargs['select_value'] is not None:
        #     select_value = ' AND ' + select_column + ' = ' + '\'' + kwargs['select_value'] + '\''
        # else:
        #     select_value = ''

        select_value = ''
        value = ''
        column = ''
        all_column = 'site , category, cert_no, applicant, pid, issue_date, exp_date'
        #  all_column要顯示的欄位

        sql = '''
        SELECT %(all_column)s
        FROM %(DataCenter_table)s

        ''' % (
            {'DataCenter_table' : self.db_tables['DataCenter'], 'all_column' : all_column, 'column' : column,
             'value' : value , 'select_value' : select_value
             }
        )
        print(sql)

        return self.manipulate_db(sql, dtype='list')

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
