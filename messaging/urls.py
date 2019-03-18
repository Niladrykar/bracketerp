from django.conf.urls import url
from messaging import views

app_name = 'messaging'

urlpatterns = [
	url(r'^messagecreate/$',views.messagecreate.as_view(),name='messagecreate'),
	url(r'^messageinbox/$',views.messageinbox.as_view(),name='messageinbox'),
	url(r'^messagesend/$',views.messagesend.as_view(),name='messagesend'),
	url(r'^messagedetails/(?P<pk>\d+)/$',views.message_details,name='messagedetails'),
]