from django.core.exceptions import PermissionDenied
from userprofile.models import Profile, Product_activation


def product_1_activation(function):
    def wrap(request, *args, **kwargs):
        products = Product_activation.objects.filter(User=request.user,product__id = 1, is_active=True)
        if products:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap