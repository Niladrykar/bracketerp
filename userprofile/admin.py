from django.contrib import admin
from userprofile.models import Profile, Product_activation, Post, Post_comment, Pro_services, achivements, pro_verify, Organisation, Organisation_member
# Register your models here.


class Organisation_admin(admin.ModelAdmin):
	model = Organisation
	list_display = ['User','name', 'location']
	search_fields = ['name','User']


class Organisation_member_admin(admin.ModelAdmin):
	model = Organisation_member
	list_display = ['User','organisation', 'member_name','is_admin']
	search_fields = ['organisation','User']


admin.site.register(Profile)
admin.site.register(Product_activation)
admin.site.register(Post)
admin.site.register(Post_comment)
admin.site.register(Pro_services)
admin.site.register(achivements)
admin.site.register(pro_verify)
admin.site.register(Organisation,Organisation_admin)
admin.site.register(Organisation_member,Organisation_member_admin)