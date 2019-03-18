from django import forms
from userprofile.models import Profile, Post, Post_comment, Pro_services, achivements, pro_verify, Organisation, Organisation_member

class profileform(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(profileform, self).__init__(*args, **kwargs)
		self.fields['E_mail'].widget.attrs = {'class': 'form-control',}
		self.fields['user_type'].required = False
		self.fields['user_type'].widget.attrs['disabled'] = 'disabled'
		self.fields['Phone_no'].widget.attrs = {'class': 'form-control',}
		self.fields['basic_info'].widget.attrs = {'class': 'form-control',}
		self.fields['Full_Name'].widget.attrs = {'class': 'form-control',}
		self.fields['Permanant_Address'].widget.attrs = {'class': 'form-control',}
		self.fields['District'].widget.attrs = {'class': 'form-control',}
		self.fields['State'].widget.attrs = {'class': 'form-control',}
		self.fields['City'].widget.attrs = {'class': 'form-control',}
		self.fields['Country'].widget.attrs = {'class': 'form-control',}




	class Meta:
		model = Profile
		fields = ('Full_Name', 'user_type', 'E_mail','Permanant_Address','District','State','City','Country', 'Phone_no', 'basic_info', 'image')


	def clean(self):
		cleaned_data = super(profileform, self).clean()
		E_mail = cleaned_data.get('E_mail')
		Phone_no = cleaned_data.get('Phone_no')

	def clean_user_type(self):
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			return instance.user_type
		else:
			return self.cleaned_data['user_type']

class organisationform(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(organisationform, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs = {'class': 'form-control'}
		self.fields['location'].widget.attrs = {'class': 'form-control'}

	class Meta:
		model = Organisation
		fields = ['name','location']

class organisation_memberform(forms.ModelForm):

	class Meta:
		model = Organisation_member
		fields = ['is_admin']


class proverifyform(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(proverifyform, self).__init__(*args, **kwargs)
		self.fields['product'].widget.attrs = {'class': 'form-control select2'}
		self.fields['phone_no'].widget.attrs = {'class': 'form-control'}
		self.fields['e_mail'].widget.attrs = {'class': 'form-control'}

	class Meta:
		model = pro_verify
		fields = ['product','phone_no', 'e_mail', 'upload_1','upload_2', 'upload_3']


class Postform(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('post',)

class postcommentform(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(postcommentform, self).__init__(*args, **kwargs)
		self.fields['text'].widget.attrs = {'class': 'form-control', 'placeholder' : 'Post Comments Here'}

	class Meta:
		model = Post_comment
		fields = ['text',]

class Service_form(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(Service_form, self).__init__(*args, **kwargs)
		self.fields['service_name'].widget.attrs = {'class': 'form-control'}
		self.fields['details'].widget.attrs = {'class': 'form-control'}
		self.fields['service_type'].widget.attrs = {'class': 'form-control select2'}
		self.fields['duration'].widget.attrs = {'class': 'form-control select2'}
		self.fields['service_mode'].widget.attrs = {'class': 'form-control select2'}
		self.fields['rate'].widget.attrs = {'class': 'form-control'}

	class Meta:
		model = Pro_services
		fields = ['service_name','details','service_type','duration','service_mode','rate']


class Achievement_form(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(Achievement_form, self).__init__(*args, **kwargs)
		self.fields['act'].widget.attrs = {'class': 'form-control'}
		self.fields['location'].widget.attrs = {'class': 'form-control'}
		self.fields['facts'].widget.attrs = {'class': 'form-control'}
		self.fields['issue'].widget.attrs = {'class': 'form-control'}
		self.fields['argument'].widget.attrs = {'class': 'form-control'}
		self.fields['judgement'].widget.attrs = {'class': 'form-control'}
		self.fields['user_role'].widget.attrs = {'class': 'form-control'}

	class Meta:
		model = achivements
		fields = ['legal_case','act','location','facts','issue','argument','judgement','user_role']
