from django.conf import settings
from django.db import models
import datetime
from userprofile.models import Product_activation
from django.db.models.signals import pre_save,post_save,post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.functions import Coalesce 
from django.db.models import Case, When, CharField, Value, Sum, F, ExpressionWrapper, Subquery, OuterRef, Count
from company.models import company
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
import datetime
import string
import random
from functools import wraps
# from django.utils.encoding import python_2_unicode_compatible


# def prevent_recursion(func):

#     @wraps(func)
#     def no_recursion(sender, instance=None, **kwargs):

#         if not instance:
#             return

#         if hasattr(instance, '_dirty'):
#             return

#         func(sender, instance=instance, **kwargs)

#         try:
#             instance._dirty = True
#             instance.save()
#         finally:
#             del instance._dirty

#     return no_recursion


class selectdatefield(models.Model):
	User       = models.OneToOneField(settings.AUTH_USER_MODEL,related_name="Users",on_delete=models.CASCADE,null=True,blank=True)
	Start_Date = models.DateField(default=datetime.date(2018,4,1),blank=True, null=True)
	End_Date   = models.DateField(default=datetime.date(2019,3,31),blank=True, null=True)

	def __str__(self):
		return str(self.Start_Date)

	def clean(self):
		if self.Start_Date > self.End_Date:
			raise ValidationError({'Start_Date':["Start Date Cannot Be Greater Than End Date"],'End_Date':["Start Date Cannot Be Greater Than End Date"]})

@receiver(pre_save, sender=Product_activation)
def daterange_autocreate(sender,instance,*args,**kwargs):
	if instance.product.id == 1 and instance.is_active == True:
		selectdatefield.objects.update_or_create(User=instance.User,Start_Date=datetime.date((datetime.datetime.now().year),4,1),End_Date=datetime.date((datetime.datetime.now().year) + 1,3,31))

@receiver(pre_save, sender=Product_activation)
def daterange_autodelete(sender,instance,*args,**kwargs):
	if instance.product.id == 1 and instance.is_active == False:
		selectdatefield.objects.filter(User=instance.User,Start_Date=datetime.date((datetime.datetime.now().year),4,1),End_Date=datetime.date((datetime.datetime.now().year) + 1,3,31)).delete()
		

