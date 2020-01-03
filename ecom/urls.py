from django.urls import include, re_path
from . import views
from .ecn import ecn_views
from .datacenter import dc_views


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
                        ]
                    )
                ),
                re_path(
                    r'^data_center/',
                    include(
                        [
                            re_path(r'select_category_by_site/', dc_views.api_checking_status_by_category),
                            re_path(r'select_site_by_category/', dc_views.api_checking_status_by_site),
                            re_path(r'get_all_data/', dc_views.api_get_all_data),
                            re_path(r'upload/', dc_views.dc_upload),
                            re_path(r'upload_excel/', dc_views.upload_excel),
                            re_path(r'get_path/', dc_views.get_path_by_cert),
                            re_path(r'delete/', dc_views.delete_by_path),
                            re_path(r'preview/', dc_views.preview_by_path),
                            re_path(r'download/', dc_views.download_by_path),
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
