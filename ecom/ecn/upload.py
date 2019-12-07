from django import forms
from datetime import datetime
from fii_ai_api.settings import BASE_DIR
from pandas import DataFrame, read_excel


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()

    def save_upload_file(self, file, filename):

        import os
        path = os.path.join(BASE_DIR, 'ecom/ecn/doc')
        try:
            with open(os.path.join(path, filename), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()
            return 'Upload successfully.'

        except Exception:
            return Exception

    def read_upload_file(self, file, dbio, uploader):

        df = DataFrame(columns=['site', 'category', 'cert_no', 'pid', 'uploader', 'create_time'])

        excel_df = read_excel(file, index_col=0, header=0).fillna(method='ffill')

        for row in range(0, len(excel_df.index)):
            site = excel_df.iloc[row][0]
            category = excel_df.iloc[row][1]
            cert_no = excel_df.iloc[row][2].replace('\'', '')
            pid = excel_df.iloc[row][3].replace('\n', ' ')
            create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df = df.append({'site': site, 'category': category, 'cert_no': cert_no,
                                    'pid': pid, 'uploader': uploader, 'create_time': create_time}, ignore_index=True)
            if row > 0 and cert_no == excel_df.iloc[row - 1][2].replace('\'', ''):
                continue
            else:
                dbio.create_ECN(site, category, cert_no, pid, uploader, create_time)
        return df
