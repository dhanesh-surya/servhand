from django import forms
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .models import (
    AppUser,
    ServiceProvider,
    ServiceProviderCategory,
    Booking,
    CompanyInfo,
    PasswordReset,
    AuditLog,
)

ALLOWED_DOMAINS = ['@edu', '@edu.in', '@ac.in', '@gov.in', '@nic.in', '@companyname.com', '@companyname.in', '@startupname.io', '@organization.org', '@college.edu', '@college.ac.in', '@rediffmail.com', '@yandex.com', '@gmail.com', '@yahoo.com', '@yahoo.co.in', '@outlook.com', '@hotmail.com', '@live.com', '@icloud.com', '@aol.com', '@protonmail.com', '@zoho.com']

def validate_email_domain(email: str) -> bool:
    if '@' not in email:
        return False
    domain = email[email.find('@'):]
    return any(domain.endswith(d) for d in ALLOWED_DOMAINS)

class AppUserForm(forms.ModelForm):
    raw_password = forms.CharField(label='Password', required=False, widget=forms.PasswordInput)
    class Meta:
        model = AppUser
        fields = ['name', 'phone', 'email', 'address', 'role', 'raw_password']
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if not validate_email_domain(email):
            raise forms.ValidationError('Email domain not allowed.')
        return email
    def save(self, commit=True):
        obj = super().save(commit=False)
        raw = self.cleaned_data.get('raw_password')
        if raw:
            obj.password = make_password(raw)
        if commit:
            obj.save()
        return obj

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['name', 'phone', 'email', 'address']
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if not validate_email_domain(email):
            raise forms.ValidationError('Email domain not allowed.')
        return email

class UserChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Current Password')
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    def clean(self):
        cleaned = super().clean()
        new = cleaned.get('new_password')
        confirm = cleaned.get('confirm_password')
        if new and len(new) < 6:
            raise forms.ValidationError('New password must be at least 6 characters.')
        if new != confirm:
            raise forms.ValidationError('New password and confirm do not match.')
        return cleaned

class ServiceProviderForm(forms.ModelForm):
    raw_password = forms.CharField(label='Password', required=False, widget=forms.PasswordInput)
    class Meta:
        model = ServiceProvider
        fields = ['name', 'phone', 'location', 'role', 'raw_password']
    def save(self, commit=True):
        obj = super().save(commit=False)
        raw = self.cleaned_data.get('raw_password')
        if raw:
            obj.password = make_password(raw)
        if commit:
            obj.save()
        return obj

class ServiceProviderCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceProviderCategory
        fields = ['provider', 'category_name', 'description', 'rent_value', 'other_charges']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_reference_id', 'user', 'service_provider', 'service_name', 'booking_datetime', 'status', 'final_amount']
    def save(self, commit=True):
        obj = super().save(commit=False)
        if not obj.booking_reference_id:
            year = str(timezone.now().year)
            last = Booking.objects.filter(booking_reference_id__startswith=f'GS{year}-').order_by('-id').first()
            if last:
                last_num = int(last.booking_reference_id.split('-')[1])
                new_num = f'{last_num + 1:06d}'
            else:
                new_num = '000001'
            obj.booking_reference_id = f'GS{year}-{new_num}'
        if commit:
            obj.save()
        return obj

class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = ['company_name', 'owner', 'email', 'mobile', 'address', 'social_links']

class PasswordResetForm(forms.ModelForm):
    class Meta:
        model = PasswordReset
        fields = ['user', 'service_provider', 'token', 'expiry']
    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('user') and not cleaned.get('service_provider'):
            raise forms.ValidationError('Either user or service provider must be set.')
        return cleaned

class AuditLogForm(forms.ModelForm):
    class Meta:
        model = AuditLog
        fields = ['admin', 'action', 'timestamp']
