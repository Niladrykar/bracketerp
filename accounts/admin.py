from django.contrib import admin
from django.contrib.auth.models import User

class MyUserAdmin(admin.ModelAdmin):
	search_fields = ['id','username']
	list_display = ['id','username','email', 'first_name', 'last_name', 'is_active','is_superuser', 'last_login']

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)