# define your CRON_JOBS list here, will be involved by django automatically.
# refer to below link to know how to set schedule.
# https://en.wikipedia.org/wiki/Cron#Format


from fii_ai_api.utils.utility import log, fii_cronlog_handler
from fii_ai_api.utils.files import FileHandler
import ecom.pvt.models
import ecom.datacenter.models
from fii_ai_api.utils.mail import BasicMail
import os
from django.conf import settings

path = '>> ' + os.path.join(settings.BASE_DIR, '.logs', 'ecom.log')
CRON_JOBS = [
    #  ('* 9 * * *', 'ecom.cron.dc_alarm', path),
    #  ('* 9 * * *', 'ecom.cron.pvt_alarm', path),
]


@fii_cronlog_handler
def my_cron_job_demo():
    """
    Cron Jobs are used for scheduling tasks to run on the server.

    Return
    --------------
    results: any type but `None`
        if return `None`, `fii_cronlog_handler` will show error message in log file
        (ex. |YYYY-MM-DD hh:mm:ss|[CRON Fail]`my_cron_job_demo`),
        if return as another data type, `fii_cronlog_handler` will show sucess message
        (ex. |YYYY-MM-DD hh:mm:ss|[CRON Sucess]`my_cron_job_demo` (0.001s))

    NOTE: If you want to show more information in log for debug, you can use `log`
          function instead of built-in `print` to record your custom messages.

    Custom log message example.
    ```
        from fii_ai_api.utils.utility import fii_cronlog_handler, log
        @fii_cron_handler
        def my_cron_job_demo():
            # Do your magic...
            log('Show custom log message')
            return 'Hello cron job demo.'
    ```
    """
    results = "Algorithm results"
    log('Use `log` in cron job as built-in `print` to record your custom messages.')
    return results


@fii_cronlog_handler
def dc_alarm():

    dc_alarm_msg = str(ecom.datacenter.models.alarm_list())  # 取得dc需要警示的資料
    dc_alarm_mail = BasicMail()                                    # 實例化mail物件
    result = dc_alarm_mail.send_fii_mail('dc_alarm', dc_alarm_msg, 'IAI', ['leo.mm.li@mail.foxconn.com'])
    #  寄發mail
    print(dc_alarm_msg)  # 將取得pvt goods警示資料結果記錄在log
    print(result)              # 將寄發mail結果記錄在log

    return 'dc mail alarm function'


@fii_cronlog_handler
def pvt_alarm():

    pvtgoods_alarm_msg = str(ecom.pvt.models.alarm_list(page='goods'))  # 取得PVT需要警示的資料
    pvtcomp_alarm_msg = str(ecom.pvt.models.alarm_list(page='comp'))    # 取得PVT需要警示的資料
    pvt_alarm_mail = BasicMail()                                    # 實例化mail物件
    result = pvt_alarm_mail.send_fii_mail('pvt_alarm', pvtcomp_alarm_msg, 'IAI', ['leo.mm.li@mail.foxconn.com'])
    #  寄發mail
    print(pvtgoods_alarm_msg)  # 將取得pvt goods警示資料結果記錄在log
    print(pvtcomp_alarm_msg)   # 將取得pvt comp警示資料結果記錄在log
    print(result)              # 將寄發mail結果記錄在log

    return 'PVT mail alarm function'
