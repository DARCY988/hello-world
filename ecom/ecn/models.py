from pandas import DataFrame
from datetime import datetime, timezone, timedelta


# Cert Tab
def count_by_category(dbio, site):
    categories = [
        'CCC',
        'CSA',
        'ETL',
        'IECEx',
        'MET',
        'Nemko',
        'TUV',
        'UL',
    ]

    data = dbio.cert_amount('category', 'site' if site else None, site)

    # TODO: Check Agile system and get the status

    result = {}
    for row in range(0, len(data.index)):
        category = data.iloc[row]['category']

        result[category] = {'value': data.iloc[row]['amount'], 'status': 'Not Ready.'}

        # Remove none-zero category from list
        if category in categories:
            categories.remove(category)

    for empty in categories:
        result[empty] = {'value': 0, 'status': 'Not Ready.'}

    return result


def count_by_site(dbio, category):
    locations = {
        "FCZ": [15.2120232, 49.9493036],
        "FOC": [115.0491412, 27.7198832],
        "FOL": [113.899891, 18.6764474],
        "FTX": [-94.0602476, 44.8204983],
        "FJZ": [-106.543702, 31.6859596],
    }

    data = dbio.cert_amount('site', 'category' if category else None, category)

    # TODO: Check Agile system and get the status

    result = []
    for row in range(0, len(data.index)):
        site = data.iloc[row]['site']

        result.append(
            {
                'name': data.iloc[row]['site'],
                'coord': locations[site],
                'value': data.iloc[row]['amount'],
                'status': 'Not Ready.'
            }
        )

        # Remove none-zero site from dictionary
        if site in locations:
            del locations[site]

    for empty in locations:
        result.append(
            {
                'name': empty,
                'coord': locations[empty],
                'value': 0,
                'status': 'Not Ready.'
            }
        )

    return result


def list_all_cert(dbio, category, site):
    data = dbio.ecn_info(category, site)

    # TODO: Check Agile system and get the status

    result = []
    for row in range(0, len(data.index)):
        result.append(
            {
                'Site': data.iloc[row]['site'],
                'Category': data.iloc[row]['category'],
                'Certificate No.': data.iloc[row]['cert_no'],
                'Product PID': data.iloc[row]['pid'],
                'CCL': data.iloc[row]['CCL'],
                'CCL Supplier': data.iloc[row]['supplier'],
                'CCL Model': data.iloc[row]['model'],
                'CCL Spec.': data.iloc[row]['spec'],
                'CCL PN': data.iloc[row]['PN'],
                # 'CCL Model compare': data.iloc[row]['model_compare'],
                # 'CCL PN compare': data.iloc[row]['PN_compare'],
            }
        )

    return result


# Agile Tab
def list_all_ecn(agile_dbio, ecn_dbio, site):
    agile_df = agile_dbio.agile_info(site)
    cert_df = ecn_dbio.ecn_info(site)

    result = []
    for agile_row in range(0, len(agile_df.index)):
        ecn_no = agile_df.iloc[agile_row]['no']
        model = agile_df.iloc[agile_row]['model']
        pn = agile_df.iloc[agile_row]['pn']
        manufacturer = agile_df.iloc[agile_row]['manufacturer']

        # Mapping two tables by PN
        filtered_cert_df = cert_df[cert_df['PN'][:-3] == pn[:-3]]

        for cert_row in range(0, len(filtered_cert_df.index)):
            filtered_site = site if site else filtered_cert_df.iloc[cert_row]['site']
            cert_no = ', '.join(filtered_cert_df['cert_no'].to_list())
            pid = ', '.join(filtered_cert_df['pid'].to_list())
            component = filtered_cert_df.iloc[cert_row]['CCL']
            spec = filtered_cert_df.iloc[cert_row]['spec']
            categories = ', '.join(filtered_cert_df['category'].to_list())

            result.append(
                {
                    'Site': filtered_site,
                    'ECN No.': ecn_no,
                    'Certificate No.': cert_no,
                    'PID': pid,
                    'Component Name': component,
                    'Model': model,
                    'Component PN': pn,
                    'Manufacturer': manufacturer,
                    'Specification': spec,
                    'Category': categories,
                    'Affecting Cert(Y/N)': 'N',
                    'Owner': 'Nancy Kuang/Cindy',
                    'Status': 'To be Comfirmed',
                }
            )

    return result


# Utils
def alarm(mail_service, subject, text_content, attachments=None):
    alarm_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    notify_list = [
        'BonJu <bonju.huang@gmail.com>',
    ]
    cc_list = [
        'IAI Alarm Center <iai_reply@163.com>',
    ]
    mail_service.send_alarm(
        subject=subject,
        message=alarm_time + ' ' + text_content,
        recipient_list=notify_list,
        cc=cc_list,
        attachments=attachments
    )
    # send_mail(
    #     subject='ECN Alarm',
    #     text_content='This is a mail sent from IAI Innovation Application Department.',
    #     html_content='<p>This is an <strong>IMPORTANT</strong> notification.</p>',
    #     send_to=notify_list,
    #     cc=cc_list,
    #     headers=headers
    # )

    return 'Alarm Complete.'
