from fii_ai_api.utils.mysql import MySQL
from .config import MYSQL_login_info


class DemoMySQL(MySQL):
    super(MySQL).__init__(**MYSQL_login_info)

    def test(self, v):
        sql = '''
        SELECT * FROM demo
        '''
        return self.manipulate_db(sql)
