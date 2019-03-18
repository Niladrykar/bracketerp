from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404# Create your views here.
from ecommerce_cart.extras import generate_order_id
from ecommerce_cart.models import OrderItem, Order
from ecommerce_integration.models import Product
from userprofile.models import Profile
from todogst.models import Todo
from django.db.models.functions import Coalesce
from django.db.models import Value, Sum, Count
import datetime
from userprofile.models import Profile, Product_activation
from messaging.models import Message


def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, Name=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, Name=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
    # check if the user already owns this product
    if product in request.user.profile.subscribed_products.all():
        messages.info(request, 'You already own this ebook')
        return redirect(reverse('ecommerce_integration:productlist')) 
    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    return redirect(reverse('ecommerce_integration:productlist'))

@login_required
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    order_list = Order.objects.all().order_by('-id')

    inbox = Message.objects.filter(reciever=request.user)
    inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
    send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

    context = {
        'order'         : existing_order,
        'order_list'    : order_list,
        'Products'      : Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True),
        'inbox'         : inbox,
        'inbox_count'   : inbox_count,
        'send_count'    : send_count,
        'Todos'         : Todo.objects.filter(User=request.user, complete=False),
        'Todos_total'   : Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
    }
    return render(request, 'cart/cart.html', context)

@login_required
def checkout(request, **kwargs):
    existing_order = get_user_pending_order(request)
    order_list = Order.objects.all()

    inbox = Message.objects.filter(reciever=request.user)
    inbox_count = inbox.aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
    send_count = Message.objects.filter(sender=request.user).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']

    context = {
        'order'         : existing_order,
        'order_list'    : order_list,
        'inbox'         : inbox,
        'inbox_count'   : inbox_count,
        'send_count'    : send_count,
        'Products'      : Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True),
        'Todos'         : Todo.objects.filter(User=request.user, complete=False),
        'Todos_total'   : Todo.objects.filter(User=request.user, complete=False).aggregate(the_sum=Coalesce(Count('id'), Value(0)))['the_sum']
    }
    return render(request, 'cart/checkout.html', context)

@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
    return redirect(reverse('ecommerce_cart:order_summary'))

@login_required()
def update_transaction_records(request):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update the placed order
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = datetime.datetime.now()
    order_to_purchase.save()
    
    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add products to user profile
    user_profile = get_object_or_404(Profile, Name=request.user)
    # get the products from the items
    order_products = [item.product for item in order_items]
    user_profile.subscribed_products.add(*order_products)
    user_profile.save()

    
    # # create a transaction
    # transaction = Transaction(profile=request.user.profile,
    #                         token=token,
    #                         order_id=order_to_purchase.id,
    #                         amount=order_to_purchase.get_cart_total(),
    #                         success=True)
    # # save the transcation (otherwise doesn't exist)
    # transaction.save()


    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    # messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('ecommerce_integration:productlist'))



