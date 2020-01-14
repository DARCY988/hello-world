from ecom.pvt.dbio import PVTMySQLIO
import datetime
from ecom.config import __CATEGORIES__, __LOCATIONS__
# Define your DataBase IO Module
db = PVTMySQLIO(debug=True)


def checking_expire(**kwargs):  # EX: category = ccc or site = FOC

    time_now = datetime.datetime.now()   # 取得現在時間
    result = []
    data = db.get_all_data(**kwargs)     # 取得數據庫所有資料
    for row in data:                     # 取出每一筆證書
        diff_day = row['nexttime'] - time_now  # 到期時間減去現在時間
        if diff_day.days >= 120:               # >120天為正常 狀態0
            status = 0
        if diff_day.days < 120:              # <120 要預警 呈現橘色 狀態1
            status = 1
        if diff_day.days < 30:               # <30 每天預警 呈現紅色 狀態2
            status = 2
        # 將取出的資料與日期比對結果寫入result，不同分頁回傳不同欄位
        # status取出是bytes, 要轉ord
        if kwargs['page'] == 'goods':
            result.append({'Site' : row['site'],
                           'Category' : row['category'],
                           'Certificate' : row['cert_no'],
                           'Pid': row['pid'],
                           'PVT type' : row['type'],
                           'PVT_date' : row['pvt_date'],
                           'Report_no' : row['report_no'],
                           'Test_result' : ord(row['test_result']),
                           'Next time for PVT' : row['nexttime'],
                           'Upload' : row['upload'],
                           'Create_time' : row['create_time'],
                           'Update_time' : row['update_time'],
                           'Exp_date_status' : status
                           })
        else:
            result.append({'Site' : row['site'],
                           'Category' : row['category'],
                           'Compname' : row['compname'],
                           'Manufacturer': row['manufacturer'],
                           'Model' : row['model'],
                           'P/N' : row['pn'],
                           'PVT_date' : row['pvtdate'],
                           'Report_NO' : row['report_no'],
                           'Test_result' : ord(row['test_result']),
                           'Next time for PVT' : row['nexttime'],
                           'Upload' : row['upload'],
                           'Create_time' : row['create_time'],
                           'Update_time' : row['upload_time'],
                           'Exp_date_status' : status
                           })

    return result


def checking_status_by_category(column, **kwargs):
    #  EX: column = category , EX: column = site , kwargs {category:CCC, site:FOC}
    result = {}
    category_list = __CATEGORIES__

    for category_value in category_list:
        status = 1  # 預設Goods Test Result為1:有效
        category_count = db.get_count('category', category_value, **kwargs)  # 取得證書數量
        count = category_count[0][0]  # 回傳值是list 指定[0][0]取出數字
        fail_status_count = db.get_count('category', category_value, status_value='0', **kwargs)
        # 0 = fail , 1 = pass, category_value = 要搜尋的catgory 用迴圈一次搜一個
        if fail_status_count[0][0] != 0 :  # fail_status_count數量大於一 代表有fail的證書 要回傳status 0給前臺
            status = 0
        result.update({category_value : {'status' : status, 'value' : count}})

    return result


def checking_status_by_site(column, **kwargs):  # EX: column = site , kwargs {category:CCC, site:FOC}
    result = []
    coord = __LOCATIONS__

    for site_value in coord.keys():
        status = 1  # 預設證書狀態為1:有效
        site_count = db.get_count(column, site_value, **kwargs)  # 取得證書數量
        count = site_count[0][0]  # 回傳值是list 指定[0][0]取出數字
        fail_status_count = db.get_count(column, site_value, status_value='0', **kwargs)
        #  指定搜索的column 傳入指定的value  0 = fail , 1 = pass , site value = 用迴圈一次搜一個site
        if fail_status_count[0][0] != 0 :  # if fail_status_count數量大於零 代表有失效的證書 要回傳status 0給前臺
            status = 0
        result.append({'name' : site_value , 'coord' : coord[site_value], 'status' : status, 'value' : count})
        #  將結果寫入
    return result


def alarm_list(**kwargs):  # EX: category = ccc or site = FOC
    time_now = datetime.datetime.now()   # 取得現在時間
    result = []
    data = db.get_all_data(**kwargs)     # 取得數據庫所有資料
    for row in data:                     # 取出每一筆證書
        diff_day = row['nexttime'] - time_now  # 到期時間減去現在時間
        if diff_day.days >= 90:               # >90天為正常 狀態0
            status = 0
        if diff_day.days < 90:              # <90 要預警 呈現橘色 狀態1
            status = 1
        if diff_day.days < 30:               # <30 每天預警 呈現紅色 狀態2
            status = 2
        # 將取出的資料與日期比對結果寫入result，不同分頁回傳不同欄位
        # status取出是bytes, 要轉ord
        if status != 0:  # 只回傳狀態有問題的項目
            if kwargs['page'] == 'goods':
                result.append({'Site' : row['site'],
                               'Category' : row['category'],
                               'Certificate' : row['cert_no'],
                               'Pid': row['pid'],
                               'PVT type' : row['type'],
                               'PVT_date' : row['pvt_date'],
                               'Report_no' : row['report_no'],
                               'Test_result' : ord(row['test_result']),
                               'Next time for PVT' : row['nexttime'],
                               'Upload' : row['upload'],
                               'Create_time' : row['create_time'],
                               'Update_time' : row['update_time'],
                               'Exp_date_status' : status
                               })
            else:
                result.append({'Site' : row['site'],
                               'Category' : row['category'],
                               'Compname' : row['compname'],
                               'Manufacturer': row['manufacturer'],
                               'Model' : row['model'],
                               'P/N' : row['pn'],
                               'PVT_date' : row['pvtdate'],
                               'Report_NO' : row['report_no'],
                               'Test_result' : ord(row['test_result']),
                               'Next time for PVT' : row['nexttime'],
                               'Upload' : row['upload'],
                               'Create_time' : row['create_time'],
                               'Update_time' : row['upload_time'],
                               'Exp_date_status' : status
                               })

    return result
