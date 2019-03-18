from django import forms
from accounting_double_entry.models import journal,group1,ledger1,selectdatefield,Payment,Particularspayment,Receipt,Particularsreceipt,Contra,Particularscontra,Multijournal,Multijournaltotal
from company.models import company
from Gst.models import Gst_input,Gst_output,Stock_gst
import datetime
from django.db.models import Q
from django.forms import inlineformset_factory


class DateInput(forms.DateInput):
    input_type = 'date'


class Gst_inputForm(forms.ModelForm):		
	class Meta:
		model = Gst_input
		fields = ('date', 'gstin_vendor', 'gstin_self','cgst', 'sgst', 'igst','ugst','purchase','withinstate')
		widgets = {
            'date': DateInput(),
        }

	def __init__(self, *args, **kwargs):
		super(group1Form, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs = {'class': 'form-control',}
		self.fields['gstin_vendor'].widget.attrs = {'class': 'form-control',}
		self.fields['gstin_self'].widget.attrs = {'class': 'form-control',}
		self.fields['cgst'].widget.attrs = {'class': 'form-control',}		
		self.fields['sgst'].widget.attrs = {'class': 'form-control',}
		self.fields['ugst'].widget.attrs = {'class': 'form-control',}		
		self.fields['purchase'].widget.attrs = {'class': 'form-control',}
		self.fields['withinstate'].widget.attrs = {'class': 'form-control',}


class Gst_outputForm(forms.ModelForm):		
	class Meta:
		model = Gst_output
		fields = ('date', 'gstin_vendor', 'gstin_self','cgst', 'sgst', 'igst','ugst','sales','withinstate')
		widgets = {
            'date': DateInput(),
        }

	def __init__(self, *args, **kwargs):
		super(group1Form, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs = {'class': 'form-control',}
		self.fields['gstin_vendor'].widget.attrs = {'class': 'form-control',}
		self.fields['gstin_self'].widget.attrs = {'class': 'form-control',}
		self.fields['cgst'].widget.attrs = {'class': 'form-control',}		
		self.fields['sgst'].widget.attrs = {'class': 'form-control',}
		self.fields['ugst'].widget.attrs = {'class': 'form-control',}		
		self.fields['sales'].widget.attrs = {'class': 'form-control',}
		self.fields['withinstate'].widget.attrs = {'class': 'form-control',}


class Stock_gstForm(forms.ModelForm):		
	class Meta:
		model = Stock_gst
		fields = ('date', 'stock_item', 'gst_rate')
		widgets = {
            'date': DateInput(),
        }

	def __init__(self, *args, **kwargs):
		super(group1Form, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs = {'class': 'form-control',}
		self.fields['stock_item'].widget.attrs = {'class': 'form-control',}
		self.fields['gst_rate'].widget.attrs = {'class': 'form-control',}

		
		
		

