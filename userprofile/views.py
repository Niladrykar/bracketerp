from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView,UpdateView,CreateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from userprofile.models import Profile, Product_activation, Post, Post_comment, Pro_services, achivements, Organisation, Organisation_member
from messaging.models import Message
from userprofile.forms import profileform, Postform, postcommentform, Service_form, Achievement_form, proverifyform, organisationform, organisation_memberform
from django.shortcuts import get_object_or_404
from company.models import company
from django.shortcuts import get_object_or_404
from todogst.models import Todo
from django.db.models.functions import Coalesce 
from django.db.models import Count, Value, Q, Sum
from ecommerce_integration.models import coupon, Product, Product_review, Services, API
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Blog,categories,Blog_comments
from consultancy.models import consultancy,Answer
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse

# Create your views here.

class profiledetailview(LoginRequiredMixin,DetailView):
	context_object_name = 'profile_details'
	model = Profile
	template_name = 'userprofile/profile.html'

	def get_object(self):
		return self.request.user.profile

	def get_context_data(self, **kwargs):
		context = super(profiledetailview, self).get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
			context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
			context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['inbox'] = Message.objects.filter(reciever=self.request.user)
			context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['blog_user']  = Blog.objects.filter(User=self.request.user).order_by('id')
			context['blog_count'] = context['blog_user'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))
			context['consultancy_user'] = consultancy.objects.filter(User=self.request.user).order_by('id') 
			context['consultancy_count'] = context['consultancy_user'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))
			context['blogs']  = Blog.objects.all().order_by('-id') 
			context['consultancies'] = consultancy.objects.all().order_by('-id')
			context['post_list'] = Post.objects.filter(User=self.request.user).order_by('-id')
			context['post_count'] = context['post_list'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))
			context['services'] = Pro_services.objects.filter(User=self.request.user).order_by('-id')
			context['case_count'] = achivements.objects.filter(User=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		else:
			context['Products'] = Product_activation.objects.filter(product__id = 1, is_active=True)
			context['Todos'] = Todo.objects.filter(complete=False)
			context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
			context['inbox'] = Message.objects.all()
			context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['send_count'] = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['services'] = Pro_services.objects.all().order_by('-id')
			context['case_count'] = achivements.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context

class profileupdateview(LoginRequiredMixin,UpdateView):
	model = Profile
	form_class = profileform
	template_name = 'userprofile/profile_form.html'

	def get_object(self):
		return self.request.user.profile


	def get_context_data(self, **kwargs):
		context = super(profileupdateview, self).get_context_data(**kwargs) 
		context['profile_details'] = Profile.objects.all()
		if self.request.user.is_authenticated:
			context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
			context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
			context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['inbox'] = Message.objects.filter(reciever=self.request.user)
			context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 

		else:
			context['Products'] = Product_activation.objects.filter(product__id = 1, is_active=True)
			context['Todos'] = Todo.objects.filter(complete=False)
			context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
			context['inbox'] = Message.objects.all()
			context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['send_count'] = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context


def specific_profile(request, pk):
	profile_details = get_object_or_404(Profile, pk=pk)

	if request.user.is_authenticated:
		Products = Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True)
		Todos = Todo.objects.filter(User=request.user,complete=False)
		Todos_total = Todo.objects.filter(User=request.user,complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		inbox = Message.objects.filter(reciever=request.user)
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
	else:
		Products = Product_activation.objects.filter(product__id = 1, is_active=True)
		Todos = Todo.objects.filter(complete=False)
		Todos_total = Todo.objects.filter(complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		inbox = Message.objects.all()
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

	blog_user  = Blog.objects.filter(User=profile_details.Name).order_by('id') 
	consultancy_user = consultancy.objects.filter(User=profile_details.Name).order_by('id') 
	blogs  = Blog.objects.all().order_by('-id') 
	consultancies = consultancy.objects.all().order_by('-id')
	services = Pro_services.objects.filter(User=profile_details.Name).order_by('-id')
	case_count = achivements.objects.filter(User=profile_details.Name).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']


	context = {
		'profile_details' : profile_details,
		'inbox'			  : inbox,
		'inbox_count'	  : inbox_count,
		'send_count'	  : send_count,
		'Products'		  : Products,
		'Todos'			  : Todos,
		'Todos_total' 	  : Todos_total, 
		'blog_user'		  : blog_user,
		'consultancy_user': consultancy_user,
		'blogs'			  : blogs,
		'consultancies'	  : consultancies,
		'services'		  : services,
		'case_count' 	  : case_count,
	}
	return render(request, 'userprofile/specific_profile.html', context)


@login_required
def activate_subscriptions(request, product_activation_id):
    product = Product_activation.objects.get(pk=product_activation_id)
    product.is_active = True
    product.save()

    return redirect('ecommerce_integration:subscribedproductlist')

@login_required
def activate_subscriptions_productlist(request, product_activation_id):
    product = Product_activation.objects.get(pk=product_activation_id)
    product.is_active = True
    product.save()

    return redirect('ecommerce_integration:productlist')


@login_required
def deactivate_subscriptions(request, product_activation_id):
    product = Product_activation.objects.get(pk=product_activation_id)
    product.is_active = False
    product.save()

    return redirect('ecommerce_integration:subscribedproductlist')


@login_required
def deactivate_subscriptions_productlist(request, product_activation_id):
    product = Product_activation.objects.get(pk=product_activation_id)
    product.is_active = False
    product.save()

    return redirect('ecommerce_integration:productlist')




def search_professionals(request):
	template = 'userprofile/find_professional.html'

	user_profile = Profile.objects.filter(user_type__icontains='Professional')

	query = request.GET.get('q')

	if query:
		result = user_profile.filter(Q(Name__username__icontains=query) | Q(E_mail__icontains=query) | Q(Full_Name__icontains=query))
	else:
		result = Profile.objects.filter(user_type__icontains='Professional').order_by('-id')[:8]

	professional_count = result.count()

	page = request.GET.get('page', 1)
	paginator = Paginator(result, 9)
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)

	if not request.user.is_authenticated:
		Products = Product_activation.objects.filter(product__id = 1, is_active=True)
		Todos = Todo.objects.filter(complete=False)
		Todos_total = Todo.objects.filter(complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		inbox = Message.objects.all()
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		
	else:
		Products = Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True)
		Todos = Todo.objects.filter(User=request.user,complete=False)
		Todos_total = Todo.objects.filter(User=request.user,complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		inbox = Message.objects.filter(reciever=request.user)
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

	context = {
		'professionals'			: result,
		'users'					: users,
		'professional_count'	: professional_count,
		'Products'				: Products,
		'inbox'					: inbox,
		'inbox_count'			: inbox_count,
		'send_count'			: send_count,
		'Todos'					: Todos,
		'Todos_total' 			: Todos_total 

	}

	return render(request, template, context)



@login_required
def post_list(request):
	post_list = Post.objects.all().order_by('-id')

	form = Postform()

	if not request.user.is_authenticated:
		Products = Product_activation.objects.filter(product__id = 1, is_active=True)
		Todos = Todo.objects.filter(complete=False)
		Todos_total = Todo.objects.filter(complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		todo_list = Todo.objects.none()
		inbox = Message.objects.all()
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		blog_user  = Blog.objects.filter(User=request.user).order_by('id') 
		consultancy_user = consultancy.objects.filter(User=request.user).order_by('id') 
		blogs  = Blog.objects.all().order_by('-id') 
		consultancies = consultancy.objects.all().order_by('-id')
		
	else:
		Products = Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True)
		Todos = Todo.objects.filter(User=request.user,complete=False)
		Todos_total = Todo.objects.filter(User=request.user,complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		todo_list = Todo.objects.filter(User=request.user)
		inbox = Message.objects.filter(reciever=request.user)
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		blog_user  = Blog.objects.filter(User=request.user).order_by('id') 
		consultancy_user = consultancy.objects.filter(User=request.user).order_by('id') 
		blogs  = Blog.objects.all().order_by('-id') 
		consultancies = consultancy.objects.all().order_by('-id')

	context = {
		'post_list' 	  : post_list,
		'form'			  : form,
		'inbox'			  : inbox,
		'inbox_count'	  : inbox_count,
		'send_count'	  : send_count,
		'Products'		  : Products,
		'Todos'			  : Todos,
		'Todos_total' 	  : Todos_total, 
		'blog_user'		  : blog_user,
		'consultancy_user': consultancy_user,
		'blogs'			  : blogs,
		'consultancies'	  : consultancies,
		'todo_list'		  : todo_list,
	}
	return render(request, 'social/social_wall.html', context)


class postcreateview(LoginRequiredMixin,CreateView):
	form_class = Postform
	template_name = 'social/social_wall.html'

	def get_success_url(self,**kwargs):
		return reverse('userprofile:social')


	def form_valid(self, form):
		form.instance.User = self.request.user
		return super(postcreateview, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(postcreateview, self).get_context_data(**kwargs)
		context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context


def post_detail(request, pk):
	post_details = get_object_or_404(Post, pk=pk)
	comments = Post_comment.objects.filter(post=post_details.pk).order_by('-id')

	is_liked = False
	if post_details.like.filter(pk=request.user.id).exists():
		is_liked = True

	if request.method == "POST":
		Comment_form = postcommentform(request.POST or None)
		if Comment_form.is_valid():
			text = request.POST.get('text')
			post_comment = Post_comment.objects.create(post=post_details, User=request.user, text=text)
			post_comment.save()
			return HttpResponseRedirect(post_details.get_absolute_url())
	else:
		Comment_form = postcommentform()

	if not request.user.is_authenticated:
		Products = Product_activation.objects.filter(product__id = 1, is_active=True)
		Todos = Todo.objects.filter(complete=False)
		Todos_total = Todo.objects.filter(complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		inbox = Message.objects.all()
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
	else:
		Products = Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True)
		Todos = Todo.objects.filter(User=request.user,complete=False)
		Todos_total = Todo.objects.filter(User=request.user,complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		inbox = Message.objects.filter(reciever=request.user)
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

	context = {
		'post_details' 			: post_details,
		'comments' 				: comments,	
		'is_liked' 				: is_liked,
		'total_like' 			: post_details.total_like(),
		'Comment_form' 			: Comment_form,
		'Products'				: Products,
		'inbox'					: inbox,
		'inbox_count'			: inbox_count,
		'send_count'			: send_count,
		'Todos'					: Todos,
		'Todos_total' 			: Todos_total

	}

	return render(request, 'social/post_details.html', context)


@login_required
def liked_post(request):
	post_details = get_object_or_404(Post, pk=request.POST.get('post_details_id'))

	is_liked = False
	if post_details.like.filter(pk=request.user.id).exists():
		post_details.like.remove(request.user)
		is_liked = False
	else:
		post_details.like.add(request.user)
		is_liked = True

	context = {
		'post_details' 	: post_details,
		'is_liked' 		: is_liked,
		'total_like' 	: post_details.total_like(),
	}

	if request.is_ajax():
		html = render_to_string('social/post_like.html', context, request=request)
		return JsonResponse({'form' : html})

def save_all(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			post_comments = Post_comment.objects.all().order_by('-id')
			data['post_comment'] = render_to_string('social/post_comment.html',{'post_comments':post_comments})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

def post_comment_update(request,id):
	comment = get_object_or_404(Post_comment,id=id)
	if request.method == 'POST':
		form = postcommentform(request.POST,instance=comment)
	else:
		form = postcommentform(instance=comment)
	return save_all(request,form,'social/post_comment_update.html')

def post_comment_delete(request,id):
	data = dict()
	comment = get_object_or_404(Post_comment,id=id)
	if request.method == "POST":
		comment.delete()
		data['form_is_valid'] = True
		post_comments = Post_comment.objects.all().order_by('-id')
		data['post_comment'] = render_to_string('social/post_comment.html',{'post_comments':post_comments})
	else:
		context = {'comment':comment}
		data['html_form'] = render_to_string('social/post_comment_delete.html',context,request=request)

	return JsonResponse(data)

class servicecreateview(LoginRequiredMixin,CreateView):
	form_class = Service_form
	template_name = 'services/service_create.html'


	def form_valid(self, form):
		form.instance.User = self.request.user
		return super(servicecreateview, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(servicecreateview, self).get_context_data(**kwargs)
		context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context


class serviceupdateview(LoginRequiredMixin,UpdateView):
	model = Pro_services
	form_class = Service_form
	template_name = 'services/service_create.html'


	def get_context_data(self, **kwargs):
		context = super(serviceupdateview, self).get_context_data(**kwargs)
		context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']  
		return context

def service_detail(request, pk):
	service_details = get_object_or_404(Pro_services, pk=pk)

	if not request.user.is_authenticated:
		Products = Product_activation.objects.filter(product__id = 1, is_active=True)
		Todos = Todo.objects.filter(complete=False)
		Todos_total = Todo.objects.filter(complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		inbox = Message.objects.all()
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
	else:
		Products = Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True)
		Todos = Todo.objects.filter(User=request.user,complete=False)
		Todos_total = Todo.objects.filter(User=request.user,complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		inbox = Message.objects.filter(reciever=request.user)
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

	context = {
		'service_details' 		: service_details,
		'Products'				: Products,
		'inbox'					: inbox,
		'inbox_count'			: inbox_count,
		'send_count'			: send_count,
		'Todos'					: Todos,
		'Todos_total' 			: Todos_total

	}

	return render(request, 'services/service_details.html', context)


def service_delete(request,id):
	data = dict()
	service_details = get_object_or_404(Pro_services, id=id)
	if request.method == "POST":
		service_details.delete()
		data['form_is_valid'] = True
		services = Pro_services.objects.filter(User=profile_details.Name).order_by('id')
		data['service'] = render_to_string('services/service_list.html',{'services':services})
	else:
		context = {'service_details':service_details}
		data['html_form'] = render_to_string('services/service_delete.html',context,request=request)

	return JsonResponse(data)


class casecreateview(LoginRequiredMixin,CreateView):
	form_class = Achievement_form
	template_name = 'achievement/case_form.html'


	def form_valid(self, form):
		form.instance.User = self.request.user
		return super(casecreateview, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(casecreateview, self).get_context_data(**kwargs)
		context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context


class caseupdateview(LoginRequiredMixin,UpdateView):
	model = achivements
	form_class = Achievement_form
	template_name = 'achievement/case_form.html'


	def get_context_data(self, **kwargs):
		context = super(caseupdateview, self).get_context_data(**kwargs)
		context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']  
		return context

class CaseListView(LoginRequiredMixin,ListView):
	model = achivements
	paginate_by = 10

	def get_queryset(self):
		return achivements.objects.filter(User=self.request.user).order_by('-id')

	def get_template_names(self):
		if True:  
			return ['achievement/case_list.html']
		else:
			pass

	def get_context_data(self, **kwargs):
		context = super(CaseListView, self).get_context_data(**kwargs)
		context['case_list'] = achivements.objects.filter(User=self.request.user).order_by('-id')
		context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

@login_required
def case_detail(request, pk):
	case_details = get_object_or_404(achivements, pk=pk)

	if not request.user.is_authenticated:
		Products = Product_activation.objects.filter(product__id = 1, is_active=True)
		Todos = Todo.objects.filter(complete=False)
		Todos_total = Todo.objects.filter(complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		inbox = Message.objects.all()
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
	else:
		Products = Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True)
		Todos = Todo.objects.filter(User=request.user,complete=False)
		Todos_total = Todo.objects.filter(User=request.user,complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		inbox = Message.objects.filter(reciever=request.user)
		inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

	context = {
		'case_details' 			: case_details,
		'Products'				: Products,
		'inbox'					: inbox,
		'inbox_count'			: inbox_count,
		'send_count'			: send_count,
		'Todos'					: Todos,
		'Todos_total' 			: Todos_total

	}

	return render(request, 'achievement/case_details.html', context)

@login_required
def case_delete(request,id):
	data = dict()
	case_details = get_object_or_404(achivements, id=id)
	if request.method == "POST":
		case_details.delete()
		data['form_is_valid'] = True
		case_list = achivements.objects.filter(User=self.request.user).order_by('-id')
		data['cases'] = render_to_string('achievement/case_list2.html',{'case_list':case_list})
	else:
		context = {'case_details':case_details}
		data['html_form'] = render_to_string('achievement/case_delete.html',context,request=request)

	return JsonResponse(data)

class proverifycreateview(LoginRequiredMixin,CreateView):
	form_class = proverifyform
	template_name = 'pro_verify/pro_verify_form.html'


	def form_valid(self, form):
		form.instance.User = self.request.user
		return super(proverifycreateview, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(proverifycreateview, self).get_context_data(**kwargs)
		context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context


class organisationupdateview(LoginRequiredMixin,UpdateView):
	model = Organisation
	form_class = organisationform
	template_name = 'Organisation/Organisation_form.html'


	def get_context_data(self, **kwargs):
		context = super(organisationupdateview, self).get_context_data(**kwargs) 
		context['organisation_details'] = Organisation.objects.all()
		if self.request.user.is_authenticated:
			context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
			context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
			context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['inbox'] = Message.objects.filter(reciever=self.request.user)
			context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 

		else:
			context['Products'] = Product_activation.objects.filter(product__id = 1, is_active=True)
			context['Todos'] = Todo.objects.filter(complete=False)
			context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
			context['inbox'] = Message.objects.all()
			context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['send_count'] = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context

class Organisation_member_listview(LoginRequiredMixin,ListView):
	model = Organisation_member
	paginate_by = 10
	template_name = 'Organisation_member/organisation_member_list.html'


	def get_queryset(self):
		return Organisation_member.objects.filter(User=self.request.user).order_by('id')

	def get_context_data(self, **kwargs):
		context = super(Organisation_member_listview, self).get_context_data(**kwargs) 
		context['organisation_member_list'] = Organisation_member.objects.filter(User=self.request.user).order_by('id')
		if self.request.user.is_authenticated:
			context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
			context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
			context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['inbox'] = Message.objects.filter(reciever=self.request.user)
			context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 

		else:
			context['Products'] = Product_activation.objects.filter(product__id = 1, is_active=True)
			context['Todos'] = Todo.objects.filter(complete=False)
			context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
			context['inbox'] = Message.objects.all()
			context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['send_count'] = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']		

		return context

class organisation_member_updateview(LoginRequiredMixin,UpdateView):
	model = Organisation_member
	form_class = organisation_memberform
	template_name = 'Organisation_member/organisation_member_form.html'

	def get_success_url(self,**kwargs):
		return reverse('userprofile:organisation_member_list')


	def get_context_data(self, **kwargs):
		context = super(organisation_member_updateview, self).get_context_data(**kwargs) 
		context['organisation_member_details'] = get_object_or_404(Organisation_member, pk=self.kwargs['pk'])
		if self.request.user.is_authenticated:
			context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
			context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
			context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['inbox'] = Message.objects.filter(reciever=self.request.user)
			context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 

		else:
			context['Products'] = Product_activation.objects.filter(product__id = 1, is_active=True)
			context['Todos'] = Todo.objects.filter(complete=False)
			context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
			context['inbox'] = Message.objects.all()
			context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
			context['send_count'] = Message.objects.all().aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context


@login_required()
def delete_members(request, pk):
	user_organisation = get_object_or_404(Organisation, User=request.user)
	member_to_delete = Organisation_member.objects.filter(pk=pk)
	if member_to_delete.exists():
		member_to_delete[0].delete()
	return redirect(reverse('userprofile:organisation_member_list'))