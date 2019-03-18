from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from ckeditor_uploader.fields import RichTextUploadingField
import sys
from sorl.thumbnail import ImageField, get_thumbnail
from ecommerce_integration.models import coupon, Product, Product_review, Services, API
# Create your models here.

def file_size(value): # add this to some file where you can import it from
	limit = 2 * 1024 * 1024 * 1024 * 1024 * 1024 
	if value.size > limit:
		raise ValidationError('File too large. Size should not exceed 5 MB.')

class Profile(models.Model):
	Date = models.DateTimeField(auto_now_add=True)
	Full_Name = models.CharField(max_length=32,blank=True)
	user_types = (
		('Bussiness User','Bussiness User'),
		('Professional','Professional'),
		)
	user_type = models.CharField(max_length=32,choices=user_types,default='Bussiness User',blank=False)
	Name = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	E_mail = models.EmailField(max_length=70,blank=True)
	Permanant_Address = models.TextField(blank=True)
	District = models.CharField(max_length=32,blank=True)
	State_Name = (
		('Choose','Choose'),
		('Andra Pradesh','Andra Pradesh'),
		('Arunachal Pradesh','Arunachal Pradesh'),
		('Assam','Assam'),
		('Bihar','Bihar'),
		('Chhattisghar','Chhattisghar'),
		('Goa','Goa'),
		('Gujrat','Gujrat'),
		('Haryana','Haryana'),
		('Himachal Pradesh','Himachal Pradesh'),
		('Jammu and Kashmir','Jammu and Kashmir'),
		('Jharkhand','Jharkhand'),
		('Karnataka','Karnataka'),
		('Kerala','Kerala'),
		('Madhya Pradesh','Madhya Pradesh'),
		('Maharasthra','Maharasthra'),
		('Manipur','Manipur'),
		('Meghalaya','Meghalaya'),
		('Mizoram','Mizoram'),
		('Nagaland','Nagaland'),
		('Odisha','Odisha'),
		('Punjab','Punjab'),
		('Rajasthan','Rajasthan'),
		('Sikkim','Sikkim'),
		('Tamil Nadu','Tamil Nadu'),
		('Telengana','Telengana'),
		('Tripura','Tripura'),
		('Uttar Pradesh','Uttar Pradesh'),
		('Uttarakhand','Uttarakhand'),
		('West Bengal','West Bengal'),
		)
	
    		
	State = models.CharField(max_length=100,choices=State_Name,default='Choose',blank=True)
	City = models.CharField(max_length=100,blank=True)
	Country = models.CharField(max_length=32,blank=True)
	Phone_no = models.BigIntegerField(null=True,blank=True)
	basic_info = models.TextField(blank=True)
	image = models.ImageField(upload_to='user_images', null=True, blank=True)
	subscribed_products = models.ManyToManyField(Product,related_name='products_subscribed',blank=True)

	def __str__(self):
		return str(self.Name)


	def get_absolute_url(self):
		return reverse("userprofile:profiledetail")


	def save(self, *args, **kwargs):
		if self.image:
			imageTemproary = Image.open(self.image)
			outputIoStream = BytesIO()
			imageTemproaryResized = imageTemproary.resize( (128,128) ) 
			imageTemproaryResized.save(outputIoStream , format='JPEG', quality=150)
			outputIoStream.seek(0)
			self.image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
			super(Profile, self).save(*args, **kwargs)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_created_profilespecific(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(Name=instance,image='userprofile/download (1).jpg')


class Product_activation(models.Model):
	User 	    = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	product     = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_activate')
	is_active   = models.BooleanField(default=False)

	def __str__(self):
		return str(self.id)

@receiver(post_save, sender=Profile)
def product_activation(sender, instance, created, **kwargs):
	for product in instance.subscribed_products.all():
		if Product_activation.objects.filter(User=instance.Name,product=product).exists():
			pass
		else:
			Product_activation.objects.update_or_create(User=instance.Name,product=product,is_active=False)

class Organisation(models.Model):
	User 		= models.OneToOneField(settings.AUTH_USER_MODEL,related_name='organisation_user',on_delete=models.CASCADE)
	name 		= models.CharField(max_length=100,blank=True)
	location 	= models.CharField(max_length=100,blank=True)
	qualification_status = (
		('Pending for verification','Pending for verification'),
		('Verified','Verified'),
		)
	qualification   = models.CharField(max_length=100,choices=qualification_status,default='Pending for verification',blank=True)
	members 		= models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='organisation_members',blank=True)

	def __str__(self):
		return str(self.User)

	def get_absolute_url(self):
		return reverse("userprofile:profiledetail")

