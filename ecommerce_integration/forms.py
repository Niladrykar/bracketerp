from django import forms
from ecommerce_integration.models import coupon, Product, Product_review, Services, API


class Product_review_form(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(Product_review_form, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs = {'class': 'form-control', 'placeholder':"Name",}
		self.fields['e_mail'].widget.attrs = {'class': 'form-control', 'placeholder':"Email",}
		self.fields['text'].widget.attrs = {'class': 'form-control', 'placeholder':"Your review",}	
	
	class Meta:
		model = Product_review
		fields = ['name', 'e_mail', 'text'] 