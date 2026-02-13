from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from core.models import AppUser

class Command(BaseCommand):
    help = "Ensure admin users exist for Django admin and AppUser"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@sh.com', 'admin1239')
            self.stdout.write(self.style.SUCCESS('Created Django superuser: admin'))
        else:
            self.stdout.write('Django superuser already exists: admin')

        if not AppUser.objects.filter(email='admin@sh.com').exists():
            AppUser.objects.create(
                name='Admin',
                phone='1234567890',
                email='admin@sh.com',
                password=make_password('admin1239'),
                address='Admin Address',
                role='admin',
            )
            self.stdout.write(self.style.SUCCESS('Created AppUser admin: admin@sh.com'))
        else:
            self.stdout.write('AppUser admin already exists: admin@sh.com')
