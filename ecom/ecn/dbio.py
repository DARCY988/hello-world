from django.db import models
from fii_ai_api.utils.dbio.mysql import MySQL
from ecom.config import MYSQL_login_info, AGILE_login_info


class ECNMySQLIO(MySQL):
    def __init__(self, debug=False, db_tables={}, custom_login_info={}, **kwargs):
        super().__init__(debug=debug, db_tables=db_tables, login_info=MYSQL_login_info, **kwargs)

    def read_cert_info(self, category=None, site=None):
        sql = '''
        SELECT ecn.site, ecn.category, ecn.cert_no, ecn.pid, ccl.CCL,
        model.supplier, model.model, model.spec, model.PN,
        model.model_compare, model.PN_compare, ecn.upload, ecn.create_time
        FROM `%(ecn)s` as ecn
        INNER JOIN `%(ecn_ccl)s` as ccl
        INNER JOIN `%(ecn_model)s` as model
        WHERE ecn.cert_no = model.cert_no and model.PN = ccl.PN
        %(category)s
        %(site)s
        ''' % (
            {'ecn': self.db_tables['ECN'],
             'ecn_ccl': self.db_tables['ECN_CCL'],
             'ecn_model': self.db_tables['ECN_model'],
             'category': 'and ecn.category = "%s"' % category if category else '',
             'site': 'and ecn.site = "%s"' % site if site else ''}
        )
        return self.manipulate_db(sql, dtype='DataFrame')

    def cert_amount(self, target, key=None, value=None):
        sql = '''
        SELECT `%(target)s`, COUNT(DISTINCT cert_no) as 'amount' FROM `%(ecn)s`
        %(condition)s
        GROUP BY `%(target)s`
        ORDER BY amount DESC
        ''' % (
            {'target': target, 'ecn': self.db_tables['ECN'],
             'condition': 'WHERE %s = "%s"' % (key, value) if (key and value) else ''}
        )
        return self.manipulate_db(sql, dtype='DataFrame')

    # def ccl_cert_amount(self, category=None, site=None):
    #     sql = '''
    #     SELECT ccl.CCL as 'CCL', COUNT(DISTINCT model.cert_no) as 'amount' FROM `%(ecn)s` as ecn
    #     INNER JOIN `%(ecn_model)s` as model
    #     INNER JOIN `%(ecn_ccl)s` as ccl
    #     WHERE model.PN = ccl.PN and model.cert_no = ecn.cert_no
    #     %(category)s
    #     %(site)s
    #     GROUP BY ccl.CCL
    #     ''' % (
    #         {'ecn': self.db_tables['ECN'], 'ecn_model': self.db_tables['ECN_model'],
    #          'ecn_ccl': self.db_tables['ECN_CCL'],
    #          'category': 'and ecn.category = "%s"' % category if category else '',
    #          'site': 'and ecn.site = "%s"' % site if site else ''}
    #     )
    #     return self.manipulate_db(sql, dtype='DataFrame')

    # def create_cert_info(self, site, category, cert_no, pid, ccl, supplier, model, spec, pn, uploader, create_time):
    #     sql = '''
    #     INSERT INTO `%(ecn)s`
    #     '''

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

    def update_cert_info(self, site, category, cert_no, pid, CCL, supplier, model, spec, PN, updater, update_time,
                         new_PN=None, new_supplier=None, new_model=None, new_spec=None):
        update = new_PN or new_model or new_supplier or new_spec
        if update:
            sql = '''
            UPDATE `%(ecn)s` as ecn, `%(ecn_ccl)s` as ccl, `%(ecn_model)s` as model
            SET %(update_pn)s %(update_supplier)s %(update_model)s %(update_spec)s %(update_uploader)s %(update_time)s
            WHERE %(conditions)s
            ''' % (
                {
                    # Tables
                    'ecn': self.db_tables['ECN'],
                    'ecn_ccl': self.db_tables['ECN_CCL'],
                    'ecn_model': self.db_tables['ECN_model'],

                    # Update item
                    'update_pn': ('ccl.PN=%s, model.PN=%s,' % new_PN) if new_PN else '',
                    'update_supplier': ('and model.supplier=%s,' % new_supplier) if new_supplier else '',
                    'update_model': ('and model.model=%s,' % new_model) if new_model else '',
                    'update_spec': ('and model.spec=%s,' % new_spec) if new_spec else '',
                    'update_uploader': 'and ecn.upload=%s,' % updater,
                    'update_time': 'and ecn.create_time=%s' % update_time,

                    # Conditions
                    'conditions': '''
                                ccl.PN=%(old_pn)s and ccl.CCL=%(ccl)s and
                                model.PN=%(old_pn)s and model.cert_no=%(cert_no)s and
                                model.supplier=%(old_supplier)s and model.spec=%(old_spec)s and
                                model.model=%(old_model)s and
                                ecn.cert_no=%(cert_no)s and ecn.site=%(site)s and
                                ecn.category=%(category)s and ecn.pid=%(pid)s
                                ''' % ({'site': site, 'category': category, 'cert_no': cert_no,
                                        'pid': pid, 'ccl': CCL,
                                        'old_pn': PN, 'old_supplier': supplier, 'old_model': model, 'old_spec': spec})
                }
            )

            result = self.manipulate_db(sql)

        else:
            result = False

        return result

    def check_duplicated(self, table, key, value):
        sql = '''
        SELECT EXISTS(SELECT * FROM `%(table)s` WHERE %(key)s = '%(value)s') AS count
        ''' % (
            {'table': table, 'key': key, 'value': value}
        )
        result = self.manipulate_db(sql, dtype='DataFrame').iloc[0][0]

        if result == 0:
            return False
        else:
            return True


class AgileMySQLIO(MySQL):
    def __init__(self, debug=False, db_tables={}, custom_login_info={}, **kwargs):
        super().__init__(debug=debug, db_tables=db_tables, login_info=AGILE_login_info, **kwargs)

    def read_agile_info(self, site=None):
        sql = '''
        SELECT ecn.no, ecn.pn, detail.manufacturer, detail.model FROM `%(ecn_table)s` as ecn
        INNER JOIN `%(pn_table)s` as detail
        WHERE ecn.pn = detail.pn
        %(site)s
        ''' % (
            {'ecn_table': self.db_tables['ECN'], 'pn_table': self.db_tables['PN'],
             'site': site if site else ''}
        )

        return self.manipulate_db(sql, dtype='DataFrame')
