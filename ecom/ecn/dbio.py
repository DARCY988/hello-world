from django.db import models
from fii_ai_api.utils.dbio.mysql import MySQL
from ecom.config import MYSQL_login_info


class ECNMySQLIO(MySQL):
    def __init__(self, debug=False, db_tables={}, custom_login_info={}, **kwargs):
        super().__init__(debug=debug, db_tables=db_tables, login_info=MYSQL_login_info, **kwargs)

    def ecn_info(self):

        sql = '''
        SELECT * FROM `%(ecn)s`
        INNER JOIN `%(ecn_ccl)s` as ccl
        INNER JOIN `%(ecn_model)s` as model
        WHERE `%(ecn)s`.cert_no = model.cert_no
        and model.PN = ccl.PN
        ''' % (
            {'ecn': self.db_tables['ECN'], 'ecn_ccl': self.db_tables['ECN_CCL'],
             'ecn_model': self.db_tables['ECN_model']}
        )
        return self.manipulate_db(sql, dtype='DataFrame')

    def site_cert_amount(self, v):
        sql = '''
        SELECT `%(target)s`, COUNT(cert_no) as 'amount' FROM `%(ecn)s`
        GROUP BY `%(target)s`
        ''' % (
            {'target': v, 'ecn': self.db_tables['ECN']}
        )
        return self.manipulate_db(sql, dtype='DataFrame')
