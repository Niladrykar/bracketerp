from django.db import models
from accounting_double_entry.models import group1,ledger1,journal,selectdatefield,Pl_journal
from company.models import company
from django.conf import settings
from django.core.exceptions import ValidationError
import datetime
from django.db.models.signals import pre_save,post_save,post_delete
from django.dispatch import receiver
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.db.models.functions import Coalesce
from django.db.models import Value
from django.db.models import F
from sorl.thumbnail import ImageField, get_thumbnail
# Create your models here.

class Stockgroup(models.Model):
	User       = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company    = models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True)
	counter    = models.IntegerField(blank=True,null=True)
	urlhash    = models.CharField(max_length=100, null=True, blank=True, unique=True)
	name       = models.CharField(max_length=32)
	under      = models.ForeignKey("self",on_delete=models.CASCADE,related_name='Stock_group',null=True)
	quantities = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	def save(self, **kwargs):
		super(Stockgroup, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SSG') + str(self.counter)
				Stockgroup.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SSG') + str(self.counter)
				Stockgroup.objects.filter(pk=self.pk).update(urlhash=self.urlhash)

@receiver(post_save, sender=company)
def user_created_stockgroup(sender, instance, created, **kwargs):
	c = Stockgroup.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		Stockgroup.objects.create(counter=c, User=instance.User,Company=instance,name='Primary',quantities=False)


class Simpleunits(models.Model):
	User       	= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company    	= models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True)
	counter 	= models.IntegerField(blank=True,null=True)
	urlhash		= models.CharField(max_length=100, null=True, blank=True, unique=True)
	symbol     	= models.CharField(max_length=32)
	formal     	= models.CharField(max_length=32)

	def __str__(self):
		return self.symbol

	def save(self, **kwargs):
		super(Simpleunits, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SSU') + str(self.counter)
				Simpleunits.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SSU') + str(self.counter)
				Simpleunits.objects.filter(pk=self.pk).update(urlhash=self.urlhash)


class Compoundunits(models.Model):
	User       		= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company    		= models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True)
	counter	 		= models.IntegerField(blank=True,null=True)
	urlhash 		= models.CharField(max_length=100, null=True, blank=True, unique=True)
	firstunit  		= models.ForeignKey(Simpleunits,on_delete=models.CASCADE,related_name='firsts')
	conversion 		= models.DecimalField(max_digits=19,decimal_places=2)
	seconds_unit 	= models.ForeignKey(Simpleunits,on_delete=models.CASCADE,related_name='seconds')

	def __str__(self):
		return str(self.firstunit) +  '  of  '  + str(self.seconds_unit)

	def clean(self):
		if self.firstunit == self.seconds_unit:
			raise ValidationError('First Unit Should Not Be Equal To Second Unit')


	def save(self, **kwargs):
		super(Compoundunits, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SCU') + str(self.counter)
				Compoundunits.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SCU') + str(self.counter)
				Compoundunits.objects.filter(pk=self.pk).update(urlhash=self.urlhash)


class Stockdata(models.Model):
	User        = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company     = models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True)
	counter 	= models.IntegerField(blank=True,null=True)
	urlhash 	= models.CharField(max_length=100, null=True, blank=True, unique=True)
	Date 		= models.DateField(default=datetime.date.today,blank=False, null=True)
	daterange	= models.ForeignKey(selectdatefield,on_delete=models.CASCADE,null=True,blank=True,related_name='stockrange')
	stock_name  = models.CharField(max_length=32)
	batch_no	= models.PositiveIntegerField(blank=True, null=True)
	bar_code 	= ImageField(upload_to='stockmanagement', null=True, blank=True)
	mnf_date	= models.DateField(blank=True, null=True)
	exp_date	= models.DateField(blank=True, null=True)
	under       = models.ForeignKey(Stockgroup,on_delete=models.CASCADE,related_name='stocks')
	unitsimple  = models.ForeignKey(Simpleunits,on_delete=models.CASCADE,null=True,blank=True,related_name='firsts_unit')
	unitcomplex = models.ForeignKey(Compoundunits,on_delete=models.CASCADE,null=True,blank=True,related_name='seconds_unit_complex')
	gst_rate    = models.DecimalField(max_digits=4,decimal_places=2,default=5)
	hsn         = models.PositiveIntegerField()

	def __str__(self):
		return self.stock_name

	def clean(self):
		if self.unitsimple != None and self.unitcomplex != None:
			raise ValidationError({'unitcomplex':["You are not supposed to select both units!"],'unitsimple':["You are not supposed to select both units!"]})

	def save(self, *args, **kwargs):
		if self.bar_code:
			self.bar_code = get_thumbnail(self.bar_code, '128x128', quality=150, format='JPEG').url
		super(Stockdata, self).save(*args, **kwargs)

	def save(self, **kwargs):
		super(Stockdata, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SSD') + str(self.counter)
				Stockdata.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SSD') + str(self.counter)
				Stockdata.objects.filter(pk=self.pk).update(urlhash=self.urlhash)


class Purchase(models.Model):
	User         	= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company      	= models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True)
	counter 	 	= models.IntegerField(blank=True,null=True)
	urlhash 	 	= models.CharField(max_length=100, null=True, blank=True, unique=True)
	date         	= models.DateField(default=datetime.date.today,blank=False, null=True)
	ref_no       	= models.PositiveIntegerField()
	Party_ac     	= models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='partyledger')
	purchase     	= models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='purchaseledger')
	billname     	= models.CharField(max_length=32,default='Supplier')
	Address		 	= models.CharField(max_length=32,blank=True)
	GSTIN        	= models.CharField(max_length=32,blank=True)
	PAN          	= models.CharField(max_length=32,blank=True)
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
	State 		 	= models.CharField(max_length=100,choices=State_Name,default='Choose')
	Contact      	= models.BigIntegerField(blank=True,null=True)
	DeliveryNote 	= models.CharField(max_length=32,blank=True)
	Supplierref  	= models.CharField(max_length=32,blank=True)
	Mode         	= models.CharField(max_length=32,blank=True)
	sub_total 		= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
	cgst_alltotal	= models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	gst_alltotal	= models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	Total 		 	= models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

	def __str__(self):
		return str(self.Party_ac)

	def save(self, **kwargs):
		super(Purchase, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SP') + str(self.counter)
				Purchase.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SP') + str(self.counter)
				Purchase.objects.filter(pk=self.pk).update(urlhash=self.urlhash)


class Sales(models.Model):
	User         	= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company      	= models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True)
	counter 	 	= models.IntegerField(blank=True,null=True)
	urlhash 	 	= models.CharField(max_length=100, null=True, blank=True, unique=True)
	ref_no       	= models.PositiveIntegerField()
	Party_ac     	= models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='partyledgersales')
	sales        	= models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='saleledger')
	billname     	= models.CharField(max_length=32,default='Customer')
	date         	= models.DateField(default=datetime.date.today,blank=False, null=True)
	Address		 	= models.CharField(max_length=32,blank=True)
	GSTIN        	= models.CharField(max_length=32,blank=True)
	PAN         	= models.CharField(max_length=32,blank=True)
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
	State 		 	= models.CharField(max_length=100,choices=State_Name,default='Choose')
	Contact      	= models.BigIntegerField(blank=True,null=True)
	DeliveryNote 	= models.CharField(max_length=32,blank=True)
	Supplierref  	= models.CharField(max_length=32,blank=True)
	Mode         	= models.CharField(max_length=32,blank=True)
	sub_total 	 	= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
	cgst_alltotal	= models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	gst_alltotal	= models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	Total 		 	= models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

	def __str__(self):
		return str(self.Party_ac)

	def save(self, **kwargs):
		super(Sales, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SS') + str(self.counter)
				Sales.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SS') + str(self.counter)
				Sales.objects.filter(pk=self.pk).update(urlhash=self.urlhash)


class Stock_Total(models.Model):
	purchases   = models.ForeignKey(Purchase,on_delete=models.CASCADE,null=True,blank=False,related_name='purchasetotal') 
	stockitem   = models.ForeignKey(Stockdata,on_delete=models.CASCADE,null=True,blank=True,related_name='purchasestock') 
	Quantity_p  = models.PositiveIntegerField()
	rate_p		= models.DecimalField(max_digits=10,decimal_places=2)
	Disc_p    	= models.DecimalField(max_digits=10,decimal_places=2,default=0)
	cgst 		= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True)
	sgst 		= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True)
	igst 		= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True)
	ugst 		= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True)
	cgst_total	= models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	gst_total	= models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	Total_p     = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	grand_total = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

	def __str__(self):
		return str(self.purchases)



