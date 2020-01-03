from django.db import models
from fii_ai_api.utils.dbio.mysql import MySQL
from ecom.config import MYSQL_login_info


class ECNMySQLIO(MySQL):
    def __init__(self, debug=False, db_tables={}, custom_login_info={}, **kwargs):
        super().__init__(debug=debug, db_tables=db_tables, login_info=MYSQL_login_info, **kwargs)

    def create_file(self, table, key, value, name, path, uploader, upload_time, type):
        sql = '''
        INSERT INTO `%(table)s` ('%(key)s', name, path, upload, upload_time, type)
        VALUES ('%(value)s', '%(name)s', '%(path)s', '%(uploader)s', '%(time)s', '%(type)s');
        SELECT LAST_INSERT_ID()
        ''' % (
            {'table': self.db_tables[table], 'key': key, 'value': value,
             'name': name, 'path': path, 'uploader': uploader, 'time': upload_time, 'type': type}
        )
        return self.manipulate_db(sql)

    def get_seq(self, table, **kwargs):
        sql = '''
        SELECT seq FROM `%(table)s` WHERE %(conditions)s
        ''' % (
            {'table': self.db_tables[table],
             'conditions': ' and '.join('%s="%s"' % (k, v) for (k, v) in kwargs.items())}
        )
        return self.manipulate_db(sql, dtype='DataFrame')
