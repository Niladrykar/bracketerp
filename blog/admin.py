from django.contrib import admin
from blog.models import Blog,categories
# Register your models here.

class blogadmin(admin.ModelAdmin):
	model = Blog
	list_display = ['Date', 'Blog_title']
	search_fields = ['Blog_title']
	readonly_fields = ('User',)

admin.site.register(Blog, blogadmin)
admin.site.register(categories)
