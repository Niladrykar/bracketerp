from django.conf.urls import url
from consultancy import views

app_name = 'consultancy'

urlpatterns = [
	url(r'^$',views.consultancyListView.as_view(),name='consultancylist'),
	url(r'^(?P<pk>\d+)/$',views.consultancy_detail,name='consultancydetail'),
	url(r'^consultancycreate/$',views.consultancycreate.as_view(),name='consultancycreate'),

	url(r'^consultancyupdate/(?P<id>\d+)/$',views.query_update,name='consultancyupdate'),
	url(r'^consultancydelete/(?P<id>\d+)/$',views.query_delete,name='consultancydelete'),

	url(r'^consultancylike/$', views.liked_post, name="like_question"),

	url(r'^myquestions/$',views.myconsultancyListView.as_view(),name='myquestions'),

	url(r'^answers/(?P<id>\d+)/update$', views.answer_update, name='answersupdate'),

	url(r'^answers/(?P<id>\d+)/delete$', views.answer_delete, name='answersdelete'),

	url(r'^consultancyresult/$', views.search, name='search'),


]
