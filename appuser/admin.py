from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(BaseModel)
class BaseAdminSite(admin.ModelAdmin):
    list_display = ["id", "updated_at", "created_at"]
   

@admin.register(Users)
class UsersAdminSite(admin.ModelAdmin):
    list_display = ["id", "username", "email", "fname", "lname", "profile" ]



@admin.register(UserPost)
class BaseAdminSite(admin.ModelAdmin):
    list_display = ["id", "user", "image", "caption", "time"]
    
    

@admin.register(Likes)
class BaseAdminSite(admin.ModelAdmin):
    list_display = ["id", "user", "post", "time"]


@admin.register(Comment)
class BaseAdminSite(admin.ModelAdmin):
    list_display = ["id", "post", "time", "text"]            

    