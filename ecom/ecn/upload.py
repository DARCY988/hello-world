from django import forms
from fii_ai_api.settings import BASE_DIR
import os


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()
    path = os.path.join(BASE_DIR, 'ecom/ecn/doc')

    def handle_upload_file(self, file, filename):

        path = os.path.join(self.path, filename)
        with open(path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