class Stock_Total_sales(models.Model):
	sales       = models.ForeignKey(Sales,on_delete=models.CASCADE,null=True,blank=False,related_name='saletotal')
	stockitem   = models.ForeignKey(Stockdata,on_delete=models.CASCADE,null=True,blank=True,related_name='salestock') 
	Quantity    = models.PositiveIntegerField(null=True,blank=True)
	rate		= models.DecimalField(max_digits=10,decimal_places=2)
	Disc    	= models.DecimalField(max_digits=10,decimal_places=2,default=0)
	cgst 		= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True)
	sgst 		= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True)
	igst 		= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True)
	ugst 		= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True)
	cgst_total	= models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	gst_total	= models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	Total 		= models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	grand_total = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

	def __str__(self):
		return str(self.sales)




@receiver(pre_save, sender=Stock_Total)
def update_gst_rate_purchase(sender, instance, *args, **kwargs):
	if instance.purchases.State == instance.purchases.Company.State:
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.sgst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.ugst = 0
	elif instance.purchases.State == 'Delhi':
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.sgst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.ugst = 0
	elif instance.purchases.State == 'Puducherry':
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.sgst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.ugst = 0
	elif instance.purchases.State == 'Andaman & Nicobar Islands':
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.ugst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.sgst = 0
	elif instance.purchases.State == 'Chandigarh':
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.ugst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.sgst = 0
	elif instance.purchases.State == 'Dadra and Nagar Haveli':
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.ugst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.sgst = 0
	elif instance.purchases.State == 'Daman and Diu':
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.ugst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.sgst = 0
	elif instance.purchases.State == 'Lakshadweep':
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.ugst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.sgst = 0
	else:
		instance.cgst = 0
		instance.igst = instance.stockitem.gst_rate 
		instance.ugst = 0
		instance.sgst = 0

