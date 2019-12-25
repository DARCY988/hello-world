from .dbio import DataCenterMySQLIO
import datetime
# Define your DataBase IO Module
db = DataCenterMySQLIO(debug=True)


def checking_expire(**kwargs):  # EX: column = site OR category

    time_now = datetime.datetime.now()
    result = []

    exp_time = db.get_all_column()

    for i in exp_time:
        diff_day = i[6] - time_now
        if diff_day.days >= 120:
            status = 0
        elif diff_day.days < 120:
            status = 1
        elif diff_day.days < 30:
            status = 2
        result.append({'site' : i[0],
                       'category' : i[1],
                       'certificate' : i[2],
                       'pid': i[3],
                       'applicant' : i[5],
                       'issue_date' : i[4],
                       'exp_date' : i[6],
                       'exp_date_status' : status
                       })
#  sorted(result, key=itemgetter(6))
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
