from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
import datetime

from django.contrib.auth import get_user_model
User = get_user_model()



class company(models.Model):
	User = models.ForeignKey(User,related_name="Company_Owner",on_delete=models.CASCADE,null=True,blank=True)
	counter = models.IntegerField(blank=True,null=True)
	urlhash = models.CharField(max_length=100, null=True, blank=True, unique=True)
	created_date = models.DateField(auto_now_add=True)
	modified_date = models.DateField(auto_now=True)
	Name = models.CharField(max_length=50,blank=False)
	types = (   ('Individual','Individual'),
				('HUF','HUF'),
				('Partnership','Partnership'),
				('Trust','Trust'),
				('Private Company','Private Company'),
				('Public Company','Public Company'),
				('LLP','LLP'),
				#('',''),
			)
	Business_nature_Service_Provider = models.BooleanField(default=False)
	Business_nature_Retail = models.BooleanField(default=False)
	Business_nature_Wholesale = models.BooleanField(default=False)
	Business_nature_Works_Contract  = models.BooleanField(default=False)
	Business_nature_Leasing = models.BooleanField(default=False)
	Business_nature_Factory_Manufacturing = models.BooleanField(default=False)
	Business_nature_Bonded_Warehouse = models.BooleanField(default=False)
	Business_nature_Other = models.BooleanField(default=False)
	Please_specify = models.BooleanField(default=False)
	Type_of_company = models.CharField(max_length=32,choices=types,default='Individual')
	Shared_Users = models.CharField(max_length=32,default="Current User only") # company data sharing
	Address = models.TextField()
	Country = models.CharField(max_length=32,default='India')
	State_Name 		= (
		('Choose','Choose'),
		('Andhra Pradesh','Andhra Pradesh'),
		('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
		('Arunachal Pradesh','Arunachal Pradesh'),
		('Assam','Assam'),
		('Bihar','Bihar'),
		('Chandigarh','Chandigarh'),
		('Chhattisgarh','Chhattisgarh'),
		('Dadra and Nagar Haveli','Dadra and Nagar Haveli'),
		('Daman and Diu','Daman and Diu'),
		('Delhi','Delhi '),
		('Goa','Goa'),
		('Gujrat','Gujrat'),
		('Haryana','Haryana'),
		('Himachal Pradesh','Himachal Pradesh'),
		('Jammu and Kashmir','Jammu and Kashmir'),
		('Jharkhand','Jharkhand'),
		('Karnataka','Karnataka'),
		('Kerala','Kerala'),
		('Lakshadweep','Lakshadweep'),
		('Madhya Pradesh','Madhya Pradesh'),
		('Maharashtra','Maharashtra'),
		('Manipur','Manipur'),
		('Meghalaya','Meghalaya'),
		('Mizoram','Mizoram'),
		('Nagaland','Nagaland'),
		('Odisha','Odisha'),
		('Puducherry','Puducherry'),
		('Punjab','Punjab'),
		('Rajasthan','Rajasthan'),
		('Sikkim','Sikkim'),
		('Tamil Nadu','Tamil Nadu'),
		('Telangana','Telangana'),
		('Tripura','Tripura'),	
		('Uttar Pradesh','Uttar Pradesh'),
		('Uttarakhand','Uttarakhand'),
		('West Bengal','West Bengal'),
		)   		
	State = models.CharField(max_length=100,choices=State_Name,default='Choose')
	Pincode = models.CharField(max_length=32)
	Telephone_No = models.BigIntegerField(blank=True,null=True)
	Mobile_No = models.BigIntegerField(blank=True,null=True)

	financial_date = (
		(datetime.date((datetime.datetime.now().year),4,1),datetime.date((datetime.datetime.now().year),4,1)),
		(datetime.date((datetime.datetime.now().year),1,1),datetime.date((datetime.datetime.now().year),1,1))
		)


	Financial_Year_From = models.DateField(choices=financial_date,default=datetime.date(int(datetime.datetime.now().year),4,1), blank=False)
	Books_Begining_From = models.DateField(default=datetime.date(2018,4,1), blank=False)
	gst  = models.CharField(max_length=20,blank=True,null=True)
	pan  = models.CharField(max_length=18,blank=True,null=True)


	def __str__(self):
		return self.Name

	def save(self):
		if self.id:
			self.modified_date = datetime.datetime.now()
		else:
			self.created_date = datetime.datetime.now()
		super(company,self).save()

	def save(self, **kwargs):
		super(company, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.counter) 
				company.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.counter) 
				company.objects.filter(pk=self.pk).update(urlhash=self.urlhash)

	class Meta:
		ordering = ["Name"]
		



 










# def create_company(sender, **kwargs):
# 	if kwargs['created']:
# 		Company_Name = companyowner.objects.create(Company=kwargs['instance'])


# post_save.connect(create_user, sender=company)



