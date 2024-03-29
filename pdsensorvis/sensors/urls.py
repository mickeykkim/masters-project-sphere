from django.urls import path, re_path
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search_results, name="search-results"),
    path("patientdata/", views.PatientDataListView.as_view(), name="patientdata"),
    re_path(
        r"^patientdata/(?P<pk>\d+)$",
        views.PatientDataDetailView.as_view(),
        name="patientdata-detail",
    ),
    re_path(
        r"^patientdata/create/$", views.create_patientdata, name="create-patientdata"
    ),
    re_path(
        r"^patientdata/(?P<pk>[\w-]+)/create/wearable/$",
        views.create_wearabledata,
        name="create-wearabledata",
    ),
    re_path(
        r"^patientdata/(?P<pk>[\w-]+)/create/camera/$",
        views.create_cameradata,
        name="create-cameradata",
    ),
    re_path(
        r"^patientdata/(?P<pk>[\w-]+)/edit/$",
        views.edit_patientdata,
        name="edit-patientdata",
    ),
    re_path(
        r"^patientdata/(?P<pk>[\w-]+)/delete/$",
        views.delete_patientdata,
        name="delete-patientdata",
    ),
    path("wearabledata/", views.WearableDataListView.as_view(), name="wearabledata"),
    re_path(
        r"^wearabledata/(?P<pk>[\w-]+)$",
        views.WearableDataDetailView.as_view(),
        name="wearabledata-detail",
    ),
    re_path(
        r"^wearabledata/(?P<uuid>[\w-]+)/(?P<pk>\d+)$",
        views.WearableAnnotationDetailView.as_view(),
        name="wearableannotation-detail",
    ),
    re_path(
        r"^wearabledata/(?P<uuid>[\w-]+)/edit/$",
        views.edit_wearabledata,
        name="edit-wearabledata",
    ),
    re_path(
        r"^wearabledata/(?P<uuid>[\w-]+)/delete/$",
        views.delete_wearabledata,
        name="delete-wearabledata",
    ),
    re_path(
        r"^wearabledata/(?P<uuid>[\w-]+)/import/annotation/$",
        views.upload_wearable_annotations,
        name="upload-wearable-annotations",
    ),
    re_path(
        r"^wearabledata/(?P<uuid>[\w-]+)/create/$",
        views.create_wearable_annotation,
        name="create-wearable-annotation",
    ),
    re_path(
        r"^wearabledata/(?P<uuid>[\w-]+)/(?P<pk>\d+)/edit/$",
        views.edit_wearable_annotation,
        name="edit-wearable-annotation",
    ),
    re_path(
        r"^wearabledata/(?P<uuid>[\w-]+)/(?P<pk>\d+)/delete/$",
        views.delete_wearable_annotation,
        name="delete-wearable-annotation",
    ),
    path("cameradata/", views.CameraDataListView.as_view(), name="cameradata"),
    re_path(
        r"^cameradata/(?P<pk>[\w-]+)$",
        views.CameraDataDetailView.as_view(),
        name="cameradata-detail",
    ),
    re_path(
        r"^cameradata/(?P<uuid>[\w-]+)/edit/$",
        views.edit_cameradata,
        name="edit-cameradata",
    ),
    re_path(
        r"^cameradata/(?P<uuid>[\w-]+)/delete/$",
        views.delete_cameradata,
        name="delete-cameradata",
    ),
    re_path(
        r"^cameradata/(?P<pk>[\w-]+)/export/csv/$",
        views.export_annotations_csv,
        name="export-annotations-csv",
    ),
    re_path(
        r"^cameradata/(?P<pk>[\w-]+)/export/xls/$",
        views.export_annotations_xls,
        name="export-annotations-xls",
    ),
    re_path(
        r"^cameradata/(?P<pk>[\w-]+)/export/srt/$",
        views.export_annotations_srt,
        name="export-annotations-srt",
    ),
    re_path(
        r"^cameradata/(?P<uuid>[\w-]+)/(?P<pk>\d+)$",
        views.CameraAnnotationDetailView.as_view(),
        name="cameraannotation-detail",
    ),
    re_path(
        r"^cameradata/(?P<uuid>[\w-]+)/(?P<pk>\d+)/edit/$",
        views.edit_camera_annotation,
        name="edit-camera-annotation",
    ),
    re_path(
        r"^cameradata/(?P<uuid>[\w-]+)/(?P<pk>\d+)/delete/$",
        views.delete_camera_annotation,
        name="delete-camera-annotation",
    ),
    re_path(
        r"^cameradata/(?P<uuid>[\w-]+)/(?P<pk>\d+)/(?P<cid>\d+)/edit/$",
        views.edit_cameraannotation_comment,
        name="edit-cameraannotation-comment",
    ),
    re_path(
        r"^cameradata/(?P<uuid>[\w-]+)/(?P<pk>\d+)/(?P<cid>\d+)/delete/$",
        views.delete_cameraannotation_comment,
        name="delete-cameraannotation-comment",
    ),
    url(r"^data/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_URL}),
    url(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_URL}),
    path(
        "myannotations/",
        views.CameraAnnotationByUserListView.as_view(),
        name="my-annotations",
    ),
]
