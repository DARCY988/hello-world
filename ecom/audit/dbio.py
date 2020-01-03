from django.db import models
from fii_ai_api.utils.dbio.mysql import MySQL
from ecom.config import MYSQL_login_info


class ECNMySQLIO(MySQL):
    def __init__(self, debug=False, db_tables={}, custom_login_info={}, **kwargs):
        super().__init__(debug=debug, db_tables=db_tables, login_info=MYSQL_login_info, **kwargs)

    def create_file(self, table, key, value, name, path, uploader, upload_time, f_type):
        sql = '''
        INSERT INTO `%(table)s` ('%(key)s', name, path, upload, upload_time, type)
        VALUES ('%(value)s', '%(name)s', '%(path)s', '%(uploader)s', '%(time)s', '%(type)s')
        ''' % (
            {'table': self.db_tables[table], 'key': key, 'value': value,
             'name': name, 'path': path, 'uploader': uploader, 'time': upload_time, 'type': f_type}
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

    def create_info(self, site, name, path, uploader, upload_time, f_type):
        sql = '''
        INSERT INTO `%(table)s`
        (site, name, path, upload, upload_time, type)
        VALUES
        ('%(site)s', '%(name)s', '%(path)s', '%(uploader)s', '%(time)s', '%(type)s')
        ''' % (
            {'table': self.db_tables['FAInfo'], 'site': site, 'name': name,
             'path': path, 'uploader': uploader, 'time': upload_time, 'type': f_type}
        )
        return self.manipulate_db(sql)

    def create_report(self, site, category, r_class, audit_date,
                      audit_result, next_time, uploader, create_time, update_time):
        sql = '''
        INSERT INTO `%(table)s`
        (site, category, class, audit_date, audit_result, nextaudittime, upload, create_time, update_time)
        VALUES
        ('%(site)s', '%(category)s', '%(class)s', '%(audit_date)s', '%(audit_result)s',
         '%(nextaudittime)s', '%(upload)s', '%(create_time)s', '%(update_time)s')
        ''' % (
            {'table': self.db_tables['FAReport'], 'site': site, 'category': category, 'class': r_class,
             'audit_date': audit_date, 'audit_result': audit_result, 'nextaudittime': next_time,
             'upload': uploader, 'create_time': create_time, 'update_time': update_time}
        )
        return self.manipulate_db(sql)

    def create_check(self, site, category, audit_date, sample_category, sample_pid,
                     sample_applicant, sample_conform, uploader, create_time, update_time):
        sql = '''
        INSERT INTO `%(table)s`
        (site, category, audit_date, sample_category, sample_pid,
         sample_applicant, sample_conform, upload, create_time, update_time)
        VALUES
        ('%(site)s', '%(category)s', '%(audit_date)s', '%(sample_category)s', '%(sample_pid)s',
         '%(sample_applicant)s', '%(sample_conform)s', %(upload)s', '%(create_time)s', '%(update_time)s')
        ''' % (
            {'table': self.db_tables['FACheck'], 'site': site, 'category': category,
             'audit_date': audit_date, 'sample_category': sample_category, 'sample_pid': sample_pid,
             'sample_applicant': sample_applicant, 'sample_conform': sample_conform, 'upload': uploader,
             'create_time': create_time, 'update_time': update_time}
        )
        return self.manipulate_db(sql)
