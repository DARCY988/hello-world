from django import forms
from datetime import datetime, timezone
from fii_ai_api.settings import BASE_DIR
from pandas import DataFrame, read_excel
import os


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()

    def save_upload_file(self, file, filename):

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

        df = DataFrame(columns=['site', 'category', 'cert_no', 'pid', 'ccl', 'supplier',
                                'model', 'spec', 'pn', 'uploader', 'create_time'])

        excel_df = read_excel(file, index_col=0, header=0).fillna(method='ffill')

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
            model_comp = excel_df.iloc[row][9]
            pn_comp = excel_df.iloc[row][10]
            create_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            df = df.append({'site': site, 'category': category, 'cert_no': cert_no, 'pid': pid,
                            'ccl': ccl, 'supplier': supplier, 'model': model, 'spec': spec,
                            'pn': pn, 'model_comp': model_comp, 'pn_comp': pn_comp,
                            'uploader': uploader, 'create_time': create_time}, ignore_index=True)

            # Avoid duplicated cert_no
            if dbio.check_duplicated('ECN_copy1', 'cert_no', cert_no):
                continue
            else:
                dbio.create_ECN(site, category, cert_no, pid, uploader, create_time)

            if dbio.check_duplicated('ECN_CCL_copy1', 'PN', pn):
                continue
            else:
                dbio.create_ccl(ccl, pn)

            # if dbio.check_duplicated('ECN_CCL_model1', 'model', model):
            #     continue
            # else:
            dbio.create_model(supplier, model, spec, pn, model_comp, pn_comp, cert_no)
        return df
