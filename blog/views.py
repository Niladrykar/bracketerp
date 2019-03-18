from django.shortcuts import render
from django.views.generic import (ListView,DetailView,
								  CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from blog.models import Blog,categories,Blog_comments
from ecommerce_integration.models import coupon, Product, Product_review, Services, API
from userprofile.models import Profile, Product_activation
from blog.forms import Blogform,BlogSearchForm,Blog_comments_form
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from todogst.models import Todo
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models.functions import Coalesce
from messaging.models import Message
from django.db.models import Value, Sum, Count, F, ExpressionWrapper, Subquery, OuterRef, FloatField



# Create your views here.

class viewbloglistview(ListView):
	model = Blog
	paginate_by = 3

	def get_template_names(self):
		if True:  
			return ['blog/view_blogs.html']
		else:
			return ['blog/blog_list.html']

	def get_queryset(self):
		return Blog.objects.all().order_by('-blog_views')[:20]

	def get_context_data(self, **kwargs):
		context = super(viewbloglistview, self).get_context_data(**kwargs) 
		context['categories_list'] = categories.objects.all()
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

class likebloglistview(ListView):
	model = Blog
	paginate_by = 3

	def get_template_names(self):
		if True:  
			return ['blog/blog_by_likes.html']
		else:
			return ['blog/blog_list.html']

	def get_queryset(self):
		return Blog.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:20]

	def get_context_data(self, **kwargs):
		context = super(likebloglistview, self).get_context_data(**kwargs) 
		context['categories_list'] = categories.objects.all()
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



class latestbloglistview(ListView):
	model = Blog
	paginate_by = 3

	def get_template_names(self):
		if True:  
			return ['blog/latest_blog.html']
		else:
			return ['blog/blog_list.html']

	def get_queryset(self):
		return Blog.objects.all().order_by('-id')

	def get_context_data(self, **kwargs):
		context = super(latestbloglistview, self).get_context_data(**kwargs) 
		context['categories_list'] = categories.objects.all()
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



class bloglistview(LoginRequiredMixin,ListView):
	model = Blog
	paginate_by = 3
	
	
	def get_queryset(self):
		return Blog.objects.filter(User=self.request.user).order_by('id')

	def get_context_data(self, **kwargs):
		context = super(bloglistview, self).get_context_data(**kwargs) 
		context['categories_list'] = categories.objects.all()
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


class allbloglistview(ListView):
	model = Blog
	paginate_by = 3


	def get_template_names(self):
		if True:  
			return ['blog/all_blogs.html']
		else:
			return ['blog/blog_list.html']
		
	def get_queryset(self):
		return Blog.objects.all().order_by('id')

	def get_context_data(self, **kwargs):
		context = super(allbloglistview, self).get_context_data(**kwargs) 
		context['categories_list'] = categories.objects.all()
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




def post_detail(request, pk):
	blog_details = get_object_or_404(Blog, pk=pk)
	blogcomments = Blog_comments.objects.filter(Questions=blog_details.pk).order_by('-id')

	blog_details.blog_views=blog_details.blog_views + 1
	blog_details.save()	

	is_liked = False
	if blog_details.likes.filter(pk=request.user.id).exists():
		is_liked = True

	if request.method == "POST":
		Blog_comments_user_form = Blog_comments_form(request.POST or None)
		if Blog_comments_user_form.is_valid():
			text = request.POST.get('text')
			answer = Blog_comments.objects.create(Questions=blog_details, User=request.user, text=text)
			answer.save()
			return HttpResponseRedirect(blog_details.get_absolute_url())
	else:
		Blog_comments_user_form = Blog_comments_form()

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

		'blogcomments'		: blogcomments,
		'Blog_comments_user_form'	: Blog_comments_user_form,
		'blog_details' : blog_details,
		'is_liked' : is_liked,
		'total_likes' : blog_details.total_likes(),
		'Products'	: Products,
		'categories_list' : categories.objects.all(),
		'inbox'			: inbox,
		'inbox_count'	: inbox_count,
		'send_count'	: send_count,
		'Todos'		 : Todos,
		'Todos_total' 	: Todos_total 
		
		
	}

	return render(request, 'blog/blog_details.html', context)
	

@login_required
def like_post(request):
	blog_details = get_object_or_404(Blog, pk=request.POST.get('blog_details_id'))
	is_liked = False
	if blog_details.likes.filter(pk=request.user.id).exists():
		blog_details.likes.remove(request.user)
		is_liked = False
	else:
		blog_details.likes.add(request.user)
		is_liked = True

	context = {
		'blog_details' : blog_details,
		'is_liked' : is_liked,
		'total_likes' : blog_details.total_likes(),
		
	}

	if request.is_ajax():
		html = render_to_string('blog/like_section.html', context, request=request)
		return JsonResponse({'form' : html})



class blogcreateview(LoginRequiredMixin,CreateView):
	form_class = Blogform
	template_name = 'blog/blog_form.html'

	def form_valid(self, form):
		form.instance.User = self.request.user
		return super(blogcreateview, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(blogcreateview, self).get_context_data(**kwargs)
		context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class blogupdateview(LoginRequiredMixin,UpdateView):
	model = Blog
	form_class = Blogform
	template_name = 'blog/blog_form.html'


	def get_context_data(self, **kwargs):
		context = super(blogupdateview, self).get_context_data(**kwargs)
		context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']  
		return context


class blogdeleteview(LoginRequiredMixin,DeleteView):
	model = Blog
	success_url = reverse_lazy("blog:bloglist")

	def get_context_data(self, **kwargs):
		context = super(blogdeleteview, self).get_context_data(**kwargs)
		context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		return context


class categoryListView(ListView):
	model = categories
	template_name = 'blog/blog_list.html'
	paginate_by = 6

	def get_queryset(self):
		return Blog.objects.order_by('-id')

	def get_context_data(self, **kwargs):
		context = super(categoryListView, self).get_context_data(**kwargs)
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


class categoryDetailView(DetailView):
	context_object_name = 'category_details'
	model = categories
	template_name = 'blog/category_detail.html'
	paginate_by = 6

	def get_context_data(self, **kwargs):
		context = super(categoryDetailView, self).get_context_data(**kwargs)
		context['blog_list'] = Blog.objects.all()
		context['categories_list'] = categories.objects.all()
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

def search(request):
	template = 'blog/blog_list.html'

	query = request.GET.get('q')

	if query:
		result = Blog.objects.filter(Q(Blog_title__icontains=query) | Q(Description__icontains=query) | Q(Category__Title__icontains=query))
	else:
		result = Blog.objects.all().order_by('id')

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
		'blogs'			: result,
		'categories_l'	: categories.objects.all(),
		'Products'		: Products,
		'inbox'			: inbox,
		'inbox_count'	: inbox_count,
		'send_count'	: send_count,
		'Todos'			: Todos,
		'Todos_total' 	: Todos_total 

	}

	return render(request, template, context)



