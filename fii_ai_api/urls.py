"""Fii AI API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/

Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  re_path(r'', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  re_path(r'', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls', namespace='blog'))

The `urls.include` attribute `namespace` allow you to uniquely reverse named URL patterns
even if different applications use the same URL names. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/#url-namespaces

Examples:
     Consider an example of two instances of the polls application from the tutorial:
     one called 'author-polls' and one called 'publisher-polls'.

     Assume we have enhanced that application so that it takes the instance namespace into
     consideration when creating and displaying `polls`.

    ```python <urls.py>
        from django.urls import include, path

        urlpatterns = [
            path('author-polls/', include('polls.urls', namespace='author-polls')),
            path('publisher-polls/', include('polls.urls', namespace='publisher-polls')),
        ]
    ```

    ```python <polls/urls.py>
        from django.urls import path

        from . import views

        app_name = 'polls'
        urlpatterns = [
            path('', views.IndexView.as_view(), name='index'),
            path('<int:pk>/', views.DetailView.as_view(), name='detail'),
            ...
        ]
    ```

    Deploying the `polls` application from the tutorial in two different locations
    so we can serve the same functionality to two different audiences (authors and publishers).
"""
from django.contrib import admin
from django.urls import include, re_path

app_name = 'fii_ai_api'

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(
        r'^(?P<debug>test/)*(?P<api_version>(latest|v\w+\.\w+(\.\w*)*))/',
        include(
            [
                re_path(r'^demo/', include('demo.urls', namespace='demo-api')),
                # Add your app path here,
                # Example. re_path(r'^<app name>/', include('<app name>.urls', namespace='<app name>')),
            ]
        ),
    ),
]