@receiver(pre_save, sender=Stock_Total)
def update_amount_purchase(sender, instance, *args, **kwargs):
	instance.Total_p = instance.rate_p * instance.Quantity_p * (1 - (instance.Disc_p/100))


@receiver(pre_save, sender=Stock_Total)
def update_gst_rate_purchasetotal(sender, instance, *args, **kwargs):
	if instance.purchases.State == instance.purchases.Company.State:
		instance.cgst_total = instance.cgst * instance.Total_p / 100
		instance.gst_total 	= instance.sgst * instance.Total_p / 100

	elif instance.purchases.State == 'Delhi':
		instance.cgst_total = instance.cgst * instance.Total_p / 100
		instance.gst_total 	= instance.sgst * instance.Total_p / 100

	elif instance.purchases.State == 'Puducherry':
		instance.cgst_total = instance.cgst * instance.Total_p / 100
		instance.gst_total 	= instance.sgst * instance.Total_p / 100

	elif instance.purchases.State == 'Andaman & Nicobar Islands':
		instance.cgst_total = instance.cgst * instance.Total_p / 100
		instance.gst_total = instance.ugst * instance.Total_p / 100

	elif instance.purchases.State == 'Chandigarh':
		instance.cgst_total = instance.cgst * instance.Total_p / 100
		instance.gst_total = instance.ugst * instance.Total_p / 100

	elif instance.purchases.State == 'Dadra and Nagar Haveli':
		instance.cgst_total = instance.cgst * instance.Total_p / 100
		instance.gst_total = instance.ugst * instance.Total_p / 100

	elif instance.purchases.State == 'Daman and Diu':
		instance.cgst_total = instance.cgst * instance.Total_p / 100
		instance.gst_total = instance.ugst * instance.Total_p / 100

	elif instance.purchases.State == 'Lakshadweep':
		instance.cgst_total = instance.cgst * instance.Total_p / 100
		instance.gst_total = instance.ugst * instance.Total_p / 100

	else:
		instance.gst_total = instance.igst * instance.Total_p / 100
	if instance.cgst_total == None:
		instance.grand_total = instance.Total_p + instance.gst_total 
	else:
		instance.grand_total = instance.Total_p + instance.cgst_total + instance.gst_total 



@receiver(pre_save, sender=Stock_Total_sales)
def update_gst_rate(sender, instance, *args, **kwargs):
	if instance.sales.State == instance.sales.Company.State:
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.sgst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.ugst = 0
	elif instance.sales.State == 'Delhi':
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.sgst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.ugst = 0
	elif instance.sales.State == 'Puducherry':
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.sgst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.ugst = 0
	elif instance.sales.State == 'Andaman & Nicobar Islands':
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.ugst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.sgst = 0
	elif instance.sales.State == 'Chandigarh':
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.ugst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.sgst = 0
	elif instance.sales.State == 'Dadra and Nagar Haveli':
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.ugst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.sgst = 0
	elif instance.sales.State == 'Daman and Diu':
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.ugst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.sgst = 0
	elif instance.sales.State == 'Lakshadweep':
		instance.cgst = instance.stockitem.gst_rate / 2
		instance.ugst = instance.stockitem.gst_rate / 2
		instance.igst = 0
		instance.sgst = 0
	else:
		instance.cgst = 0
		instance.igst = instance.stockitem.gst_rate 
		instance.ugst = 0
		instance.sgst = 0

