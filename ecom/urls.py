from django.urls import include, re_path
from . import views
from .ecn import ecn_views
from .dataCenter import DataCenter_views


app_name = 'ecom'

urlpatterns = [
    re_path(
        r'^view/',  # [AT/SD Team]TODO: Add your view api for fornt-end engineer.
        include(
            [
                re_path(
                    r'^ecn/',  # Add ECN module here.
                    include(
                        [
                            re_path(r'category/(?P<site>\w+)*', ecn_views.category_cert_view),
                            re_path(r'site/(?P<category>\w+)*', ecn_views.site_cert_view),
                            re_path(r'all/', ecn_views.all_cert_view),
                            # re_path(r'files/preview/(?P<file_name>.*\..+)', ecn_views.file_preview),
                        ]
                    )
                ),
                re_path(
                    r'^audit/',  # Add Factory Audit module here.
                    include(
                        [
                            re_path(r'category/(?P<site>\w+)*', ecn_views.category_cert_view),
                            re_path(r'site/(?P<category>\w+)*', ecn_views.site_cert_view),
                            re_path(r'all/', ecn_views.all_cert_view),
                            # re_path(r'files/preview/(?P<file_name>.*\..+)', ecn_views.file_preview),
                        ]
                    )
                ),
                re_path(
                    r'^data_center/',
                    include(
                        [
                            re_path(r'select_category_by_site/', DataCenter_views.api_checking_status_by_category),
                            re_path(r'select_site_by_category/', DataCenter_views.api_checking_status_by_site),
                            re_path(r'get_all_data/', DataCenter_views.api_get_all_data),
                        ]
                    )
                )
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
                    r'^ecn/',  # Add ECN module here.
                    include(
                        [
                            re_path(r'info/', ecn_views.api_ecn_read),
                            re_path(r'count/(?P<key>\w+)*', ecn_views.api_cert_count),
                            re_path(r'files/', ecn_views.api_file_io),
                        ]
                    )
                ),
                re_path(
                    r'^ecn/',  # Add Factory Audit module here.
                    include(
                        [
                            re_path(r'files/(?P<module>\w+)*/', ecn_views.api_file_io),
                        ]
                    )
                ),
                # Add your api path here,
                # Example. re_path(r'^<custom url path>/', views.<function>),
            ]
        ),
    ),
]
