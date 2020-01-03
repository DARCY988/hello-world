from django.urls import include, re_path
from . import views
from .ecn import ecn_views
from .datacenter import datacenter_views
from .audit import audit_views


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
                            # re_path(r'category/(?P<site>\w+)*', ecn_views.category_cert_view),
                        ]
                    )
                ),
                re_path(
                    r'^data_center/',
                    include(
                        [
                            re_path(r'select_category_by_site/', datacenter_views.api_checking_status_by_category),
                            re_path(r'select_site_by_category/', datacenter_views.api_checking_status_by_site),
                            re_path(r'get_all_data/', datacenter_views.api_get_all_data),
                            re_path(r'upload/', datacenter_views.dc_upload),
                            #  re_path(r'excel_upload/', datacenter_views.get_excel),
                            re_path(r'get_path/', datacenter_views.get_path_by_cert),
                            re_path(r'delete/', datacenter_views.delete_by_path),
                            re_path(r'preview/', datacenter_views.preview_by_path),
                            re_path(r'download/', datacenter_views.download_by_path),
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
                    r'^audit/',  # Add Factory Audit module here.
                    include(
                        [
                            re_path(r'files/(?P<module>\w+)*/', audit_views.api_file_io),
                        ]
                    )
                ),
                # Add your api path here,
                # Example. re_path(r'^<custom url path>/', views.<function>),
            ]
        ),
    ),
]
