# Envirement
- Python: 3.6.9
- pip: 19.1.1

# Download Project
```bash
$ git clone http://10.124.131.87:8860/fii-iaiia-dept/api-server.git
```

# Install python requirements
NOTE: create your own virtual envirement and get into it.
```bash
# Windows
$ source <path to your venv>/Scripts/activate

# Mac or Linux
$ source <path to your venv>/bin/activate

# Install Cython
(venv)$ pip install Cython

# Install requirements
(venv)$ pip install -r requirements.txt
```

---
# 3 Steps to Create API service
## (1) Create your own App
```bash
$ python manage.py startapp --template=demo <your app name>
```

## (2) Install app
- modify attribute `INSTALLED_APPS` in `fii_ai_api/settings.py`:
```python
# fii_ai_api/settings.py
INSTALLED_APPS=[
    ...
    # project list
    'demo',
    # add your app name under the list
    <your app name>,
]
```
- add api route attribute `urlpatterns` in `fii_ai_api/urls.py`:
```python
# fii_ai_api/urls.py
urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(
        r'^(?P<debug>test/)*(?P<api_version>(latest|v\w+\.\w+(\.\w*)*))/',
        include(
            [
                re_path(r'^demo/', include('demo.urls', namespace='demo-api')),
                # Add your app path here,
                re_path(r'^<your app name>/', include('<your app name>.urls', namespace='<your app name>'))
            ]
        ),
    ),
]
```

## (3) MVC Architecture
We use `Model - View - Controller(MVC)` Architecture [more info](https://www.tutorialsteacher.com/mvc/mvc-architecture).
- (3-1)Model: Put your model into `<your app>/models.py` (in demo we use class, but you can use function as well)
```python
# <your app>/models.py
## function base
def model_in_function(input1, input2, ...):
    # do your magic ~~~
    return result


## class base
class model_in_class(...):
    def __init__(self, ...):
        # initialize your class object
    
    def cls_func1(self, input1, input2, ...):
        # do your magic ~~
        return result
```

- (3-2)View: Construct and response your result for front-end engineer. (lazy usage: @fii_api_handler)

NOTE: For now, front-end only acccpt `dict`, `list`, `pandas.DataFrame` type. We create `fii_api_handler` decorator for you guys to use.
```python
# <your app>/views.py
from .models import *

@fii_api_handler(['get', 'post'])
def your_view(request, debug, api_version, # These three are static parameters
              input1, input2, ...): # your input parameters from RESTful api url

    # get requests input variables, more info: https://stackabuse.com/the-python-requests-module/
    ## from `GET` method
    input_GET_var = request.GET.get('apple')
    ## from `POST` method
    input_POST_var = request.POST.get('pen')
    
    # call function-based model
    func_result = model_in_function(input1, input2, ...)
    return func_result

    # call class-based model
    cls_result = model_in_class.cls_func1(input1, input2, ...)
    return cls_result
```

- (3-3)Controller: Django is already finished the controller module, we only need to modify the api route in `<your app>/urls.py` to let the controller know which route redirect to which function.
```python
# <your app>/urls.py
from django.urls import include, re_path
from . import views

app_name = '<your app name>'

urlpatterns = [
    # this url module supports `Regular Expression` to collect input parameter from RESTful api
    # more info: https://docs.djangoproject.com/en/2.2/topics/http/urls/
    re_path(r'<make your own root>/(?P<value>\w+)*', views.your_view),
]
```

# Run API Server
```bash
(venv)$ python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
October 08, 2019 - 03:51:54
Django version 2.1.10, using settings 'fii_ai_api.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
Done! you can test on your api like `localhost:8000/<your app name>/<urlpattern>`.

---
# Create CronTab Jobs
## add current jobs to crontab
> python3 manage.py crontab add

## show current jobs
> python3 manage.py crontab show

## remove all jobs
> python3 manage.py crontab remove