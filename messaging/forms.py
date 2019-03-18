from django import forms
from .models import Message
from django.conf import settings

User = settings.AUTH_USER_MODEL



class messageform(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(messageform, self).__init__(*args, **kwargs)
		self.fields['reciever'].widget.attrs = {'class': 'form-control select2',}
		self.fields['subject'].widget.attrs = {'class': 'form-control',}
		self.fields['msg_content'].widget.attrs = {'class': 'form-control',}
		self.fields['attchment'].widget.attrs = {'class': 'form-control',}

	class Meta:
		model = Message
		fields = ['reciever', 'subject', 'msg_content', 'attchment']
		

	# def clean(self):
	# 	cleaned_data = super(consultancyform, self).clean()
	# 	Questions = cleaned_data.get('Questions')


