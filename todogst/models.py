from django.db import models
from django.conf import settings
from datetime import datetime, timezone
from django.utils.timesince import timesince
from django.utils import timezone 
from django.db.models.signals import pre_save


# Create your models here.


class Todo(models.Model):
	User 			= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	Date 			= models.DateTimeField(auto_now_add=True)
	text 			= models.CharField(max_length=128)
	complete_by 	= models.DateTimeField(default= timezone.now)
	complete 		= models.BooleanField(default=False)
    

	def __str__(self):
		return self.text

	def daysince(self):
		now = datetime.now(timezone.utc)
		dt = self.complete_by - now
		return dt.days


	



