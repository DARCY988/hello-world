from django.db import models
from fii_ai_api.utils.mysql import MySQL
from .config import MYSQL_login_info


class DemoModel(MySQL):
    def __init__(self, debug=False, db_tables={}, **login_info):
        _default_login_info = MYSQL_login_info.copy()

        if any(login_info):
            _default_login_info.update(login_info)

        super().__init__(debug=debug, db_tables=db_tables, **_default_login_info)

    def test(self, v):

        sql = '''
        SELECT * FROM `%(demo)s`
        %(select_id)s
        ''' % (
            {'demo': self.db_tables['demo'], 'select_id': 'WHERE id = %s' % v if v else ''}
        )
        return self.manipulate_db(sql)
