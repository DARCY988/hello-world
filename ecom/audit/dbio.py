from django.db import models
from fii_ai_api.utils.dbio.mysql import MySQL
from ecom.config import MYSQL_login_info


class ECNMySQLIO(MySQL):
    def __init__(self, debug=False, db_tables={}, custom_login_info={}, **kwargs):
        super().__init__(debug=debug, db_tables=db_tables, login_info=MYSQL_login_info, **kwargs)

    def get_seq(self, table, **kwargs):
        sql = '''
        SELECT seq FROM `%(table)s` WHERE %(conditions)s
        ''' % (
            {'table': self.db_tables[table],
             'conditions': ' and '.join('%s="%s"' % (k, v) for (k, v) in kwargs.items())}
        )
        return self.manipulate_db(sql, dtype='DataFrame')

    def create_file(self, table, key, value, name, path, uploader, upload_time, f_type):  # Create info is included
        sql = '''
        INSERT INTO `%(table)s` (%(key)s, name, path, upload, upload_time, type)
        VALUES ('%(value)s', '%(name)s', '%(path)s', '%(uploader)s', '%(time)s', %(type)s)
        ''' % (
            {'table': self.db_tables[table], 'key': key, 'value': value,
             'name': name, 'path': path, 'uploader': uploader, 'time': upload_time, 'type': f_type}
        )
        return self.manipulate_db(sql)

    def create_report(self, site, category, r_class, audit_date,
                      audit_result, next_time, uploader, create_time):
        sql = '''
        INSERT INTO `%(table)s`
        (site, category, class, audit_date, audit_result, nextaudittime, upload, create_time)
        VALUES
        ('%(site)s', '%(category)s', '%(class)s', '%(audit_date)s', %(audit_result)s,
         '%(nextaudittime)s', '%(upload)s', '%(create_time)s')
        ''' % (
            {'table': self.db_tables['FAReport'], 'site': site, 'category': category, 'class': r_class,
             'audit_date': audit_date, 'audit_result': audit_result, 'nextaudittime': next_time,
             'upload': uploader, 'create_time': create_time}
        )
        return self.manipulate_db(sql)

    def create_check(self, site, category, audit_date, sample_category, sample_pid,
                     sample_applicant, sample_conform, uploader, create_time):
        sql = '''
        INSERT INTO `%(table)s`
        (site, category, audit_date, sample_category, sample_pid,
         sample_applicant, sample_conform, upload, create_time)
        VALUES
        ('%(site)s', '%(category)s', '%(audit_date)s', '%(sample_category)s', '%(sample_pid)s',
         '%(sample_applicant)s', %(sample_conform)s, '%(upload)s', '%(create_time)s')
        ''' % (
            {'table': self.db_tables['FACheck'], 'site': site, 'category': category,
             'audit_date': audit_date, 'sample_category': sample_category, 'sample_pid': sample_pid,
             'sample_applicant': sample_applicant, 'sample_conform': sample_conform, 'upload': uploader,
             'create_time': create_time}
        )
        return self.manipulate_db(sql)

    def read_info(self, site=None):
        sql = '''
        SELECT site, name, path, type, upload, upload_time
        FROM `%(table)s`
        %(condition)s
        ''' % (
            {'table': self.db_tables['FAInfo_upload'], 'condition': 'WHERE site="%s"' % site if site else ''}
        )
        return self.manipulate_db(sql, dtype='DataFrame')

    def read_report(self, site=None, category=None):
        sql = '''
        SELECT site, category, class, audit_date, audit_result, nextaudittime, upload, create_time, update_time
        FROM `%(table)s`
        %(condition)s
        ''' % (
            {
                'table': self.db_tables['FAReport'],
                'condition': 'WHERE %(site)s %(category)s' % ({
                    'site': 'site="%s"' % site if site else '',
                    'category': 'and category="%s"' % category if category else ''}) if (site or category) else ''
            }
        )
        return self.manipulate_db(sql, dtype='DataFrame')

    def read_check(self, site=None, category=None, sample_category=None, sample_pid=None):
        sql = '''
        SELECT site, category, audit_date, sample_category, sample_pid, sample_applicant, sample_conform,
        upload, create_time, update_time
        FROM `%(table)s`
        %(condition)s
        ''' % (
            {'table': self.db_tables['FACheck'],
             'condition': 'WHERE %(site)s %(category)s %(sample_category)s %(sample_pid)s' % (
                 {'site': 'site="%s"' % site if site else '',
                  'category': 'and category="%s"' % category if category else '',
                  'sample_category': 'and sample_category="%s"' % sample_category if sample_category else '',
                  'sample_pid': 'and sample_pid="%s"' % sample_pid if sample_pid else ''})
                if (site or category or sample_category or sample_pid) else ''}
        )
        return self.manipulate_db(sql, dtype='DataFrame')

    def update_report(self, site, category, new_class=None, new_date=None, new_result=None,
                      new_nexttime=None, uploader=None, update_time=None):
        sql = '''
        UPDATE `%(table)s`
        SET %(update_class)s %(update_date)s %(update_result)s %(update_nexttime)s %(update_uploader)s %(update_time)s
        WHERE site='%(site)s' and category='%(category)s'
        ''' % (
            {
                'table': self.db_tables['FAReport'], 'site': site, 'category': category,
                'update_class': 'class="%s",' % new_class if new_class else '',
                'update_date': 'audit_date="%s",' % new_date if new_date else '',
                'update_result': 'audit_result="%s",' % new_result if new_result else '',
                'update_nexttime': 'nextaudittime="%s",' % new_nexttime if new_nexttime else '',
                'update_uploader': 'upload="%s",' % uploader if uploader else '',
                'update_time': 'update_time="%s"' % update_time if update_time else '',
            }
        )
        return self.manipulate_db(sql)

    def update_check(self, site, category, sample_category, sample_pid, new_date=None,
                     new_applicant=None, new_conform=None, uploader=None, update_time=None):
        sql = '''
        UPDATE `%(table)s`
        SET %(update_date)s %(update_applicant)s %(update_conform)s %(update_uploader)s %(update_time)s
        WHERE site='%(site)s' and category='%(category)s' and sample_category='%(sample_category)s' and
        sample_pid='%(sample_pid)s'
        ''' % (
            {
                'table': self.db_tables['FACheck'],
                'site': site, 'category': category, 'sample_category': sample_category, 'sample_pid': sample_pid,
                'update_date': 'audit_date="%s",' % new_date if new_date else '',
                'update_applicant': 'sample_applicant="%s",' % new_applicant if new_applicant else '',
                'update_conform': 'sample_conform=%s,' % new_conform if new_conform else '',
                'update_uploader': 'upload="%s",' % uploader if uploader else '',
                'update_time': 'update_time="%s"' % update_time if update_time else '',
            }
        )
        return self.manipulate_db(sql)
