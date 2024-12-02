from django_tenants.admin import TenantAdminMixin

from django.contrib import admin
from django_tenants.utils import schema_context
from tenantapp.models import User 
from adminapp.models import Tenant, Domain

from django.contrib import admin
from .models import Domain

@admin.register(Domain)
class DomainAdmin(TenantAdminMixin,admin.ModelAdmin):
    # def has_change_permission(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return True
    #     return False

    # def has_add_permission(self, request):
    #     if request.user.is_superuser:
    #         return True
    #     return False

    list_display = ('domain', )


@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin,admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'created_on')
    actions = ['view_tenant_data']

    def view_tenant_data(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(request, "Please select only one tenant to view data.")
            return

        tenant = queryset.first()
        with schema_context(tenant.schema_name):
            users = User.objects.all()
            user_names = [user.name for user in users]
            self.message_user(request, f"Users in {tenant.name}: {', '.join(user_names)}")

    view_tenant_data.short_description = "View Tenant-Specific Data"