from django.contrib import admin
from . import models
# Register your models here.


class companyAdmin(admin.ModelAdmin):

	search_fields = ['Name']
	readonly_fields = ('User',)

	list_display = ['Name','Type_of_company' ,'Shared_Users', 'Mobile_No', 'Financial_Year_From']


admin.site.register(models.company,companyAdmin)
