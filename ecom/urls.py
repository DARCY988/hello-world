from django.urls import include, re_path
from . import views
from .ecn import ecn_views

app_name = 'ecom'

urlpatterns = [
    re_path(
        r'^view/',  # [AT/SD Team]TODO: Add your view api for fornt-end engineer.
        include(
            [
                re_path(
                    r'^ecn',  # Add ECN module here.
                    include(
                        [
                            re_path(r'category/(?P<site>\w+)*', ecn_views.category_cert_view),
                            re_path(r'site/(?P<category>\w+)*', ecn_views.site_cert_view),
                            re_path(r'all/', ecn_views.all_cert_view),
                        ]
                    )
                ),
                # Add your api path here,
                # Example. re_path(r'^<custom url path>/', views.<function>),
            ]
        ),
    ),
    re_path(
        r'^api/',  # [DE/SD Team]TODO: Add api for new AT Team members to use.
        include(
            [
                re_path(
                    r'^ecn',  # Add ECN module here.
                    include(
                        [
                            re_path(r'info/', ecn_views.api_ecn_read),
                            re_path(r'count/(?P<key>\w+)*', ecn_views.api_cert_count),
                            re_path(r'upload/', ecn_views.api_file_upload),
                            re_path(r'download/(?P<file_name>.*\..+)', ecn_views.api_file_download),
                            re_path(r'preview/(?P<file_name>.*\..+)', ecn_views.api_file_preview),
                            re_path(r'delete/(?P<file_name>.*\..+)', ecn_views.api_file_delete),
                        ]
                    )
                ),
                # Add your api path here,
                # Example. re_path(r'^<custom url path>/', views.<function>),
            ]
        ),
    ),
]
