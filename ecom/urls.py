"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, re_path
from . import views
from .ecn import ecn_views

app_name = 'ecom'

urlpatterns = [
    re_path(
        r'^view/',  # [AT/SD Team]TODO: Add your view api for fornt-end engineer.
        include(
            [
                re_path(r'print/(?P<value>\w+)*', views.demo_ai_view),
                # Add your api path here,
                # Example. re_path(r'^<custom url path>/', views.<function>),
            ]
        ),
    ),
    re_path(
        r'^api/',  # [DE/SD Team]TODO: Add api for new AT Team members to use.
        include(
            [
                re_path(r'print/(?P<value>\w+)*', views.api_demo_read),
                re_path(
                    r'^ecn',  # Add ECN module here.
                    include(
                        [
                            re_path(r'info/', ecn_views.api_ecn_read),
                            re_path(r'count/(?P<value>\w+)*', ecn_views.api_cert_count),
                        ]
                    )
                ),
                # Add your api path here,
                # Example. re_path(r'^<custom url path>/', views.<function>),
            ]
        ),
    ),
]
