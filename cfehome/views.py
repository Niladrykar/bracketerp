from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView,TemplateView
from django.shortcuts import render
from django.template import RequestContext
from django.conf import settings
from blog.models import Blog
from django.db.models import Count
from company.models import company
from django.shortcuts import get_object_or_404
from accounting_double_entry.models import selectdatefield
from stockkeeping.models import Sales, Purchase
from consultancy.models import consultancy,Answer 
from userprofile.models import Profile
from ecommerce_integration.models import coupon, Product, Services, API
from messaging.models import Message
from todogst.models import Todo
from userprofile.models import Profile, Product_activation
from django.db.models import Case, When, Value, Sum, Count, F, ExpressionWrapper, Subquery, OuterRef, FloatField
from django.db.models.fields import DecimalField
from django.db.models.functions import Coalesce 
import calendar
import dateutil
import collections




 
class HomePage(ListView):
	template_name = "clouderp/index.html"

	def get_queryset(self):
		return Blog.objects.all().annotate(num_submissions=Count('likes')).order_by('-num_submissions')[:4]

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse("ecommerce_integration:productlist"))
		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(HomePage, self).get_context_data(**kwargs) 
		context['total_consultancies'] = consultancy.objects.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Bussiness_users'] = Profile.objects.filter(user_type__icontains='Bussiness User').aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Professional_users'] = Profile.objects.filter(user_type__icontains='Professional').aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Products'] = Product.objects.all()
		context['Products_count'] = Product.objects.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context

class base(TemplateView):
	template_name = "clouderp/base.html"

	def get_context_data(self, **kwargs):
		context = super(base, self).get_context_data(**kwargs) 
		company_details = get_object_or_404(company, pk=self.kwargs['pk'])
		context['company_details'] = company_details
		selectdatefield_details = get_object_or_404(selectdatefield, pk=self.kwargs['pk3'])
		context['selectdatefield_details'] = selectdatefield_details
		context['Todos'] = Todo.objects.filter(User=request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['Products'] = Product_activation.objects.filter(User=self.request.user,id=1, activate=True)
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

		results = collections.OrderedDict()
		result = Sales.objects.filter(User=self.request.user, Company=company_details.pk,date__gte=selectdatefield_details.Start_Date, date__lt=selectdatefield_details.End_Date).annotate(real_total = Case(When(Total_Amount__isnull=True, then=0),default=F('Total_Amount')))
		result_purchase = Purchase.objects.filter(User=self.request.user, Company=company_details.pk,date__gte=selectdatefield_details.Start_Date, date__lt=selectdatefield_details.End_Date).annotate(real_total_purchase = Case(When(Total_Purchase__isnull=True, then=0),default=F('Total_Purchase')))
		date_cursor = selectdatefield_details.Start_Date

		while date_cursor <= selectdatefield_details.End_Date:
			month_partial_total = result.filter(date__month=date_cursor.month).aggregate(partial_total=Sum('real_total'))['partial_total']
			month_partial_total_purchase = result_purchase.filter(date__month=date_cursor.month).aggregate(partial_total_purchase=Sum('real_total_purchase'))['partial_total_purchase']

			if month_partial_total == None:

				month_partial_total = int(0)
				e = month_partial_total
				
			else:

				e = month_partial_total


			if month_partial_total_purchase == None:

				month_partial_total_purchase = int(0)
				z = month_partial_total_purchase
				
			else:

				z = month_partial_total_purchase
			
			

			results[calendar.month_name[date_cursor.month]] =  [e,z]			

			date_cursor += dateutil.relativedelta.relativedelta(months=1)


		context['data'] = results.items()
		return context



def custom_404(request):
	return render(request,'404.html')

def custom_500(request):
	return render(request,'505.html')
