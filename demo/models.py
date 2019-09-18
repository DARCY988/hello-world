from django.db import models
from fii_ai_api.utils.mysql import MySQL
from .config import mysql_login_info


class DemoMySQL(MySQL):

    def test(self, v):
        return 'Pass value: {}'.format(v)


demo_db = DemoMySQL(**mysql_login_info)
