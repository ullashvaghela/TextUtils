from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,BlackList,UserVerification

# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None,{'fields':('username','password')}),
        ('Personal info',{'fields':('email','first_name','last_name','address','state','zipcode','contact_number')}),
        ('Important dates',{'fields':('last_login','date_joined')}),
        )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2','email'),
        }),
    )

    list_display = ('username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name','email')
    ordering = ('email',)

admin.site.register(UserVerification)
admin.site.register(BlackList)
