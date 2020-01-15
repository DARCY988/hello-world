from django.db import models
from fii_ai_api.utils.dbio.mysql import MySQL
from fii_ai_api.utils.files import FileHandler
from ecom.config import MYSQL_login_info
import datetime
import os


class PVTMySQLIO(MySQL):
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
        # PVT下有兩個分頁 需連到不同資料庫與取得不同欄位
        if kwargs['page'] == 'goods':  # goods分頁 需連到不同資料庫與取得不同欄位

            table = 'PVTGoods'
            get_column = '''
            site, category, cert_no, pid, type, pvt_date, report_no,
            test_result, nexttime, upload, create_time, update_time
            '''
        else:                           # comps分頁 需連到不同資料庫與取得不同欄位
            table = 'PVTComp'
            get_column = '''
            site, category, compname, manufacturer, model, pn, report_no, pvtdate,
            test_result, nexttime, upload, create_time, upload_time
            '''

        sql = '''
        SELECT %(get_column)s
        FROM %(PVT_table)s
        %(select_site)s %(select_category)s
        ''' % (
            {'PVT_table' : self.db_tables[table], 'get_column' : get_column,
             'select_category' : select_category, 'select_site' : select_site
             }
        )

        return self.manipulate_db(sql, dtype='dict')

    def get_count(self, column, value, **kwargs):
        #  傳入必要參數column及可附加條件kwargs計算數量
        #  EX column = site ,  value = FOL
        #  EX column = category ,  value = CCC
        #  應該可以改寫為迴圈
        if kwargs['page'] == 'goods':
            table = 'PVTGoods'
        else:
            table = 'PVTComp'

        try:
            status_value = ' AND ' + 'test_result' + ' = ' + '\'' + kwargs['status_value'] + '\''
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
        FROM %(PVT_table)s
        WHERE  %(column)s = '%(value)s' %(status_value)s %(select_site)s %(select_category)s
        ''' % (
            {'PVT_table' : self.db_tables[table], 'column' : column,
             'value' : value , 'status_value' : status_value, 'select_category' : select_category,
             'select_site' : select_site
             }
        )

        return self.manipulate_db(sql, dtype='list')

    def pvt_upload(self, **kwargs):                                # 存放goods or comps報告
        # 數據庫key值為seq
        if kwargs['page'] == 'goods':
            table = 'PVTGoods_upload'
            seq_column = 'pvtgoods_seq'
        else:
            table = 'PVTComp_upload'
            seq_column = 'pvtcomp_seq'

        upload_time = datetime.datetime.now()                            # 取得上傳時間
        temp_path = '/' + str(datetime.datetime.timestamp(upload_time))  # 取得timestamp,當成唯一資料夾名稱
        file_path = kwargs['path'] + '/pvt/' + kwargs['page'] + '/' + temp_path
        # 檔案存放路徑 為.static/pvt/goods/timestamp/檔案名稱
        sql_path = file_path + '/' + kwargs['name']                      # sql寫入的路徑字串
        # seq_column = pvtgoods_seq or pvtcomp_seq
        # seq = int
        sql = '''
        INSERT INTO %(PVT_table)s(%(seq_column)s, name, path, upload_time, upload)
        VALUES ('%(seq)s', '%(name)s', '%(path)s', '%(upload_time)s', '%(upload)s')
        ''' % (
            {'PVT_table' : self.db_tables[table], 'seq_column' : seq_column,
             'seq' : kwargs['seq'],
             'name' : kwargs['name'] , 'path' : sql_path, 'upload_time' : upload_time,
             'upload' : kwargs['upload']
             }
        )
        result = self.manipulate_db(sql, dtype='list')                                   # 將檔案資訊寫入資料庫
        FileHandler.save(self=self, file=kwargs['file'], path=file_path)       # 存放檔案,考慮將結果寫入pvt.log

        return result

    # def select_cert_files(self, cert_no):

    #     sql = '''
    #     SELECT path, name
    #     FROM DC_upload
    #     WHERE cert_no = %(cert_no)s
    #     ''' % (
    #         {'DataCenter_table' : self.db_tables['DC_upload'], 'cert_no' : cert_no
    #          }
    #     )
    #     result = self.manipulate_db(sql, dtype='list')             # 讀取該證書有哪些檔案

    #     return result

    def delete_files(self, path, page):
        if page == 'goods':
            table = 'PVTGoods_upload'
        else:
            table = 'PVTComp_upload'

        sql = '''
        DELETE FROM %(pvt_table)s
        WHERE path = '%(path)s'
        ''' % (
            {'pvt_table' : self.db_tables[table], 'path' : path
             }
        )
        result = self.manipulate_db(sql, dtype='list')          # 刪除數據庫資料
        temp_path = os.path.split(path)                         # 分割路徑與檔案名稱
        path = temp_path[0]                                     # 取得路徑
        filename = temp_path[1]                                 # 取得檔案名稱
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

    # def insert_pvt_goods(self, sql_dict):                                #upload excel file into db
    #     upload_time = datetime.datetime.now()                                                       # 取得上傳時間
    #     exp_date = datetime.datetime.strptime(str(sql_dict['exp_date']), '%Y-%m-%d %H:%M:%S')       # 格式化時間
    #     issue_date = datetime.datetime.strptime(str(sql_dict['issue_date']), '%Y-%m-%d %H:%M:%S')   # 格式化時間
    #     cert_no = str(sql_dict['cert_no']).replace(" ", "")                                     # 格式化證書號碼 刪除空白
    #     if sql_dict['status'] == 'fail':                                               # 將狀態改為int格式寫入數據庫
    #         status = 0
    #     else:
    #         status = 1

    #     sql = '''
    #     INSERT INTO %(DataCenter_table)s(site, category, cert_no, pid, type
    #     pvt_date, report_no, test_result, nexttime, upload, create_time, update_time)
    #     VALUES ('%(site)s', '%(category)s', '%(cert_no)s, '%(pid)s', '%(type)s',
    #     '%(pvt_date)s', '%(report_no)s', %(test_result)s,'%(nexttime)s') '%(upload)s', '%(create_time)s'
    #     '%(update_time)s')
    #     ''' % (
    #         {'pvt_table' : self.db_tables['PVTGoods'], 'site' : sql_dict['site'],
    #          'category' : sql_dict['category'], 'cert_no' : cert_no,
    #          'pid' : sql_dict['pid'], 'type' : sql_dict['type'], 'pvt_date' : pvt_date,
    #          'report_no' : report_no, 'test_result' : test_result, 'nexttime' : sql_dict['nexttime'],
    #          'upload' : upload, 'create_time' : create_time, 'update_time' : update_time
    #          }
    #     )
    #     result = self.manipulate_db(sql, dtype='list')                                  # 將檔案資訊寫入資料庫

    #     return result