@receiver(pre_save, sender=Stock_Total_sales)
def update_amount(sender, instance, *args, **kwargs):
	instance.Total = instance.rate * instance.Quantity * (1 - (instance.Disc/100))


@receiver(pre_save, sender=Stock_Total_sales)
def update_gst_rate_saletotal(sender, instance, *args, **kwargs):
	if instance.sales.State == instance.sales.Company.State:
		instance.cgst_total = instance.cgst * instance.Total / 100
		instance.gst_total 	= instance.sgst * instance.Total / 100

	elif instance.sales.State == 'Delhi':
		instance.cgst_total = instance.cgst * instance.Total / 100
		instance.gst_total 	= instance.sgst * instance.Total / 100

	elif instance.sales.State == 'Puducherry':
		instance.cgst_total = instance.cgst * instance.Total / 100
		instance.gst_total 	= instance.sgst * instance.Total / 100

	elif instance.sales.State == 'Andaman & Nicobar Islands':
		instance.cgst_total = instance.cgst * instance.Total / 100
		instance.gst_total = instance.ugst * instance.Total / 100

	elif instance.sales.State == 'Chandigarh':
		instance.cgst_total = instance.cgst * instance.Total / 100
		instance.gst_total = instance.ugst * instance.Total / 100

	elif instance.sales.State == 'Dadra and Nagar Haveli':
		instance.cgst_total = instance.cgst * instance.Total / 100
		instance.gst_total = instance.ugst * instance.Total / 100

	elif instance.sales.State == 'Daman and Diu':
		instance.cgst_total = instance.cgst * instance.Total / 100
		instance.gst_total = instance.ugst * instance.Total / 100

	elif instance.sales.State == 'Lakshadweep':
		instance.cgst_total = instance.cgst * instance.Total / 100
		instance.gst_total = instance.ugst * instance.Total / 100

	else:
		instance.gst_total = instance.igst * instance.Total / 100
	if instance.cgst_total == None:
		instance.grand_total = instance.Total + instance.gst_total 
	else:
		instance.grand_total = instance.Total + instance.cgst_total + instance.gst_total 
			
	
@receiver(pre_save, sender=Purchase)
def update_subtotal(sender,instance,*args,**kwargs):
	total = instance.purchasetotal.aggregate(the_sum=Coalesce(Sum('Total_p'), Value(0)))['the_sum']
	instance.sub_total = total

@receiver(pre_save, sender=Purchase)
def update_totalgst(sender,instance,*args,**kwargs):
	total_cgst = instance.purchasetotal.aggregate(the_sum=Coalesce(Sum('cgst_total'), Value(0)))['the_sum']
	total_gst = instance.purchasetotal.aggregate(the_sum=Coalesce(Sum('gst_total'), Value(0)))['the_sum']
	total 	= instance.purchasetotal.aggregate(the_sum=Coalesce(Sum('grand_total'), Value(0)))['the_sum']
	instance.cgst_alltotal = total_cgst
	instance.gst_alltotal = total_gst
	instance.Total = total


@receiver(pre_save, sender=Sales)
def update_total_sales(sender,instance,*args,**kwargs):
	total1 = instance.saletotal.aggregate(the_sum=Coalesce(Sum('Total'), Value(0)))['the_sum']
	instance.sub_total = total1

@receiver(pre_save, sender=Sales)
def update_totalgst_sales(sender,instance,*args,**kwargs):
	total_cgst = instance.saletotal.aggregate(the_sum=Coalesce(Sum('cgst_total'), Value(0)))['the_sum']
	total_gst = instance.saletotal.aggregate(the_sum=Coalesce(Sum('gst_total'), Value(0)))['the_sum']
	total 	= instance.saletotal.aggregate(the_sum=Coalesce(Sum('grand_total'), Value(0)))['the_sum']
	instance.cgst_alltotal = total_cgst
	instance.gst_alltotal = total_gst
	instance.Total = total


@receiver(pre_save, sender=Purchase)
def user_created(sender,instance,*args,**kwargs):
	c = journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if instance.sub_total != None:
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Purchase",By=instance.purchase,To=instance.Party_ac,Debit=instance.sub_total,Credit=instance.sub_total)

