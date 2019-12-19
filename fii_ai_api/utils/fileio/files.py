from django import forms
from django.http import StreamingHttpResponse
from rest_framework.response import Response
import os


class FileHandler(forms.Form):
    title = forms.CharField(max_length=100)
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))  # Multi-files
    # file = forms.FileField()  # Only one file

    def save(self, file, path):

        if not os.path.exists(path):
            os.mkdir(path)

        result = {}
        try:
            with open(os.path.join(path, file.name), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()
                result['message'] = 'Upload successfully.'

        except Exception as e:
            print(e)
            result['message'] = 'Upload failed.'

        return result

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
                'message': 'File \'%s\' not found.' % (file_name)
            }
            result = Response(result)

        return result

    def preview(self, path, file_name):

        target = os.path.join(path, file_name)
        file_type = file_name.split('.')[-1]
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
                'message': 'File \'%s\' not found.' % (file_name)
            }
            result = Response(result)

        return result

    def delete(self, path, file_name):

        target = os.path.join(path, file_name)
        if os.path.exists(target):
            os.remove(target)

            result = {
                'message': 'File \'%s\' has been deleted.' % (file_name)
            }
        else:
            result = {
                'message': 'File \'%s\' not found.' % (file_name)
            }

        return Response(result)