class group1(models.Model):
	counter = models.IntegerField(blank=True,null=True)
	urlhash = models.CharField(max_length=100, null=True, blank=True, unique=True)
	User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	group_Name = models.CharField(max_length=32)
	Company = models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True,related_name='Company_group')  		
	Master = models.ForeignKey("self",on_delete=models.CASCADE,related_name='master_group',null=True)

	Name1 = (
		('Assets','Assets'),
		('Expenses','Expenses'),
		('Income','Income'),
		('Liabilities','Liabilities'),
		('Not Applicable','Not Applicable'),
		)

	Nature_of_group1 = models.CharField(max_length=32,choices=Name1,default='Assets')

	Nature = (
		('Debit','Debit'),
		('Credit','Credit'),
		('Not Applicable','Not Applicable'),
		)

	balance_nature = models.CharField(max_length=32,choices=Nature,default='Debit',blank=False)
	Group_behaves_like_a_Sub_Group = models.BooleanField(default=False)
	Nett_Debit_or_Credit_Balances_for_Reporting = models.BooleanField(default=False)
	

	def __str__(self):
		return self.group_Name


	def get_absolute_url(self, **kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		return reverse("accounting_double_entry:groupdetail", kwargs={'pk2':self.pk, 'pk1':company_details.pk})

	def save(self, **kwargs):
		super(group1, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('AG') + str(self.counter)
				group1.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('AG') + str(self.counter)
				group1.objects.filter(pk=self.pk).update(urlhash=self.urlhash)



@receiver(post_save, sender=company)
def create_default_groups1(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Primary',Nature_of_group1='Not Applicable',balance_nature='Not Applicable',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups2(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Branch/Divisions',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Liabilities',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)

@receiver(post_save, sender=company)
def create_default_groups3(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Capital A/c',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Liabilities',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)

@receiver(post_save, sender=company)
def create_default_groups4(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Current Assets',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Assets',balance_nature='Debit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups5(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Current Liabilities',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Liabilities',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups6(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Direct Expenses',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Expenses',balance_nature='Debit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups7(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Direct Incomes',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Income',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups8(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Fixed Assets',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Assets',balance_nature='Debit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)

@receiver(post_save, sender=company)
def create_default_groups9(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Indirect Income',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Income',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=True)

@receiver(post_save, sender=company)
def create_default_groups10(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Indirect Expense',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Expenses',balance_nature='Debit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=True)


@receiver(post_save, sender=company)
def create_default_groups11(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Investments',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Assets',balance_nature='Debit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)

@receiver(post_save, sender=company)
def create_default_groups12(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Loans (Liability)',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Liabilities',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)

@receiver(post_save, sender=company)
def create_default_groups13(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Misc Expenses (ASSET)',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Assets',balance_nature='Debit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups14(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Purchase Accounts',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Expenses',balance_nature='Debit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups15(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Sales Account',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Income',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups16(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Suspense A/c',Master=instance.Company_group.get(group_Name='Primary'),Nature_of_group1='Liabilities',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups17(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Bank Accounts',Master=instance.Company_group.get(group_Name='Current Assets'),Nature_of_group1='Not Applicable',balance_nature='Debit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups18(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Bank OD A/c',Master=instance.Company_group.get(group_Name='Loans (Liability)'),Nature_of_group1='Not Applicable',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups19(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Cash-in-hand',Master=instance.Company_group.get(group_Name='Current Assets'),Nature_of_group1='Not Applicable',balance_nature='Debit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False),

@receiver(post_save, sender=company)
def create_default_groups20(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Deposits(Asset)',Master=instance.Company_group.get(group_Name='Current Assets'),Nature_of_group1='Not Applicable',balance_nature='Debit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False),

@receiver(post_save, sender=company)
def create_default_groups21(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Duties & Taxes',Master=instance.Company_group.get(group_Name='Current Liabilities'),Nature_of_group1='Not Applicable',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False),

@receiver(post_save, sender=company)
def create_default_groups22(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Loans & Advances(Asset)',Master=instance.Company_group.get(group_Name='Current Assets'),Nature_of_group1='Not Applicable',balance_nature='Debit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)

@receiver(post_save, sender=company)
def create_default_groups23(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Provisions',Master=instance.Company_group.get(group_Name='Current Liabilities'),Nature_of_group1='Not Applicable',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups24(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Reserves & Surplus',Master=instance.Company_group.get(group_Name='Capital A/c'),Nature_of_group1='Not Applicable',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups25(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Secured Loans',Master=instance.Company_group.get(group_Name='Loans (Liability)'),Nature_of_group1='Not Applicable',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)

@receiver(post_save, sender=company)
def create_default_groups26(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Stock-in-hand',Master=instance.Company_group.get(group_Name='Current Assets'),Nature_of_group1='Not Applicable',balance_nature='Debit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)

@receiver(post_save, sender=company)
def create_default_groups27(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Sundry Creditors',Master=instance.Company_group.get(group_Name='Current Liabilities'),Nature_of_group1='Not Applicable',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups28(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Sundry Debtors',Master=instance.Company_group.get(group_Name='Current Assets'),Nature_of_group1='Not Applicable',balance_nature='Debit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


@receiver(post_save, sender=company)
def create_default_groups30(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='Unsecured Loans',Master=instance.Company_group.get(group_Name='Loans (Liability)'),Nature_of_group1='Not Applicable',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)

@receiver(post_save, sender=company)
def create_default_groups32(sender, instance, created, **kwargs):
	c = group1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		group1.objects.create(counter=c,User=instance.User,Company=instance,group_Name='GST',Master=instance.Company_group.get(group_Name='Current Liabilities'),Nature_of_group1='Not Applicable',balance_nature='Credit',Group_behaves_like_a_Sub_Group=False,Nett_Debit_or_Credit_Balances_for_Reporting=False)


class ledger1(models.Model):
	User 			= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company 		= models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True,related_name='Companys')
	counter 		= models.IntegerField(blank=True,null=True)
	urlhash			= models.CharField(max_length=100, null=True, blank=True, unique=True)
	Creation_Date	= models.DateField(default=datetime.date.today,blank=True, null=True)
	name 			= models.CharField(max_length=32)
	group1_Name 	= models.ForeignKey(group1,on_delete=models.CASCADE,null=True,related_name='ledgergroups')
	Opening_Balance = models.DecimalField(default=0.00,max_digits=19,decimal_places=2,null=True)
	Balance_opening = models.DecimalField(default=0.00,max_digits=19,decimal_places=2,null=True)
	User_Name 		= models.CharField(max_length=100,blank=True)
	Address 		= models.TextField(blank=True)
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
	State 			= models.CharField(max_length=100,choices=State_Name,default='Choose',blank=True)
	Pin_Code 		= models.BigIntegerField(blank=True,null=True)
	PanIt_No 		= models.CharField(max_length=100,blank=True)
	GST_No 			= models.CharField(max_length=100,blank=True)
	Closing_balance = models.DecimalField(default=0.00,max_digits=10,decimal_places=2,blank=True)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self, **kwargs):
		company_details = get_object_or_404(company, pk=kwargs['pk'])
		return reverse("accounting_double_entry:ledgerdetail", kwargs={'pk2':self.pk, 'pk1':company_details.pk})

	def save(self, **kwargs):
		super(ledger1, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('AL') + str(self.counter)
				ledger1.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('AL') + str(self.counter)
				ledger1.objects.filter(pk=self.pk).update(urlhash=self.urlhash)

		

@receiver(post_save, sender=company)
def create_default_ledger01(sender, instance, created, **kwargs):
	c = ledger1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		ledger1.objects.create(counter=c, User=instance.User,Company=instance,Creation_Date=instance.Books_Begining_From,group1_Name=instance.Company_group.get(group_Name='Primary'),name='Cash',Opening_Balance=0)


@receiver(post_save, sender=company)
def create_default_ledger02(sender, instance, created, **kwargs):
	c = ledger1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		ledger1.objects.create(counter=c, User=instance.User,Company=instance,Creation_Date=instance.Books_Begining_From,group1_Name=instance.Company_group.get(group_Name='Primary'),name='Profit & Loss A/c',Opening_Balance=0)

@receiver(post_save, sender=company)
def create_default_ledger03(sender, instance, created, **kwargs):
	c = ledger1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		ledger1.objects.create(counter=c, User=instance.User,Company=instance,Creation_Date=instance.Books_Begining_From,group1_Name=instance.Company_group.get(group_Name='Purchase Accounts'),name='Purchase A/c(Interstate)',Opening_Balance=0)
	
@receiver(post_save, sender=company)
def create_default_ledger04(sender, instance, created, **kwargs):
	c = ledger1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		ledger1.objects.create(counter=c, User=instance.User,Company=instance,Creation_Date=instance.Books_Begining_From,group1_Name=instance.Company_group.get(group_Name='Purchase Accounts'),name='Purchase A/c(Intrastate)',Opening_Balance=0)

@receiver(post_save, sender=company)
def create_default_ledger05(sender, instance, created, **kwargs):
	c = ledger1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		ledger1.objects.create(counter=c, User=instance.User,Company=instance,Creation_Date=instance.Books_Begining_From,group1_Name=instance.Company_group.get(group_Name='Sales Account'),name='Sales A/c(Interstate)',Opening_Balance=0)


@receiver(post_save, sender=company)
def create_default_ledger06(sender, instance, created, **kwargs):
	c = ledger1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		ledger1.objects.create(counter=c, User=instance.User,Company=instance,Creation_Date=instance.Books_Begining_From,group1_Name=instance.Company_group.get(group_Name='Sales Account'),name='Sales A/c(Intrastate)',Opening_Balance=0)	


@receiver(post_save, sender=company)
def create_default_ledger07(sender, instance, created, **kwargs):
	c = ledger1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		ledger1.objects.create(counter=c, User=instance.User,Company=instance,Creation_Date=instance.Books_Begining_From,group1_Name=instance.Company_group.get(group_Name='GST'),name='CGST',Opening_Balance=0)

@receiver(post_save, sender=company)
def create_default_ledger08(sender, instance, created, **kwargs):
	c = ledger1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		ledger1.objects.create(counter=c, User=instance.User,Company=instance,Creation_Date=instance.Books_Begining_From,group1_Name=instance.Company_group.get(group_Name='GST'),name='SGST',Opening_Balance=0)

@receiver(post_save, sender=company)
def create_default_ledger09(sender, instance, created, **kwargs):
	c = ledger1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		ledger1.objects.create(counter=c, User=instance.User,Company=instance,Creation_Date=instance.Books_Begining_From,group1_Name=instance.Company_group.get(group_Name='GST'),name='IGST',Opening_Balance=0)

@receiver(post_save, sender=company)
def create_default_ledger10(sender, instance, created, **kwargs):
	c = ledger1.objects.filter(User=instance.User, Company=instance).count() + 1
	if created:
		ledger1.objects.create(counter=c, User=instance.User,Company=instance,Creation_Date=instance.Books_Begining_From,group1_Name=instance.Company_group.get(group_Name='GST'),name='UTGST',Opening_Balance=0)




class journal(models.Model):
	User       		= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company    		= models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True,related_name='Companyname')
	counter 		= models.IntegerField(blank=True,null=True)
	urlhash 		= models.CharField(max_length=100, null=True, blank=True, unique=True)
	Date       		= models.DateField(default=datetime.date.today)
	voucher_id		= models.PositiveIntegerField(blank=True,null=True)
	voucher_type	= models.CharField(max_length=100,blank=True)
	By         		= models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='Debitledgers')
	To         		= models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='Creditledgers')
	Debit      		= models.DecimalField(max_digits=10,decimal_places=2,null=True)
	Credit     		= models.DecimalField(max_digits=10,decimal_places=2,null=True)
	narration  		= models.TextField(blank=True)


	def __str__(self):
		return str(self.By)

	def get_absolute_url(self):
		return reverse("accounting_double_entry:detail", kwargs={'pk':self.pk})

	def clean(self):
		if self.Debit != self.Credit:
			raise ValidationError('Debit Amount Should Be Equal To Credit Amount')
		elif self.To == self.By:
			raise ValidationError('Particular Entry Cannot be same')

	def save(self, **kwargs):
		super(journal, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('AJ') + str(self.counter)
				journal.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('AJ') + str(self.counter)
				journal.objects.filter(pk=self.pk).update(urlhash=self.urlhash)


# @receiver(post_save, dispatch_uid="my_unique_identifier", sender=journal)
# def pl_journal_indirectexp(sender, instance, created=False, **kwargs):
# 	c=0
# 	c=c+1
# 	if created  and c==1:
# 		if instance.To.group1_Name.group_Name == 'Indirect Expense':
# 			journal.objects.update_or_create(User=instance.User,Company=instance.Company,Date=instance.Date, voucher_id=instance.id, voucher_type= "Journal",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='Profit & Loss A/c').first(),To=instance.To,Debit=instance.Debit,Credit=instance.Credit)
# 			c=c+1
	

class Pl_journal(models.Model):
	User       		= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company    		= models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True,related_name='Companynamepl')
	counter 		= models.IntegerField(blank=True,null=True)
	urlhash 		= models.CharField(max_length=100, null=True, blank=True, unique=True)
	Date       		= models.DateField(default=datetime.date.today)
	voucher_id		= models.PositiveIntegerField(blank=True,null=True)
	voucher_type	= models.CharField(max_length=100,blank=True)
	By         		= models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='Debitledgerspl')
	To         		= models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='Creditledgerspl')
	Debit      		= models.DecimalField(max_digits=10,decimal_places=2,null=True)
	Credit     		= models.DecimalField(max_digits=10,decimal_places=2,null=True)
	tax_expense		= models.BooleanField(default=True)
	it 				= (
			('Salaries','Salaries'),
			('Income_from_house_property','Income_from_house_property'),
			('Profit_&_Gains_of_Business_and_Professions','Profit_&_Gains_of_Business_and_Professions'),
			('Capital_Gains','Capital_Gains'),
			('Income_from_other_sources','Income_from_other_sources'),
			)
	it_head			= models.CharField(max_length=32,choices=it,default='Profit_&_Gains_of_Business_and_Professions',blank=False)

	def __str__(self):
		return str(self.By)

	def clean(self):
		if self.Debit != self.Credit:
			raise ValidationError('Debit Amount Should Be Equal To Credit Amount')
		elif self.To == self.By:
			raise ValidationError('Particular Entry Cannot be same')

	def save(self, **kwargs):
		super(Pl_journal, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('AJ') + str(self.counter)
				Pl_journal.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('AJ') + str(self.counter)
				Pl_journal.objects.filter(pk=self.pk).update(urlhash=self.urlhash)

@receiver(post_save, sender=journal)
def create_pl_indirectexp(sender, instance, created, **kwargs):
	c = Pl_journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if created:
		if instance.To.group1_Name.group_Name == 'Indirect Expense':
			Pl_journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.Date, voucher_id=instance.id, voucher_type= "Journal",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='Profit & Loss A/c').first(),To=instance.To,Debit=instance.Debit,Credit=instance.Credit,tax_expense=True,it_head='Profit_&_Gains_of_Business_and_Professions')

@receiver(post_save, sender=journal)
def create_pl_purchase(sender, instance, created, **kwargs):
	c = Pl_journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if created:
		if instance.To.group1_Name.group_Name == 'Purchase Accounts':
			Pl_journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.Date, voucher_id=instance.id, voucher_type= "Journal",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='Profit & Loss A/c').first(),To=instance.To,Debit=instance.Debit,Credit=instance.Credit,tax_expense=True,it_head='Profit_&_Gains_of_Business_and_Professions')

@receiver(post_save, sender=journal)
def create_pl_directexp(sender, instance, created, **kwargs):
	c = Pl_journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if created:
		if instance.To.group1_Name.group_Name == 'Direct Expenses':
			Pl_journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.Date, voucher_id=instance.id, voucher_type= "Journal",By=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='Profit & Loss A/c').first(),To=instance.To,Debit=instance.Debit,Credit=instance.Credit,tax_expense=True,it_head='Profit_&_Gains_of_Business_and_Professions')

@receiver(post_save, sender=journal)
def create_pl_sales(sender, instance, created, **kwargs):
	c = Pl_journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if created:
		if instance.By.group1_Name.group_Name == 'Sales Account':
			Pl_journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.Date, voucher_id=instance.id, voucher_type= "Journal",By=instance.By,To=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='Profit & Loss A/c').first(),Debit=instance.Debit,Credit=instance.Credit,tax_expense=True,it_head='Profit_&_Gains_of_Business_and_Professions')


@receiver(post_save, sender=journal)
def create_pl_directinc(sender, instance, created, **kwargs):
	c = Pl_journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if created:
		if instance.By.group1_Name.group_Name == 'Direct Incomes':
			Pl_journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.Date, voucher_id=instance.id, voucher_type= "Journal",By=instance.By,To=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='Profit & Loss A/c').first(),Debit=instance.Debit,Credit=instance.Credit,tax_expense=True,it_head='Profit_&_Gains_of_Business_and_Professions')

