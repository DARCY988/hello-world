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
                            re_path(r'upload/', ecn_views.upload_file),
                            re_path(r'category/', ecn_views.category_cert_view),
                            re_path(r'site/(?P<category>\w+)*', ecn_views.site_cert_view),
                            re_path(r'ccl/((?P<category>\w+)/(?P<site>\w+))*', ecn_views.ccl_cert_view),
                            re_path(r'all/((?P<category>\w+)/(?P<site>\w+)/(?P<ccl>[\w\s]+))*',
                                    ecn_views.all_cert_view),
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
                        ]
                    )
                ),
                # Add your api path here,
                # Example. re_path(r'^<custom url path>/', views.<function>),
            ]
        ),
    ),
]
