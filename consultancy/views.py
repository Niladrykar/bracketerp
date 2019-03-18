from django.shortcuts import render
from consultancy.models import consultancy,Answer
from consultancy.forms import consultancyform,Answerform
from django.views.generic import (ListView,DetailView,
								  CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from todogst.models import Todo
from django.db.models import Value, Sum, Count, Q, F, ExpressionWrapper, Subquery, OuterRef, FloatField
from django.db.models.functions import Coalesce
from ecommerce_integration.models import coupon, Product, Product_review, Services, API
from userprofile.models import Profile, Product_activation
from messaging.models import Message
# Create your views here.


class consultancyListView(ListView):
	model = consultancy
	paginate_by = 6

	def get_queryset(self):
		return consultancy.objects.all().order_by('-id')

	def get_context_data(self, **kwargs):
		context = super(consultancyListView, self).get_context_data(**kwargs)
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





class myconsultancyListView(LoginRequiredMixin,ListView):
	model = consultancy
	paginate_by = 6

	def get_queryset(self):
		return consultancy.objects.filter(User=self.request.user).order_by('-id')

	def get_template_names(self):
		if True:  
			return ['consultancy/myconsultancy.html']
		else:
			return ['consultancy/consultancy_list.html']

	def get_context_data(self, **kwargs):
		context = super(myconsultancyListView, self).get_context_data(**kwargs)
		context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context





def consultancy_detail(request, pk):
	consultancy_details = get_object_or_404(consultancy, pk=pk)
	comments = Answer.objects.filter(Questions=consultancy_details.pk).order_by('-id')

	is_liked = False
	if consultancy_details.like.filter(pk=request.user.id).exists():
		is_liked = True

	if request.method == "POST":
		Answer_form = Answerform(request.POST or None)
		if Answer_form.is_valid():
			text = request.POST.get('text')
			answer = Answer.objects.create(Questions=consultancy_details, User=request.user, text=text)
			answer.save()
			return HttpResponseRedirect(consultancy_details.get_absolute_url())
	else:
		Answer_form = Answerform()

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
		'consultancy_details' 	: consultancy_details,
		'comments' 				: comments,	
		'is_liked' 				: is_liked,
		'total_like' 			: consultancy_details.total_like(),
		'Answer_form' 			: Answer_form,
		'Products'				: Products,
		'inbox'					: inbox,
		'inbox_count'			: inbox_count,
		'send_count'			: send_count,
		'Todos'					: Todos,
		'Todos_total' 			: Todos_total

	}

	return render(request, 'consultancy/consultancy_details.html', context)


@login_required
def liked_post(request):
	consultancy_details = get_object_or_404(consultancy, pk=request.POST.get('consultancy_details_id'))
	is_liked = False
	if consultancy_details.like.filter(pk=request.user.id).exists():
		consultancy_details.like.remove(request.user)
		is_liked = False
	else:
		consultancy_details.like.add(request.user)
		is_liked = True

	context = {
		'consultancy_details' : consultancy_details,
		'is_liked' : is_liked,
		'total_like' : consultancy_details.total_like(),
	}

	if request.is_ajax():
		html = render_to_string('consultancy/consultancy_like.html', context, request=request)
		return JsonResponse({'form' : html})



class consultancycreate(LoginRequiredMixin,CreateView):
	form_class = consultancyform
	template_name = "consultancy/consultancy_form.html"

	def form_valid(self, form):
		form.instance.User = self.request.user
		return super(consultancycreate, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(consultancycreate, self).get_context_data(**kwargs)
		context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context

class consultancyupdate(LoginRequiredMixin,UpdateView):
	model = consultancy
	form_class  = consultancyform
	template_name = "consultancy/consultancy_form.html"

	def get_context_data(self, **kwargs):
		context = super(consultancyupdate, self).get_context_data(**kwargs)
		context['Products'] = Product_activation.objects.filter(User=self.request.user,product__id = 1, is_active=True)
		context['Todos'] = Todo.objects.filter(User=self.request.user, complete=False)
		context['Todos_total'] = context['Todos'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['inbox'] = Message.objects.filter(reciever=self.request.user)
		context['inbox_count'] = context['inbox'].aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
		context['send_count'] = Message.objects.filter(sender=self.request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
		return context


def save_all(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			queries = consultancy.objects.all().order_by('-id')
			data['query'] = render_to_string('consultancy/Questions.html',{'queries':queries})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

def query_update(request,id):
	query_details = get_object_or_404(consultancy,id=id)
	if request.method == 'POST':
		form = consultancyform(request.POST,instance=query_details)
	else:
		form = consultancyform(instance=query_details)
	return save_all(request,form,'consultancy/consultancy_update.html')

def query_delete(request,id):
	data = dict()
	query_details = get_object_or_404(consultancy,id=id)
	if request.method == "POST":
		query_details.delete()
		data['form_is_valid'] = True
		queries = consultancy.objects.all().order_by('-id')
		data['query'] = render_to_string('consultancy/Questions.html',{'queries':queries})
	else:
		context = {'query_details':query_details}
		data['html_form'] = render_to_string('consultancy/consultancy_confirm_delete.html',context,request=request)

	return JsonResponse(data)



def save_all(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			answers = Answer.objects.all().order_by('-id')
			data['comments'] = render_to_string('consultancy/answers.html',{'answers':answers})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

def answer_update(request,id):
	answer = get_object_or_404(Answer,id=id)
	if request.method == 'POST':
		form = Answerform(request.POST,instance=answer)
	else:
		form = Answerform(instance=answer)
	return save_all(request,form,'consultancy/answer_update.html')

def answer_delete(request,id):
	data = dict()
	answer = get_object_or_404(Answer,id=id)
	if request.method == "POST":
		answer.delete()
		data['form_is_valid'] = True
		answers = Answer.objects.all().order_by('-id')
		data['comments'] = render_to_string('consultancy/answers.html',{'answers':answers})
	else:
		context = {'answer':answer}
		data['html_form'] = render_to_string('consultancy/answer_delete.html',context,request=request)

	return JsonResponse(data)

def search(request):
	template = 'consultancy/consultancy_list.html'

	query = request.GET.get('q')

	if query:
		result = consultancy.objects.filter(Q(Questions__icontains=query) | Q(Date__icontains=query))
	else:
		result = consultancy.objects.all().order_by('id')

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
		'consultancy_list'	: result,
		'Products'			: Products,
		'inbox'				: inbox,
		'inbox_count'		: inbox_count,
		'send_count'		: send_count,
		'Todos'				: Todos,
		'Todos_total' 		: Todos_total 

	}

	return render(request, template, context)