@receiver(post_save, sender=journal)
def create_pl_indirectinc(sender, instance, created, **kwargs):
	c = Pl_journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if created:
		if instance.By.group1_Name.group_Name == 'Indirect Income':
			Pl_journal.objects.update_or_create(counter=c,User=instance.User,Company=instance.Company,Date=instance.Date, voucher_id=instance.id, voucher_type= "Journal",By=instance.By,To=ledger1.objects.filter(User=instance.User,Company=instance.Company,name__icontains='Profit & Loss A/c').first(),Debit=instance.Debit,Credit=instance.Credit,tax_expense=True,it_head='Profit_&_Gains_of_Business_and_Professions')

class Payment(models.Model):
	User       = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company    = models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True,related_name='Companynamepayment')
	counter    = models.IntegerField(blank=True,null=True)
	urlhash    = models.CharField(max_length=100, null=True, blank=True, unique=True)
	date       = models.DateField(default=datetime.date.today)
	account    = models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='Payledgers')
	total_amt  = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)

	def __str__(self):
		return str(self.account)

	def save(self, **kwargs):
		super(Payment, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('AJ') + str(self.counter)
				Payment.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('AJ') + str(self.counter)
				Payment.objects.filter(pk=self.pk).update(urlhash=self.urlhash)


class Particularspayment(models.Model):
	payment    = models.ForeignKey(Payment,on_delete=models.CASCADE,related_name='payments')
	particular = models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='particularpayment')
	amount     = models.DecimalField(max_digits=10,decimal_places=2,null=True)

	def __str__(self):
		return str(self.payment)

