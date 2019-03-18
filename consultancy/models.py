from django.db import models
from django.conf import settings
from django.urls import reverse
# Create your models here.


class consultancy(models.Model):
	User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Date = models.DateTimeField(auto_now_add=True)
	Questions = models.TextField()
	like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='like',blank=True)

	def __str__(self):
		return self.Questions

	def get_absolute_url(self):
		return reverse("consultancy:consultancydetail", kwargs={'pk':self.pk})


	def total_like(self):
		return self.like.count()

class Answer(models.Model):
	User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Questions = models.ForeignKey(consultancy,on_delete=models.CASCADE,related_name='consultancies')
	text = models.TextField()
	Date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.text





