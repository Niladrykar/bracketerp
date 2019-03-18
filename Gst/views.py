from django.shortcuts import render
from django.views.generic import (ListView,DetailView,
								  CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from ecommerce_integration.models import coupon, Product, Product_review, Services, API
from Gst.models import Gst_input,Gst_output,Stock_gst
from accounting_double_entry.models import journal,group1,ledger1,selectdatefield,Payment,Particularspayment,Receipt,Particularsreceipt,Contra,Particularscontra,Multijournal,Multijournaltotal
from stockkeeping.models import Stockgroup,Simpleunits,Compoundunits,Stockdata,Purchase,Sales,Stock_Total,Stock_Total_sales
from django.core.exceptions import PermissionDenied
from ecommerce_integration.decorators import product_1_activation
# Create your views here.


class ProductExistsRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if Product_activation.objects.filter(User=self.request.user,product__id = 1, activate=True):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


