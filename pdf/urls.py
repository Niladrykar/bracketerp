from django.conf.urls import url
from pdf import views

app_name = 'pdf'

urlpatterns = [

########################################### PDF URLS ############################################################################################################################
	url(r'^company/(?P<pk1>\d+)/purchasedetailpdf/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Generate_Purchase_PDF.as_view(),name='purchasedetailpdf'),
	url(r'^company/(?P<pk1>\d+)/saledetailpdf/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Generate_Sales_PDF.as_view(),name='salesdetailpdf'),
    url(r'^company/(?P<pk>\d+)/ledgermonthlypdf/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Generate_Ledger_Monthly_PDF.as_view(),name='ledgerdetailmonthlypdf'),


]