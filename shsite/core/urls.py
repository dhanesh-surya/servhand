from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:token>', views.reset_password, name='reset_password'),
    path('user_dashboard', views.user_dashboard, name='user_dashboard'),
    path('admin_dashboard', views.user_dashboard, name='admin_dashboard'),
    path('service_provider_dashboard', views.user_dashboard, name='service_provider_dashboard'),
    path('browse_services', views.browse_services, name='browse_services'),
    path('providers/<int:pk>', views.provider_detail, name='provider_detail'),
    path('providers/<int:pk>/hire', views.hire_provider, name='hire_provider'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('bookings/<int:pk>/cancel', views.booking_cancel, name='booking_cancel'),
    path('bookings/<int:pk>/complete', views.booking_complete, name='booking_complete'),
]
