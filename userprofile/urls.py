from django.conf.urls import url
from django.urls import path
from userprofile import views

app_name = 'userprofile'

urlpatterns = [
	

	url(r'^$',views.profiledetailview.as_view(),name='profiledetail'),
    url(r'^userprofile/(?P<pk>\d+)/$',views.specific_profile,name='specific_profile'),
	url(r'^profileupdate/$',views.profileupdateview.as_view(),name='profileupdate'),

	path('activate/<product_activation_id>', views.activate_subscriptions, name='activate'),
	path('deactivate/<product_activation_id>', views.deactivate_subscriptions, name='deactivate'),

	path('activate/product/<product_activation_id>', views.activate_subscriptions_productlist, name='activate_product'),
	path('deactivate/product/<product_activation_id>', views.deactivate_subscriptions_productlist, name='deactivate_product'),

	url(r'^profresult/$', views.search_professionals, name='search'),

	url(r'^social/$',views.post_list,name='social'),
	url(r'^post_add/$',views.postcreateview.as_view(),name='post_add'),
	url(r'^(?P<pk>\d+)/$',views.post_detail,name='post_details'),

	url(r'^postlike/$', views.liked_post, name="like_post"),

	url(r'^postcomment/(?P<id>\d+)/update$', views.post_comment_update, name='postcommentupdate'),

	url(r'^postcomment/(?P<id>\d+)/delete$', views.post_comment_delete, name='postcommentdelete'),

############################# Service Url ##############################################################

	url(r'^service/create/$',views.servicecreateview.as_view(),name='service_create'),
	url(r'^service/(?P<pk>\d+)/update/$',views.serviceupdateview.as_view(),name='service_update'),
	url(r'^service/(?P<pk>\d+)/details/$',views.service_detail,name='service_details'),
	url(r'^service/(?P<id>\d+)/delete$', views.service_delete, name='servicedelete'),


############################# Achievements Url ##############################################################

	url(r'^case/create/$',views.casecreateview.as_view(),name='case_create'),
	url(r'^case/(?P<pk>\d+)/update/$',views.caseupdateview.as_view(),name='case_update'),
	url(r'^caselist/$',views.CaseListView.as_view(),name='case_list'),
	url(r'^case/(?P<pk>\d+)/details/$',views.case_detail,name='case_details'),
	url(r'^case/(?P<id>\d+)/delete$', views.case_delete, name='casedelete'),

	url(r'^pro_verify/create/$',views.proverifycreateview.as_view(),name='pro_verify'),

	url(r'^organisationupdate/(?P<pk>\d+)/$',views.organisationupdateview.as_view(),name='organisationupdate'),

	url(r'^organisation/member/update/(?P<pk>\d+)/$',views.organisation_member_updateview.as_view(),name='organisation_member_update'),
	url(r'^organisation/member/list/$',views.Organisation_member_listview.as_view(),name='organisation_member_list'),
	url(r'^organisation/member/(?P<pk>\d+)/delete$', views.delete_members, name='delete_members'),
]