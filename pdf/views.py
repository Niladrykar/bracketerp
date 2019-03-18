from django.shortcuts import render
from pdf.utils import render_to_pdf
from django.http import HttpResponse
from django.views.generic import (View,ListView,DetailView,
								  CreateView,UpdateView,DeleteView)
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from stockkeeping.models import Stockgroup,Simpleunits,Compoundunits,Stockdata,Purchase,Sales,Stock_Total,Stock_Total_sales
from company.models import company
from accounting_double_entry.models import group1,ledger1,journal,selectdatefield
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import datetime
from django.db.models import Value
from django.db.models.functions import Coalesce 
from itertools import zip_longest
from django.db.models import Case, When, CharField, Value, Sum, F, ExpressionWrapper, Subquery, OuterRef, Count
from django.db.models.fields import DecimalField
import calendar
import dateutil
import collections        

# Create your views here.


############################### Sale and Purchase PDF ######################################

class Generate_Purchase_PDF(View):
	def get(self, request, *args, **kwargs):
		template = get_template('purchase_details_pdf.html')

		purchase_details = get_object_or_404(Purchase, pk=self.kwargs['pk2'])
		stocklist = Stock_Total.objects.filter(purchases=purchase_details.pk)

		context = {

			"company_details"          : get_object_or_404(company, pk=self.kwargs['pk1']),
			"selectdatefield_details"  : get_object_or_404(selectdatefield, pk=self.kwargs['pk3']),
			"purchase_details"         : purchase_details,
			"stocklist" 			   : stocklist,
		}
		html = template.render(context)
		pdf = render_to_pdf('purchase_details_pdf.html', context)
		if pdf:
			return HttpResponse(pdf, content_type='application/pdf')
		return HttpResponse("PDF Not Found")



class Generate_Sales_PDF(View):
	def get(self, request, *args, **kwargs):
		template = get_template('sales_details_pdf.html')

		sales_details = get_object_or_404(Sales, pk=self.kwargs['pk2'])
		stocklist  = Stock_Total_sales.objects.filter(sales=sales_details.pk)

		context = {

			"company_details"          : get_object_or_404(company, pk=self.kwargs['pk1']),
			"selectdatefield_details"  : get_object_or_404(selectdatefield, pk=self.kwargs['pk3']),
			"sales_details"            : sales_details,
			"stocklist" 			   : stocklist,
		}
		html = template.render(context)
		pdf = render_to_pdf('sales_details_pdf.html', context)
		if pdf:
			return HttpResponse(pdf, content_type='application/pdf')
		return HttpResponse("PDF Not Found")



################################ Ledger PDF ##################################

class Generate_Ledger_Monthly_PDF(View):
	def get(self, request, *args, **kwargs):
		template = get_template('ledger_monthly_pdf.html')

		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		ledger1_details = get_object_or_404(ledger1, pk=self.kwargs['pk2'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])


		# opening balance
		qsob  = journal.objects.filter(User=self.request.user, Company=company_details.pk, By=ledger1_details.pk, Date__gte=ledger1_details.Creation_Date, Date__lte=selectdatefield_details.Start_Date)
		qsob2 = journal.objects.filter(User=self.request.user, Company=company_details.pk, To=ledger1_details.pk, Date__gte=ledger1_details.Creation_Date, Date__lte=selectdatefield_details.Start_Date)

		total_debitob = qsob.aggregate(the_sum=Coalesce(Sum('Debit'), Value(0)))['the_sum']
		total_creditob = qsob2.aggregate(the_sum=Coalesce(Sum('Credit'), Value(0)))['the_sum']



		if(ledger1_details.Creation_Date!=selectdatefield_details.Start_Date):
			if(ledger1_details.group1_Name.balance_nature == 'Debit'):
				opening_balance = abs(ledger1_details.Opening_Balance) + abs(total_debitob) - abs(total_creditob)
			else:
				opening_balance = abs(ledger1_details.Opening_Balance) + abs(total_creditob) - abs(total_debitob) 
		else:
			opening_balance = abs(ledger1_details.Opening_Balance)


		results = collections.OrderedDict()

		qscb  = journal.objects.filter(User=self.request.user, Company=company_details.pk, By=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).annotate(real_total_debit = Case(When(Debit__isnull=True, then=0),default=F('Debit')))
		qscb2 = journal.objects.filter(User=self.request.user, Company=company_details.pk, To=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).annotate(real_total_credit = Case(When(Debit__isnull=True, then=0),default=F('Debit')))	
		
		date_cursor = selectdatefield_details.Start_Date

		z = 0
		k = 0

		while date_cursor < selectdatefield_details.End_Date:
			month_partial_total_debit = qscb.filter(Date__month=date_cursor.month).aggregate(partial_total_debit=Sum('real_total_debit'))['partial_total_debit']
			month_partial_total_credit = qscb2.filter(Date__month=date_cursor.month).aggregate(partial_total_credit=Sum('real_total_credit'))['partial_total_credit']

			if month_partial_total_debit == None:

				month_partial_total_debit = int(0)

				e = month_partial_total_debit

			else:

				e = month_partial_total_debit


			if month_partial_total_credit == None:

				month_partial_total_credit = int(0)

				f = month_partial_total_credit

			else:

				f = month_partial_total_credit

			if(ledger1_details.group1_Name.balance_nature == 'Debit'):

				z = z + e - f 

			else:
				z = z + f - e 

			k = z + opening_balance

			results[calendar.month_name[date_cursor.month]] =  [e,f,k]

			date_cursor += dateutil.relativedelta.relativedelta(months=1)

		total_debit = qscb.aggregate(the_sum=Coalesce(Sum('Debit'), Value(0)))['the_sum']
		total_credit = qscb2.aggregate(the_sum=Coalesce(Sum('Credit'), Value(0)))['the_sum']

		if(ledger1_details.group1_Name.balance_nature == 'Debit'):

			total1 = total_debit - total_credit

		else:

			 total1 = total_credit - total_debit

		total = total1 + opening_balance

		context = {

			'company_details' : company_details,
			'ledger1_details' : ledger1_details,
			'selectdatefield_details' : selectdatefield_details,
			'total_debit'     : total_debit,
			'total_credit'    : total_credit,
			'total'			  : total,
			'data'			  : results.items(),
			'opening_balance' : opening_balance,

					
		}

		html = template.render(context)
		pdf = render_to_pdf('ledger_monthly_pdf.html', context)
		if pdf:
			return HttpResponse(pdf, content_type='application/pdf')
		return HttpResponse("PDF Not Found")



