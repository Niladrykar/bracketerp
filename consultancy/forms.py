from django import forms
from consultancy.models import consultancy,Answer



class consultancyform(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(consultancyform, self).__init__(*args, **kwargs)
		self.fields['Questions'].widget.attrs = {'class': 'form-control'}

	class Meta:
		model = consultancy
		fields = ['Questions',]
		

	def clean(self):
		cleaned_data = super(consultancyform, self).clean()
		Questions = cleaned_data.get('Questions')

class Answerform(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(Answerform, self).__init__(*args, **kwargs)
		self.fields['text'].widget.attrs = {'class': 'form-control', 'placeholder' : 'Post Answers Here'}

	class Meta:
		model = Answer
		fields = ['text',]