class Receipt(models.Model):
	User       = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company    = models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True,related_name='Companynamereceipt')
	counter    = models.IntegerField(blank=True,null=True)
	urlhash    = models.CharField(max_length=100, null=True, blank=True, unique=True)
	date       = models.DateField(default=datetime.date.today)
	account    = models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='receiptledgers')
	total_amt  = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)

	def __str__(self):
		return str(self.account)

	def save(self, **kwargs):
		super(Receipt, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('AJ') + str(self.counter)
				Receipt.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('AJ') + str(self.counter)
				Receipt.objects.filter(pk=self.pk).update(urlhash=self.urlhash)


class Particularsreceipt(models.Model):
	receipt    = models.ForeignKey(Receipt,on_delete=models.CASCADE,related_name='receipts')
	particular = models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='particularreceipt')
	amount     = models.DecimalField(max_digits=10,decimal_places=2,null=True)

	def __str__(self):
		return str(self.receipt)


class Contra(models.Model):
	User       = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company    = models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True,related_name='Companynamecontra')
	counter    = models.IntegerField(blank=True,null=True)
	urlhash	   = models.CharField(max_length=100, null=True, blank=True, unique=True)
	date       = models.DateField(default=datetime.date.today)
	account    = models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='contraledgers')
	total_amt  = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)

	def __str__(self):
		return str(self.account)

	def save(self, **kwargs):
		super(Contra, self).save()
		if not self.urlhash:
			if self.User.profile.user_type == 'Bussiness User':
				self.urlhash = 'BU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('AJ') + str(self.counter)
				Contra.objects.filter(pk=self.pk).update(urlhash=self.urlhash)
			else:
				self.urlhash = 'PU'+ '-' + str(self.User.id) + '-'+ 'P' + '-' + '1' + '-'+ 'C' + str(self.Company.counter) + '-' + ('AJ') + str(self.counter)
				Contra.objects.filter(pk=self.pk).update(urlhash=self.urlhash)

