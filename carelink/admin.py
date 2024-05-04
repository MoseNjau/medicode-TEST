from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .forms import CreateUserForm
#import the room and message from the model 
from .models import Room, Message

class CustomUserAdmin(BaseUserAdmin):
    add_form = CreateUserForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'id_number', 'phone_number', 'password1', 'password2'),
        }),
    )

# Register the User model with the custom admin class
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register your room and message here.
admin.site.register(Room)
admin.site.register(Message)
