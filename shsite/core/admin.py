from django.contrib import admin
from .models import (
    AppUser,
    ServiceProvider,
    ServiceProviderCategory,
    Booking,
    CompanyInfo,
    PasswordReset,
    AuditLog,
)
from .forms import (
    AppUserForm,
    ServiceProviderForm,
    ServiceProviderCategoryForm,
    BookingForm,
    CompanyInfoForm,
    PasswordResetForm,
    AuditLogForm,
)

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    form = AppUserForm
    list_display = ('name', 'email', 'phone', 'role')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('role',)

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    form = ServiceProviderForm
    list_display = ('name', 'phone', 'location', 'role')
    search_fields = ('name', 'phone', 'location')
    list_filter = ('role',)

@admin.register(ServiceProviderCategory)
class ServiceProviderCategoryAdmin(admin.ModelAdmin):
    form = ServiceProviderCategoryForm
    list_display = ('provider', 'category_name', 'rent_value', 'other_charges')
    search_fields = ('category_name', 'provider__name')
    list_filter = ('category_name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    form = BookingForm
    list_display = ('booking_reference_id', 'user', 'service_provider', 'service_name', 'booking_datetime', 'status', 'final_amount')
    search_fields = ('booking_reference_id', 'service_name', 'user__email', 'service_provider__name')
    list_filter = ('status', 'booking_datetime')

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    form = CompanyInfoForm
    list_display = ('company_name', 'owner', 'email', 'mobile')
    search_fields = ('company_name', 'owner', 'email', 'mobile')

@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    form = PasswordResetForm
    list_display = ('token', 'user', 'service_provider', 'expiry')
    search_fields = ('token', 'user__email', 'service_provider__name')
    list_filter = ('expiry',)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    form = AuditLogForm
    list_display = ('admin', 'timestamp', 'action')
    search_fields = ('admin__email', 'action')
    list_filter = ('timestamp',)