class Particularscontra(models.Model):
	contra     = models.ForeignKey(Contra,on_delete=models.CASCADE,related_name='contras')
	particular = models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='particularcontra')
	amount     = models.DecimalField(max_digits=10,decimal_places=2,null=True)

	def __str__(self):
		return str(self.contra)




@receiver(pre_save, sender=Payment)
def update_total_payment(sender,instance,*args,**kwargs):
	total1 = instance.payments.aggregate(the_sum=Coalesce(Sum('amount'), Value(0)))['the_sum']
	instance.total_amt = total1


@receiver(pre_save, sender=Particularspayment)
def user_created_payment(sender,instance,*args,**kwargs):
	c = journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if instance.amount != None:
		journal.objects.update_or_create(counter=c,User=instance.payment.User,Company=instance.payment.Company,Date=instance.payment.date, voucher_id=instance.payment.id, voucher_type= "Payment",By=instance.particular,To=instance.payment.account,Debit=instance.amount,Credit=instance.amount)


@receiver(pre_save, sender=Receipt)
def update_total_receipt(sender,instance,*args,**kwargs):
	total1 = instance.receipts.aggregate(the_sum=Coalesce(Sum('amount'), Value(0)))['the_sum']
	instance.total_amt = total1


@receiver(pre_save, sender=Particularsreceipt)
def user_created_receipt(sender,instance,*args,**kwargs):
	c = journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if instance.amount != None:
		journal.objects.update_or_create(counter=c,User=instance.receipt.User,Company=instance.receipt.Company,Date=instance.receipt.date, voucher_id=instance.receipt.id, voucher_type= "Receipt",By=instance.receipt.account,To=instance.particular,Debit=instance.amount,Credit=instance.amount)

