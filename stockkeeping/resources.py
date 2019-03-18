from import_export import resources
from stockkeeping.models import Stockgroup,Simpleunits,Compoundunits,Stockdata,Purchase,Sales,Stock_Total,Stock_Total_sales

class PurchaseResource(resources.ModelResource):
    class Meta:
        model = Purchase



class SalesResource(resources.ModelResource):
    class Meta:
        model = Sales