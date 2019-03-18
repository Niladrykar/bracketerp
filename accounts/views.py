from django.contrib.auth import login, logout
from django.urls import reverse_lazy,reverse
from django.views.generic import TemplateView,CreateView
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from userprofile.models import Profile, Product_activation
from messaging.models import Message
from todogst.models import Todo
from django.db.models.functions import Coalesce 
from django.db.models import Count, Value
from . import forms




# class DashboardPage(TemplateView):
#     template_name = "accounts/Dashboard.html"



class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/Signup.html"


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

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
        'form'            : form,
        'inbox'           : inbox,
        'inbox_count'     : inbox_count,
        'send_count'      : send_count,
        'Products'        : Products,
        'Todos'           : Todos,
        'Todos_total'     : Todos_total 
    }

    return render(request, 'accounts/change_password.html', context)
