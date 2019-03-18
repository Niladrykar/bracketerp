from django.db import models
from django.conf import settings
from company.models import company
from stockkeeping.models import Stockgroup,Simpleunits,Compoundunits,Stockdata,Purchase,Sales
from accounting_double_entry.models import journal,group1,ledger1
from datetime import datetime
import datetime
from django.db.models.signals import pre_save,post_save,post_delete
from django.dispatch import receiver
# Create your models here.

class Gst_input(models.Model):
	User 			= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company			= models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True,related_name='Company_gstinput')
	counter 	 	= models.IntegerField(blank=True,null=True)
	urlhash 		= models.CharField(max_length=100, null=True, blank=True, unique=True)
	date			= models.DateField(default=datetime.date.today)
	gstin_vendor 	= models.CharField(max_length=100, default= '19ABCDE1234F2Z5',unique=True,null=True)
	gstin_self 		= models.CharField(max_length=100, default= '19ABCDE1234F2Z5',unique=True,null=True) 
	cgst 			= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True,null=True)
	sgst 			= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True,null=True)
	igst 			= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True,null=True)
	ugst 			= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True,null=True)
	purchase 		= models.ForeignKey(Purchase,on_delete=models.CASCADE,related_name='Purchasegst')
	total_purchase	= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
	withinstate	 	= models.BooleanField(default=False)

	def __str__(self):
		return str(self.id)

	def save(self, **kwargs):
		super(Gst_input, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SS') + str(self.counter)
				Gst_input.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SS') + str(self.counter)
				Gst_input.objects.filter(pk=self.pk).update(urlhash=self.urlhash)




class Gst_output(models.Model):
	User 			= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company			= models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True,related_name='Company_gstoutput')
	counter 	 	= models.IntegerField(blank=True,null=True)
	urlhash 	 	= models.CharField(max_length=100, null=True, blank=True, unique=True)
	date			= models.DateField(default=datetime.date.today)
	gstin_vendor 	= models.CharField(max_length=100, default= '19ABCDE1234F2Z5',unique=True,null=True)
	gstin_self 		= models.CharField(max_length=100, default= '19ABCDE1234F2Z5',unique=True,null=True) 
	cgst 			= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True,null=True)
	sgst 			= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True,null=True)
	igst 			= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True,null=True)
	ugst 			= models.DecimalField(default=0.00,max_digits=5,decimal_places=2,blank=True,null=True)
	sales 			= models.ForeignKey(Sales,on_delete=models.CASCADE,related_name='salesgst')
	total_sales		= models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
	withinstate	 	= models.BooleanField(default=False)

	def __str__(self):
		return str(self.id)

	def save(self, **kwargs):
		super(Gst_output, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SS') + str(self.counter)
				Gst_output.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SS') + str(self.counter)
				Gst_output.objects.filter(pk=self.pk).update(urlhash=self.urlhash)



class Stock_gst(models.Model):
	User 			= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company			= models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True,related_name='Company_stockgst')
	counter 	 	= models.IntegerField(blank=True,null=True)
	urlhash 	 	= models.CharField(max_length=100, null=True, blank=True, unique=True)
	date			= models.DateField(default=datetime.date.today)
	stock_item		= models.ForeignKey(Stockdata,on_delete=models.CASCADE,related_name='stockgst')
	gst_rate		= models.DecimalField(max_digits=4,decimal_places=2,default=5)
	hsn        	 	= models.PositiveIntegerField()


	def __str__(self):
		return str(self.id)

	def save(self, **kwargs):
		super(Stock_gst, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SS') + str(self.counter)
				Stock_gst.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('SS') + str(self.counter)
				Stock_gst.objects.filter(pk=self.pk).update(urlhash=self.urlhash)


# @receiver(post_save, sender=Sales)
# def user_created_gstoutput(sender, instance, created, **kwargs):
# 	c = Gst_output.objects.filter(User=instance.User, Company=instance.Company).count() + 1
# 	if created:
# 		if instance.State == instance.Company.State:
# 			Gst_output.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,date=instance.date,gstin_vendor=instance.GSTIN,gstin_self=instance.Company.gst,cgst=instance.cgst_alltotal,sgst=instance.gst_alltotal,igst=0,ugst=0,sales=instance,total_sales=instance.Total,withinstate=True)
# 		elif instance.State == 'Delhi':
# 			Gst_output.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,date=instance.date,gstin_vendor=instance.GSTIN,gstin_self=instance.Company.gst,cgst=instance.cgst_alltotal,sgst=instance.gst_alltotal,igst=0,ugst=0,sales=instance,total_sales=instance.Total,withinstate=True)
# 		elif instance.State == 'Puducherry':
# 			Gst_output.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,date=instance.date,gstin_vendor=instance.GSTIN,gstin_self=instance.Company.gst,cgst=instance.cgst_alltotal,sgst=instance.gst_alltotal,igst=0,ugst=0,sales=instance,total_sales=instance.Total,withinstate=True)
# 		elif instance.State == 'Andaman & Nicobar Islands':
# 			Gst_output.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,date=instance.date,gstin_vendor=instance.GSTIN,gstin_self=instance.Company.gst,cgst=instance.cgst_alltotal,ugst=instance.gst_alltotal,igst=0,sgst=0,sales=instance,total_sales=instance.Total,withinstate=True)
# 		elif instance.State == 'Chandigarh':
# 			Gst_output.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,date=instance.date,gstin_vendor=instance.GSTIN,gstin_self=instance.Company.gst,cgst=instance.cgst_alltotal,ugst=instance.gst_alltotal,igst=0,sgst=0,sales=instance,total_sales=instance.Total,withinstate=True)
# 		elif instance.State == 'Dadra and Nagar Haveli':
# 			Gst_output.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,date=instance.date,gstin_vendor=instance.GSTIN,gstin_self=instance.Company.gst,cgst=instance.cgst_alltotal,ugst=instance.gst_alltotal,igst=0,sgst=0,sales=instance,total_sales=instance.Total,withinstate=True)
# 		elif instance.State == 'Daman and Diu':
# 			Gst_output.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,date=instance.date,gstin_vendor=instance.GSTIN,gstin_self=instance.Company.gst,cgst=instance.cgst_alltotal,ugst=instance.gst_alltotal,igst=0,sgst=0,sales=instance,total_sales=instance.Total,withinstate=True)
# 		elif instance.State == 'Lakshadweep':
# 			Gst_output.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,date=instance.date,gstin_vendor=instance.GSTIN,gstin_self=instance.Company.gst,cgst=instance.cgst_alltotal,ugst=instance.gst_alltotal,igst=0,sgst=0,sales=instance,total_sales=instance.Total,withinstate=True)
# 		else:
# 			Gst_output.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,date=instance.date,gstin_vendor=instance.GSTIN,gstin_self=instance.Company.gst,cgst=instance.cgst_alltotal,igst=instance.gst_alltotal,ugst=0,sgst=0,sales=instance,total_sales=instance.Total,withinstate=True)


@receiver(post_save, sender=Stockdata)
def user_created_stockdata_gst(sender, instance, created, **kwargs):
	c = Stock_gst.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if created:
		Stock_gst.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,date=instance.Date,stock_item=instance,gst_rate=instance.gst_rate,hsn=instance.hsn)