@receiver(pre_save, sender=Contra)
def update_total_contra(sender,instance,*args,**kwargs):
	total1 = instance.contras.aggregate(the_sum=Coalesce(Sum('amount'), Value(0)))['the_sum']
	instance.total_amt = total1


@receiver(pre_save, sender=Particularscontra)
def user_created_contra(sender,instance,*args,**kwargs):
	c = journal.objects.filter(User=instance.User, Company=instance.Company).count() + 1
	if instance.amount != None:
		journal.objects.update_or_create(counter=c,User=instance.contra.User,Company=instance.contra.Company,Date=instance.contra.date, voucher_id=instance.contra.id, voucher_type= "Contra",By=instance.particular,To=instance.contra.account,Debit=instance.amount,Credit=instance.amount)



class Multijournaltotal(models.Model):
	User         = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Company      = models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True,related_name='Companynamemultijournaltotal')
	Date         = models.DateField(default=datetime.date.today)
	Total_Debit  = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
	Total_Credit = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)

	def __str__(self):
		return str(self.Total_Debit)

	def clean(self):
		if self.Total_Debit != self.Total_Credit:
			raise ValidationError('Debit Amount Should Be Equal To Credit Amount')

	def get_absolute_url(self, **kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)
		return reverse("accounting_double_entry:multijournaldetail", kwargs={'pk2':self.pk, 'pk':company_details.pk, 'pk3':selectdatefield_details.pk })


