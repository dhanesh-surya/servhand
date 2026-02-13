from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from .forms import UserProfileForm, UserChangePasswordForm
from .models import AppUser, ServiceProvider, ServiceProviderCategory, Booking, CompanyInfo, PasswordReset
from django.db.models import Count
import random
import string

def seed_demo_data():
    if ServiceProvider.objects.count() == 0:
        p1 = ServiceProvider.objects.create(name='Rahul Kumar', phone='9876543210', password=make_password('pass123'), location='Janjgir, CG')
        p2 = ServiceProvider.objects.create(name='Sita Devi', phone='9123456780', password=make_password('pass123'), location='Pamgarh, CG')
        p3 = ServiceProvider.objects.create(name='Arjun Verma', phone='9001122334', password=make_password('pass123'), location='Champa, CG')
        ServiceProviderCategory.objects.bulk_create([
            ServiceProviderCategory(provider=p1, category_name='Electrician'),
            ServiceProviderCategory(provider=p1, category_name='AC Repair'),
            ServiceProviderCategory(provider=p2, category_name='Plumber'),
            ServiceProviderCategory(provider=p2, category_name='Water Purifier'),
            ServiceProviderCategory(provider=p3, category_name='Carpenter'),
        ])

def generate_booking_ref():
    year = str(timezone.now().year)
    last = Booking.objects.filter(booking_reference_id__startswith=f'GS{year}-').order_by('-id').first()
    if last:
        last_num = int(last.booking_reference_id.split('-')[1])
        new_num = f'{last_num + 1:06d}'
    else:
        new_num = '000001'
    return f'GS{year}-{new_num}'

def generate_reset_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def validate_email_domain(email: str):
    allowed = ['@edu', '@edu.in', '@ac.in', '@gov.in', '@nic.in', '@companyname.com', '@companyname.in', '@startupname.io', '@organization.org', '@college.edu', '@college.ac.in', '@rediffmail.com', '@yandex.com', '@gmail.com', '@yahoo.com', '@yahoo.co.in', '@outlook.com', '@hotmail.com', '@live.com', '@icloud.com', '@aol.com', '@protonmail.com', '@zoho.com']
    domain = email[email.find('@'):]
    return any(domain.endswith(d) for d in allowed)

def home(request: HttpRequest) -> HttpResponse:
    company = CompanyInfo.objects.first()
    if not company:
        company = CompanyInfo.objects.create()
    seed_demo_data()
    providers = ServiceProvider.objects.prefetch_related('categories').all().order_by('name')[:6]
    services = ServiceProviderCategory.objects.values('category_name').annotate(count=Count('id')).order_by('category_name')[:8]
    return render(request, 'home.html', {'company': company, 'providers': providers, 'services': services})

def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        password = make_password(request.POST.get('password', ''))
        address = request.POST.get('address', '')
        role = request.POST.get('role', 'user')
        if not validate_email_domain(email):
            messages.error(request, 'Email domain not allowed for registration.')
            return redirect('register')
        if AppUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')
        user = AppUser.objects.create(name=name, phone=phone, email=email, password=password, address=address, role=role)
        if role == 'service_provider':
            ServiceProvider.objects.create(name=name, phone=phone, password=password)
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')
    return render(request, 'register.html')

