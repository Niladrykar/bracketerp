from django.shortcuts import render
from django.views.generic import (ListView,DetailView,
								  CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from accounting_double_entry.models import Pl_journal,journal,group1,ledger1,selectdatefield,Payment,Particularspayment,Receipt,Particularsreceipt,Contra,Particularscontra,Multijournal,Multijournaltotal
from stockkeeping.models import Stockgroup,Simpleunits,Compoundunits,Stockdata,Purchase,Sales,Stock_Total,Stock_Total_sales
from accounting_double_entry.forms import pl_journalForm,journalForm,group1Form,Ledgerform,DateRangeForm,PaymentForm,Payment_formSet,ParticularspaymentForm,ReceiptForm,ParticularsreceiptForm,Receipt_formSet,ContraForm,ParticularscontraForm,Contra_formSet,MultijournalForm,MultijournaltotalForm,Multijournal_formSet
from userprofile.models import Profile, Product_activation
from todogst.models import Todo
from company.models import company
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from messaging.models import Message
import datetime
from django.db.models.functions import Coalesce 
from itertools import zip_longest
from django.db.models import Case, When, CharField, Value, Sum, F, Q, ExpressionWrapper, Subquery, OuterRef, Count
from django.db.models.fields import DecimalField
from ecommerce_integration.models import coupon, Product, Product_review, Services, API
import calendar
import dateutil
import collections   
from django.db import transaction  
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.template.loader import render_to_string
from ecommerce_integration.decorators import product_1_activation
from django.core.exceptions import PermissionDenied



class ProductExistsRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

# Create your views here.
###################### Views For Group Display ############################################

class groupsummaryListView(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = group1
	paginate_by = 15

	def get_template_names(self):
		if True:  
			return ['Group_Summary/group_summary.html']
		else:
			return ['accounting_double_entry/group1_list.html']

	def get_queryset(self):
		return self.model.objects.filter(User=self.request.user, Company=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super(groupsummaryListView, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['group1_list'] = group1.objects.filter(User=self.request.user, Company= company_details.pk)
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context



class group1ListView(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = group1
	paginate_by = 15

	def get_queryset(self):
		return self.model.objects.filter(User=self.request.user, Company=self.kwargs['pk']).order_by('id')

	def get_context_data(self, **kwargs):
		context = super(group1ListView, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context


@login_required
@product_1_activation
def groupsummary_detail_view(request, pk, pk2, pk3):
	company_details = get_object_or_404(company, pk=pk)
	group1_details = get_object_or_404(group1, pk=pk2)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)

	group1_obj = group1.objects.filter(User=request.user, Company=company_details.pk, Master=group1_details.pk, ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date)
	groups_cb  = group1_obj.annotate(
				closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0),
			)

	ledger1_obj = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name=group1_details.pk, Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	ledger1_cb  = ledger1_obj.annotate(
				closing = Coalesce(Sum('Closing_balance'), 0),
			)

	# For Primary Groups

	groupprimary = group1.objects.filter(User=request.user, Company=company_details.pk, Master__group_Name__icontains='Primary', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date)
	groupprimarycb = groupprimary.annotate(
			closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0))

	groupprimarytcb = groupprimarycb.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	
	ledprimary = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Primary', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)	
	ledprimarycb = ledprimary.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	total_primarycb = groupprimarytcb + ledprimarycb	



	# Groups and ledger with debit balance nature

	groupsdebit = group1.objects.filter(User=request.user, Company=company_details.pk, Master=group1_details.pk, balance_nature__icontains='Debit', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date)
	groups_cbc = groupsdebit.annotate(
				closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0)).filter(closing__gt = 0)

	groupcbl = groupsdebit.annotate(
			closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0)).filter(closing__lt = 0)

	posgroup = groups_cbc.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	neggroup = groupcbl.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']




	ledger1debit = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name=group1_details.pk, group1_Name__balance_nature__icontains='Debit', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	ledger1_cbc = ledger1debit.annotate(
				closing = Coalesce(Sum('Closing_balance'), 0)).filter(closing__gt = 0)

	ledger1cbl = ledger1debit.annotate(
			closing = Coalesce(Sum('Closing_balance'), 0)).filter(closing__lt = 0)

	posledger = ledger1_cbc.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	negledger = ledger1cbl.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']


	# Groups and ledger with Credit balance nature

	groupscredit = group1.objects.filter(User=request.user, Company=company_details.pk, Master=group1_details.pk, balance_nature__icontains='Credit', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date)
	groups_credpo = groupscredit.annotate(
				closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0)).filter(closing__gt = 0)

	groups_creneg = groupscredit.annotate(
			closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0)).filter(closing__lt = 0)

	posgroupcre = groups_credpo.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	neggroupcre = groups_creneg.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']



	ledger1credit = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name=group1_details.pk, group1_Name__balance_nature__icontains='Credit', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	ledger1_crepo = ledger1credit.annotate(
				closing = Coalesce(Sum('Closing_balance'), 0)).filter(closing__gt = 0)

	ledger1_creneg = ledger1credit.annotate(
			closing = Coalesce(Sum('Closing_balance'), 0)).filter(closing__lt = 0)

	posledgercre = ledger1_crepo.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	negledgercre = ledger1_creneg.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']

	debitside = posgroup + neggroupcre + posledger + negledgercre

	creditside = posledgercre + negledger + posgroupcre + neggroup

	inbox = Message.objects.filter(reciever=request.user)
	inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
	send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']


	context = {

		'company_details' 		  : company_details,
		'group1_details'  		  : group1_details,
		'selectdatefield_details' : selectdatefield_details,
		'group1_obj'      		  : groups_cb,
		'ledger1_obj'    		  : ledger1_cb,
		'debitside'				  : debitside,
		'creditside'			  : creditside,
		'primary_groups'		  : groupprimarycb,
		'primary_ledgers'		  : ledprimary,
		'total_primary'			  : total_primarycb,
		'inbox'					  : inbox,
		'inbox_count'			  : inbox_count,
		'send_count'			  : send_count,
		'Todos'					  : Todo.objects.filter(User=request.user, complete=False),
		'Todos_total' 			  : Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 

				
	}

	return render(request, 'Group_Summary/group_summary_details.html', context)



