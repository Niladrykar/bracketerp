from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

def file_size(value): # add this to some file where you can import it from
	limit = 2 * 1024 * 1024
	if value.size > limit:
		raise ValidationError('File too large. Size should not exceed 2 MB.')


class Message(models.Model):
	sender 		=	models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="sender")
	reciever 	= 	models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="receiver")
	subject		=	models.CharField(max_length=100,null=True)
	msg_content =	RichTextUploadingField(blank=True, null=True,config_name='special')
	attchment	= 	models.FileField(upload_to="message_picture",blank=True, validators=[file_size])
	created_at 	=	models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.msg_content

	@property
	def filename(self):
		name = self.attchment.name.split("/")[1].replace('_',' ').replace('-',' ')
		return name