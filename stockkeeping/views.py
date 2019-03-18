from django.shortcuts import render
from django.views.generic import (View,ListView,DetailView,
								  CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from accounting_double_entry.models import group1,ledger1,journal,selectdatefield
from company.models import company
from stockkeeping.models import Stockgroup,Simpleunits,Compoundunits,Stockdata,Purchase,Sales,Stock_Total,Stock_Total_sales
from stockkeeping.forms import Stockgroup_form,Simpleunits_form,Compoundunits_form,Stockdata_form,Purchase_form,Sales_form,Purchase_formSet,Sales_formSet,Stock_Totalform
from userprofile.models import Profile, Product_activation
from messaging.models import Message
from ecommerce_integration.models import coupon, Product, Product_review, Services, API
from todogst.models import Todo
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models.functions import Coalesce
from django.db.models import Case, When, CharField, Value, Sum, Count, F, ExpressionWrapper, Subquery, OuterRef, FloatField
from django.db.models.fields import DecimalField
import calendar
import dateutil
import collections
from ecommerce_integration.decorators import product_1_activation
from django.core.exceptions import PermissionDenied

# Create your views here.


class ProductExistsRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

##################################### Simple Unit Views #####################################

class Simpleunits_listview(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = Simpleunits
	template_name = 'stockkeeping/simpleunits/simpleunits_list.html'
	paginate_by = 15


	def get_queryset(self):
		return self.model.objects.filter(User=self.request.user, Company=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super(Simpleunits_listview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Simpleunits_detailsview(ProductExistsRequiredMixin,LoginRequiredMixin,DetailView):
	context_object_name = 'simpleunits_details'
	model = Simpleunits
	template_name = 'stockkeeping/simpleunits/simpleunits_details.html'

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		pk3 = self.kwargs['pk3']
		get_object_or_404(selectdatefield, pk=pk3)
		get_object_or_404(company, pk=pk1)
		simpleunit = get_object_or_404(Simpleunits, pk=pk2)
		return simpleunit


	def get_context_data(self, **kwargs):
		context = super(Simpleunits_detailsview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Simpleunits_createview(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = Simpleunits_form
	template_name = "stockkeeping/simpleunits/simpleunits_form.html"

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:simplelist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c
		counter = Simpleunits.objects.filter(User=self.request.user, Company=c).count() + 1
		form.instance.counter = counter
		return super(Simpleunits_createview, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(Simpleunits_createview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Simpleunits_updateview(ProductExistsRequiredMixin,LoginRequiredMixin,UpdateView):
	model = Simpleunits
	form_class  = Simpleunits_form
	template_name = "stockkeeping/simpleunits/simpleunits_form.html"


	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		simpleunits_details  = get_object_or_404(Simpleunits, pk=self.kwargs['pk2'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:simpledetail', kwargs={'pk1':company_details.pk, 'pk2':group1_details.pk,'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		simpleunit = get_object_or_404(Simpleunits, pk=pk2)
		return simpleunit

	def get_context_data(self, **kwargs):
		context = super(Simpleunits_updateview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context


class Simpleunits_deleteview(ProductExistsRequiredMixin,LoginRequiredMixin,DeleteView):
	model = Simpleunits
	template_name = "stockkeeping/simpleunits/simpleunits_confirm_delete.html"

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:simplelist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk = self.kwargs['pk']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk)
		simpleunit = get_object_or_404(Simpleunits, pk=pk2)
		return simpleunit

	def get_context_data(self, **kwargs):
		context = super(Simpleunits_deleteview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context


##################################### Compound Unit Views #####################################



class Compoundunit_listview(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = Compoundunits
	template_name = 'stockkeeping/compoundunits/compoundunits_list.html'
	paginate_by = 15


	def get_queryset(self):
		return self.model.objects.filter(User=self.request.user, Company=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super(Compoundunit_listview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context


class Compoundunits_detailsview(ProductExistsRequiredMixin,LoginRequiredMixin,DetailView):
	context_object_name = 'compoundunits_details'
	model = Compoundunits
	template_name = 'stockkeeping/compoundunits/compoundunits_details.html'

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		pk3 = self.kwargs['pk3']
		get_object_or_404(selectdatefield, pk=pk3)
		get_object_or_404(company, pk=pk1)
		compoundunit = get_object_or_404(Compoundunits, pk=pk2)
		return compoundunit


	def get_context_data(self, **kwargs):
		context = super(Compoundunits_detailsview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Compoundunits_createview(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = Compoundunits_form
	template_name = "stockkeeping/compoundunits/compoundunits_form.html"

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:compoundlist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c
		counter = Compoundunits.objects.filter(User=self.request.user, Company=c).count() + 1
		form.instance.counter = counter
		return super(Compoundunits_createview, self).form_valid(form)

	def get_form_kwargs(self):
		data = super(Compoundunits_createview, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data

	def get_context_data(self, **kwargs):
		context = super(Compoundunits_createview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Compoundunits_updateview(ProductExistsRequiredMixin,LoginRequiredMixin,UpdateView):
	model = Compoundunits
	form_class  = Compoundunits_form
	template_name = "stockkeeping/compoundunits/compoundunits_form.html"


	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		compoundunits_details  = get_object_or_404(Compoundunits, pk=self.kwargs['pk2'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:compounddetail', kwargs={'pk1':company_details.pk, 'pk2':compoundunits_details.pk,'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		compoundunit = get_object_or_404(Compoundunits, pk=pk2)
		return compoundunit

	def get_form_kwargs(self):
		data = super(Compoundunits_updateview, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data

	def get_context_data(self, **kwargs):
		context = super(Compoundunits_updateview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Compoundunits_deleteview(ProductExistsRequiredMixin,LoginRequiredMixin,DeleteView):
	model = Compoundunits
	template_name = "stockkeeping/compoundunits/compoundunits_confirm_delete.html"

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:compoundlist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		compoundunit = get_object_or_404(Compoundunits, pk=pk2)
		return compoundunit

	def get_context_data(self, **kwargs):
		context = super(Compoundunits_deleteview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

		
##################################### Stockgroup Views #####################################

class Stockgroup_listview(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = Stockgroup
	template_name = 'stockkeeping/stockgroup/stockgroup_list.html'
	paginate_by = 15


	def get_queryset(self):
		return self.model.objects.filter(User=self.request.user, Company=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super(Stockgroup_listview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Stockgroup_detailsview(ProductExistsRequiredMixin,LoginRequiredMixin,DetailView):
	context_object_name = 'stockgrp_details'
	model = Stockgroup
	template_name = 'stockkeeping/stockgroup/stockgroup_details.html'

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		pk3 = self.kwargs['pk3']
		get_object_or_404(selectdatefield, pk=pk3)
		get_object_or_404(company, pk=pk1)
		stockgroup = get_object_or_404(Stockgroup, pk=pk2)
		return Stockgroup


	def get_context_data(self, **kwargs):
		context = super(Stockgroup_detailsview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		stockgrp_details = get_object_or_404(Stockgroup, pk=self.kwargs['pk2'])
		context['stockgrp_details'] = stockgrp_details
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Stockgroup_createview(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = Stockgroup_form
	template_name = "stockkeeping/stockgroup/stockgroup_form.html"

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:stockgrouplist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c
		counter = Stockgroup.objects.filter(User=self.request.user, Company=c).count() + 1
		form.instance.counter = counter
		return super(Stockgroup_createview, self).form_valid(form)

	def get_form_kwargs(self):
		data = super(Stockgroup_createview, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data

	def get_context_data(self, **kwargs):
		context = super(Stockgroup_createview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Stockgroup_updateview(ProductExistsRequiredMixin,LoginRequiredMixin,UpdateView):
	model = Stockgroup
	form_class  = Stockgroup_form
	template_name = "stockkeeping/stockgroup/stockgroup_form.html"


	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		stockgroup_details  = get_object_or_404(Stockgroup, pk=self.kwargs['pk2'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:stockgroupdetail', kwargs={'pk1':company_details.pk, 'pk2':stockgroup_details.pk,'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		stockgroup = get_object_or_404(Stockgroup, pk=pk2)
		return stockgroup

	def get_form_kwargs(self):
		data = super(Stockgroup_updateview, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk1'])
			)
		return data

	def get_context_data(self, **kwargs):
		context = super(Stockgroup_updateview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Stockgroup_deleteview(ProductExistsRequiredMixin,LoginRequiredMixin,DeleteView):
	model = Stockgroup
	template_name = "stockkeeping/stockgroup/stockgroup_confirm_delete.html"

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:stockgrouplist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		stockgroup = get_object_or_404(Stockgroup, pk=pk2)
		return stockgroup

	def get_context_data(self, **kwargs):
		context = super(Stockgroup_deleteview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

##################################### Stockitems Monthly Views #####################################

@login_required
@product_1_activation
def Stockitems_Monthly_view(request, pk, pk2, pk3):
	company_details = get_object_or_404(company, pk=pk)
	selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)
	stockdata_details = get_object_or_404(Stockdata, pk=pk2)


	results = collections.OrderedDict()
	result1 = Stock_Total_sales.objects.filter(sales__User=request.user, sales__Company=company_details.pk, stockitem=stockdata_details.pk, sales__date__gte=selectdatefield_details.Start_Date, sales__date__lt=selectdatefield_details.End_Date).annotate(real_total_quantity_s = Case(When(Quantity__isnull=True, then=0),default=F('Quantity')))
	result2 = Stock_Total.objects.filter(purchases__User=request.user, purchases__Company=company_details.pk, stockitem=stockdata_details.pk, purchases__date__gte=selectdatefield_details.Start_Date, purchases__date__lt=selectdatefield_details.End_Date).annotate(real_total_quantity_p = Case(When(Quantity_p__isnull=True, then=0),default=F('Quantity_p')))
	result3 = Stock_Total.objects.filter(purchases__User=request.user, purchases__Company=company_details.pk, stockitem=stockdata_details.pk, purchases__date__gte=selectdatefield_details.Start_Date, purchases__date__lt=selectdatefield_details.End_Date).annotate(real_total_p = Case(When(Total_p__isnull=True, then=0),default=F('Total_p')))
	result4 = Stock_Total_sales.objects.filter(sales__User=request.user, sales__Company=company_details.pk, stockitem=stockdata_details.pk, sales__date__gte=selectdatefield_details.Start_Date, sales__date__lt=selectdatefield_details.End_Date).annotate(real_total_s = Case(When(Total__isnull=True, then=0),default=F('Total')))

	date_cursor = selectdatefield_details.Start_Date

	w = 0
	x = 0
	y = 0
	z = 0

	while date_cursor <= selectdatefield_details.End_Date:
		month_partial_purchase_quantity = result2.filter(purchases__date__month=date_cursor.month).aggregate(partial_total_purchase_quantity=Sum('real_total_quantity_p'))['partial_total_purchase_quantity']
		month_partial_sale_quantity = result1.filter(sales__date__month=date_cursor.month).aggregate(partial_total_sale_quantity=Sum('real_total_quantity_s'))['partial_total_sale_quantity']
		month_partial_purchase = result3.filter(purchases__date__month=date_cursor.month).aggregate(partial_total_purchase=Sum('real_total_p'))['partial_total_purchase']
		month_partial_sale = result4.filter(sales__date__month=date_cursor.month).aggregate(partial_total_sale=Sum('real_total_s'))['partial_total_sale']

		if month_partial_purchase_quantity == None:

			month_partial_purchase_quantity = int(0)
			e = month_partial_purchase_quantity
		else:
			e = month_partial_purchase_quantity

		if month_partial_sale_quantity == None:

			month_partial_sale_quantity = int(0)
			f = month_partial_sale_quantity
		else:
			f = month_partial_sale_quantity	

		if month_partial_purchase == None:

			month_partial_purchase = int(0)
			g = month_partial_purchase
		else:
			g = month_partial_purchase


		if month_partial_sale == None:

			month_partial_sale = int(0)
			h = month_partial_sale
		else:
			h = month_partial_sale


		w = w + e - f

		x = x + e

		y = y + g

		if x == 0:
			z = y * w
		else:
			z = y / x * w			

		results[calendar.month_name[date_cursor.month]] =  [w,e,f,g,h,z]			
		date_cursor += dateutil.relativedelta.relativedelta(months=1)

	total_purchase_quantity = result2.aggregate(the_sum=Coalesce(Sum('real_total_quantity_p'), Value(0)))['the_sum']
	total_sale_quantity = result1.aggregate(the_sum=Coalesce(Sum('real_total_quantity_s'), Value(0)))['the_sum']
	total_purchase = result3.aggregate(the_sum=Coalesce(Sum('real_total_p'), Value(0)))['the_sum']
	total_sale = result4.aggregate(the_sum=Coalesce(Sum('real_total_s'), Value(0)))['the_sum']

	Closing_balance = z

	inbox = Message.objects.filter(reciever=request.user)
	inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
	send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']


	context = {

		'company_details'             : company_details,
		'stockdata_details'           : stockdata_details,
		'selectdatefield_details' 	  : selectdatefield_details,
		'total_purchase_quantity'     : total_purchase_quantity,
		'total_sale_quantity'         : total_sale_quantity,
		'total_purchase'			  : total_purchase,
		'total_sale'                  : total_sale,
		'data'			              : results.items(),
		'Closing_balance'			  : Closing_balance,
		'inbox'						  : inbox,
		'inbox_count'				  : inbox_count,
		'send_count'				  : send_count,
		'Todos'					      : Todo.objects.filter(User=request.user, complete=False),
		'Todos_total' 			      : Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 

				
	}

	return render(request, 'stockkeeping/stockitem/Stock_Monthly.html', context)



##################################### Stockitems Views #####################################

class closing_list_view(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = Stockdata
	paginate_by = 15

	def get_template_names(self):
		if True:  
			return ['stockkeeping/closing_stock.html']
		else:
			return ['stockkeeping/stockitem/stockdata_list.html']


	def get_queryset(self):
		return self.model.objects.filter(User=self.request.user, Company=self.kwargs['pk']).order_by('-id')

	def get_context_data(self, **kwargs):
		context = super(closing_list_view, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		qs = Stockdata.objects.filter(User=self.request.user, Company=company_details.pk, Date__lte=selectdatefield_details.End_Date)
		qs = qs.annotate(
    		sales_sum = Subquery(
    			Stock_Total_sales.objects.filter(sales__User=self.request.user, sales__Company=company_details.pk,
    				stockitem = OuterRef('pk'),sales__date__gte=selectdatefield_details.Start_Date, sales__date__lt=selectdatefield_details.End_Date
    				).values(
    					'stockitem'
    				).annotate(
    					the_sum = Sum('Quantity')
    				).values('the_sum'),
    			output_field=FloatField()),
    		purchase_sum =  Coalesce(Sum('purchasestock__Quantity_p'),0),
    		purchase_tot = Subquery(
    			Stock_Total.objects.filter(purchases__User=self.request.user, purchases__Company=company_details.pk,
    				stockitem = OuterRef('pk'),purchases__date__gte=selectdatefield_details.Start_Date, purchases__date__lt=selectdatefield_details.End_Date
    				).values(
    					'stockitem'
    				).annotate(
    					the_sum = Sum('Total_p')
    				).values(
    					'the_sum'
    				),
    			output_field=FloatField()),
		)

		qs1 = qs.annotate(
	    	difference = ExpressionWrapper(F('purchase_sum') - F('sales_sum'), output_field=FloatField()),
	    	total = ExpressionWrapper((F('purchase_tot') / F('purchase_sum')) * (F('purchase_sum') - F('sales_sum')), output_field=FloatField())
		) 
		context['Totalquantity'] = qs1.values()
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Stockdata_listview(LoginRequiredMixin,ListView):
	model = Stockdata
	template_name = 'stockkeeping/stockitem/stockdata_list.html'
	paginate_by = 15


	def get_queryset(self):
		return self.model.objects.filter(User=self.request.user, Company=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super(Stockdata_listview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context


class Stockdata_detailsview(ProductExistsRequiredMixin,LoginRequiredMixin,DetailView):
	context_object_name = 'stockdata_details'
	model = Stockdata
	template_name = 'stockkeeping/stockitem/stockdata_details.html'

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		pk3 = self.kwargs['pk3']
		get_object_or_404(selectdatefield, pk=pk3)
		get_object_or_404(company, pk=pk1)
		stockdata = get_object_or_404(Stockdata, pk=pk2)
		return stockdata


	def get_context_data(self, **kwargs):
		context = super(Stockdata_detailsview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Stockdata_createview(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = Stockdata_form
	template_name = "stockkeeping/stockitem/stockdata_form.html"

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:stockdatalist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c
		counter = Stockdata.objects.filter(User=self.request.user, Company=c).count() + 1
		form.instance.counter = counter
		return super(Stockdata_createview, self).form_valid(form)

	def get_form_kwargs(self):
		data = super(Stockdata_createview, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data

	def get_context_data(self, **kwargs):
		context = super(Stockdata_createview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Stockdata_updateview(ProductExistsRequiredMixin,LoginRequiredMixin,UpdateView):
	model = Stockdata
	form_class  = Stockdata_form
	template_name = "stockkeeping/stockitem/stockdata_form.html"


	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		stockdata_details  = get_object_or_404(Stockdata, pk=self.kwargs['pk2'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:stockdatadetail', kwargs={'pk1':company_details.pk, 'pk2':stockdata_details.pk,'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		stockdata = get_object_or_404(Stockdata, pk=pk2)
		return stockdata

	def get_form_kwargs(self):
		data = super(Stockdata_updateview, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk1'])
			)
		return data

	def get_context_data(self, **kwargs):
		context = super(Stockdata_updateview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Stockdata_deleteview(ProductExistsRequiredMixin,LoginRequiredMixin,DeleteView):
	model = Stockdata
	template_name = "stockkeeping/stockitem/stockdataunits_confirm_delete.html"

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:stockdatalist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		compoundunit = get_object_or_404(Stockdata, pk=pk2)
		return compoundunit

	def get_context_data(self, **kwargs):
		context = super(Stockdata_deleteview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

##################################### Purchase Views #####################################

class Purchase_listview(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = Purchase
	template_name = 'stockkeeping/purchase/purchase_list.html'
	paginate_by = 15


	def get_queryset(self):
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return self.model.objects.filter(User=self.request.user, Company=self.kwargs['pk'], date__gte=selectdatefield_details.Start_Date, date__lte=selectdatefield_details.End_Date).order_by('-id')

	def get_context_data(self, **kwargs):
		context = super(Purchase_listview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context


class Purchase_detailsview(LoginRequiredMixin,DetailView):
	context_object_name = 'purchase_details'
	model = Purchase
	template_name = 'stockkeeping/purchase/purchase_details.html'

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		pk3 = self.kwargs['pk3']
		get_object_or_404(selectdatefield, pk=pk3)
		get_object_or_404(company, pk=pk1)
		purchase = get_object_or_404(Purchase, pk=pk2)
		return purchase


	def get_context_data(self, **kwargs):
		context = super(Purchase_detailsview, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		purchase_details = get_object_or_404(Purchase, pk=self.kwargs['pk2'])
		qsob  = Stock_Total.objects.filter(purchases=purchase_details.pk)
		context['stocklist'] = qsob
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Purchase_createview(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = Purchase_form
	template_name = 'stockkeeping/purchase/purchase_form.html'

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:purchaselist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def get_context_data(self, **kwargs):
		context = super(Purchase_createview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		if self.request.POST:
			context['stocks'] = Purchase_formSet(self.request.POST)
		else:
			context['stocks'] = Purchase_formSet()

		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c
		counter = Purchase.objects.filter(User=self.request.user, Company=c).count() + 1
		form.instance.counter = counter
		context = self.get_context_data()
		stocks = context['stocks']
		with transaction.atomic():
			self.object = form.save()
			if stocks.is_valid():
				stocks.instance = self.object
				stocks.save()
		return super(Purchase_createview, self).form_valid(form)

	def get_form_kwargs(self):
		data = super(Purchase_createview, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data



class Purchase_updateview(ProductExistsRequiredMixin,LoginRequiredMixin,UpdateView):
	model = Purchase
	form_class  = Purchase_form
	template_name = 'stockkeeping/purchase/purchase_form.html'


	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		purchase_details  = get_object_or_404(Purchase, pk=self.kwargs['pk2'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:purchasedetail', kwargs={'pk1':company_details.pk, 'pk2':purchase_details.pk,'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		purchase = get_object_or_404(Purchase, pk=pk2)
		return purchase

	def get_form_kwargs(self):
		data = super(Purchase_updateview, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk1'])
			)
		return data

	def get_context_data(self, **kwargs):
		context = super(Purchase_updateview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Purchase_deleteview(ProductExistsRequiredMixin,LoginRequiredMixin,DeleteView):
	model = Purchase
	template_name = "stockkeeping/purchase/purchase_confirm_delete.html"

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:purchaselist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		purchase = get_object_or_404(Purchase, pk=pk2)
		return purchase

	def get_context_data(self, **kwargs):
		context = super(Purchase_deleteview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context


##################################### Purchase Register Views #####################################

class Purchase_Register_view(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = Purchase
	template_name = 'stockkeeping/purchase/Purchase_Register.html'

	def get_context_data(self, **kwargs):
		context = super(Purchase_Register_view, self).get_context_data(**kwargs)
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['company_details'] = company_details
		context['selectdatefield_details'] = selectdatefield_details

		results = collections.OrderedDict()
		result = Purchase.objects.filter(User=self.request.user, Company=company_details.pk,date__gte=selectdatefield_details.Start_Date, date__lt=selectdatefield_details.End_Date).annotate(real_total = Case(When(sub_total__isnull=True, then=0),default=F('sub_total')))
		date_cursor = selectdatefield_details.Start_Date

		z = 0

		while date_cursor <= selectdatefield_details.End_Date:
			month_partial_total = result.filter(date__month=date_cursor.month).aggregate(partial_total=Sum('real_total'))['partial_total']

			if month_partial_total == None:

				month_partial_total = int(0)

				e = month_partial_total

			else:

				e = month_partial_total


			z = z + e
			

			results[calendar.month_name[date_cursor.month]] =  [e,z]			

			date_cursor += dateutil.relativedelta.relativedelta(months=1)

		total_purchase = result.aggregate(the_sum=Coalesce(Sum('real_total'), Value(0)))['the_sum']

		context['data'] = results.items()
		
		context['total_purchase'] = total_purchase
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context


##################################### Sales Register Views #####################################



class Sales_Register_view(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = Sales
	template_name = 'stockkeeping/sales/Sales_Register.html'

	def get_context_data(self, **kwargs):
		context = super(Sales_Register_view, self).get_context_data(**kwargs)
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['company_details'] = company_details
		context['selectdatefield_details'] = selectdatefield_details

		results = collections.OrderedDict()
		result = Sales.objects.filter(User=self.request.user, Company=company_details.pk,date__gte=selectdatefield_details.Start_Date, date__lt=selectdatefield_details.End_Date).annotate(real_total = Case(When(sub_total__isnull=True, then=0),default=F('sub_total')))
		date_cursor = selectdatefield_details.Start_Date

		z = 0

		while date_cursor <= selectdatefield_details.End_Date:
			month_partial_total = result.filter(date__month=date_cursor.month).aggregate(partial_total=Sum('real_total'))['partial_total']

			if month_partial_total == None:

				month_partial_total = int(0)

				e = month_partial_total

			else:

				e = month_partial_total


			z = z + e
			

			results[calendar.month_name[date_cursor.month]] =  [e,z]			

			date_cursor += dateutil.relativedelta.relativedelta(months=1)

		total_sale = result.aggregate(the_sum=Coalesce(Sum('real_total'), Value(0)))['the_sum']

		context['Debit'] = e
		context['data'] = results.items()
		
		context['total_sale'] = total_sale
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context


##################################### Sales Views #####################################

class Sales_listview(ProductExistsRequiredMixin,LoginRequiredMixin,ListView):
	model = Sales
	template_name = 'stockkeeping/sales/sales_list.html'
	paginate_by = 15


	def get_queryset(self):
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return self.model.objects.filter(User=self.request.user, Company=self.kwargs['pk'], date__gte=selectdatefield_details.Start_Date, date__lte=selectdatefield_details.End_Date).order_by('-id')

	def get_context_data(self, **kwargs):
		context = super(Sales_listview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context



class Sales_detailsview(ProductExistsRequiredMixin,LoginRequiredMixin,DetailView):
	context_object_name = 'sales_details'
	model = Sales
	template_name = 'stockkeeping/sales/sales_details.html'

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		pk3 = self.kwargs['pk3']
		get_object_or_404(selectdatefield, pk=pk3)
		get_object_or_404(company, pk=pk1)
		sales = get_object_or_404(Sales, pk=pk2)
		return sales


	def get_context_data(self, **kwargs):
		context = super(Sales_detailsview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		sales_details = get_object_or_404(Sales, pk=self.kwargs['pk2'])
		qsjb  = Stock_Total_sales.objects.filter(sales=sales_details.pk)
		context['stocklist'] = qsjb
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class Sales_createview(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = Sales_form
	template_name = 'stockkeeping/sales/sales_form.html'

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:saleslist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})


	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c
		counter = Sales.objects.filter(User=self.request.user, Company=c).count() + 1
		form.instance.counter = counter
		context = self.get_context_data()
		stocksales = context['stocksales']
		with transaction.atomic():
			self.object = form.save()
			if stocksales.is_valid():
				stocksales.instance = self.object
				stocksales.save()
		return super(Sales_createview, self).form_valid(form)

	def get_form_kwargs(self):
		data = super(Sales_createview, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data

	def get_context_data(self, **kwargs):
		context = super(Sales_createview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		if self.request.POST:
			context['stocksales'] = Sales_formSet(self.request.POST)
		else:
			context['stocksales'] = Sales_formSet()
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context





class Sales_updateview(ProductExistsRequiredMixin,LoginRequiredMixin,UpdateView):
	model = Sales
	form_class  = Sales_form
	template_name = 'stockkeeping/sales/sales_form.html'


	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		sales_details  = get_object_or_404(Sales, pk=self.kwargs['pk2'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:salesdetail', kwargs={'pk1':company_details.pk, 'pk2':sales_details.pk,'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk1']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		sales = get_object_or_404(Sales, pk=pk2)
		return sales

	def get_context_data(self, **kwargs):
		context = super(Sales_updateview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		if self.request.POST:
			context['stocksales'] = Sales_formSet(self.request.POST)
		else:
			context['stocksales'] = Sales_formSet()
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c
		context = self.get_context_data()
		stocksales = context['stocksales']
		with transaction.atomic():
			self.object = form.save()
			if stocksales.is_valid():
				stocksales.instance = self.object
				stocksales.save()
		return super(Sales_updateview, self).form_valid(form)

	def get_form_kwargs(self):
		data = super(Sales_updateview, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk1'])
			)
		return data



class Sales_deleteview(ProductExistsRequiredMixin,LoginRequiredMixin,DeleteView):
	model = Sales
	template_name = "stockkeeping/sales/sales_confirm_delete.html"

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:saleslist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def get_object(self):
		pk1 = self.kwargs['pk']
		pk2 = self.kwargs['pk2']
		get_object_or_404(company, pk=pk1)
		sales = get_object_or_404(Sales, pk=pk2)
		return sales

	def get_context_data(self, **kwargs):
		context = super(Sales_deleteview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context	



##################################### Stock_Total #####################################

class Stock_Total_createview(ProductExistsRequiredMixin,LoginRequiredMixin,CreateView):
	form_class  = Stock_Totalform
	template_name = 'stockkeeping/purchase/purchase_form.html'

	def get_success_url(self,**kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		return reverse('stockkeeping:purchaselist', kwargs={'pk':company_details.pk, 'pk3':selectdatefield_details.pk})

	def get_context_data(self, **kwargs):
		context = super(Stock_Total_createview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

	def form_valid(self, form):
		form.instance.User = self.request.user
		c = company.objects.get(pk=self.kwargs['pk'])
		form.instance.Company = c

	def get_form_kwargs(self):
		data = super(Stock_Total_createview, self).get_form_kwargs()
		data.update(
			User=self.request.user,
			Company=company.objects.get(pk=self.kwargs['pk'])
			)
		return data



##################################### Profit & Loss A/c #####################################


@login_required
@product_1_activation
def profit_and_loss_view(request,pk,pk3):
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
		'Todos'					  : Todo.objects.filter(User=request.user, complete=False),
		'Todos_total' 			  : Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
	}


	return render(request, 'stockkeeping/P&L.html', context)

##################################### Trial Balance #####################################

@login_required
@product_1_activation
def trial_balance_view(request,pk,pk3):
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


	total_debit_closing = posdebcb + abs(necrcl) + qo2
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

		'total_credit_closing' : total_credit_closing,
		'total_credit_opening' : total_credit_opening,

		'inbox'			: inbox,
		'inbox_count'	: inbox_count,
		'send_count'	: send_count,

		'Todos'			: Todo.objects.filter(User=request.user, complete=False),
		'Todos_total' 	: Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
	}

	return render(request, 'stockkeeping/Trial_Balance/trial_bal.html', context)

##################################### Balance Sheet #####################################

@login_required
@product_1_activation
def balance_sheet_view(request,pk,pk3):
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
	groupcacb = groupcach.annotate(
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
		'totalpl' : tp,
		'totalplright' : tc,


		# From Trial Balance
		'total_debit_closing' : total_debit_closing,
		'total_credit_closing' : total_credit_closing,


		# Total
		'total_liabilities' : total_liabilities,
		'total_asset' : total_asset,

		'inbox'			: inbox,
		'inbox_count'	: inbox_count,
		'send_count'	: send_count,


		'Todos'					  : Todo.objects.filter(User=request.user, complete=False),
		'Todos_total' 			  : Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 


	}


	return render(request, 'stockkeeping/balance_sheet.html', context)



