from django.conf.urls import url
from stockkeeping import views

app_name = 'stockkeeping'

urlpatterns = [


################################### Simple Units Url #######################################

	url(r'^company/(?P<pk>\d+)/date/(?P<pk3>\d+)/simpleunitlist$',views.Simpleunits_listview.as_view(),name='simplelist'),
	url(r'^company/(?P<pk1>\d+)/simpleunitdetail/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Simpleunits_detailsview.as_view(),name='simpledetail'),
	url(r'^company/(?P<pk>\d+)/date/(?P<pk3>\d+)/simpleunitcreate/$',views.Simpleunits_createview.as_view(),name='simplecreate'),
	url(r'^company/(?P<pk1>\d+)/simpleunitupdate/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Simpleunits_updateview.as_view(),name='simpleupdate'),
	url(r'^company/(?P<pk>\d+)/simpleunitdelete/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Simpleunits_deleteview.as_view(),name='simpledelete'),

################################### Compound Units Url #######################################

	url(r'^company/(?P<pk>\d+)/date/(?P<pk3>\d+)/compoundunitlist$',views.Compoundunit_listview.as_view(),name='compoundlist'),
	url(r'^company/(?P<pk1>\d+)/compoundunitdetail/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Compoundunits_detailsview.as_view(),name='compounddetail'),
	url(r'^company/(?P<pk>\d+)/date/(?P<pk3>\d+)/compoundunitcreate/$',views.Compoundunits_createview.as_view(),name='compoundcreate'),
	url(r'^company/(?P<pk1>\d+)/compoundunitupdate/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Compoundunits_updateview.as_view(),name='compoundupdate'),
	url(r'^company/(?P<pk>\d+)/compoundunitdelete/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Compoundunits_deleteview.as_view(),name='compounddelete'),

################################### Stockgroup Url #######################################

	url(r'^company/(?P<pk>\d+)/date/(?P<pk3>\d+)/stockgrouplist$',views.Stockgroup_listview.as_view(),name='stockgrouplist'),
	url(r'^company/(?P<pk1>\d+)/stockgroupdetail/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Stockgroup_detailsview.as_view(),name='stockgroupdetail'),
	url(r'^company/(?P<pk>\d+)/date/(?P<pk3>\d+)/stockgroupcreate/$',views.Stockgroup_createview.as_view(),name='stockgroupcreate'),
	url(r'^company/(?P<pk1>\d+)/stockgroupupdate/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Stockgroup_updateview.as_view(),name='stockgroupupdate'),
	url(r'^company/(?P<pk>\d+)/stockgroupdelete/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Stockgroup_deleteview.as_view(),name='stockgroupdelete'),


################################### Stockdata Monthly Url ######################################

    url(r'^company/(?P<pk>\d+)/stockmonthly/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Stockitems_Monthly_view,name='stockmonthly'),


################################### Stockdata Url #######################################

	url(r'^company/(?P<pk>\d+)/date/(?P<pk3>\d+)/stockdata$',views.Stockdata_listview.as_view(),name='stockdatalist'),
	url(r'^company/(?P<pk1>\d+)/stockdatadetail/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Stockdata_detailsview.as_view(),name='stockdatadetail'),
	url(r'^company/(?P<pk>\d+)/date/(?P<pk3>\d+)/stockdatacreate/$',views.Stockdata_createview.as_view(),name='stockdatacreate'),
	url(r'^company/(?P<pk1>\d+)/stockdataupdate/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Stockdata_updateview.as_view(),name='stockdataupdate'),
	url(r'^company/(?P<pk>\d+)/stockdatadelete/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Stockdata_deleteview.as_view(),name='stockdatadelete'),

################################### Purchase Url #######################################

	url(r'^company/(?P<pk>\d+)/date/(?P<pk3>\d+)/purchase$',views.Purchase_listview.as_view(),name='purchaselist'),
	url(r'^company/(?P<pk1>\d+)/purchasedetail/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Purchase_detailsview.as_view(),name='purchasedetail'),
	url(r'^company/(?P<pk>\d+)/date/(?P<pk3>\d+)/purchasecreate/$',views.Purchase_createview.as_view(),name='purchasecreate'),
	url(r'^company/(?P<pk1>\d+)/purchaseupdate/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Purchase_updateview.as_view(),name='purchaseupdate'),
	url(r'^company/(?P<pk>\d+)/purchasedelete/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Purchase_deleteview.as_view(),name='purchasedelete'),


################################### Purchase Register Url #######################################

	url(r'^company/(?P<pk>\d+)/Purchase_Register/date/(?P<pk3>\d+)/$',views.Purchase_Register_view.as_view(),name='purchase_register'),



################################### Sale Register Url #######################################

	url(r'^company/(?P<pk>\d+)/Sale_Register/date/(?P<pk3>\d+)/$',views.Sales_Register_view.as_view(),name='sale_register'),

################################### Sales Url #######################################

	url(r'^company/(?P<pk>\d+)/date/(?P<pk3>\d+)/sales$',views.Sales_listview.as_view(),name='saleslist'),
	url(r'^company/(?P<pk1>\d+)/salesdetail/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Sales_detailsview.as_view(),name='salesdetail'),
	url(r'^company/(?P<pk>\d+)/date/(?P<pk3>\d+)/salescreate/$',views.Sales_createview.as_view(),name='salescreate'),
	url(r'^company/(?P<pk1>\d+)/salesupdate/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Sales_updateview.as_view(),name='salesupdate'),
	url(r'^company/(?P<pk>\d+)/salesdelete/(?P<pk2>\d+)/date/(?P<pk3>\d+)/$',views.Sales_deleteview.as_view(),name='salesdelete'),


	url(r'^company/(?P<pk>\d+)/date/(?P<pk3>\d+)/stcreate/$',views.Stock_Total_createview.as_view(),name='stocktotalcreate'),


################################### Closing Stock Url #######################################
	
	url(r'^company/(?P<pk>\d+)/date/(?P<pk3>\d+)/$',views.closing_list_view.as_view(),name='closingstock'),


################################### Profit & Loss Url #######################################

    url(r'^company/(?P<pk>\d+)/Profitloss/date/(?P<pk3>\d+)/$',views.profit_and_loss_view,name='profitloss'),

################################### Trial Balance Url #######################################

	url(r'^company/(?P<pk>\d+)/trialbalance/date/(?P<pk3>\d+)/$',views.trial_balance_view,name='trialbal'),

################################### Balance Sheet Url #######################################

	
	url(r'^company/(?P<pk>\d+)/balancesheet/date/(?P<pk3>\d+)/$',views.balance_sheet_view,name='balsht'),

]

