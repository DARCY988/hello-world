from .dbio import DataCenterMySQLIO
import datetime
# Define your DataBase IO Module
db = DataCenterMySQLIO(debug=True)


def checking_expire(**kwargs):  # EX: category = ccc or site = FOC

    time_now = datetime.datetime.now()   # 取得現在時間
    result = []
    data = db.get_all_data(**kwargs)     # 取得數據庫所有資料
    for row in data:                     # 取出每一筆證書
        diff_day = row['exp_date'] - time_now  # 到期時間減去現在時間
        if diff_day.days >= 120:               # >120天為正常 狀態0
            status = 0
        elif diff_day.days < 120:              # <120 要預警 呈現橘色 狀態1
            status = 1
        elif diff_day.days < 30:               # <30 每天預警 呈現紅色 狀態2
            status = 2

        # 將取出的資料與日期比對結果寫入result
        # status取出是bytes, 要轉ord
        result.append({'site' : row['site'],
                       'category' : row['category'],
                       'certificate' : row['cert_no'],
                       'pid': row['pid'],
                       'applicant' : row['applicant'],
                       'issue_date' : row['issue_date'],
                       'exp_date' : row['exp_date'],
                       'status' : ord(row['status']),
                       'upload' : row['upload'],
                       'Date' : row['Date'],
                       'exp_date_status' : status
                       })
    return result


def checking_status_by_category(column, **kwargs):
    #  EX: column = category , EX: column = site , kwargs {category:CCC, site:FOC}
    result = {}
    category_list = ['CCC', 'ETL', 'ETC', 'XXX']

    for category_value in category_list:
        status = 1  # 預設證書狀態為1:有效
        category_count = db.get_count('category', category_value, **kwargs)  # 取得證書數量
        count = category_count[0][0]  # 回傳值是list 指定[0][0]取出數字
        suspended_status_count = db.get_count('category', category_value, status_value='0', **kwargs)
        # 0 = suspended , 1 = pass or valid , select_site = 固定此site
        if suspended_status_count[0][0] != 0 :  # suspended_status_count數量大於一 代表有失效的證書 要回傳status 0給前臺
            status = 0
        result.update({category_value : {'status' : status, 'value' : count}})

    return result


def checking_status_by_site(column, **kwargs):  # EX: column = site , kwargs {category:CCC, site:FOC}

    result = []
    site_list = ['FCZ', 'FTX', 'FJZ', 'FOC', 'FOL']
    coord = {
        "FCZ": [49.9493036, 15.2120232],
        "FTX": [44.8204983, -94.0602476],
        "FJZ": [31.6859596, -106.543702],
        "FOC": [22.7198832, 114.0491412],
        "FOL": [22.6764474, 113.899891]}

    for site_value in site_list:
        status = 1  # 預設證書狀態為1:有效
        site_count = db.get_count(column, site_value, **kwargs)  # 取得證書數量
        count = site_count[0][0]  # 回傳值是list 指定[0][0]取出數字
        suspended_status_count = db.get_count(column, site_value, status_value='0', **kwargs)
        #  指定搜索的column 傳入指定的value  0 = suspended , 1 = pass or valid , select_site = 固定此site
        if suspended_status_count[0][0] != 0 :  # if suspended_status_count數量大於零 代表有失效的證書 要回傳status 0給前臺
            status = 0
        result.append({'name' : site_value , 'coord' : coord[site_value], 'status' : status, 'value' : count})
        #  將結果寫入
    return result
