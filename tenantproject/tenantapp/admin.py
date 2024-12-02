from django.contrib import admin
from tenantapp.models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name',)