class Multijournal(models.Model):
	By           = models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='Debitledgersmulti')
	To           = models.ForeignKey(ledger1,on_delete=models.CASCADE,related_name='Creditledgersmulti')
	Debit        = models.DecimalField(max_digits=10,decimal_places=2,null=True)	
	Credit       = models.DecimalField(max_digits=10,decimal_places=2,null=True)
	total 		 = models.ForeignKey(Multijournaltotal,on_delete=models.CASCADE,related_name='totals')	
	narration    = models.TextField(blank=True)


	def __str__(self):
		return str(self.By)

	def get_absolute_url(self, **kwargs):
		company_details = get_object_or_404(company, pk=self.kwargs['pk1'])
		selectdatefield_details = get_object_or_404(selectdatefield, pk=pk3)
		return reverse("accounting_double_entry:multijournaldetail", kwargs={'pk2':self.pk, 'pk':company_details.pk, 'pk3':selectdatefield_details.pk })




@receiver(pre_save, sender=Multijournaltotal)
def update_total_journaldebit(sender,instance,*args,**kwargs):
	total_debit = instance.totals.aggregate(the_sum=Coalesce(Sum('Debit'), Value(0)))['the_sum']
	instance.Total_Debit = total_debit

@receiver(pre_save, sender=Multijournaltotal)
def update_total_journalcredit(sender,instance,*args,**kwargs):
	total_credit = instance.totals.aggregate(the_sum=Coalesce(Sum('Credit'), Value(0)))['the_sum']
	instance.Total_Credit = total_credit


