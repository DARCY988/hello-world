# from fii_ai_api.utils.response import fii_api_handler
from .dbio import DemoMySQLIO
import pandas as pd
import numpy as np
from .ai_models import current_grade,chose_managers,probation,options_output,sub_bg_option,bu_option
from .ai_models import leave_type,under_halfyear,options_output
from .ai_models import select_class_rank,select_GJRC,select_work_type,regular_leave_plus,chose_in_interval
from .ai_models import monthly_report,leave_type_report,grade_report,GJRC_report,SEX_report,InCompanyYear_report
from .ai_models import Bu_class_chart,Bu_grade_chart,Bu_hireyear_chart,SUB_BG_report,BU_report



from django.shortcuts import render
from django.http import JsonResponse
from demo.models import ToCsv2
from datetime import datetime,timedelta
from django.db import connection
from datetime import datetime

# -------------------- #
# AI Model Results API
# -------------------- #
# @fii_api_handler(['get'])
# def demo_ai_view(request, debug, api_version,  # these three parameters always place at index 0:2
#                  value):  # Add your parameters here
#     db = DemoMySQLIO(debug=debug, api_version=api_version)

#     result = demo_ai_model(db, value)

#     return result

# -------------------- #
# DataBase CRUD API
# -------------------- #
# @fii_api_handler(['get'])

def big_chart(request):  # Add your parameters here
    connection.cursor()
    # #連上資料庫後用下面這行
    # t = datetime.now()
    # df = pd.read_sql('SELECT * FROM to_csv2', con=con).fillna('NA')    
    # print(datetime.now()-t )
    # print(datetime.now()-t )
    df = pd.DataFrame(list(ToCsv2.objects.all().values()))
    # print(datetime.now()-t )
    
    extra_options =  request.GET['extra_options']# list
    df = regular_leave_plus(df,extra_options)

    s_date = datetime.strptime(request.GET['s_date'],'%Y/%m/%d')
    e_date = datetime.strptime(request.GET['e_date'],'%Y/%m/%d')

    s_y = s_date.year
    s_m = s_date.month
    s_d = s_date.day
    
    e_y = e_date.year
    e_m = e_date.month
    e_d = e_date.day
    

    chart_type = request.GET['chart_type']
    print(chart_type)
    if chart_type == '事業處 - 資位':
        # t = datetime.now()
        result = Bu_class_chart(df,
                                s_y = s_y,s_m = s_m, s_d = s_d,
                                e_y = e_y,e_m = e_m, e_d = e_d)
        # print(datetime.now()-t )  

        result = result.reset_index().to_dict(orient='dict')

    elif chart_type == '事業處 - 考績':
        # t = datetime.now()
        result = Bu_grade_chart(df,
                                s_y = s_y,s_m = s_m, s_d = s_d,
                                e_y = e_y,e_m = e_m, e_d = e_d) 
        # print(datetime.now()-t )
        result = result.reset_index().to_dict(orient='dict')

    elif chart_type == '事業處 - 離職類別':
        s = str(df.shape)
        result = {'1':s}

    elif chart_type == '事業處 - 年資':
        t = datetime.now()
        result = Bu_hireyear_chart(df,
                                s_y = s_y,s_m = s_m, s_d = s_d,
                                e_y = e_y,e_m = e_m, e_d = e_d) 
        print(datetime.now()-t )
        result = result.reset_index().to_dict(orient='dict')

    elif chart_type == '考績 - 資位':
        # t = datetime.now()
        result = current_grade(df,
                                s_y = s_y,s_m = s_m, s_d = s_d,
                                e_y = e_y,e_m = e_m, e_d = e_d) 
        # print(datetime.now()-t )
        result = result.reset_index().to_dict(orient='dict')
        # return JsonResponse(result,safe=False)
    elif chart_type == '離職類別 - 資位':
        # t = datetime.now()
        result = leave_type(df,
                            s_y = s_y,s_m = s_m, s_d = s_d,
                            e_y = e_y,e_m = e_m, e_d = e_d) 
        # print(datetime.now()-t )
        result = result.reset_index().to_dict(orient='dict')
    elif chart_type == '年資 - 資位':
        # t = datetime.now()
        result = under_halfyear(df,
                                s_y = s_y,s_m = s_m, s_d = s_d,
                                e_y = e_y,e_m = e_m, e_d = e_d) 
        # print(datetime.now()-t )
        result = result.reset_index().to_dict(orient='dict')
    else:
        return JsonResponse({'data':'12312'})
    
    return JsonResponse(result)
    

