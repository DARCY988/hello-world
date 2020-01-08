""" Uploaded file handling class.
Variables:
---
NOTE:
    All variables are named by the parameters in front-web `BODY`.
    Example.
    ```
        file_field: A parameter named "file_field" in front-web `BODY`.
    ```
"""
from django import forms
from django.http import StreamingHttpResponse
from rest_framework.response import Response
import os


class FileHandler(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))  # Multi-files
    # file = forms.FileField()  # Only one file

    def save(self, file, path):
        ''' Save file.
        Parameters
        ---
        file: UploadedFile
            Your uploaded file.

        path: str
            Set the file location you want to save.

        Return
        ---
        result: str
            File saving status.
        '''
        if not os.path.exists(path):
            os.makedirs(path)

        try:
            with open(os.path.join(path, file.name), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                result = 'Upload successfully.'

        except Exception as e:
            print(e)
            result = 'Upload failed.'

        finally:
            destination.close()

        return result

    def download(self, path, file_name):
        ''' Download file.
        Parameters
        ---
        path: str
            Set the file location.

        file_name: str
            Set the file name.

        Return
        ---
        CASE I: `result`: StreamingHttpResponse
            File streaming response.

        CASE II: `error`: Response
            File not found message response.
        '''
        target = os.path.join(path, file_name)
        if os.path.exists(target):
            def file_iterator(chunk_size=512):

                try:
                    with open(target, 'rb') as file:
                        while True:
                            tmp = file.read(chunk_size)
                            if tmp:
                                yield tmp
                            else:
                                break

                except Exception as e:
                    print(e)
                    return e

                finally:
                    file.close()

            result = StreamingHttpResponse(file_iterator())
            result['Content-Type'] = 'application/octet-stream'
            result['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)

            return result
        else:
            error = {
                'message': 'File \'%s\' not found.' % (file_name)
            }
            error = Response(error)

            return error

    def preview(self, path, file_name):
        ''' Preview file.
        Parameters
        ---
        path: str
            Set the file location.

        file_name: str
            Set the file name.

        Return
        ---
        CASE I: `result`: StreamingHttpResponse
            File streaming response.

        CASE II: `error`: Response
            File not found message response.
        '''
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

                try:
                    with open(target, 'rb') as file:
                        while True:
                            tmp = file.read(chunk_size)
                            if tmp:
                                yield tmp
                            else:
                                break

                except Exception as e:
                    print(e)
                    return e

                finally:
                    file.close()

            result = StreamingHttpResponse(file_iterator())
            result['Content-Type'] = type_dict[file_type]
            result['Content-Disposition'] = 'inline;filename="{0}"'.format(file_name)

            return result
        else:
            error = {
                'message': 'File \'%s\' not found.' % (file_name)
            }
            error = Response(error)

            return error

    def delete(self, path, file_name):
        ''' Delete file.
        Parameters
        ---
        path: str
            Set the file location.

        file_name: str
            Set the file name.

        Return
        ---
        result: Response
            Delete message response.
        '''
        if os.path.isdir(path):
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

            if not os.listdir(path):
                os.rmdir(path)

        else:
            result = {
                'message': 'Check the path \'%s\' is correct or not.' % (path)
            }

        return Response(result)
