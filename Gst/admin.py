from django.contrib import admin
from Gst.models import Gst_input,Gst_output,Stock_gst
# Register your models here.

admin.site.register(Gst_input)
admin.site.register(Gst_output)
admin.site.register(Stock_gst)