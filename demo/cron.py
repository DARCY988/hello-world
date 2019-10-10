# define your CRON_JOBS list here, will be involved by django automatically.
# refer to below link to know how to set schedule.
# https://en.wikipedia.org/wiki/Cron#Format


from fii_ai_api.utils.utility import log, fii_cronlog_handler

CRON_JOBS = [
    # ('*/1 * * * *', 'demo.cron.my_cron_job_demo', '>> /srv/logs/demo_cron_job.log'),
]


# Define your corn jobs function here.
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
