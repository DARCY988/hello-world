from django.db import models
from fii_ai_api.utils.dbio.mysql import MySQL
from ecom.config import MYSQL_login_info


class ECNMySQLIO(MySQL):
    def __init__(self, debug=False, db_tables={}, custom_login_info={}, **kwargs):
        super().__init__(debug=debug, db_tables=db_tables, login_info=MYSQL_login_info, **kwargs)

    def ecn_info(self, category=None, site=None, ccl=None):

        sql = '''
        SELECT ecn.site, ecn.category, ecn.cert_no, ecn.pid, ccl.CCL,
        model.supplier, model.model, model.spec, model.PN,
        model.model_compare, model.PN_compare, ecn.upload, ecn.create_time
        FROM `%(ecn)s` as ecn
        INNER JOIN `%(ecn_ccl)s` as ccl
        INNER JOIN `%(ecn_model)s` as model
        WHERE ecn.cert_no = model.cert_no %(condition)s
        and model.PN = ccl.PN
        ''' % (
            {'ecn': self.db_tables['ECN'], 'ecn_ccl': self.db_tables['ECN_CCL'],
             'ecn_model': self.db_tables['ECN_model'],
             'condition': 'and ecn.category = "%s" and ecn.site = "%s" and ccl.CCL = "%s"' % (
                 category, site, ccl) if category else ''}
        )
        return self.manipulate_db(sql, dtype='DataFrame')

    def cert_amount(self, key, v=None):
        sql = '''
        SELECT `%(key)s`, COUNT(DISTINCT cert_no) as 'amount' FROM `%(ecn)s`
        %(condition)s
        GROUP BY `%(key)s`
        ''' % (
            {'key': key, 'ecn': self.db_tables['ECN'], 'condition': 'WHERE category = "%s"' % v if v else ''}
        )
        return self.manipulate_db(sql, dtype='DataFrame')

    def ccl_cert_amount(self, category=None, site=None):
        sql = '''
        SELECT c.CCL as 'CCL', COUNT(DISTINCT b.cert_no) as 'amount' FROM `%(ecn)s` as a
        INNER JOIN `%(ecn_model)s` as b
        INNER JOIN `%(ecn_ccl)s` as c
        WHERE b.PN = c.PN and b.cert_no = a.cert_no %(condition)s
        GROUP BY c.CCL
        ''' % (
            {'ecn': self.db_tables['ECN'], 'ecn_model': self.db_tables['ECN_model'],
             'ecn_ccl': self.db_tables['ECN_CCL'],
             'condition': 'and a.category = "%s" and a.site = "%s"' % (category, site) if category else ''}
        )
        return self.manipulate_db(sql, dtype='DataFrame')

    def create_ECN(self, site, category, cert_no, pid, uploader, create_time):
        sql = '''
        INSERT INTO `%(table)s` (site, category, cert_no, pid, upload, create_time)
        VALUES ('%(site)s', '%(category)s', '%(cert_no)s', '%(pid)s', '%(uploader)s', '%(create_time)s')
        ''' % (
            {'table': self.db_tables['ECN'], 'site': site, 'category': category, 'cert_no': cert_no,
             'pid': pid, 'uploader': uploader, 'create_time': create_time}
        )
        return self.manipulate_db(sql)

    def create_ccl(self, ccl, pn):
        sql = '''
        INSERT INTO `%(table)s` (CCL, PN)
        VALUES ('%(CCL)s', '%(PN)s')
        ''' % (
            {'table': self.db_tables['ECN_CCL'], 'CCL': ccl, 'PN': pn}
        )
        return self.manipulate_db(sql)

    def create_model(self, supplier, model, spec, pn, model_comp, pn_comp, cert_no):
        sql = '''
        INSERT INTO `%(table)s` (supplier, model, spec, PN, model_compare, PN_compare, cert_no)
        VALUES ('%(supplier)s', '%(model)s', '%(spec)s', '%(pn)s', '%(model_comp)s', '%(pn_comp)s', '%(cert_no)s')
        ''' % (
            {'table': self.db_tables['ECN_model'], 'supplier': supplier, 'model': model, 'spec': spec,
             'pn': pn, 'model_comp': model_comp, 'pn_comp': pn_comp, 'cert_no': cert_no}
        )
        return self.manipulate_db(sql)

    def check_duplicated(self, table, key, value):
        sql = '''
        SELECT EXISTS(SELECT * FROM `%(table)s` WHERE '%(key)s' = '%(value)s') AS count
        ''' % (
            {'table': table, 'key': key, 'value': value}
        )
        result = self.manipulate_db(sql, dtype='DataFrame').iloc[0][0]

        if result == 0:
            return False
        else:
            return True