def small_chart(request):
    # PATH = 'D:\\ALL\\HR\\data\\HRDATA'
    # df = pd.read_csv(PATH + '\\_V14.csv',engine = 'python',encoding = 'big5hkscs')
    connection.cursor()
    # 連上資料庫後用下面這行
    df = pd.DataFrame(list(ToCsv2.objects.all().values()))

    s_date = datetime.strptime(request.GET['s_date'],'%Y/%m/%d')
    e_date = datetime.strptime(request.GET['e_date'],'%Y/%m/%d')

    s_y = s_date.year
    s_m = s_date.month
    s_d = s_date.day
    
    e_y = e_date.year
    e_m = e_date.month
    e_d = e_date.day
    # certain
    work_year = request.GET['work_year'] # 年資

    # 選擇人員 選擇是否包含試用期
    emp_option = request.GET['emp_option']
    if emp_option:
        df = probation(df, emp_option=emp_option,  e_date=  e_date)
    
    #選擇資位 #原/師/預原
    class_ = request.GET['class_'] # 資位
    df = select_class_rank(df,select = class_)

    # 選擇職系
    work_type = request.GET['work_type'] # 職系
    df = select_work_type(df , select = work_type)

    # 處理入職時間段
    IN_s_date = request.GET['IN_s_date']# 入集團時間
    IN_e_date = request.GET['IN_e_date']# 入集團時間
    if IN_s_date:
        df = df[df.IN_CONPANY_DATE.apply(lambda x :chose_in_interval(x,IN_s_date,IN_e_date))]
    
    ## 管理職uncertain 
    
    m_option = request.GET['m_option']
    if m_option:
        df = chose_managers(df, m_option = m_option)
    
    # no god damn data 
    # 事業次群
    # 事業處
    
    sub_bg = request.GET['sub_bg']
    _bu = request.GET['_bu']

    if sub_bg:
        df = sub_bg_option(df,sub_bg)
    if _bu:
        df = bu_option(df,_bu) 
    
    # 選擇圖表類型
    chart_type_1 = request.GET['chart_type_1']
    
    if chart_type_1 == '月份':
        df = regular_leave_plus(df,extra_options = [])
        result = monthly_report(df,
                                s_y = s_y,s_m = s_m, s_d = s_d,
                                e_y = e_y,e_m = e_m, e_d = e_d) 
        result = result.reset_index().to_dict(orient='dict')
    elif chart_type_1 == '性別':
        df = regular_leave_plus(df,extra_options = [])
        result = SEX_report(df,year = work_year,
                                s_y = s_y,s_m = s_m, s_d = s_d,
                                e_y = e_y,e_m = e_m, e_d = e_d) 
    
        result = result.reset_index().to_dict(orient='dict')
    elif chart_type_1 == '年資':
        df = regular_leave_plus(df,extra_options = [])
        result =  InCompanyYear_report(df,
                                s_y = s_y,s_m = s_m, s_d = s_d,
                                e_y = e_y,e_m = e_m, e_d = e_d) 
        result = result.reset_index().to_dict(orient='dict')
    elif chart_type_1 == '考績':
        df = regular_leave_plus(df,extra_options = [])
        result = grade_report(df,year = work_year,
                                s_y = s_y,s_m = s_m, s_d = s_d,
                                e_y = e_y,e_m = e_m, e_d = e_d) 
        result = result.reset_index().to_dict(orient='dict')

    elif chart_type_1 == '事業次群':
        df = regular_leave_plus(df,extra_options = [])
        result = SUB_BG_report(df,year = work_year,
                                s_y = s_y,s_m = s_m, s_d = s_d,
                                e_y = e_y,e_m = e_m, e_d = e_d) 
        result = result.reset_index().to_dict(orient='dict')

    elif chart_type_1 == '事業處':
        df = regular_leave_plus(df,extra_options = [])
        result = BU_report(df,year = work_year,
                                s_y = s_y,s_m = s_m, s_d = s_d,
                                e_y = e_y,e_m = e_m, e_d = e_d) 
        result = result.reset_index().to_dict(orient='dict')    

    elif chart_type_1 == '離職原因':
        result =leave_type_report(df,year = work_year,
                                s_y = s_y,s_m = s_m, s_d = s_d,
                                e_y = e_y,e_m = e_m, e_d = e_d) 
        result = result.reset_index().to_dict(orient='dict')

    
    sub_bg_bu_option = options_output(df)

        
    return JsonResponse({'bu_bg':sub_bg_bu_option ,'table' :result})

    # 線在資料庫沒有
  