@receiver(post_save, sender=Profile)
def user_created_organisation(sender, instance, created, **kwargs):
	if instance.user_type == 'Professional':
		Organisation.objects.create(User=instance.Name)


class Organisation_member(models.Model):
	User 	    	= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	organisation    = models.ForeignKey(Organisation,on_delete=models.CASCADE,related_name='organisation_staff')
	member_name 	= models.ForeignKey(settings.AUTH_USER_MODEL,related_name='organisation_staff_member',on_delete=models.CASCADE,null=True,blank=True)
	is_admin  	   	= models.BooleanField(default=False)

	def __str__(self):
		return str(self.organisation)

	def get_absolute_url(self):
		return reverse("userprofile:organisation_member_list")

@receiver(post_save, sender=Organisation)
def organisation_admin(sender, instance, created, **kwargs):
	for member in instance.members.all():
		if Organisation_member.objects.filter(User=instance.User,organisation=Organisation.objects.filter(User=instance.User,name=instance.name).first(),member_name=member).exists():
			pass
		else:
			Organisation_member.objects.update_or_create(User=instance.User,organisation=Organisation.objects.filter(User=instance.User,name=instance.name).first(),member_name=member,is_admin=False)


class pro_verify(models.Model):
	User 		= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	product 	= models.ForeignKey(Product,on_delete=models.CASCADE,related_name='pro_product')
	phone_no 	= models.BigIntegerField(null=True,blank=True)
	e_mail 		= models.EmailField(max_length=70,blank=True)
	upload_1	= models.FileField(upload_to="pro_verification",blank=True, validators=[file_size])
	u1_status 	= models.BooleanField(default=False)
	upload_2	= models.FileField(upload_to="pro_verification",blank=True, validators=[file_size])
	u2_status 	= models.BooleanField(default=False)
	upload_3	= models.FileField(upload_to="pro_verification",blank=True, validators=[file_size])
	u3_status 	= models.BooleanField(default=False)

	def __str__(self):
		return str(self.User)

	def get_absolute_url(self):
		return reverse("userprofile:profiledetail")

class Post(models.Model):
	User 	= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	post 	= RichTextUploadingField(blank=True, null=True,
                                      config_name='special',
                                      external_plugin_resources=[(
                                          'youtube',
                                          '/static/ckeditor/ckeditor/plugins/youtube_2.1.13/youtube/',
                                          'plugin.js',
                                          )],
                                      )
	date 	= models.DateTimeField(auto_now_add=True)
	like 	= models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='like_post',blank=True)



	def __str__(self):
		return str(self.post)

	def get_absolute_url(self):
		return reverse("userprofile:post_details", kwargs={'pk':self.pk})

	def total_like(self):
		return self.like.count()

		
class Post_comment(models.Model):
	User 		= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	post 		= models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_comment')
	text 		= models.TextField()
	Date 		= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.text

class Pro_services(models.Model):
	User 			= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	service_name	= models.CharField(max_length=100,blank=True)
	details 		= models.CharField(max_length=100,blank=True)
	types = (
		('Returns','Returns'),
		('Communication','Communication'),
		('License','License')
		)
	service_type 	= models.CharField(max_length=100,choices=types,default='Returns',blank=True)
	time = (
		('ANNUALLY','ANNUALLY'),
		('QUARTERLY','QUARTERLY'),
		('ONE TIME','ONE TIME')
		)
	duration 		= models.CharField(max_length=100,choices=time,default='ANNUALLY',blank=True)
	mode = (
		('ON-PREMISES','ON-PREMISES'),
		('CALLS - VOIP','CALLS - VOIP'),
		('COLLECTION FROM CLIENT','COLLECTION FROM CLIENT')
		)
	service_mode 	= models.CharField(max_length=100,choices=mode,default='ON-PREMISES',blank=True)
	rate 			= models.DecimalField(default=0.00,max_digits=10,decimal_places=2,blank=True)

	def __str__(self):
		return self.service_name

	def get_absolute_url(self):
		return reverse("userprofile:service_details", kwargs={'pk':self.pk})

class achivements(models.Model):
	User 		= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	legal_case 	= models.BooleanField(default=False)
	act 		= models.CharField(max_length=100,blank=True)
	location 	= models.CharField(max_length=100,blank=True)
	facts 		= models.CharField(max_length=100,blank=True)
	issue 		= models.CharField(max_length=100,blank=True)
	argument 	= models.CharField(max_length=100,blank=True)
	judgement 	= models.CharField(max_length=100,blank=True)
	user_role 	= models.CharField(max_length=100,blank=True)

	def __str__(self):
		return self.act

	def get_absolute_url(self):
		return reverse("userprofile:case_details", kwargs={'pk':self.pk})


		



