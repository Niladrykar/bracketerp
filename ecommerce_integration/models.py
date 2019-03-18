from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.urls import reverse_lazy, reverse



# Create your models here.
class coupon(models.Model):
	title_code 	= models.CharField(max_length=32)
	description	= models.TextField(null=True)

	def __str__(self):
		return str(self.title)

class Product(models.Model):
	title 		= models.CharField(max_length=32)
	price 		= models.DecimalField(default=10000.00,max_digits=10,decimal_places=2)
	image		= models.ImageField(upload_to='product_images',default='userprofile/comming soon.jpg', null=True, blank=True)
	rating		= models.DecimalField(default=4.5,max_digits=4,decimal_places=2)
	summary		= models.TextField(max_length=150,null=True)
	description	= models.TextField(null=True)
	coupons		= models.ForeignKey(coupon,on_delete=models.CASCADE,null=True,blank=True,related_name='product_coupons')


	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		return reverse("ecommerce_integration:productdetail", kwargs={'pk':self.pk})

	def save(self, *args, **kwargs):
		if self.image:
			imageTemproary = Image.open(self.image).convert('RGB')
			outputIoStream = BytesIO()
			imageTemproaryResized = imageTemproary.resize( (1000,400) ) 
			imageTemproaryResized.save(outputIoStream , format='JPEG', quality=300)
			outputIoStream.seek(0)
			self.image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
			super(Product, self).save(*args, **kwargs)




class Product_review(models.Model):
	User 	= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	date 	= models.DateTimeField(auto_now_add=True)
	name 	= models.CharField(max_length=32)
	e_mail 	= models.EmailField(max_length=70, null=True, blank=True)
	reviews	= models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_review')
	text 	= models.TextField()


	def __str__(self):
		return self.text
			

class Services(models.Model):
	User 		= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	title 		= models.CharField(max_length=32)
	image		= models.ImageField(upload_to='service_images',default='userprofile/comming soon.jpg', null=True, blank=True)
	summary		= models.TextField(max_length=150,null=True)
	description	= models.TextField(null=True)


	def __str__(self):
		return str(self.title)

	def save(self, *args, **kwargs):
		if self.image:
			imageTemproary = Image.open(self.image).convert('RGB')
			outputIoStream = BytesIO()
			imageTemproaryResized = imageTemproary.resize( (1000,400) ) 
			imageTemproaryResized.save(outputIoStream , format='JPEG', quality=300)
			outputIoStream.seek(0)
			self.image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
			super(Services, self).save(*args, **kwargs)

class API(models.Model):
	User 		= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	title 		= models.CharField(max_length=32)
	price 		= models.DecimalField(default=10000.00,max_digits=10,decimal_places=2)
	image		= models.ImageField(upload_to='api_images',default='userprofile/comming soon.jpg', null=True, blank=True)
	rating		= models.DecimalField(default=4.5,max_digits=4,decimal_places=2)
	summary		= models.TextField(max_length=150,null=True)
	description	= models.TextField(null=True)
	coupons		= models.ForeignKey(coupon,on_delete=models.CASCADE,null=True,blank=True,related_name='api_coupons')


	def __str__(self):
		return str(self.title)

	def save(self, *args, **kwargs):
		if self.image:
			imageTemproary = Image.open(self.image).convert('RGB')
			outputIoStream = BytesIO()
			imageTemproaryResized = imageTemproary.resize( (1000,400) ) 
			imageTemproaryResized.save(outputIoStream , format='JPEG', quality=300)
			outputIoStream.seek(0)
			self.image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
			super(API, self).save(*args, **kwargs)

	