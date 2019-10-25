from django.contrib import admin
from app1.models import UserProfileInfo
from app1.models import Friends,CurrentTransaction
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Friends)
admin.site.register(CurrentTransaction) 
