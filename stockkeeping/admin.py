from django.contrib import admin
from stockkeeping.models import Stockgroup,Simpleunits,Compoundunits,Stockdata,Purchase,Stock_Total,Sales,Stock_Total_sales
from stockkeeping.forms import Stockgroup_form,Simpleunits_form,Compoundunits_form,Stockdata_form,Purchase_form,Sales_form,Purchase_formSet,Sales_formSet,Sales_formadmin,Purchase_formadmin

# Register your models here.


class Stockgroupadmin(admin.ModelAdmin):
	model = Stockgroup
	list_display = ['User', 'Company','name','under','quantities']
	search_fields = ['name']

class Simpleunitsadmin(admin.ModelAdmin):
	model = Simpleunits
	list_display = ['User', 'Company','symbol','formal']
	search_fields = ['symbol','formal']

class Compoundunitsadmin(admin.ModelAdmin):
	model = Compoundunits
	list_display = ['User', 'Company','firstunit','conversion','seconds_unit']
	search_fields = ['firstunit','seconds_unit']

class Stockdataadmin(admin.ModelAdmin):
	model = Stockdata
	list_display = ['User', 'Company','stock_name','gst_rate','hsn']
	search_fields = ['stock_name','hsn']

class Stock_Totaladmin(admin.ModelAdmin):
	model = Stock_Total
	list_display = ['purchases','stockitem','Quantity_p','rate_p','Total_p']
	search_fields = ['stockitem']

class Stock_Total_salesadmin(admin.ModelAdmin):
	model = Stock_Total_sales
	list_display = ['sales','stockitem','Quantity','rate','Total']
	search_fields = ['stockitem']

class Stock_Totalinline(admin.TabularInline):
	model = Stock_Total

class Stock_Total_salesinline(admin.TabularInline):
	model = Stock_Total_sales

class Purchaseadmin(admin.ModelAdmin):
	model = Purchase
	list_display = ['User', 'Company','ref_no','Party_ac','purchase','sub_total']
	search_fields = ['stock_name','id']
	inlines = [Stock_Totalinline]

class Salesadmin(admin.ModelAdmin):
	model = Sales
	list_display = ['User', 'Company','ref_no','Party_ac','sales','sub_total']
	search_fields = ['stock_name','hsn']
	inlines = [Stock_Total_salesinline]


admin.site.register(Stockgroup, Stockgroupadmin)
admin.site.register(Simpleunits, Simpleunitsadmin)
admin.site.register(Compoundunits, Compoundunitsadmin)
admin.site.register(Stockdata, Stockdataadmin)
admin.site.register(Purchase, Purchaseadmin)
admin.site.register(Sales, Salesadmin)
admin.site.register(Stock_Total, Stock_Totaladmin)
admin.site.register(Stock_Total_sales, Stock_Total_salesadmin)