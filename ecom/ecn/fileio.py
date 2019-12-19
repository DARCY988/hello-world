from fii_ai_api.utils.fileio.files import FileHandler
from datetime import datetime, timezone, timedelta
from pandas import DataFrame, read_excel


class FileFormIO(FileHandler):
    def read(self, file, dbio, uploader):

        # Read excel file
        pre_df = read_excel(file, sheet_name=0, index_col=0, header=0)
        excel_df = pre_df.fillna(method='ffill')
        pre_df.fillna('', inplace=True)

        result = []
        for row in range(0, len(excel_df.index)):
            site = excel_df.iloc[row][0]
            category = excel_df.iloc[row][1]
            cert_no = excel_df.iloc[row][2].replace('\'', '').strip()
            pid = excel_df.iloc[row][3].replace('\n', ' ')
            ccl = excel_df.iloc[row][4]
            supplier = excel_df.iloc[row][5]
            model = excel_df.iloc[row][6]
            spec = excel_df.iloc[row][7]
            pn = excel_df.iloc[row][8]
            model_comp = pre_df.iloc[row][9]
            pn_comp = pre_df.iloc[row][10]
            create_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")

            result.append(
                {
                    'site': site,
                    'category': category,
                    'cert_no': cert_no,
                    'pid': pid,
                    'ccl': ccl,
                    'supplier': supplier,
                    'model': model,
                    'spec': spec,
                    'pn': pn,
                    'model_comp': model_comp,
                    'pn_comp': pn_comp,
                    'uploader': uploader,
                    'create_time': create_time,
                }
            )

            # Avoid duplicated
            if not dbio.check_duplicated(dbio.db_tables['ECN'], 'cert_no', cert_no):
                dbio.create_ECN(site, category, cert_no, pid, uploader, create_time)

            if not dbio.check_duplicated(dbio.db_tables['ECN_CCL'], 'PN', pn):
                dbio.create_ccl(ccl, pn)

            if not dbio.check_duplicated(dbio.db_tables['ECN_model'], 'model', model):
                dbio.create_model(supplier, model, spec, pn, model_comp, pn_comp, cert_no)

        return result
