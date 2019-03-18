from django.db import models
from ecommerce_integration.models import Product
from userprofile.models import Profile
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.db.models import Sum

# Create your models here.


class OrderItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.title


class Order(models.Model):
    ref_code        = models.CharField(max_length=15)
    owner           = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    is_ordered      = models.BooleanField(default=False)
    items           = models.ManyToManyField(OrderItem)
    date_ordered    = models.DateTimeField(auto_now=True)
    
    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return self.items.aggregate(total=Sum('product__price'))['total'] or 0

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)
