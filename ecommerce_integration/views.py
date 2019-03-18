from django.shortcuts import render, redirect
from django.views.generic import (View,ListView,DetailView,
								  CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from ecommerce_integration.models import coupon, Product, Product_review, Services, API
from todogst.models import Todo
from messaging.models import Message
from ecommerce_cart.models import Order
from django.db.models.functions import Coalesce
from django.db.models import Value, Sum, Count, F, ExpressionWrapper, Subquery, OuterRef, FloatField
from ecommerce_integration.forms import Product_review_form
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from userprofile.models import Profile, Product_activation
from django.shortcuts import render_to_response
# Create your views here.



def Products_listview(request):
	products_list = Product.objects.get_queryset().order_by('id')
	page = request.GET.get('page', 1)
	paginator = Paginator(products_list, 9)
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)

	if not request.user.is_authenticated:
		filtered_orders = Order.objects.filter(is_ordered=False)
		current_order_products = []
		if filtered_orders.exists():
			user_order = filtered_orders[0]
			user_order_items = user_order.items.all()
			current_order_products = [product.product for product in user_order_items]

		Products = Product_activation.objects.filter(product__id = 1, is_active=True)
		inbox = Message.objects.all()
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		Todos = Todo.objects.filter(complete=False)
		Todos_total = Todos.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']		
	else:
		filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
		current_order_products = []
		if filtered_orders.exists():
			user_order = filtered_orders[0]
			user_order_items = user_order.items.all()
			current_order_products = [product.product for product in user_order_items]

		Products = Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True)
		inbox = Message.objects.filter(reciever=request.user)
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		Todos = Todo.objects.filter(User=request.user, complete=False)
		Todos_total = Todos.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
 


	context = {
		'products_list'			: products_list,
		'users'					: users,
		'current_order_products': current_order_products,
		'Products'			 	: Products,
        'inbox'         		: inbox,
        'inbox_count'   		: inbox_count,
        'send_count'			: send_count,
		'Todos'				 	: Todos,
		'Todos_total'		 	: Todos_total
	}

	return render(request, "products/product_list.html", context)

@login_required
def Subscribed_Products_listview(request):
	products_list = Product.objects.all()
	Todos = Todo.objects.filter(User=request.user, complete=False)
	Todos_total = Todos.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

	inbox = Message.objects.filter(reciever=request.user)
	inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
	send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

	context = {
		'products'		: products_list,
        'inbox'         : inbox,
        'inbox_count'   : inbox_count,
        'send_count'	: send_count,
		'Products'		: Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True),
		'Todos'			: Todos,
		'Todos_total'	: Todos_total,
	}

	return render(request, "products/subscribed_product.html", context)


def Products_detailsview(request, pk):
	products_details = get_object_or_404(Product, pk=pk)
	reviews = Product_review.objects.filter(reviews=products_details.pk).order_by('-id')

	if request.method == "POST":
		Productreview_form = Product_review_form(request.POST or None)
		if Productreview_form.is_valid():
			name = request.POST.get('name')
			e_mail = request.POST.get('e_mail')
			text = request.POST.get('text')
			answer = Product_review.objects.create(reviews=products_details, User=request.user, name=name, e_mail=e_mail, text=text)
			answer.save()
			return HttpResponseRedirect(products_details.get_absolute_url())
	else:
		Productreview_form = Product_review_form()


	if not request.user.is_authenticated:
		filtered_orders = Order.objects.filter(is_ordered=False)
		current_order_products = []
		if filtered_orders.exists():
			user_order = filtered_orders[0]
			user_order_items = user_order.items.all()
			current_order_products = [product.product for product in user_order_items]

		Products = Product_activation.objects.filter(product__id = 1, is_active=True)
		inbox = Message.objects.all()
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		Todos = Todo.objects.filter(complete=False)
		Todos_total = Todos.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']		
	else:
		filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
		current_order_products = []
		if filtered_orders.exists():
			user_order = filtered_orders[0]
			user_order_items = user_order.items.all()
			current_order_products = [product.product for product in user_order_items]

		Products = Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True)
		inbox = Message.objects.filter(reciever=request.user)
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		Todos = Todo.objects.filter(User=request.user, complete=False)
		Todos_total = Todos.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']


	context = {

		'products_details'   	: products_details,
		'reviews'		   	 	: reviews,
		'Productreview_form' 	: Productreview_form,
		'Todos'				 	: Todos,
		'Todos_total'		 	: Todos_total,
        'inbox'         		: inbox,
        'inbox_count'   		: inbox_count,
        'send_count'			: send_count,
		'current_order_products': current_order_products,
		'Products'				: Products,


	}

	return render(request, 'products/product_details.html', context)


