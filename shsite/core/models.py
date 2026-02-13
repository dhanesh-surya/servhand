from django.db import models
from django.utils import timezone

class AppUser(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    address = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=50, default='user')
    def __str__(self):
        return self.name

class ServiceProvider(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=256)
    location = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=50, default='service_provider')
    def __str__(self):
        return self.name

class ServiceProviderCategory(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='categories')
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    rent_value = models.FloatField(null=True, blank=True)
    other_charges = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.category_name

class Booking(models.Model):
    booking_reference_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=150)
    booking_datetime = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, default='pending')
    final_amount = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.booking_reference_id

class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=150, default='Arrival Unscripted')
    owner = models.CharField(max_length=150, default='Toshendra Kumar')
    email = models.EmailField(default='servicehand1710@gmail.com')
    mobile = models.CharField(max_length=20, default='Editable Mobile')
    address = models.TextField(default='Cyber Zone CSC, Janjgir Road Pamgarh, Janjgir-Champa (CG) – 495554')
    social_links = models.TextField(blank=True)
    def __str__(self):
        return self.company_name

class PasswordReset(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True, blank=True)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, null=True, blank=True)
    token = models.CharField(max_length=200)
    expiry = models.DateTimeField()
    def __str__(self):
        return self.token

class AuditLog(models.Model):
    admin = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.admin.email} {self.timestamp.isoformat()}'
