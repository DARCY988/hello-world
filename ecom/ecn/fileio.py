from django import forms
from datetime import datetime, timezone, timedelta
from pandas import DataFrame, read_excel
from django.http import StreamingHttpResponse
from rest_framework.response import Response
import os


class FileFormIO(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()

    def save_upload_file(self, file, path):

        if not os.path.exists(path):
            os.mkdir(path)

        try:
            with open(os.path.join(path, file.name), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()
            return 'Upload successfully.'

        except Exception:
            return Exception

    def read_upload_file(self, file, dbio, uploader):

        df = DataFrame(columns=['site', 'category', 'cert_no', 'pid', 'ccl', 'supplier',
                                'model', 'spec', 'pn', 'uploader', 'create_time'])

        # Read excel file
        pre_df = read_excel(file, index_col=0, header=0)
        excel_df = pre_df.fillna(method='ffill')
        pre_df.fillna('', inplace=True)

        for row in range(0, len(excel_df.index)):
            site = excel_df.iloc[row][0]
            category = excel_df.iloc[row][1]
            cert_no = excel_df.iloc[row][2].replace('\'', '')
            pid = excel_df.iloc[row][3].replace('\n', ' ')
            ccl = excel_df.iloc[row][4]
            supplier = excel_df.iloc[row][5]
            model = excel_df.iloc[row][6]
            spec = excel_df.iloc[row][7]
            pn = excel_df.iloc[row][8]
            model_comp = pre_df.iloc[row][9]
            pn_comp = pre_df.iloc[row][10]
            create_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
            df = df.append({'site': site, 'category': category, 'cert_no': cert_no, 'pid': pid,
                            'ccl': ccl, 'supplier': supplier, 'model': model, 'spec': spec,
                            'pn': pn, 'model_comp': model_comp, 'pn_comp': pn_comp,
                            'uploader': uploader, 'create_time': create_time}, ignore_index=True)

            # Avoid duplicated cert_no
            if dbio.check_duplicated(dbio.db_tables['ECN'], 'cert_no', cert_no):
                continue
            else:
                dbio.create_ECN(site, category, cert_no, pid, uploader, create_time)

            if dbio.check_duplicated(dbio.db_tables['ECN_CCL'], 'PN', pn):
                continue
            else:
                dbio.create_ccl(ccl, pn)

            # if dbio.check_duplicated('ECN_CCL_model1', 'model', model):
            #     continue
            # else:
            dbio.create_model(supplier, model, spec, pn, model_comp, pn_comp, cert_no)
        return df

    def download(self, path, file_name):

        target = os.path.join(path, file_name)
        if os.path.exists(target):
            def file_iterator(chunk_size=512):

                with open(target, 'rb') as file:
                    while True:
                        tmp = file.read(chunk_size)
                        if tmp:
                            yield tmp
                        else:
                            break

            result = StreamingHttpResponse(file_iterator())
            result['Content-Type'] = 'application/octet-stream'
            result['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        else:
            result = {
                'message': 'File \'%s\' is not found.' % (file_name)
            }
            result = Response(result)

        return result

    def preview(self, path, file_name):

        target = os.path.join(path, file_name)
        file_type = file_name.split('.')[1]
        type_dict = {
            'png': 'image/png',
            'jpg': 'image/jpg',
            'jpeg': 'image/jpeg',
            'pdf': 'application/pdf',
        }
        if os.path.exists(target):
            def file_iterator(chunk_size=512):

                with open(target, 'rb') as file:
                    while True:
                        tmp = file.read(chunk_size)
                        if tmp:
                            yield tmp
                        else:
                            break

            result = StreamingHttpResponse(file_iterator())
            result['Content-Type'] = type_dict[file_type]
            result['Content-Disposition'] = 'inline;filename="{0}"'.format(file_name)
        else:
            result = {
                'message': 'File \'%s\' is not found.' % (file_name)
            }
            result = Response(result)

        return result
