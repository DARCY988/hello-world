from django.db import models
from fii_ai_api.utils.dbio.mysql import MySQL
from fii_ai_api.utils.files import FileHandler
from ecom.config import MYSQL_login_info
import datetime
import os


class DataCenterMySQLIO(MySQL):
    def __init__(self, debug=False, db_tables={}, custom_login_info={}, **kwargs):
        super().__init__(debug=debug, db_tables=db_tables, login_info=MYSQL_login_info, **kwargs)

    def get_all_data(self, **kwargs):
        #  將kwargs 寫入變數
        try:
            select_site = ' WHERE ' + 'site' + ' = ' + '\'' + kwargs['select_site'] + '\''
        except Exception:
            select_site = ''
        try:
            select_category = ' WHERE ' + 'category' + ' = ' + '\'' + kwargs['select_category'] + '\''
        except Exception:
            select_category = ''

        if select_site and select_category :
            select_category = ' AND ' + 'category' + ' = ' + '\'' + kwargs['select_category'] + '\''

        get_column = 'site, category, cert_no, applicant, pid, issue_date, exp_date, status, upload, update_time'
        #  get_column 要顯示的欄位

        sql = '''
        SELECT %(get_column)s
        FROM %(DataCenter_table)s
        %(select_site)s %(select_category)s
        ''' % (
            {'DataCenter_table' : self.db_tables['DataCenter'], 'get_column' : get_column,
             'select_category' : select_category, 'select_site' : select_site
             }
        )

        return self.manipulate_db(sql, dtype='dict')

    def get_count(self, column, value, **kwargs):
        #  傳入必要參數column及可附加條件kwargs計算數量
        #  EX column = site ,  value = FOL
        #  EX column = category ,  value = CCC
        #  應該可以改寫迴圈
        try:
            status_value = ' AND ' + 'status' + ' = ' + '\'' + kwargs['status_value'] + '\''
        except Exception:
            status_value = ''
        try:
            select_site = ' AND ' + 'site' + ' = ' + '\'' + kwargs['select_site'] + '\''
        except Exception:
            select_site = ''
        try:
            select_category = ' AND ' + 'category' + ' = ' + '\'' + kwargs['select_category'] + '\''
        except Exception:
            select_category = ''
        #  改寫為迴圈
        sql = '''
        SELECT COUNT(%(column)s)
        FROM %(DataCenter_table)s
        WHERE  %(column)s = '%(value)s' %(status_value)s %(select_site)s %(select_category)s
        ''' % (
            {'DataCenter_table' : self.db_tables['DataCenter'], 'column' : column,
             'value' : value , 'status_value' : status_value, 'select_category' : select_category,
             'select_site' : select_site
             }
        )

        return self.manipulate_db(sql, dtype='list')

    def insert_dc_upload(self, **kwargs):                                # 考慮將路徑改為timestamp or UUID
        # 證書號碼，檔案名稱非唯一，數據庫key值為seq
        upload_time = datetime.datetime.now()                            # 取得上傳時間
        temp_path = '/' + str(datetime.datetime.timestamp(upload_time))  # 取得timestamp,當成唯一資料夾名稱
        #  temp_path = '/' + str(self.select_max_seq()[0][0] + 1)
        file_path = kwargs['path'] + '/dc' + temp_path                   # 檔案存放路徑 為.static/timestamp/檔案名稱
        sql_path = file_path + '/' + kwargs['name']                      # sql寫入的路徑字串

        sql = '''
        INSERT INTO DC_upload(cert_no, name, path, upload_time, upload, upload_type)
        VALUES ('%(cert_no)s', '%(name)s', '%(path)s', '%(upload_time)s', '%(upload)s', '%(upload_type)s')
        ''' % (
            {'DataCenter_table' : self.db_tables['DC_upload'], 'cert_no' : kwargs['cert_no'],
             'name' : kwargs['name'] , 'path' : sql_path, 'upload_time' : upload_time,
             'upload' : kwargs['upload'], 'upload_type' : kwargs['upload_type']
             }
        )
        result = self.manipulate_db(sql, dtype='list')                                   # 將檔案資訊寫入資料庫
        FileHandler.save(self=self, file=kwargs['file'], path=file_path)       # 存放檔案,考慮將結果寫入dc.log

        return result

    def select_cert_files(self, cert_no):

        sql = '''
        SELECT path, name
        FROM DC_upload
        WHERE cert_no = %(cert_no)s
        ''' % (
            {'DataCenter_table' : self.db_tables['DC_upload'], 'cert_no' : cert_no
             }
        )
        result = self.manipulate_db(sql, dtype='list')             # 讀取該證書有哪些檔案

        return result

    def delete_cert_files(self, path):

        sql = '''
        DELETE FROM %(dc_table)s
        WHERE path = '%(path)s'
        ''' % (
            {'dc_table' : self.db_tables['DC_upload'], 'path' : path
             }
        )
        result = self.manipulate_db(sql, dtype='list')          # 刪除數據庫資料
        temp_path = os.path.split(path)                         # 分割路徑與檔案名稱
        path = temp_path[0]                                     # 路徑
        filename = temp_path[1]                                 # 檔案名稱
        FileHandler.delete(self=self, path=path, file_name=filename)  # 刪除該路徑檔案

        return result

    def preview_files(self, path):

        temp_path = os.path.split(path)  # 分割成路徑與檔案名稱
        result = FileHandler.preview(self=self, path=temp_path[0], file_name=temp_path[1])

        return result

    def download_files(self, path):

        temp_path = os.path.split(path)  # 分割成路徑與檔案名稱
        result = FileHandler.download(self=self, path=temp_path[0], file_name=temp_path[1])

        return result

    def insert_datacenter(self, sql_dict):                                # 考慮將路徑改為timestamp or UUID
        create_time = datetime.datetime.now()                            # 取得上傳時間
        exp_date = datetime.datetime.strptime(str(sql_dict['exp_date']), '%Y-%m-%d %H:%M:%S') #格式化時間
        issue_date = datetime.datetime.strptime(str(sql_dict['issue_date']), '%Y-%m-%d %H:%M:%S') #格式化時間
        cert_no = str(sql_dict['cert_no']).replace(" ", "") #格式化證書號碼 刪除空白
        if sql_dict['status'] == 'Suspended':   # 將狀態改為int格式寫入數據庫
            status = 0
        else:
            status = 1

        sql = '''
        INSERT INTO %(DataCenter_table)s(site, category, cert_no, applicant, pid,
        issue_date, exp_date, status, upload, create_time)
        VALUES ('%(site)s', '%(category)s', '%(cert_no)s, '%(applicant)s', '%(pid)s',
        '%(issue_date)s', '%(exp_date)s', %(status)s, '%(upload)s', '%(create_time)s')
        ''' % (
            {'DataCenter_table' : self.db_tables['DataCenter'], 'site' : sql_dict['site'],
             'category' : sql_dict['category'], 'cert_no' : cert_no,
             'applicant' : sql_dict['applicant'], 'pid' : sql_dict['pid'], 'issue_date' : issue_date,
             'exp_date' : exp_date, 'status' : status, 'upload' : sql_dict['upload'],
             'create_time' : create_time
             }
        )
        result = self.manipulate_db(sql, dtype='list')                                  # 將檔案資訊寫入資料庫

        return result