def review_delete(request,id):
	data = dict()
	review = get_object_or_404(Product_review,id=id)
	if request.method == "POST":
		review.delete()
		data['form_is_valid'] = True
		reviews = Product_review.objects.all().order_by('-id')
		data['comments'] = render_to_string('products/reviews.html',{'reviews':reviews})
	else:
		context = {'review':review}
		data['html_form'] = render_to_string('products/reviews_delete.html',context,request=request)

	return JsonResponse(data)


def csrf_failure(request, reason=""):
	context = {'message' : 'Request is Forbidden'}
	return render_to_response('products/403_csrf.html', context)


def Services_listview(request):
	services_list = Services.objects.get_queryset().order_by('id')
	page = request.GET.get('page', 1)
	paginator = Paginator(services_list, 9)
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)

	if not request.user.is_authenticated:
		Products = Product_activation.objects.filter(product__id = 1, is_active=True)
		inbox = Message.objects.all()
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		Todos = Todo.objects.filter(complete=False)
		Todos_total = Todos.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']		
	else:
		Products = Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True)
		inbox = Message.objects.filter(reciever=request.user)
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		Todos = Todo.objects.filter(User=request.user, complete=False)
		Todos_total = Todos.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
 


	context = {
		'services_list'			: services_list,
		'services'				: users,
		'Products'			 	: Products,
        'inbox'         		: inbox,
        'inbox_count'   		: inbox_count,
        'send_count'			: send_count,
		'Todos'				 	: Todos,
		'Todos_total'		 	: Todos_total
	}

	return render(request, "services/services_list.html", context)

def Service_detailsview(request, pk):
	service_details = get_object_or_404(Services, pk=pk)


	if not request.user.is_authenticated:
		Products = Product_activation.objects.filter(product__id = 1, is_active=True)
		inbox = Message.objects.all()
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		Todos = Todo.objects.filter(complete=False)
		Todos_total = Todos.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']		
	else:
		Products = Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True)
		inbox = Message.objects.filter(reciever=request.user)
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		Todos = Todo.objects.filter(User=request.user, complete=False)
		Todos_total = Todos.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']


	context = {

		'service_details'   	: service_details,
		'Todos'				 	: Todos,
		'Todos_total'		 	: Todos_total,
        'inbox'         		: inbox,
        'inbox_count'   		: inbox_count,
        'send_count'			: send_count,
		'Products'				: Products,


	}

	return render(request, 'services/service_description.html', context)

def Api_listview(request):
	api_list = API.objects.get_queryset().order_by('id')
	page = request.GET.get('page', 1)
	paginator = Paginator(api_list, 9)

	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)

	if not request.user.is_authenticated:
		Products = Product_activation.objects.filter(product__id = 1, is_active=True)
		inbox = Message.objects.all()
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		Todos = Todo.objects.filter(complete=False)
		Todos_total = Todos.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']		
	else:
		Products = Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True)
		inbox = Message.objects.filter(reciever=request.user)
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		Todos = Todo.objects.filter(User=request.user, complete=False)
		Todos_total = Todos.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
 


	context = {
		'api_list'				: api_list,
		'apis'					: users,
		'Products'			 	: Products,
        'inbox'         		: inbox,
        'inbox_count'   		: inbox_count,
        'send_count'			: send_count,
		'Todos'				 	: Todos,
		'Todos_total'		 	: Todos_total
	}

	return render(request, "apis/api_list.html", context)

def Api_detailsview(request, pk):
	api_details = get_object_or_404(API, pk=pk)


	if not request.user.is_authenticated:
		Products = Product_activation.objects.filter(product__id = 1, is_active=True)
		inbox = Message.objects.all()
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		Todos = Todo.objects.filter(complete=False)
		Todos_total = Todos.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']		
	else:
		Products = Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True)
		inbox = Message.objects.filter(reciever=request.user)
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		Todos = Todo.objects.filter(User=request.user, complete=False)
		Todos_total = Todos.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']


	context = {

		'api_details'   		: api_details,
		'Todos'				 	: Todos,
		'Todos_total'		 	: Todos_total,
        'inbox'         		: inbox,
        'inbox_count'   		: inbox_count,
        'send_count'			: send_count,
		'Products'				: Products,

	}

	return render(request, 'apis/api_details.html', context)