@receiver(pre_save, sender=Purchase)
def user_created_plpurchase(sender,instance,*args,**kwargs):
	c = Pl_journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if instance.sub_total != None:
		Pl_journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Purchase",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='Profit & Loss A/c').first(),To=instance.purchase,Debit=instance.sub_total,Credit=instance.sub_total,tax_expense=True,it_head='Profit_&_Gains_of_Business_and_Professions')


@receiver(pre_save, sender=Purchase)
def user_created_purchase_cgst(sender,instance,*args,**kwargs):
	c = journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if instance.cgst_alltotal != None:
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='CGST').first(),To=instance.Party_ac,Debit=instance.cgst_alltotal,Credit=instance.cgst_alltotal)

@receiver(pre_save, sender=Purchase)
def user_created_purchase_stategst(sender,instance,*args,**kwargs):
	c = journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if instance.gst_alltotal != None and instance.State == instance.Company.State:
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='SGST').first(),To=instance.Party_ac,Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	elif instance.gst_alltotal != None and instance.State == 'Delhi':
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='SGST').first(),To=instance.Party_ac,Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	elif instance.gst_alltotal != None and instance.State == 'Puducherry':
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='SGST').first(),To=instance.Party_ac,Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	elif instance.gst_alltotal != None and instance.State == 'Andaman & Nicobar Islands':
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='UTGST').first(),To=instance.Party_ac,Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	elif instance.gst_alltotal != None and instance.State == 'Chandigarh':
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='UTGST').first(),To=instance.Party_ac,Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	elif instance.gst_alltotal != None and instance.State == 'Dadra and Nagar Haveli':
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='UTGST').first(),To=instance.Party_ac,Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	elif instance.gst_alltotal != None and instance.State == 'Daman and Diu':
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='UTGST').first(),To=instance.Party_ac,Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	elif instance.gst_alltotal != None and instance.State == 'Lakshadweep':
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='UTGST').first(),To=instance.Party_ac,Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	else:
		if instance.gst_alltotal != None:
			journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='IGST').first(),To=instance.Party_ac,Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)



@receiver(pre_save, sender=Sales)
def user_created_sales(sender,instance,*args,**kwargs):
	c = journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if instance.sub_total != None:
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Sales",By=instance.Party_ac,To=instance.sales,Debit=instance.sub_total,Credit=instance.sub_total)


@receiver(pre_save, sender=Sales)
def user_created_plsales(sender,instance,*args,**kwargs):
	c = Pl_journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if instance.sub_total != None:
		Pl_journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Sales",By=instance.sales,To=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='Profit & Loss A/c').first(),Debit=instance.sub_total,Credit=instance.sub_total,tax_expense=True,it_head='Profit_&_Gains_of_Business_and_Professions')

@receiver(pre_save, sender=Sales)
def user_created_sales_cgst(sender,instance,*args,**kwargs):
	c = journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if instance.cgst_alltotal != None:
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=instance.Party_ac,To=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='CGST').first(),Debit=instance.cgst_alltotal,Credit=instance.cgst_alltotal)

@receiver(pre_save, sender=Sales)
def user_created_sales_stategst(sender,instance,*args,**kwargs):
	c = journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if instance.gst_alltotal != None and instance.State == instance.Company.State:
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=instance.Party_ac,To=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='SGST').first(),Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	elif instance.gst_alltotal != None and instance.State == 'Delhi':
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=instance.Party_ac,To=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='SGST').first(),Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	elif instance.gst_alltotal != None and instance.State == 'Puducherry':
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=instance.Party_ac,To=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='SGST').first(),Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	elif instance.gst_alltotal != None and instance.State == 'Andaman & Nicobar Islands':
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=instance.Party_ac,To=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='SGST').first(),Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	elif instance.gst_alltotal != None and instance.State == 'Chandigarh':
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=instance.Party_ac,To=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='SGST').first(),Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	elif instance.gst_alltotal != None and instance.State == 'Dadra and Nagar Haveli':
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=instance.Party_ac,To=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='SGST').first(),Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	elif instance.gst_alltotal != None and instance.State == 'Daman and Diu':
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=instance.Party_ac,To=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='SGST').first(),Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	elif instance.gst_alltotal != None and instance.State == 'Lakshadweep':
		journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=instance.Party_ac,To=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='SGST').first(),Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)
	else:
		if instance.gst_alltotal != None:
			journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.date,voucher_id=instance.id, voucher_type= "Journal",By=instance.Party_ac,To=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='SGST').first(),Debit=instance.gst_alltotal,Credit=instance.gst_alltotal)






	