class group1DetailView(ProductExistsRequiredMixin,LoginRequiredMixin,DetailView):
	context_object_name = 'group1_details'
	model = group1
	template_name = 'accounting_double_entry/group1_details.html'

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		pk3 = self.kwargs['pk3']
		get_object_or_404(selectdatefield, pk=pk3)
		get_object_or_404(company, pk=pk1)
		group = get_object_or_404(group1, pk=pk2)
		return group


	def get_context_data(self, **kwargs):
		context = super(group1DetailView, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context


class group1CreateView(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = group1Form
	template_name = "accounting_double_entry/group1_form.html"

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:grouplist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})


	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c
		counter = group1.objects.filter(User=self.request.user, Company=c).count() + 1
		form.instance.counter = counter
		return super(group1CreateView, self).form_valid(form)

	def get_form_kwargs(self):
		data = super(group1CreateView, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data

	def get_context_data(self, **kwargs):
		context = super(group1CreateView, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context

class group1UpdateView(ProductExistsRequiredMixin,LoginRequiredMixin,UpdateView):
	model = group1
	form_class  = group1Form
	template_name = "accounting_double_entry/group1_form.html"


	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		group1_details  = get_object_or_404(group1, pk=self.kwargs['pk2'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:groupdetail', kwargs={'pk1':company_details.pk, 'pk2':group1_details.pk,'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		group = get_object_or_404(group1, pk=pk2)
		return group

	def get_form_kwargs(self):
		data = super(group1UpdateView, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk1'])
			)
		return data


	def get_context_data(self, **kwargs):
		context = super(group1UpdateView, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context

def save_all(request,form,template_name,pk, pk3):
	company_details = get_object_or_404(company, pk=pk)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			group1_list = group1.objects.filter(User= request.user, Company=company_details.pk).order_by('-id')
			data['group_list'] = render_to_string('accounting_double_entry/group1_list2.html',{'group1_list':group1_list})
		else:
			data['form_is_valid'] = False
	context = {

		'form':form,
		'company_details' : company_details,
		'selectdatefield_details' : selectdatefield_details
	}
	data['html_form'] = render_to_string(template_name,context,request=request)

	return JsonResponse(data)

@login_required
@product_1_activation
def group_delete_view(request, pk, pk2, pk3):
	data = dict()
	company_details = get_object_or_404(company, pk=pk)
	group = get_object_or_404(group1, pk=pk2)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)

	if request.method == "POST":
		group.delete()
		data['form_is_valid'] = True
		group1_list = group1.objects.filter(User= request.user, Company=company_details.pk).order_by('-id')
		context = {
			'group1_list':group1_list,
			'company_details' : company_details,
			'selectdatefield_details' : selectdatefield_details,
		}
		data['group_list'] = render_to_string('accounting_double_entry/group1_list2.html',context)
	else:
		context = {
			'group':group,
			'company_details' : company_details,
			'selectdatefield_details' : selectdatefield_details,
		}
		data['html_form'] = render_to_string('accounting_double_entry/group1_confirm_delete.html',context,request=request)

	return JsonResponse(data)




################## Views For Ledger Monthly Display ###################################


@login_required
@product_1_activation
def ledger_monthly_detail_view(request, pk, pk2, pk3):
	company_details = get_object_or_404(company, pk=pk)
	ledger1_details = get_object_or_404(ledger1, pk=pk2)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)


	# opening balance
	if (ledger1_details.name == 'Profit & Loss A/c'):
		qsob  = Pl_journal.objects.filter(User=request.user, Company=company_details.pk, By=ledger1_details.pk, Date__gte=ledger1_details.Creation_Date, Date__lte=selectdatefield_details.Start_Date)
		qsob2 = Pl_journal.objects.filter(User=request.user, Company=company_details.pk, To=ledger1_details.pk, Date__gte=ledger1_details.Creation_Date, Date__lte=selectdatefield_details.Start_Date)
	else:
		qsob  = journal.objects.filter(User=request.user, Company=company_details.pk, By=ledger1_details.pk, Date__gte=ledger1_details.Creation_Date, Date__lte=selectdatefield_details.Start_Date)
		qsob2 = journal.objects.filter(User=request.user, Company=company_details.pk, To=ledger1_details.pk, Date__gte=ledger1_details.Creation_Date, Date__lte=selectdatefield_details.Start_Date)

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

	if (ledger1_details.name == 'Profit & Loss A/c'):
		qscb  = Pl_journal.objects.filter(User=request.user, Company=company_details.pk, By=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).annotate(real_total_debit = Case(When(Debit__isnull=True, then=0),default=F('Debit')))
		qscb2 = Pl_journal.objects.filter(User=request.user, Company=company_details.pk, To=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).annotate(real_total_credit = Case(When(Credit__isnull=True, then=0),default=F('Credit')))
		qscb3 = Pl_journal.objects.filter(User=request.user, Company=company_details.pk, By=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).annotate(real_total_debit = Case(When(Debit__isnull=True, then=0),default=F('Debit')))
		qscb4 = Pl_journal.objects.filter(User=request.user, Company=company_details.pk, To=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).annotate(real_total_credit = Case(When(Credit__isnull=True, then=0),default=F('Credit')))	
	
	else:
		qscb  = journal.objects.filter(User=request.user, Company=company_details.pk, By=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).annotate(real_total_debit = Case(When(Debit__isnull=True, then=0),default=F('Debit')))
		qscb2 = journal.objects.filter(User=request.user, Company=company_details.pk, To=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).annotate(real_total_credit = Case(When(Credit__isnull=True, then=0),default=F('Credit')))	
		qscb3 = Pl_journal.objects.filter(User=request.user, Company=company_details.pk, By=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).annotate(real_total_debit = Case(When(Debit__isnull=True, then=0),default=F('Debit')))
		qscb4 = Pl_journal.objects.filter(User=request.user, Company=company_details.pk, To=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).annotate(real_total_credit = Case(When(Credit__isnull=True, then=0),default=F('Credit')))	
	
	date_cursor = selectdatefield_details.Start_Date

	z = 0
	k = 0

	while date_cursor <= selectdatefield_details.End_Date:
		month_partial_total_debit = qscb.filter(Date__month=date_cursor.month).aggregate(partial_total_debit=Sum('real_total_debit'))['partial_total_debit']
		month_partial_total_credit = qscb2.filter(Date__month=date_cursor.month).aggregate(partial_total_credit=Sum('real_total_credit'))['partial_total_credit']
		month_partial_total_debit_pl = qscb3.filter(Date__month=date_cursor.month).aggregate(partial_total_debit=Sum('real_total_debit'))['partial_total_debit']
		month_partial_total_credit_pl = qscb4.filter(Date__month=date_cursor.month).aggregate(partial_total_credit=Sum('real_total_credit'))['partial_total_credit']

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

		if month_partial_total_debit_pl == None:

			month_partial_total_debit_pl = int(0)

			g = month_partial_total_debit_pl 

		else:

			g = month_partial_total_debit_pl

		if month_partial_total_credit_pl == None:

			month_partial_total_credit_pl = int(0)

			h = month_partial_total_credit_pl 

		else:

			h = month_partial_total_credit_pl


		if (ledger1_details.name != 'Profit & Loss A/c'):
			if(ledger1_details.group1_Name.balance_nature == 'Debit'):

				z = z + e + g - f - h 

			else:
				z = z + f + h - e - g 
		else:
			if(ledger1_details.group1_Name.balance_nature == 'Debit'):

				z = z + e  - f  

			else:
				z = z + f  - e  

		k = z + opening_balance

		results[calendar.month_name[date_cursor.month]] =  [e,f,k,g,h]

		date_cursor += dateutil.relativedelta.relativedelta(months=1)

	total_debit = qscb.aggregate(the_sum=Coalesce(Sum('Debit'), Value(0)))['the_sum']
	total_credit = qscb2.aggregate(the_sum=Coalesce(Sum('Credit'), Value(0)))['the_sum']
	total_debit_pl = qscb3.aggregate(the_sum=Coalesce(Sum('Debit'), Value(0)))['the_sum']
	total_credit_pl = qscb4.aggregate(the_sum=Coalesce(Sum('Credit'), Value(0)))['the_sum']


	if (ledger1_details.name != 'Profit & Loss A/c'):
		if(ledger1_details.group1_Name.balance_nature == 'Debit'):

			total1 = total_debit + total_debit_pl - total_credit - total_credit_pl
		else:
			 total1 = total_credit + total_credit_pl - total_debit - total_debit_pl
	else:
		if(ledger1_details.group1_Name.balance_nature == 'Debit'):

			total1 = total_debit - total_credit 
		else:
			 total1 = total_credit - total_debit 


	total = total1 + opening_balance

	inbox = Message.objects.filter(reciever=request.user)
	inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
	send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']


	context = {

		'company_details' 			: company_details,
		'ledger1_details' 			: ledger1_details,
		'selectdatefield_details' 	: selectdatefield_details,
		'total_debit'     			: total_debit,
		'total_credit'   			: total_credit,
		'total_debit_pl'			: total_debit_pl,
		'total_credit_pl'			: total_credit_pl,
		'total'			  			: total,
		'data'			  			: results.items(),
		'opening_balance' 			: opening_balance,
		'inbox'					  	: inbox,
		'inbox_count'			  	: inbox_count,
		'send_count'				: send_count,
		'Todos'			  			: Todo.objects.filter(User=request.user, complete=False),
		'Todos_total' 	  			: Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 


				
	}

	return render(request, 'accounting_double_entry/ledger_monthly.html', context)



################## Views For Ledger Display ###################################


class ledger1ListView(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = ledger1
	paginate_by = 15

	def get_queryset(self):
		return ledger1.objects.filter(User=self.request.user, Company=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super(ledger1ListView, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context

@login_required
@product_1_activation
def ledger1_detail_view(request, pk, pk2, pk3):
	company_details = get_object_or_404(company, pk=pk)
	ledger1_details = get_object_or_404(ledger1, pk=pk2)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)

	# opening balance
	if (ledger1_details.name == 'Profit & Loss A/c'):
		qsob  = Pl_journal.objects.filter(User=request.user, Company=company_details.pk, By=ledger1_details.pk, Date__gte=ledger1_details.Creation_Date, Date__lte=selectdatefield_details.Start_Date)
		qsob2 = Pl_journal.objects.filter(User=request.user, Company=company_details.pk, To=ledger1_details.pk, Date__gte=ledger1_details.Creation_Date, Date__lte=selectdatefield_details.Start_Date)
	else:
		qsob  = journal.objects.filter(User=request.user, Company=company_details.pk, By=ledger1_details.pk, Date__gte=ledger1_details.Creation_Date, Date__lte=selectdatefield_details.Start_Date)
		qsob2 = journal.objects.filter(User=request.user, Company=company_details.pk, To=ledger1_details.pk, Date__gte=ledger1_details.Creation_Date, Date__lte=selectdatefield_details.Start_Date)


	total_debitob = qsob.aggregate(the_sum=Coalesce(Sum('Debit'), Value(0)))['the_sum']
	total_creditob = qsob2.aggregate(the_sum=Coalesce(Sum('Credit'), Value(0)))['the_sum']

	if(ledger1_details.Creation_Date!=selectdatefield_details.Start_Date):
		if(ledger1_details.group1_Name.balance_nature == 'Debit'):
			opening_balance = abs(ledger1_details.Opening_Balance) + abs(total_debitob) - abs(total_creditob)
		else:
			opening_balance = abs(ledger1_details.Opening_Balance) + abs(total_creditob) - abs(total_debitob) 
	else:
		opening_balance = abs(ledger1_details.Opening_Balance)

	# closing balance
	if (ledger1_details.name == 'Profit & Loss A/c'):
		qscb  = Pl_journal.objects.filter(User=request.user, Company=company_details.pk, By=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date)
		qscb2 = Pl_journal.objects.filter(User=request.user, Company=company_details.pk, To=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date)
	else:
		qscb  = journal.objects.filter(User=request.user, Company=company_details.pk, By=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).order_by('Date')
		qscb2 = journal.objects.filter(User=request.user, Company=company_details.pk, To=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).order_by('Date')	
	new   = zip_longest(qscb,qscb2)

	qscb3 = Pl_journal.objects.filter(User=request.user, Company=company_details.pk, By=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date)
	qscb4 = Pl_journal.objects.filter(User=request.user, Company=company_details.pk, To=ledger1_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date)
	new2   = zip_longest(qscb3,qscb4)

	total_debitcb = qscb.aggregate(the_sum=Coalesce(Sum('Debit'), Value(0)))['the_sum']
	total_creditcb = qscb2.aggregate(the_sum=Coalesce(Sum('Credit'), Value(0)))['the_sum']
	total_debitcbpl = qscb3.aggregate(the_sum=Coalesce(Sum('Debit'), Value(0)))['the_sum']
	total_creditcbpl = qscb4.aggregate(the_sum=Coalesce(Sum('Credit'), Value(0)))['the_sum']

	if (ledger1_details.name != 'Profit & Loss A/c'):
		if(ledger1_details.group1_Name.balance_nature == 'Debit'):
			closing_balance = opening_balance + abs(total_debitcb) + abs(total_debitcbpl) - abs(total_creditcb) - abs(total_creditcbpl) 
		else:
			closing_balance = opening_balance + abs(total_creditcb) + abs(total_creditcbpl) - abs(total_debitcb) - abs(total_debitcbpl)
	else:
		if(ledger1_details.group1_Name.balance_nature == 'Debit'):
			closing_balance = opening_balance + abs(total_debitcb) - abs(total_creditcb) 
		else:
			closing_balance = opening_balance + abs(total_creditcb) - abs(total_debitcb) 



	ledger1_detail = ledger1.objects.get(pk=ledger1_details.pk)
	ledger1_detail.Closing_balance = closing_balance
	ledger1_detail.Balance_opening = opening_balance
	ledger1_detail.save(update_fields=['Closing_balance', 'Balance_opening'])

	inbox = Message.objects.filter(reciever=request.user)
	inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
	send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

	context = {

		'company_details' 			: company_details,
		'ledger1_details' 			: ledger1_details,
		'selectdatefield_details' 	: selectdatefield_details,
		'total_debit'     			: abs(total_debitcb),
		'total_credit'    			: abs(total_creditcb),
		'total_debit_pl'			: abs(total_debitcbpl),
		'total_credit_pl'			: abs(total_creditcbpl),
		'journal_debit'   			: qscb,
		'journal_credit'  			: qscb2,
		'n'				  			: new,
		'n2'						: new2,
		'closing_balance' 			: closing_balance,
		'opening_balance' 			: opening_balance,		
		'company_list'    			: company.objects.all(),
		'inbox'					 	: inbox,
		'inbox_count'			  	: inbox_count,
		'send_count'				: send_count,
		'selectdate' 	  			: selectdatefield.objects.filter(User=request.user),
		'Todos'			  			: Todo.objects.filter(User=request.user, complete=False),
		'Todos_total' 	 			: Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 

				
	}	

	return render(request, 'accounting_double_entry/ledger1_details.html', context)


class ledger1CreateView(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class = Ledgerform
	template_name = "accounting_double_entry/ledger1_form.html"

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:ledgerlist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c
		counter = ledger1.objects.filter(User=self.request.user, Company=c).count() + 1
		form.instance.counter = counter
		return super(ledger1CreateView, self).form_valid(form)

	def get_form_kwargs(self):
		data = super(ledger1CreateView, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data

	def get_context_data(self, **kwargs):
		context = super(ledger1CreateView, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context


class ledger1UpdateView(ProductExistsRequiredMixin,LoginRequiredMixin,UpdateView):
	model = ledger1
	form_class = Ledgerform
	template_name = "accounting_double_entry/ledger1_form.html"

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		ledger1_details = get_object_or_404(ledger1, pk=self.kwargs['pk2'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:ledgerdetail', kwargs={'pk':company_details.pk, 'pk2':ledger1_details.pk, 'pk3' : selectdatefield_details.pk})

	def get_object(self):
		pk = self.kwargs['pk']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk)
		ledger = get_object_or_404(ledger1, pk=pk2)
		return ledger

	def get_form_kwargs(self):
		data = super(ledger1UpdateView, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data


	def get_context_data(self, **kwargs):
		context = super(ledger1UpdateView, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context


@login_required
@product_1_activation
def ledger_delete_view(request, pk, pk2, pk3):
	data = dict()
	company_details = get_object_or_404(company, pk=pk)
	ledger = get_object_or_404(ledger1, pk=pk2)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)

	if request.method == "POST":
		ledger.delete()
		data['form_is_valid'] = True
		ledger1_list = ledger1.objects.filter(User= request.user, Company=company_details.pk).order_by('-id')
		context = {
			'ledger1_list':ledger1_list,
			'company_details' : company_details,
			'selectdatefield_details' : selectdatefield_details,
		}
		data['ledger_list'] = render_to_string('accounting_double_entry/ledger_list_2.html',context)
	else:
		context = {
			'ledger':ledger,
			'company_details' : company_details,
			'selectdatefield_details' : selectdatefield_details,
		}
		data['html_form'] = render_to_string('accounting_double_entry/ledger1_confirm_delete.html',context,request=request)

	return JsonResponse(data)


################## Views For journal register Display ###################################
	
class Journal_Register_view(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = journal
	template_name = 'accounting_double_entry/Journal_register.html'

	def get_context_data(self, **kwargs):
		context = super(Journal_Register_view, self).get_context_data(**kwargs)
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['company_details'] = company_details
		context['selectdatefield_details'] = selectdatefield_details

		results = collections.OrderedDict()
		result = journal.objects.filter(User=self.request.user, Company=company_details.pk,Date__gte=selectdatefield_details.Start_Date, Date__lt=selectdatefield_details.End_Date).annotate(real_total = Case(When(Debit__isnull=True, then=0),default=F('Debit')))
		result2 = Pl_journal.objects.filter(User=self.request.user, Company=company_details.pk,Date__gte=selectdatefield_details.Start_Date, Date__lt=selectdatefield_details.End_Date).annotate(real_total = Case(When(Debit__isnull=True, then=0),default=F('Debit')))

		date_cursor = selectdatefield_details.Start_Date

		z = 0

		while date_cursor <= selectdatefield_details.End_Date:
			month_partial_total = result.filter(Date__month=date_cursor.month).aggregate(partial_total=Count('real_total'))['partial_total']
			month_partial_total_pl = result2.filter(Date__month=date_cursor.month).aggregate(partial_total=Count('real_total'))['partial_total']

			if month_partial_total == None:

				month_partial_total = int(0)

				e = month_partial_total

			else:

				e = month_partial_total

			if month_partial_total_pl == None:

				month_partial_total_pl = int(0)

				f = month_partial_total_pl

			else:

				f = month_partial_total_pl

			results[calendar.month_name[date_cursor.month]] = e + f			

			date_cursor += dateutil.relativedelta.relativedelta(months=1)

		total_voucher = result.aggregate(the_sum=Coalesce(Count('real_total'), Value(0)))['the_sum']
		total_voucher_pl = result2.aggregate(the_sum=Coalesce(Count('real_total'), Value(0)))['the_sum']

		total = total_voucher + total_voucher_pl

		context['data'] = results.items()
		context['total'] = total
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context


################## Views For journal Display ###################################


class journalListView(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = journal
	paginate_by = 15

	def get_queryset(self):
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return journal.objects.filter(User=self.request.user, Company=self.kwargs['pk'], Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).order_by('-id')


	def get_context_data(self, **kwargs):
		context = super(journalListView, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['pl_journals'] = Pl_journal.objects.filter(User=self.request.user, Company=company_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).order_by('-id')
		context['journal_list'] = journal.objects.filter(User=self.request.user, Company=company_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).order_by('-id')
		context['new']   = zip_longest(context['pl_journals'],context['journal_list'])
		return context

class DaybookListView(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = journal
	paginate_by = 15

	def get_template_names(self):
		if True:  
			return ['Daybook/daybook.html']
		else:
			return ['accounting_double_entry/journal_list.html']

	def get_queryset(self):
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return journal.objects.filter(User=self.request.user, Company=self.kwargs['pk'], Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).order_by('-id')


	def get_context_data(self, **kwargs):
		context = super(DaybookListView, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['pl_journals'] = Pl_journal.objects.filter(User=self.request.user, Company=company_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).order_by('-id')
		context['journal_list'] = journal.objects.filter(User=self.request.user, Company=company_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).order_by('-id')
		context['new']   = zip_longest(context['pl_journals'],context['journal_list'])
		return context

@login_required
@product_1_activation
def journal_detail(request, pk1, pk2, pk3):
	company_details = get_object_or_404(company, pk=pk1)
	journal_details = get_object_or_404(journal, pk=pk2)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)

	inbox = Message.objects.filter(reciever=request.user)
	inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
	send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

	context = {
		'journal_details'          : journal_details,
		'company_details'          : company_details,
		'inbox'					   : inbox,
		'inbox_count'			   : inbox_count,
		'send_count'			   : send_count,
		'selectdatefield_details'  : selectdatefield_details,
		'Todos'					   : Todo.objects.filter(User=request.user, complete=False),
		'Todos_total'			   : Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
	}
	return render(request, 'accounting_double_entry/journal_details.html', context)



class journalCreateView(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	model = journal
	form_class  = journalForm

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:list', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c
		counter = journal.objects.filter(User=self.request.user, Company=c).count() + 1
		form.instance.counter = counter
		return super(journalCreateView, self).form_valid(form)

	def get_form_kwargs(self):
		data = super(journalCreateView, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data


	def get_context_data(self, **kwargs):
		context = super(journalCreateView, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context

class journalUpdateView(ProductExistsRequiredMixin,LoginRequiredMixin,UpdateView):
	model = journal
	form_class  = journalForm

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		journal_details = get_object_or_404(journal, pk=self.kwargs['pk2'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:detail', kwargs={'pk1':company_details.pk, 'pk2':journal_details.pk, 'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		Journal = get_object_or_404(journal, pk=pk2)
		return Journal

	def get_form_kwargs(self):
		data = super(journalUpdateView, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk1'])
			)
		return data


	def get_context_data(self, **kwargs):
		context = super(journalUpdateView, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context

@login_required
@product_1_activation
def journal_delete_view(request, pk, pk2, pk3):
	data = dict()
	company_details = get_object_or_404(company, pk=pk)
	journals = get_object_or_404(journal, pk=pk2)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)

	if request.method == "POST":
		journals.delete()
		data['form_is_valid'] = True
		journal_list = journal.objects.filter(User= request.user, Company=company_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).order_by('-id')
		context = {
			'journal_list':journal_list,
			'company_details' : company_details,
			'selectdatefield_details' : selectdatefield_details,
		}
		data['journals_list'] = render_to_string('accounting_double_entry/journal_list_2.html',context)
	else:
		context = {
			'journals':journals,
			'company_details' : company_details,
			'selectdatefield_details' : selectdatefield_details,
		}
		data['html_form'] = render_to_string('accounting_double_entry/journal_confirm_delete.html',context,request=request)

	return JsonResponse(data)



################## Views For P&L Journal ###################################

@login_required
@product_1_activation
def pl_journal_detail(request, pk1, pk2, pk3):
	company_details = get_object_or_404(company, pk=pk1)
	pl_details = get_object_or_404(Pl_journal, pk=pk2)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)

	inbox = Message.objects.filter(reciever=request.user)
	inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
	send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

	context = {
		'pl_details'          	   : pl_details,
		'company_details'          : company_details,
		'inbox'					   : inbox,
		'inbox_count'			   : inbox_count,
		'send_count'			   : send_count,
		'selectdatefield_details'  : selectdatefield_details,
		'Todos'					   : Todo.objects.filter(User=request.user, complete=False),
		'Todos_total'			   : Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
	}
	return render(request, 'P&L/pl_details.html', context)



class pl_journalUpdateView(ProductExistsRequiredMixin,LoginRequiredMixin,UpdateView):
	model = Pl_journal
	form_class  = pl_journalForm
	template_name = 'P&L/pl_journal_form.html'

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		pl_journals = get_object_or_404(Pl_journal, pk=self.kwargs['pk2'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:pl_detail', kwargs={'pk1':company_details.pk, 'pk2':pl_journals.pk, 'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		pl_journal = get_object_or_404(Pl_journal, pk=pk2)
		return pl_journal

	def get_form_kwargs(self):
		data = super(pl_journalUpdateView, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk1'])
			)
		return data


	def get_context_data(self, **kwargs):
		context = super(pl_journalUpdateView, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context

@login_required
@product_1_activation
def pl_journal_delete_view(request, pk, pk2, pk3):
	data = dict()
	company_details = get_object_or_404(company, pk=pk)
	pl_journals = get_object_or_404(Pl_journal, pk=pk2)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)

	if request.method == "POST":
		journals.delete()
		data['form_is_valid'] = True
		pl_journals = Pl_journal.objects.filter(User= request.user, Company=company_details.pk, Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).order_by('-id')
		context = {
			'pl_journals':pl_journals,
			'company_details' : company_details,
			'selectdatefield_details' : selectdatefield_details,
		}
		data['pl_journals_list'] = render_to_string('accounting_double_entry/journal_list_2.html',context)
	else:
		context = {
			'pl_journals':pl_journals,
			'company_details' : company_details,
			'selectdatefield_details' : selectdatefield_details,
		}
		data['html_form'] = render_to_string('P&L/pl_journal_confirm_delete.html',context,request=request)

	return JsonResponse(data)


################## Views For Multijournal ###################################


class Multijournal_listview(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = Multijournaltotal
	template_name = 'Multijournal/multi_journal_list.html'
	paginate_by = 15


	def get_queryset(self):
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return self.model.objects.filter(User=self.request.user, Company=self.kwargs['pk'], Date__gte=selectdatefield_details.Start_Date, Date__lte=selectdatefield_details.End_Date).order_by('-id')

	def get_context_data(self, **kwargs):
		context = super(Multijournal_listview, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context

@product_1_activation
def multijournal_detail(request, pk, pk2, pk3):
	company_details = get_object_or_404(company, pk=pk)
	multijournal_details = get_object_or_404(Multijournaltotal, pk=pk2)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)
	Multijournals = Multijournal.objects.filter(total=multijournal_details.pk)

	inbox = Message.objects.filter(reciever=self.request.user)
	inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
	send_count = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']



	context = {

		'multijournal_details'     	: multijournal_details,
		'company_details'          	: company_details,
		'selectdatefield_details'  	: selectdatefield_details,
		'inbox'					  	: inbox,
		'inbox_count'			 	: inbox_count,
		'send_count'				: send_count,
		'Multijournals'            	: Multijournals,
		'Todos'					  	: Todo.objects.filter(User=request.user, complete=False),
		'Todos_total' 			  	: Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
	}
	return render(request, 'Multijournal/multi_journal_details.html', context)


class Multijournal_createview(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = MultijournaltotalForm
	template_name = 'Multijournal/multi_journal_form.html'


	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:multijournallist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def get_context_data(self, **kwargs):
		context = super(Multijournal_createview, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		if self.request.POST:
			context['multijournalformset'] = Multijournal_formSet(self.request.POST)
		else:
			context['multijournalformset'] = Multijournal_formSet()
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context

	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c
		context = self.get_context_data()
		multijournalformset = context['multijournalformset']
		with transaction.atomic():
			self.object = form.save()
			if multijournalformset.is_valid():
				multijournalformset.instance = self.object
				multijournalformset.save()
		return super(Multijournal_createview, self).form_valid(form)

	def get_form_kwargs(self):
		data = super(Multijournal_createview, self).get_form_kwargs()
		if self.request.POST:
			multijournalformset = Multijournal_formSet(self.request.POST)
		else:
			multijournalformset = Multijournal_formSet()
		if multijournalformset.is_valid():
			data.update(
				User=self.request.user,
				Company=company.objects.get(pk=self.kwargs['pk'])
				)
		return data



class Multijournal_updateview(ProductExistsRequiredMixin,LoginRequiredMixin,UpdateView):
	model = Multijournaltotal
	form_class  = MultijournaltotalForm
	template_name = 'Multijournal/multi_journal_form.html'


	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		multijournal_details = get_object_or_404(Multijournaltotal, pk=pk2)
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:multijournaldetail', kwargs={'pk1':company_details.pk, 'pk2':multijournal_details.pk,'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		multijournaltotal = get_object_or_404(Multijournaltotal, pk=pk2)
		return multijournaltotal

	def get_context_data(self, **kwargs):
		context = super(Multijournal_updateview, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		multijournal_details = get_object_or_404(Multijournaltotal, pk=self.kwargs['pk2'])
		total = Multijournal.objects.get(total=multijournal_details.pk)
		Multijournal_formSet = inlineformset_factory(Multijournaltotal, Multijournal,form=MultijournalForm, extra=6)	
		multijournalformset = Multijournal_formSet(self.request.POST or None, instance=total)	
		context['multijournalformset'] = multijournalformset
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context

	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk']) 
		form.instance.Company = c
		context = self.get_context_data()
		multijournalformset = context['multijournalformset']
		with transaction.atomic():
			self.object = form.save()
			if multijournalformset.is_valid():
				multijournalformset.instance = self.object
				multijournalformset.save()
		return super(Multijournal_createview, self).form_valid(form)


# @login_required
# def Multijournal_updateview(request,pk,pk2,pk3):
# 	company_details = get_object_or_404(company, pk=pk)
# 	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)
# 	multijournal_details = get_object_or_404(Multijournaltotal, pk=pk2)

# 	total = Multijournal.objects.filter(total=multijournal_details.pk)
# 	Multijournal_formSet = inlineformset_factory(Multijournaltotal, Multijournal,form=MultijournalForm, extra=6)

# 	if request.method == "POST":
# 		multijournalformset = Multijournal_formSet(request.POST or None, instance=total)

# 		if multijournalformset.is_valid():
# 			instances = multijournalformset.save(commit=False)
# 			for instance in instances:
# 				m = Multijournaltotal.objects.get(total=multijournal_details.pk)
# 				instance.total = m
# 				instance.save()
# 				return HttpResponseRedirect(total.get_absolute_url())

# 	else:
# 		multijournalformset = Multijournal_formSet()

# 	context = {

# 		'company_details' 		  : company_details,
# 		'selectdatefield_details' : selectdatefield_details,
# 		'multijournal_details'	  : multijournal_details,
# 		'multijournalformset'	  : multijournalformset
# 	}

# 	return render(request, 'Multijournal/multi_journal_form.html', context)

class multijournal_deleteview(ProductExistsRequiredMixin,LoginRequiredMixin,DeleteView):
	model = Multijournaltotal
	template_name = 'Multijournal/multijournal_delete.html'

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:multijournallist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		multijournal = get_object_or_404(Multijournaltotal, pk=pk2)
		return multijournal

	def get_context_data(self, **kwargs):
		context = super(multijournal_deleteview, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		multijournal_details = get_object_or_404(Multijournaltotal, pk=self.kwargs['pk2'])
		context['multijournal_details'] = multijournal_details	
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context	


################## Views For Multiplae Journal objects ###################################	

class Multiplae_Journal_objectsCreateView(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = Multijournal
	template_name = 'Multijournal/multi_journal_form.html'

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:multijournallist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})


	def get_form_kwargs(self):
		data = super(Multiplae_Journal_objectsCreateView, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data


	def get_context_data(self, **kwargs):
		context = super(Multiplae_Journal_objectsCreateView, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context



################## Views For Daterange Display ###################################

def save_all(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			selectdatefield_details = selectdatefield.objects.filter(User=request.user)
			data['selectdatefields_list'] = render_to_string('company/company_list_2.html',{'selectdatefield_details':selectdatefield_details})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

def selectdate_create(request):
	if request.method == 'POST':
		form = DateRangeForm(request.POST)
		if form.is_valid():
			form.instance.User = request.user
			form.save()
	else:
		form = DateRangeForm()
	return save_all(request,form,"company/selectdate_create.html")

def selectdate_update(request,pk):
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk)
	if request.method == 'POST':
		form = DateRangeForm(request.POST,instance=selectdatefield_details)
	else:
		form = DateRangeForm(instance=selectdatefield_details)
	return save_all(request,form,'company/selectdate_update.html')



################## Views For Payment ###################################

class Payment_createview(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = PaymentForm
	success_message = "%(account)s is submitted successfully"
	template_name = 'Payments/payment_form.html'


	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:paymentcreate', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def get_context_data(self, **kwargs):
		context = super(Payment_createview, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		if self.request.POST:
			context['payments'] = Payment_formSet(self.request.POST)
		else:
			context['payments'] = Payment_formSet()
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['successful_submit'] = True
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context

	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c
		counter = Payment.objects.filter(User=self.request.user, Company=c).count() + 1
		form.instance.counter = counter
		context = self.get_context_data()
		payments = context['payments']
		with transaction.atomic():
			self.object = form.save()
			if payments.is_valid():
				payments.instance = self.object
				payments.save()
		return super(Payment_createview, self).form_valid(form)

	def get_form_kwargs(self):
		data = super(Payment_createview, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data

class ParticularspaymentCreateView(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = ParticularspaymentForm
	template_name = 'Payments/payment_form.html'

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:paymentcreate', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})


	def get_form_kwargs(self):
		data = super(ParticularspaymentCreateView, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data


	def get_context_data(self, **kwargs):
		context = super(ParticularspaymentCreateView, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context


################## Views For Receipt ###################################

class Receipt_createview(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = ReceiptForm
	success_message = "%(account)s is submitted successfully"
	template_name = 'Receipt/receipt_form.html'


	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:receiptcreate', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def get_context_data(self, **kwargs):
		context = super(Receipt_createview, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		if self.request.POST:
			context['receipts'] = Receipt_formSet(self.request.POST)
		else:
			context['receipts'] = Receipt_formSet()
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c
		counter = Receipt.objects.filter(User=self.request.user, Company=c).count() + 1
		form.instance.counter = counter
		context = self.get_context_data()
		receipts = context['receipts']
		with transaction.atomic():
			self.object = form.save()
			if receipts.is_valid():
				receipts.instance = self.object
				receipts.save()
		return super(Receipt_createview, self).form_valid(form)

	def get_form_kwargs(self):
		data = super(Receipt_createview, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data

class ParticularspayreceiptCreateView(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = ParticularsreceiptForm
	template_name = 'Receipt/receipt_form.html'

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:receiptcreate', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})


	def get_form_kwargs(self):
		data = super(ParticularspayreceiptCreateView, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data


	def get_context_data(self, **kwargs):
		context = super(ParticularspayreceiptCreateView, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

################## Views For Contra ###################################

class Contra_createview(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = ContraForm
	success_message = "%(account)s is submitted successfully"
	template_name = 'Contra/contra_form.html'


	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:contracreate', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def get_context_data(self, **kwargs):
		context = super(Contra_createview, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		if self.request.POST:
			context['contras'] = Contra_formSet(self.request.POST, queryset=Particularscontra.objects.filter(contra__User=self.request.user, contra__Company=company_details.pk, particular__User=self.request.user, particular__Company=company_details.pk))
		else:
			context['contras'] = Contra_formSet()
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c
		counter = Contra.objects.filter(User=self.request.user, Company=c).count() + 1
		form.instance.counter = counter
		context = self.get_context_data()
		contras = context['contras']
		with transaction.atomic():
			self.object = form.save()
			if contras.is_valid():
				contras.instance = self.object
				contras.save()
		return super(Contra_createview, self).form_valid(form)

	def get_form_kwargs(self):
		data = super(Contra_createview, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data

class ParticularspaycontraCreateView(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = ParticularscontraForm
	template_name = 'Contra/contra_form.html'

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('accounting_double_entry:contracreate', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})


	def get_form_kwargs(self):
		data = super(ParticularspaycontraCreateView, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data


	def get_context_data(self, **kwargs):
		context = super(ParticularspaycontraCreateView, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

################## Views For Profit & Loss Display ###################################

@login_required
@product_1_activation
def profit_and_loss_condensed_view(request,pk,pk3):
	company_details = get_object_or_404(company, pk=pk)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)

	# closing stock
	qs = Stockdata.objects.filter(User=request.user, Company=company_details.pk, Date__lte=selectdatefield_details.End_Date)
	qs = qs.annotate(
    		sales_sum = Subquery(
    			Stock_Total_sales.objects.filter(
    				stockitem = OuterRef('pk')
    				).values(
    					'stockitem'
    				).annotate(
    					the_sum = Sum('Quantity')
    				).values('the_sum')
    			),
    		purchase_sum = Coalesce(Sum('purchasestock__Quantity_p'),0),
    		purchase_tot = Coalesce(Sum('purchasestock__Total_p'),0)
		)

	qs1 = qs.annotate(
	    	difference = ExpressionWrapper(F('purchase_sum') - F('sales_sum'), output_field=DecimalField()),
	    	total = ExpressionWrapper((F('purchase_tot') / F('purchase_sum')) * (F('purchase_sum') - F('sales_sum')), output_field=DecimalField())
		) 

	qs2 = qs1.aggregate(the_sum=Coalesce(Sum('total'), Value(0)))['the_sum']

	# opening stock
	qo = Stockdata.objects.filter(User=request.user, Company=company_details.pk, Date__lte=selectdatefield_details.Start_Date)
	qo = qo.annotate(
    		sales_sum = Subquery(
    			Stock_Total_sales.objects.filter(
    				stockitem = OuterRef('pk')
    				).values(
    					'stockitem'
    				).annotate(
    					the_sum = Sum('Quantity')
    				).values('the_sum')
    			),
    		purchase_sum = Coalesce(Sum('purchasestock__Quantity_p'),0),
    		purchase_tot = Coalesce(Sum('purchasestock__Total_p'),0)
		)
	qo1 = qo.annotate(
    	difference = ExpressionWrapper(F('purchase_sum') - F('sales_sum'), output_field=DecimalField()),
    	total = ExpressionWrapper((F('purchase_tot') / F('purchase_sum')) * (F('purchase_sum') - F('sales_sum')), output_field=DecimalField())
		) 

	qo2 = qo1.aggregate(the_sum=Coalesce(Sum('total'), Value(0)))['the_sum']

	ld = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Purchase Accounts', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	ldc = ld.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	ldd = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Direct Expenses', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	lddt = ldd.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	ldii = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Direct Incomes', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	lddi = ldii.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	lds = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Sales Account', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	ldsc = lds.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	lde = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Indirect Expense', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	ldse = lde.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	ldi = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Indirect Income', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	ldsi = ldi.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	# qo1 means opening stock exists

	# lddt = Direct Expenses
	# lddi = Direct Incomes


	if  lddi < 0 and lddt < 0:
		gp = abs(ldsc) + abs(qs2) + abs(lddt) - abs(qo2) - abs(ldc) - abs(lddi)
	elif lddt < 0:
		gp = abs(ldsc) + abs(qs2) + abs(lddi) + abs(lddt) - abs(qo2) - abs(ldc)
	elif lddi < 0:
		gp = abs(ldsc) + abs(qs2) - abs(lddi) - abs(qo2) - abs(ldc) - abs(lddt)
	else:	
		gp = abs(ldsc) + abs(qs2) + abs(lddi) - abs(qo2) - abs(ldc) - abs(lddt)


	if gp >=0:
		if  lddi < 0 and lddt < 0:
			tradingp  =  abs(qo2) + abs(ldc) + (gp) + abs(lddi)
			tgp = abs(qs2) + abs(ldsc) + abs(lddt) 
		elif lddt < 0:
			tradingp  =  abs(qo2) + abs(ldc) + (gp)
			tgp = abs(qs2) + abs(lddi) + abs(ldsc) + abs(lddt)
		elif lddi < 0:
			tradingp  =  abs(qo2) + abs(ldc) + abs(lddt) + (gp) + abs(lddi)
			tgp = abs(qs2) + abs(ldsc)
 						
		else:
			tradingp  =  abs(qo2) + abs(ldc) + abs(lddt) + (gp)
			tgp = abs(qs2) + abs(lddi) + abs(ldsc) 

	else: # gp <0
		if  lddi < 0 and lddt < 0:
			tradingp =  abs(qo2) + abs(ldc) + abs(lddi) 
			tgp = abs(qs2) + abs(ldsc) + abs(gp) + abs(lddt)
		elif lddt < 0:
			tradingp =  abs(qo2) + abs(ldc) 
			tgp = abs(qs2) + abs(lddi) + abs(ldsc) + abs(gp) + abs(lddt)
		elif lddi < 0:
			tradingp =  abs(qo2) + abs(ldc) + abs(lddt) + abs(lddi) 
			tgp = abs(qs2) + abs(ldsc) + abs(gp) 	
  					
		else:
			tradingp =  abs(qo2) + abs(ldc) + abs(lddt) 
			tgp = abs(qs2) + abs(lddi) + abs(ldsc) + abs(gp) 

	
	# ldse = Indirect Expense
	# ldsi = Indirect Income


	if gp >=0:
		if ldsi < 0 and ldse < 0:
			np = (gp) + abs(ldse) - abs(ldsi)
		elif ldse < 0:
			np = (gp) + abs(ldsi) + abs(ldse)
		elif ldsi < 0:
			np = (gp) - abs(ldsi) - abs(ldse)
		else:
			np = (gp) + abs(ldsi) - abs(ldse)
	else:
		if ldsi < 0 and ldse < 0:
			np = abs(ldse) - abs(ldsi) - abs(gp) 
		elif ldsi < 0:
			np = abs(ldsi) + abs(ldse) + abs(gp)
		elif ldse < 0:
			np = abs(ldsi) + abs(ldse) - abs(gp)
		else:
			np = abs(ldsi) - abs(ldse) - abs(gp) 


	# ldse = Indirect Expense
	# ldsi = Indirect Income
 


	if gp >= 0:
		if np >= 0:
			if ldsi < 0 and ldse < 0:
				tp = abs(ldsi) + np
				tc = abs(ldse) + (gp)
			elif ldsi < 0:
				tp = abs(ldsi) + np + abs(ldse)  
				tc = (gp)
			elif ldse < 0:
				tp = np
				tc = abs(ldsi) + (gp) + abs(ldse)				
			else:
				tp = abs(ldse) + np
				tc = abs(ldsi) + (gp)
		else:
			if ldsi < 0 and ldse < 0:
				tp = abs(ldsi)  
				tc = gp + np + abs(ldse)
			elif ldsi < 0:
				tp = abs(ldse)  + abs(ldsi) 
				tc = gp + np
			elif ldse < 0:
				tp =  0
				tc = gp + np + abs(ldsi) + abs(ldse)																								
			else:
				tp = abs(ldse) 
				tc = gp + np + abs(ldsi)
	else: # gp<0
		if np >= 0:
			if ldsi < 0 and ldse < 0:
				tp = abs(ldsi) + np + abs(gp)
				tc = abs(ldse) 
			elif ldsi < 0:
				tp = abs(ldse) + np + abs(gp) + abs(ldsi)
				tc = 0	
			elif ldse < 0:
				tp = np + abs(gp)
				tc = abs(ldsi) + abs(ldse) 							
			else:
				tp = abs(ldse) + np + abs(gp)
				tc = abs(ldsi) 
		else:
			if ldsi < 0 and ldse < 0:
				tp = abs(ldsi) + abs(gp)
				tc = abs(np) + abs(ldse)
			elif ldsi < 0:
				tp = abs(ldse) + abs(gp) + abs(ldsi)
				tc = abs(np) 
			elif ldse < 0:
				tp = abs(gp)
				tc = abs(np) + abs(ldsi) + abs(ldse)				
			else:
				tp = abs(ldse) + abs(gp)
				tc = abs(np) + abs(ldsi)

	inbox = Message.objects.filter(reciever=request.user)
	inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
	send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

	context = {

		'company_details' : company_details,
		'selectdatefield_details' : selectdatefield_details,
		'closing_stock' : qs2,
		'each_closing_stock' : qs1.values(),
		'opening_stock': qo2,
		'each_opening_stock' : qo1.values(),
		'purchase_ledger' : ld,
		'total_purchase_ledger' : ldc,
		'sales_ledger' : lds,
		'total_sales_ledger' : ldsc,
		'indirectexp_ledger' : lde,
		'total_indirectexp_ledger' : ldse,
		'indirectinc_ledger' : ldi,
		'total_indirectinc_ledger' : ldsi,
		'total_direct_expenses': lddt,
		'direct_expenses': ldd,
		'total_direct_incomes': lddi,
		'direct_incomes': ldii,
		'gross_profit' : gp,
		'nett_profit' : np,
		'tradingprofit': tradingp,
		'tradingprofit2': tgp,
		'totalpl' : tp,
		'totalplright' : tc,
		'inbox'			: inbox,
		'inbox_count'	: inbox_count,
		'send_count'	: send_count,
		'Todos'		   : Todo.objects.filter(User=request.user, complete=False),
		'Todos_total'  : Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'],
	}

	return render(request, 'accounting_double_entry/P&Lcondnsd.html', context)








################## Views For Trial Balance Display ###################################

@login_required
@product_1_activation
def trial_balance_condensed_view(request,pk,pk3):
	company_details = get_object_or_404(company, pk=pk)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)

	# opening stock
	qo = Stockdata.objects.filter(User=request.user, Company=company_details.pk, Date__lte=selectdatefield_details.Start_Date)
	qo = qo.annotate(
    		sales_sum = Subquery(
    			Stock_Total_sales.objects.filter(
    				stockitem = OuterRef('pk')
    				).values(
    					'stockitem'
    				).annotate(
    					the_sum = Sum('Quantity')
    				).values('the_sum')
    			),
    		purchase_sum = Coalesce(Sum('purchasestock__Quantity_p'),0),
    		purchase_tot = Coalesce(Sum('purchasestock__Total_p'),0)
		)
	qo1 = qo.annotate(
    	difference = ExpressionWrapper(F('purchase_sum') - F('sales_sum'), output_field=DecimalField()),
    	total = ExpressionWrapper((F('purchase_tot') / F('purchase_sum')) * (F('purchase_sum') - F('sales_sum')), output_field=DecimalField())
		) 

	qo2 = qo1.aggregate(the_sum=Coalesce(Sum('total'), Value(0)))['the_sum']

	groups = group1.objects.filter(User=request.user, Company=company_details.pk, ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date).exclude(group_Name__icontains='Primary')
	groups_cb = groups.annotate(
				closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0),
				opening = Coalesce(Sum('ledgergroups__Balance_opening'), 0),
			)

	# groups with debit balance nature
	groupsdebit = group1.objects.filter(User=request.user, Company=company_details.pk, balance_nature__icontains='Debit', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date).exclude(group_Name__icontains='Primary')
	groups_cbc = groupsdebit.annotate(
				closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0)).filter(closing__gt = 0)

	groupcbl = groupsdebit.annotate(
			closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0)).filter(closing__lt = 0)

	group_ob = groupsdebit.annotate(
			opening = Coalesce(Sum('ledgergroups__Balance_opening'), 0)).filter(opening__gt = 0)

	group_obl = groupsdebit.annotate(
			opening = Coalesce(Sum('ledgergroups__Balance_opening'), 0)).filter(opening__lt = 0)

	posdebcb = groups_cbc.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	negdbcl = groupcbl.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	posdebob = group_ob.aggregate(the_sum=Coalesce(Sum('opening'), Value(0)))['the_sum']
	negdebob = group_obl.aggregate(the_sum=Coalesce(Sum('opening'), Value(0)))['the_sum']


	# groups with credit balance nature
	groupscredit = group1.objects.filter(User=request.user, Company=company_details.pk, balance_nature__icontains='Credit', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date).exclude(group_Name__icontains='Primary')

	groups_ccb = groupscredit.annotate(
				closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0)).filter(closing__gt = 0)

	groupcbcl = groupscredit.annotate(
			closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0)).filter(closing__lt = 0)

	group_cob = groupscredit.annotate(
			opening = Coalesce(Sum('ledgergroups__Balance_opening'), 0)).filter(opening__gt = 0)

	group_ocbl = groupscredit.annotate(
			opening = Coalesce(Sum('ledgergroups__Balance_opening'), 0)).filter(opening__lt = 0)


	poscrcl = groups_ccb.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	necrcl = groupcbcl.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	pocrob = group_cob.aggregate(the_sum=Coalesce(Sum('opening'), Value(0)))['the_sum']
	necrob = group_ocbl.aggregate(the_sum=Coalesce(Sum('opening'), Value(0)))['the_sum']


	total_debit_closing = posdebcb + abs(necrcl)
	total_credit_closing = poscrcl + abs(negdbcl)

	total_debit_opening = posdebob + abs(necrob)
	total_credit_opening = pocrob + abs(negdebob)

	inbox = Message.objects.filter(reciever=request.user)
	inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
	send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']



	context = {

		'company_details' : company_details,
		'selectdatefield_details' : selectdatefield_details,
		'opening_stock' : qo2,
		'groups' : groups,
		'groups_closing' : groups_cb,

		'total_debit_closing' : total_debit_closing,
		'total_debit_opening' : total_debit_opening,

		'inbox'			: inbox,
		'inbox_count'	: inbox_count,
		'send_count'	: send_count,

		'total_credit_closing' : total_credit_closing,
		'total_credit_opening' : total_credit_opening,
		'Todos'		   : Todo.objects.filter(User=request.user, complete=False),
		'Todos_total'  :Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 

	}

	return render(request, 'accounting_double_entry/trial_bal_condendensed.html', context)



################## Views For Balance Sheet Display ###################################

@login_required
@product_1_activation
def balance_sheet_condensed_view(request,pk,pk3):
	company_details = get_object_or_404(company, pk=pk)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)

	# Branch/Divisions
	groupbrch = group1.objects.filter(User=request.user, Company=company_details.pk, Master__group_Name__icontains='Branch/Divisions', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date)
	groupbrchcb = groupbrch.annotate(
			closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0))

	groupbrchtcb = groupbrchcb.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	
	ledbrch = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Branch/Divisions', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)	
	ledbrchcb = ledbrch.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	total_brchtcb = ledbrchcb + groupbrchtcb

	# Capital A/c 
	groupcach = group1.objects.filter(User=request.user, Company=company_details.pk, Master__group_Name__icontains='Capital A/c', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date)
	groupcacb = groupbrch.annotate(
			closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0))

	groupcstcb = groupcacb.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	
	ledcah = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Capital A/c', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)	
	ledcacb = ledcah.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	total_cacb = groupcstcb + ledcacb


	# Current Liabilities

	groupculiach = group1.objects.filter(User=request.user, Company=company_details.pk, Master__group_Name__icontains='Current Liabilities', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date)
	groupculiacb = groupculiach.annotate(
			closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0))

	groupculiagbcb = groupculiacb.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	
	ledculiah = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Current Liabilities', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)	
	ledculiacb = ledculiah.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	total_culiacb = groupculiagbcb + ledculiacb

	# Loans (Liability)

	grouplonch = group1.objects.filter(User=request.user, Company=company_details.pk, Master__group_Name__icontains='Loans (Liability)', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date)
	grouploncb = grouplonch.annotate(
			closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0))

	grouplacb = grouploncb.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	
	ledlonh = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Loans (Liability)', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)	
	ledloncb = ledlonh.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	total_loncb = grouplacb + ledloncb

	# Suspense A/c

	groupsusch = group1.objects.filter(User=request.user, Company=company_details.pk, Master__group_Name__icontains='Suspense A/c', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date)
	groupsuscb = groupsusch.annotate(
			closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0))

	groupsustcb = groupsuscb.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	
	ledsusnh = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Suspense A/c', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)	
	ledsuscb = ledsusnh.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	total_suscb = groupsustcb + ledsuscb	


	# closing stock
	qs = Stockdata.objects.filter(User=request.user, Company=company_details.pk, Date__lte=selectdatefield_details.End_Date)
	qs = qs.annotate(
    		sales_sum = Subquery(
    			Stock_Total_sales.objects.filter(
    				stockitem = OuterRef('pk')
    				).values(
    					'stockitem'
    				).annotate(
    					the_sum = Sum('Quantity')
    				).values('the_sum')
    			),
    		purchase_sum = Coalesce(Sum('purchasestock__Quantity_p'),0),
    		purchase_tot = Coalesce(Sum('purchasestock__Total_p'),0)
		)

	qs1 = qs.annotate(
	    	difference = ExpressionWrapper(F('purchase_sum') - F('sales_sum'), output_field=DecimalField()),
	    	total = ExpressionWrapper((F('purchase_tot') / F('purchase_sum')) * (F('purchase_sum') - F('sales_sum')), output_field=DecimalField())
		) 

	qs2 = qs1.aggregate(the_sum=Coalesce(Sum('total'), Value(0)))['the_sum']

	# opening stock
	qo = Stockdata.objects.filter(User=request.user, Company=company_details.pk, Date__lte=selectdatefield_details.Start_Date)
	qo = qo.annotate(
    		sales_sum = Subquery(
    			Stock_Total_sales.objects.filter(
    				stockitem = OuterRef('pk')
    				).values(
    					'stockitem'
    				).annotate(
    					the_sum = Sum('Quantity')
    				).values('the_sum')
    			),
    		purchase_sum = Coalesce(Sum('purchasestock__Quantity_p'),0),
    		purchase_tot = Coalesce(Sum('purchasestock__Total_p'),0)
		)
	qo1 = qo.annotate(
    	difference = ExpressionWrapper(F('purchase_sum') - F('sales_sum'), output_field=DecimalField()),
    	total = ExpressionWrapper((F('purchase_tot') / F('purchase_sum')) * (F('purchase_sum') - F('sales_sum')), output_field=DecimalField())
		) 

	qo2 = qo1.aggregate(the_sum=Coalesce(Sum('total'), Value(0)))['the_sum']



	
# Current Assets
	groupcurastch = group1.objects.filter(User=request.user, Company=company_details.pk, Master__group_Name__icontains='Current Assets', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date)
	groupcurastcb = groupcurastch.annotate(
			closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0))

	groupcurascb = groupcurastcb.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	
	ledcurastnh = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Current Assets', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)	
	ledcurastcb = ledcurastnh.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	total_curastcb = groupcurascb + ledcurastcb	 + qs2

	# Fixed Asset

	groupfxdastch = group1.objects.filter(User=request.user, Company=company_details.pk, Master__group_Name__icontains='Fixed Assets', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date)
	groupfxdastcb = groupfxdastch.annotate(
			closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0))

	groupfxdascb = groupfxdastcb.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	
	ledfxdastnh = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Fixed Assets', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)	
	ledfxdastcb = ledfxdastnh.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	total_fxdastcb = groupfxdascb + ledfxdastcb	 



	# Profit & Loss A/c Calculations



	ld = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Purchase Accounts', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	ldc = ld.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	ldd = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Direct Expenses', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	lddt = ldd.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	ldii = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Direct Incomes', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	lddi = ldii.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	lds = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Sales Account', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	ldsc = lds.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	lde = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Indirect Expense', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	ldse = lde.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	ldi = ledger1.objects.filter(User=request.user, Company=company_details.pk, group1_Name__group_Name__icontains='Indirect Income', Creation_Date__gte=selectdatefield_details.Start_Date, Creation_Date__lte=selectdatefield_details.End_Date)
	ldsi = ldi.aggregate(the_sum=Coalesce(Sum('Closing_balance'), Value(0)))['the_sum']

	# qo1 means opening stock exists

	# lddt = Direct Expenses
	# lddi = Direct Incomes


	if  lddi < 0 and lddt < 0:
		gp = abs(ldsc) + abs(qs2) + abs(lddt) - abs(qo2) - abs(ldc) - abs(lddi)
	elif lddt < 0:
		gp = abs(ldsc) + abs(qs2) + abs(lddi) + abs(lddt) - abs(qo2) - abs(ldc)
	elif lddi < 0:
		gp = abs(ldsc) + abs(qs2) - abs(lddi) - abs(qo2) - abs(ldc) - abs(lddt)
	else:	
		gp = abs(ldsc) + abs(qs2) + abs(lddi) - abs(qo2) - abs(ldc) - abs(lddt)



	if gp >=0:
		if ldsi < 0 and ldse < 0:
			np = (gp) + abs(ldse) - abs(ldsi)
		elif ldse < 0:
			np = (gp) + abs(ldsi) + abs(ldse)
		elif ldsi < 0:
			np = (gp) - abs(ldsi) - abs(ldse)
		else:
			np = (gp) + abs(ldsi) - abs(ldse)
	else:
		if ldsi < 0 and ldse < 0:
			np = abs(ldse) - abs(ldsi) - abs(gp) 
		elif ldsi < 0:
			np = abs(ldsi) + abs(ldse) + abs(gp)
		elif ldse < 0:
			np = abs(ldsi) + abs(ldse) - abs(gp)
		else:
			np = abs(ldsi) - abs(ldse) - abs(gp) 


	# From Trial Balance

	# groups with debit balance nature
	groupsdebit = group1.objects.filter(User=request.user, Company=company_details.pk, balance_nature__icontains='Debit', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date).exclude(group_Name__icontains='Primary')
	groups_cbc = groupsdebit.annotate(
				closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0)).filter(closing__gt = 0)

	groupcbl = groupsdebit.annotate(
			closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0)).filter(closing__lt = 0)


	posdebcb = groups_cbc.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	negdbcl = groupcbl.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']



	# groups with credit balance nature
	groupscredit = group1.objects.filter(User=request.user, Company=company_details.pk, balance_nature__icontains='Credit', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date).exclude(group_Name__icontains='Primary')

	groups_ccb = groupscredit.annotate(
				closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0)).filter(closing__gt = 0)

	groupcbcl = groupscredit.annotate(
			closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0)).filter(closing__lt = 0)

	poscrcl = groups_ccb.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	necrcl = groupcbcl.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']


	total_debit_closing = posdebcb + abs(necrcl) + qo2
	total_credit_closing = poscrcl + abs(negdbcl)	




	if total_brchtcb < 0 and total_cacb < 0 and total_culiacb < 0 and total_loncb < 0 and total_suscb < 0 and total_curastcb < 0 and total_fxdastcb < 0:
		total_liabilities = abs(total_curastcb) + abs(total_fxdastcb)
		total_asset = abs(total_brchtcb) + abs(total_cacb) + abs(total_culiacb) + abs(total_loncb) + abs(total_suscb)		
	
	elif total_brchtcb < 0:
		total_liabilities = total_cacb + total_culiacb + total_loncb + total_suscb
		total_asset = abs(total_brchtcb) + total_curastcb + total_fxdastcb

	elif total_brchtcb < 0 and total_fxdastcb < 0:
		total_liabilities = total_cacb + total_culiacb + total_loncb + total_suscb + abs(total_fxdastcb)
		total_asset = abs(total_brchtcb) + total_curastcb 

	elif total_brchtcb < 0 and total_curastcb < 0:
		total_liabilities = total_cacb + total_culiacb + total_loncb + total_suscb + abs(total_curastcb)
		total_asset = abs(total_brchtcb) + total_fxdastcb

	elif total_cacb < 0:
		total_liabilities = total_brchtcb + total_culiacb + total_loncb + total_suscb
		total_asset = total_curastcb + total_fxdastcb + abs(total_cacb)

	elif total_cacb < 0 and total_fxdastcb < 0:	
		total_liabilities =  total_brchtcb + total_culiacb + total_loncb + total_suscb + abs(total_fxdastcb)
		total_asset = abs(total_cacb) + total_curastcb 

	elif total_cacb < 0 and total_curastcb < 0:
		total_liabilities =  total_brchtcb + total_culiacb + total_loncb + total_suscb + abs(total_curastcb)
		total_asset = abs(total_cacb) + total_fxdastcb

	elif total_culiacb < 0:
		total_liabilities = total_brchtcb + total_cacb + total_loncb + total_suscb
		total_asset = total_curastcb + total_fxdastcb + abs(total_culiacb)

	elif total_culiacb < 0 and total_fxdastcb < 0:	
		total_liabilities =  total_brchtcb + total_cacb + total_loncb + total_suscb + abs(total_fxdastcb)
		total_asset = abs(total_culiacb) + total_curastcb 

	elif total_culiacb < 0 and total_curastcb < 0:
		total_liabilities =  total_brchtcb + total_cacb + total_loncb + total_suscb + abs(total_curastcb)
		total_asset = abs(total_culiacb) + total_fxdastcb

	elif total_loncb < 0:
		total_liabilities = total_brchtcb + total_cacb + total_culiacb + total_suscb
		total_asset = total_curastcb + total_fxdastcb + abs(total_loncb)

	elif total_loncb < 0 and total_fxdastcb < 0:	
		total_liabilities =  total_brchtcb + total_cacb + total_culiacb + total_suscb + abs(total_fxdastcb)
		total_asset = abs(total_loncb) + total_curastcb 

	elif total_loncb < 0 and total_curastcb < 0:
		total_liabilities =  total_brchtcb + total_cacb + total_culiacb + total_suscb + abs(total_curastcb)
		total_asset = abs(total_loncb) + total_fxdastcb

	elif total_suscb < 0:
		total_liabilities = total_brchtcb + total_cacb + total_culiacb + total_loncb
		total_asset = total_curastcb + total_fxdastcb + abs(total_suscb)

	elif total_suscb < 0 and total_fxdastcb < 0:	
		total_liabilities =  total_brchtcb + total_cacb + total_culiacb + total_loncb + abs(total_fxdastcb)
		total_asset = abs(total_suscb) + total_curastcb 

	elif total_suscb < 0 and total_curastcb < 0:
		total_liabilities =  total_brchtcb + total_cacb + total_culiacb + total_loncb + abs(total_curastcb)
		total_asset = abs(total_suscb) + total_fxdastcb

	elif total_fxdastcb < 0:
		total_liabilities = total_brchtcb + total_cacb + total_culiacb + total_loncb + total_suscb + abs(total_fxdastcb)
		total_asset = total_curastcb

	elif total_curastcb < 0:
		total_liabilities = total_brchtcb + total_cacb + total_culiacb + total_loncb + total_suscb + abs(total_curastcb)
		total_asset = total_fxdastcb

	else:
		total_liabilities = total_brchtcb + total_cacb + total_culiacb + total_loncb + total_suscb
		total_asset = total_curastcb + total_fxdastcb

	inbox = Message.objects.filter(reciever=request.user)
	inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
	send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
	

	context = {

		'company_details' : company_details,
		'selectdatefield_details' : selectdatefield_details,
		'closing_stock' : qs2,

		# Branch/Divisions
		'branch' : groupbrchcb,
		'branchled' : ledbrch,
		'total_branch' : total_brchtcb,

		# Capital A/c
		'capital' : groupcacb,
		'capitalled' : ledcah,
		'total_capital' : total_cacb,

		# Current Liabilities
		'current' : groupculiacb,
		'currentled' : ledculiah,
		'total_current' : total_culiacb,

		# Loans (Liability)
		'loan' : grouploncb,
		'loanled' : ledlonh,
		'total_loan' : total_loncb,

		# Suspense A/c
		'suspnse' : groupsuscb,
		'suspnseled' : ledsusnh,
		'total_suspnse' : total_suscb,

		# Current Assets
		'current_asset' : groupcurastcb,
		'current_assetled' : ledcurastnh,
		'total_current_asset' : total_curastcb,

		# Fixed Asset
		'fixed_asset' : groupfxdastcb,
		'fixed_assetled' : ledfxdastnh,
		'total_fixed_asset' : total_fxdastcb,


		# P&L A/c

		'gross_profit' : gp,		
		'nett_profit' : np,


		# From Trial Balance
		'total_debit_closing' : total_debit_closing,
		'total_credit_closing' : total_credit_closing,


		# Total
		'total_liabilities' : total_liabilities,
		'total_asset' : total_asset,

		'inbox'			: inbox,
		'inbox_count'	: inbox_count,
		'send_count'	: send_count,

		'Todos'		   : Todo.objects.filter(User=request.user, complete=False),
		'Todos_total'  :Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 


	}


	return render(request, 'accounting_double_entry/balance_sheet.html', context)



@login_required
@product_1_activation
def cash_and_bank_view(request,pk,pk3):
	company_details = get_object_or_404(company, pk=pk)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)

	# Cash Account
	cash_group = group1.objects.filter(User=request.user, Company=company_details.pk, group_Name__icontains='Cash-in-hand', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date)
	cash_group_closing = cash_group.annotate(
				closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0),
			)


	groups_ca_pos = cash_group.annotate(
				closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0)
			).filter(closing__gt = 0)

	groups_ca_neg = cash_group.annotate(
				closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0)
			).filter(closing__lte = 0)

	groups_ca_positive = groups_ca_pos.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	groups_ca_negative = groups_ca_neg.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']


	# Bank Account
	bank_group = group1.objects.filter(User=request.user, Company=company_details.pk, group_Name__icontains='Bank Accounts', ledgergroups__Creation_Date__gte=selectdatefield_details.Start_Date, ledgergroups__Creation_Date__lte=selectdatefield_details.End_Date)
	bank_group_closing = bank_group.annotate(
				closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0),
			)

	groups_ba_pos = bank_group.annotate(
				closing = Coalesce(Sum('ledgergroups__Closing_balance'), 0),
			).filter(closing__gt = 0)

	# groups_ba_neg = bank_group.annotate(
	# 			closing = Sum('ledgergroups__Closing_balance')
	# 		).filter(closing__lte = 0, closing = 0),

	groups_ba_positive = groups_ba_pos.aggregate(the_sum=Coalesce(Sum('closing'), Value(0)))['the_sum']
	# groups_ba_negative = groups_ba_neg.aggregate(the_sum1=Sum('closing'))['the_sum1']



	positive = groups_ca_positive + groups_ba_positive
	negative = groups_ca_negative 

	inbox = Message.objects.filter(reciever=request.user)
	inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
	send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']



	context = {
		'company_details' : company_details,
		'selectdatefield_details' : selectdatefield_details,

		'cash_group' : cash_group_closing,

		'bank_group' : bank_group_closing,

		'positive' : positive,
		'negative' : negative, 

		'inbox'			: inbox,
		'inbox_count'	: inbox_count,
		'send_count'	: send_count,

		'Todos'		   : Todo.objects.filter(User=request.user, complete=False),
		'Todos_total'  :Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] ,

	}

	return render(request, 'Cash_Bank/cash_and_bank.html', context)

























# def search_by_date(request,pk,pk1):
# 	template = 'accounting_double_entry/ledger1_details.html'

# 	query_start = request.GET.get('s')

# 	query_end = request.GET.get('q')

# 	if query_start and query_end:
# 		# selectdaterange.objects.get_or_create(Start_Date=query_start,End_Date=query_end)
# 		result = journal.objects.filter(User=request.user, Date__gte=query_start, Date__lte=query_end)

# 	else:
# 		result = journal.objects.filter(User=request.user)

# 	company_details = get_object_or_404(company, pk=pk)
# 	ledger1_details = get_object_or_404(ledger1, pk=pk1)

# 	context = {
# 		'journal_list'    : result,
# 		'ledger1_details' : ledger1_details,
# 		'company_details' : company_details,
# 	}

# 	return render(request, template, context)