def login(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = AppUser.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            request.session['user_id'] = user.id
            request.session['role'] = user.role
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'service_provider':
                return redirect('service_provider_dashboard')
            else:
                return redirect('user_dashboard')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')

def logout(request: HttpRequest) -> HttpResponse:
    request.session.flush()
    return redirect('home')

def forgot_password(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        email = request.POST.get('email', '')
        method = request.POST.get('method', 'email')
        user = AppUser.objects.filter(email=email).first()
        if user:
            token = generate_reset_token()
            reset = PasswordReset.objects.create(user=user, token=token, expiry=timezone.now() + timezone.timedelta(hours=1))
            if method == 'email':
                link = request.build_absolute_uri(reverse('reset_password', args=[token]))
                send_mail('Password Reset', f'Your reset link: {link}', 'noreply@local', [email], fail_silently=True)
                messages.success(request, 'Reset link sent to email.')
            elif method == 'whatsapp':
                link = request.build_absolute_uri(reverse('reset_password', args=[token]))
                messages.success(request, f'Send this link via WhatsApp: {link}')
        else:
            messages.error(request, 'Email not found.')
    return render(request, 'forgot_password.html')

def reset_password(request: HttpRequest, token: str) -> HttpResponse:
    reset = PasswordReset.objects.filter(token=token).first()
    if not reset or reset.expiry < timezone.now():
        messages.error(request, 'Invalid or expired token.')
        return redirect('login')
    if request.method == 'POST':
        password = make_password(request.POST.get('password', ''))
        if reset.user_id:
            user = reset.user
            user.password = password
            user.save()
        elif reset.service_provider_id:
            provider = reset.service_provider
            provider.password = password
            provider.save()
        reset.delete()
        messages.success(request, 'Password reset successful.')
        return redirect('login')
    return render(request, 'reset_password.html')

def user_dashboard(request: HttpRequest) -> HttpResponse:
    if request.session.get('role') != 'user':
        return redirect('login')
    user = AppUser.objects.get(id=request.session['user_id'])
    bookings = Booking.objects.filter(user=user).order_by('-booking_datetime')
    company = CompanyInfo.objects.first()
    return render(request, 'dashboard_user.html', {'user': user, 'bookings': bookings, 'company': company})

def edit_profile(request: HttpRequest) -> HttpResponse:
    if request.session.get('role') != 'user':
        return redirect('login')
    user = AppUser.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('user_dashboard')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})

def change_password(request: HttpRequest) -> HttpResponse:
    if request.session.get('role') != 'user':
        return redirect('login')
    user = AppUser.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = UserChangePasswordForm(request.POST)
        if form.is_valid():
            old = form.cleaned_data['old_password']
            new = form.cleaned_data['new_password']
            if not check_password(old, user.password):
                messages.error(request, 'Current password is incorrect.')
            elif check_password(new, user.password):
                messages.error(request, 'New password must be different from current.')
            else:
                user.password = make_password(new)
                user.save()
                messages.success(request, 'Password changed successfully.')
                return redirect('user_dashboard')
    else:
        form = UserChangePasswordForm()
    return render(request, 'change_password.html', {'form': form})
def browse_services(request: HttpRequest) -> HttpResponse:
    seed_demo_data()
    providers = ServiceProvider.objects.prefetch_related('categories').all().order_by('name')
    return render(request, 'browse_services.html', {'providers': providers})

def provider_detail(request: HttpRequest, pk: int) -> HttpResponse:
    provider = get_object_or_404(ServiceProvider.objects.prefetch_related('categories'), pk=pk)
    return render(request, 'provider_detail.html', {'provider': provider})

def hire_provider(request: HttpRequest, pk: int) -> HttpResponse:
    if request.session.get('role') != 'user':
        messages.error(request, 'Please login as a user to hire.')
        return redirect('login')
    provider = get_object_or_404(ServiceProvider, pk=pk)
    user = AppUser.objects.get(id=request.session['user_id'])
    service_name = request.POST.get('service_name')
    if not service_name:
        first_category = provider.categories.first()
        service_name = first_category.category_name if first_category else 'Service'
    Booking.objects.create(
        booking_reference_id=generate_booking_ref(),
        user=user,
        service_provider=provider,
        service_name=service_name,
        status='assigned'
    )
    messages.success(request, 'Hire request created successfully.')
    return redirect('user_dashboard')

def booking_cancel(request: HttpRequest, pk: int) -> HttpResponse:
    if request.session.get('role') != 'user':
        messages.error(request, 'Please login to manage bookings.')
        return redirect('login')
    booking = get_object_or_404(Booking, pk=pk, user_id=request.session['user_id'])
    if booking.status in ['completed', 'cancelled']:
        messages.info(request, 'Booking already finalized.')
        return redirect('user_dashboard')
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, 'Booking cancelled.')
    return redirect('user_dashboard')

def booking_complete(request: HttpRequest, pk: int) -> HttpResponse:
    if request.session.get('role') != 'user':
        messages.error(request, 'Please login to manage bookings.')
        return redirect('login')
    booking = get_object_or_404(Booking, pk=pk, user_id=request.session['user_id'])
    if booking.status in ['completed', 'cancelled']:
        messages.info(request, 'Booking already finalized.')
        return redirect('user_dashboard')
    booking.status = 'completed'
    booking.save()
    messages.success(request, 'Marked booking as completed.')
    return redirect('user_dashboard')
