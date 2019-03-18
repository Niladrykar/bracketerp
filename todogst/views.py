from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Todo
from .forms import TodoForm
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Coalesce 
from django.db.models import Count, Value
from userprofile.models import Profile, Product_activation
from messaging.models import Message
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def index(request):
    todo_list = Todo.objects.filter(User=request.user).order_by('-id')

    form = TodoForm()

    inbox = Message.objects.filter(reciever=request.user)
    inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 
    send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
    
    context = {

        'todo_list'     : todo_list, 
        'form'          : form,
        'inbox'         : inbox,
        'inbox_count'   : inbox_count,
        'send_count'    : send_count,
        'Todos'         : Todo.objects.filter(User=request.user, complete=False),
        'Products'      : Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True),
        'Todos_total'   : Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum'] 

    }

    return render(request, 'todogst/index.html', context)

    

@login_required
@require_POST
def addTodo(request):
    form = TodoForm(request.POST)

    if form.is_valid(): 
        new_todo = Todo(text=request.POST['text'], complete_by=request.POST['complete_by'], User=request.user)
        new_todo.save()

    return redirect('todogst:index')


@login_required
def completeTodo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.complete = True
    todo.save()

    return redirect('todogst:index')



@login_required
def deleteCompleted(request):
    Todo.objects.filter(complete__exact=True).delete()

    return redirect('todogst:index')


@login_required
def deleteAll(request):
    Todo.objects.filter(User=request.user).delete()

    return redirect('todogst:index')