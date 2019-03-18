from django import forms
from stockkeeping.models import Stockgroup,Simpleunits,Compoundunits,Stockdata,Purchase,Sales,Stock_Total,Stock_Total_sales
import datetime
from company.models import company
from django.db.models import Q
from django.forms import inlineformset_factory
from accounting_double_entry.models import ledger1
from django.core.exceptions import ValidationError


class DateInput(forms.DateInput):
    input_type = 'date'

class Stockgroup_form(forms.ModelForm):
	class Meta:
		model   = Stockgroup
		fields  = ('name', 'under', 'quantities')

	def __init__(self, *args, **kwargs):
		self.User = kwargs.pop('User', None)		
		self.Company = kwargs.pop('Company', None)
		super(Stockgroup_form, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs       = {'class': 'form-control',}
		self.fields['under'].queryset 	       = Stockgroup.objects.filter(User= self.User,Company = self.Company)
		self.fields['under'].widget.attrs      = {'class': 'form-control select2',}


class Simpleunits_form(forms.ModelForm):
	class Meta:
		model   = Simpleunits
		fields  = ('symbol', 'formal')

	def __init__(self, *args, **kwargs):
		super(Simpleunits_form, self).__init__(*args, **kwargs)
		self.fields['symbol'].widget.attrs = {'class': 'form-control',}
		self.fields['formal'].widget.attrs = {'class': 'form-control',}

class Compoundunits_form(forms.ModelForm):
	class Meta:
		model   = Compoundunits
		fields  = ('firstunit', 'conversion','seconds_unit')

	def __init__(self, *args, **kwargs):
		self.User = kwargs.pop('User', None)		
		self.Company = kwargs.pop('Company', None)
		super(Compoundunits_form, self).__init__(*args, **kwargs)
		self.fields['firstunit'].queryset = Simpleunits.objects.filter(User= self.User,Company = self.Company)
		self.fields['firstunit'].widget.attrs = {'class': 'form-control select2',}
		self.fields['conversion'].widget.attrs = {'class': 'form-control',}
		self.fields['seconds_unit'].queryset = Simpleunits.objects.filter(User= self.User,Company = self.Company)
		self.fields['seconds_unit'].widget.attrs = {'class': 'form-control select2',}


class Stockdata_form(forms.ModelForm):
	class Meta:
		model  = Stockdata
		fields = ('Date','stock_name','batch_no','mnf_date','exp_date', 'under', 'unitsimple', 'unitcomplex', 'gst_rate', 'hsn', 'bar_code')
		widgets = {
            'Date': DateInput(),
            'mnf_date' : DateInput(),
            'exp_date' : DateInput()
        }

	def __init__(self, *args, **kwargs):
		self.User = kwargs.pop('User', None)		
		self.Company = kwargs.pop('Company', None)
		super(Stockdata_form, self).__init__(*args, **kwargs)
		self.fields['stock_name'].widget.attrs  = {'class': 'form-control',}
		self.fields['Date'].widget.attrs     = {'class': 'form-control',}
		self.fields['batch_no'].widget.attrs     = {'class': 'form-control',}
		self.fields['mnf_date'].widget.attrs     = {'class': 'form-control',}
		self.fields['exp_date'].widget.attrs     = {'class': 'form-control',}
		self.fields['under'].queryset = Stockgroup.objects.filter(User= self.User,Company = self.Company)
		self.fields['under'].widget.attrs       = {'class': 'form-control select2',}
		self.fields['unitsimple'].queryset = Simpleunits.objects.filter(User= self.User,Company = self.Company)
		self.fields['unitsimple'].widget.attrs  = {'class': 'form-control select2',}
		self.fields['unitcomplex'].queryset = Compoundunits.objects.filter(User= self.User,Company = self.Company)
		self.fields['unitcomplex'].widget.attrs = {'class': 'form-control select2',}
		self.fields['gst_rate'].widget.attrs        = {'class': 'form-control',}
		self.fields['hsn'].widget.attrs         = {'class': 'form-control',}

class Purchase_form(forms.ModelForm):
	class Meta:
		model  = Purchase
		fields = ('User','Company','date','Address','billname','GSTIN','PAN','State','Contact','DeliveryNote','Supplierref','Mode', 'ref_no', 'Party_ac', 'purchase', 'sub_total')
		widgets = {
            'date': DateInput(),
        }

	def __init__(self, *args, **kwargs):
		self.User = kwargs.pop('User', None)		
		self.Company = kwargs.pop('Company', None)
		super(Purchase_form, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs     = {'class': 'form-control',}
		self.fields['ref_no'].widget.attrs   = {'class': 'form-control',}
		self.fields['billname'].widget.attrs   = {'class': 'form-control',}
		self.fields['Party_ac'].queryset = ledger1.objects.filter(Q(User= self.User),Q(Company = self.Company) , Q(group1_Name__group_Name__icontains='Sundry Creditors') | Q(group1_Name__group_Name__icontains='Bank Accounts') | Q(group1_Name__group_Name__icontains='Cash-in-hand'))
		self.fields['Party_ac'].widget.attrs = {'class': 'form-control select2',}
		self.fields['purchase'].queryset = ledger1.objects.filter(User= self.User,Company = self.Company,group1_Name__group_Name__icontains='Purchase Accounts')
		self.fields['purchase'].widget.attrs = {'class': 'form-control select2',}
		self.fields['sub_total'].widget.attrs = {'class': 'form-control',}
		self.fields['Address'].widget.attrs = {'class': 'form-control',}
		self.fields['GSTIN'].widget.attrs = {'class': 'form-control',}
		self.fields['PAN'].widget.attrs = {'class': 'form-control',}
		self.fields['State'].widget.attrs = {'class': 'form-control select2',}
		self.fields['Contact'].widget.attrs = {'class': 'form-control',}
		self.fields['DeliveryNote'].widget.attrs = {'class': 'form-control',}
		self.fields['Supplierref'].widget.attrs = {'class': 'form-control',}
		self.fields['Mode'].widget.attrs = {'class': 'form-control',}



class Purchase_formadmin(forms.ModelForm):
	class Meta:
		model  = Purchase
		fields = ('User','Company','date','Address','billname','GSTIN','PAN','State','Contact','DeliveryNote','Supplierref','Mode', 'ref_no', 'Party_ac', 'purchase', 'sub_total')
		widgets = {
            'date': DateInput(),
        }

	def __init__(self, *args, **kwargs):
		super(Purchase_formadmin, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs     = {'class': 'form-control',}
		self.fields['ref_no'].widget.attrs   = {'class': 'form-control',}
		self.fields['billname'].widget.attrs   = {'class': 'form-control',}
		self.fields['Party_ac'].queryset = ledger1.objects.filter(Q(group1_Name__group_Name__icontains='Sundry Creditors') | Q(group1_Name__group_Name__icontains='Bank Accounts') | Q(group1_Name__group_Name__icontains='Cash-in-hand'))
		self.fields['Party_ac'].widget.attrs = {'class': 'form-control select2',}
		self.fields['purchase'].queryset = ledger1.objects.filter(group1_Name__group_Name__icontains='Purchase Accounts')
		self.fields['purchase'].widget.attrs = {'class': 'form-control select2',}
		self.fields['sub_total'].widget.attrs = {'class': 'form-control',}
		self.fields['Address'].widget.attrs = {'class': 'form-control',}
		self.fields['GSTIN'].widget.attrs = {'class': 'form-control',}
		self.fields['PAN'].widget.attrs = {'class': 'form-control',}
		self.fields['State'].widget.attrs = {'class': 'form-control select2',}
		self.fields['Contact'].widget.attrs = {'class': 'form-control',}
		self.fields['DeliveryNote'].widget.attrs = {'class': 'form-control',}
		self.fields['Supplierref'].widget.attrs = {'class': 'form-control',}
		self.fields['Mode'].widget.attrs = {'class': 'form-control',}

	def clean(self):
		Party_ac = self.cleaned_data['Party_ac']
		purchase = self.cleaned_data['purchase']
		if Party_ac not in ledger1.objects.filter(Q(group1_Name__group_Name__icontains='Sundry Creditors') | Q(group1_Name__group_Name__icontains='Bank Accounts') | Q(group1_Name__group_Name__icontains='Cash-in-hand')):
			raise forms.ValidationError("Party Account should be for that ledgers which is present under of Sundry Creditors, Bank Accounts & Cash-in-hand")
		if purchase not in ledger1.objects.filter(group1_Name__group_Name__icontains='Purchase Accounts'):
			raise forms.ValidationError("Purchase Ledgers should be for that ledgers which is present under of Purchase Accounts")

class Sales_form(forms.ModelForm):
	class Meta:
		model  = Sales
		fields = ('User','Company','date','Address','billname','GSTIN','PAN','State','Contact','DeliveryNote','Supplierref','Mode', 'ref_no', 'Party_ac', 'sales', 'sub_total')
		widgets = {
            'date': DateInput(),
        }

	def __init__(self, *args, **kwargs):
		self.User = kwargs.pop('User', None)		
		self.Company = kwargs.pop('Company', None)
		super(Sales_form, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs     = {'class': 'form-control',}
		self.fields['ref_no'].widget.attrs   = {'class': 'form-control',}
		self.fields['billname'].widget.attrs   = {'class': 'form-control',}
		self.fields['Party_ac'].queryset = ledger1.objects.filter(Q(User= self.User),Q(Company = self.Company) , Q(group1_Name__group_Name__icontains='Sundry Debtors') | Q(group1_Name__group_Name__icontains='Bank Accounts') | Q(group1_Name__group_Name__icontains='Cash-in-hand'))
		self.fields['Party_ac'].widget.attrs = {'class': 'form-control select2',}
		self.fields['sales'].queryset = ledger1.objects.filter(User= self.User,Company = self.Company,group1_Name__group_Name__icontains='Sales Account')
		self.fields['sales'].widget.attrs = {'class': 'form-control select2',}
		self.fields['sub_total'].widget.attrs = {'class': 'form-control',}
		self.fields['Address'].widget.attrs = {'class': 'form-control',}
		self.fields['GSTIN'].widget.attrs = {'class': 'form-control',}
		self.fields['PAN'].widget.attrs = {'class': 'form-control',}
		self.fields['State'].widget.attrs = {'class': 'form-control select2',}
		self.fields['Contact'].widget.attrs = {'class': 'form-control',}
		self.fields['DeliveryNote'].widget.attrs = {'class': 'form-control',}
		self.fields['Supplierref'].widget.attrs = {'class': 'form-control',}
		self.fields['Mode'].widget.attrs = {'class': 'form-control',}

	def clean(self):
		Party_ac = self.cleaned_data['Party_ac']
		sales = self.cleaned_data['sales']
		if Party_ac not in ledger1.objects.filter(Q(group1_Name__group_Name__icontains='Sundry Debtors') | Q(group1_Name__group_Name__icontains='Bank Accounts') | Q(group1_Name__group_Name__icontains='Cash-in-hand')):
			raise forms.ValidationError("Party Account should be for that ledgers which is present under of Sundry Debtors, Bank Accounts & Cash-in-hand")
		if sales not in ledger1.objects.filter(group1_Name__group_Name__icontains='Sales Account'):
			raise forms.ValidationError("Sale Ledgers should be for that ledgers which is present under of Sales Account")

class Sales_formadmin(forms.ModelForm):
	class Meta:
		model  = Sales
		fields = ('User','Company','date','Address','billname','GSTIN','PAN','State','Contact','DeliveryNote','Supplierref','Mode', 'ref_no', 'Party_ac', 'sales', 'sub_total')
		widgets = {
            'date': DateInput(),
        }

	def __init__(self, *args, **kwargs):
		super(Sales_formadmin, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs     = {'class': 'form-control',}
		self.fields['ref_no'].widget.attrs   = {'class': 'form-control',}
		self.fields['billname'].widget.attrs   = {'class': 'form-control',}
		self.fields['Party_ac'].queryset = ledger1.objects.filter(Q(group1_Name__group_Name__icontains='Sundry Debtors') | Q(group1_Name__group_Name__icontains='Bank Accounts') | Q(group1_Name__group_Name__icontains='Cash-in-hand'))
		self.fields['Party_ac'].widget.attrs = {'class': 'form-control select2',}
		self.fields['sales'].queryset = ledger1.objects.filter(group1_Name__group_Name__icontains='Sales Account')
		self.fields['sales'].widget.attrs = {'class': 'form-control select2',}
		self.fields['sub_total'].widget.attrs = {'class': 'form-control',}
		self.fields['Address'].widget.attrs = {'class': 'form-control',}
		self.fields['GSTIN'].widget.attrs = {'class': 'form-control',}
		self.fields['PAN'].widget.attrs = {'class': 'form-control',}
		self.fields['State'].widget.attrs = {'class': 'form-control select2',}
		self.fields['Contact'].widget.attrs = {'class': 'form-control',}
		self.fields['DeliveryNote'].widget.attrs = {'class': 'form-control',}
		self.fields['Supplierref'].widget.attrs = {'class': 'form-control',}
		self.fields['Mode'].widget.attrs = {'class': 'form-control',}

	def clean(self):
		Party_ac = self.cleaned_data['Party_ac']
		sales = self.cleaned_data['sales']
		if Party_ac not in ledger1.objects.filter(Q(group1_Name__group_Name__icontains='Sundry Debtors') | Q(group1_Name__group_Name__icontains='Bank Accounts') | Q(group1_Name__group_Name__icontains='Cash-in-hand')):
			raise forms.ValidationError("Party Account should be for that ledgers which is present under of Sundry Debtors, Bank Accounts & Cash-in-hand")
		if sales not in ledger1.objects.filter(group1_Name__group_Name__icontains='Sales Account'):
			raise forms.ValidationError("Sale Ledgers should be for that ledgers which is present under of Sales Account")



class Stock_Totalform(forms.ModelForm):
	class Meta:
		model  = Stock_Total
		fields = ('stockitem', 'Quantity_p', 'rate_p', 'Disc_p', 'Total_p')


	def __init__(self, *args, **kwargs):
		super(Stock_Totalform, self).__init__(*args, **kwargs)
		self.fields['stockitem'].widget.attrs = {'class': 'form-control select2',}
		self.fields['Quantity_p'].widget.attrs = {'class': 'form-control',}
		self.fields['rate_p'].widget.attrs     = {'class': 'form-control',}
		self.fields['Disc_p'].widget.attrs = {'class': 'form-control',}
		self.fields['Total_p'].widget.attrs = {'class': 'form-control',}

Purchase_formSet = inlineformset_factory(Purchase, Stock_Total,
                                            form=Stock_Totalform, extra=6)





class Stock_Totalformsales(forms.ModelForm):
	class Meta:
		model  = Stock_Total_sales
		fields = ('stockitem', 'Quantity', 'rate', 'Disc', 'Total')

	def __init__(self, *args, **kwargs):
		super(Stock_Totalformsales, self).__init__(*args, **kwargs)
		self.fields['stockitem'].widget.attrs = {'class': 'form-control select2',}
		self.fields['Quantity'].widget.attrs = {'class': 'form-control',}
		self.fields['rate'].widget.attrs     = {'class': 'form-control',}
		self.fields['Disc'].widget.attrs = {'class': 'form-control',}
		self.fields['Total'].widget.attrs = {'class': 'form-control',}


Sales_formSet =  inlineformset_factory(Sales, Stock_Total_sales,
                                            form=Stock_Totalformsales, extra=6)		


 
