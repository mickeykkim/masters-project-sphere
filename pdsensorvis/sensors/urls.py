from django.urls import path, re_path
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
from . import views

urlpatterns = [
   path('', views.index, name='index'),
   path('patientdata/', views.PatientDataListView.as_view(), name='patientdata'),
   re_path(r'^patientdata/(?P<pk>\d+)$', views.PatientDataDetailView.as_view(), name='patientdata-detail'),
   path('wearabledata/', views.WearableDataListView.as_view(), name='wearabledata'),
   re_path(r'^wearabledata/(?P<pk>[-\w]+)$', views.WearableDataDetailView.as_view(), name='wearabledata-detail'),
   re_path(r'^wearabledata/(?P<uuid>[-\w]+)/(?P<pk>\d+)$', views.WearableAnnotationDetailView.as_view(), name='wearableannotation-detail'),
   path('cameradata/', views.CameraDataListView.as_view(), name='cameradata'),
   re_path(r'^cameradata/(?P<pk>[-\w]+)$', views.CameraDataDetailView.as_view(), name='cameradata-detail'),
   re_path(r'^cameradata/(?P<uuid>[-\w]+)/(?P<pk>\d+)$', views.CameraAnnotationDetailView.as_view(), name='cameraannotation-detail'),
   url(r'^data/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
   path('myannotations/', views.CameraAnnotationByUserListView.as_view(), name='my-annotations'),
   # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]