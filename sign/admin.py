from django.contrib import admin
from sign.models import Event, Guest

# Register your models here.
'''

class EventAdmin(admin.ModelAdmin):     #继承django.contrib.admin.ModelAdmin类
	list_display = ['name','status','start_time','id']    #定义列表显示字段
	search_fields = ['name'] #搜索栏
	list_filter = ['status'] #过滤器

class GuestAdmin(admin.ModelAdmin):
	list_display = ['realname','phone','email','sign','create_time','event']
	search_fields = ['realname','phone'] #搜索栏
	list_filter = ['sign'] #过滤器

admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)
'''	
