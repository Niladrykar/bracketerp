from django.conf.urls import url
from blog import views

app_name = 'blog'

urlpatterns = [
	url(r'^$',views.bloglistview.as_view(),name='bloglist'),
	url(r'^(?P<pk>\d+)/$',views.post_detail,name='blogdetail'),
	url(r'^blogcreate/$',views.blogcreateview.as_view(),name='blogcreate'),
	url(r'^blogupdate/(?P<pk>\d+)/$',views.blogupdateview.as_view(),name='blogupdate'),
	url(r'^blogdelete/(?P<pk>\d+)/$',views.blogdeleteview.as_view(),name='blogdelete'),
	url(r'^bloglist/$',views.allbloglistview.as_view(),name='allbloglist'),
	url(r'^latestbloglist/$',views.latestbloglistview.as_view(),name='latestbloglist'),
	url(r'^likedbloglist/$',views.likebloglistview.as_view(),name='likebloglist'),
	url(r'^viewbloglist/$',views.viewbloglistview.as_view(),name='viewbloglist'),

	url(r'^like/$', views.like_post, name="like_post"),



	url(r'^categorylist/$',views.categoryListView.as_view(),name='categoryList'),
	url(r'^categorylist/(?P<pk>\d+)/$',views.categoryDetailView.as_view(),name='categoryDetail'),

	url(r'^result/$', views.search, name='search'),
]