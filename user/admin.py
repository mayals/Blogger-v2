from django.contrib import admin
from .models import UserModel, Profile

admin.site.register(UserModel)
admin.site.register(Profile)