from django.db import models
from fii_ai_api.utils.dbio.mysql import MySQL
from .config import MYSQL_login_info


class DemoMySQLIO(MySQL):
    def __init__(self, debug=False, db_tables={}, custom_login_info={}, **kwargs):
        super().__init__(debug=debug, db_tables=db_tables, **kwargs)

    def user_info(self, v):

        sql = '''
        SELECT * FROM `%(demo)s`
        %(select_id)s
        ''' % (
            {'demo': self.db_tables['demo'], 'select_id': 'WHERE id = %s' % v if v else ''}
        )
        return self.manipulate_db(sql, dtype='DataFrame')
