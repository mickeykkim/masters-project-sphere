from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
   path('', views.index, name='index'),
   url(r'^patient/$', views.patientdata_list),
   url(r'^patient/(?P<pk>[0-9]+)$', views.patientdata_detail),
]