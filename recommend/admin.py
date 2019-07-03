from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser
from myrecommender.urls import urlpatterns

# Register your models here.
class CustomUserAdmin(CustomUser):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]
    urls = urlpatterns

admin.site.register(CustomUser, CustomUserAdmin)
