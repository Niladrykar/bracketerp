from django.conf.urls import url,include
from company import views
from django.urls import path

app_name = 'company'

urlpatterns = [
######################### Company Urls ################################################
    url(r'^$',views.companyListView.as_view(),name='list'),
    url(r'^(?P<pk>\d+)/date/(?P<pk3>\d+)/$',views.companyDetailView.as_view(),name='Dashboard'),
    url(r'^create/$',views.companyCreateView.as_view(),name='create'),
    url(r'^update/(?P<pk>\d+)/$',views.companyUpdateView.as_view(),name='update'),
    url(r'^delete/(?P<id>\d+)/$',views.company_delete,name='delete'),
	
]