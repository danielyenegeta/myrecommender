from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from recommend.models import CustomUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not CustomUser.objects.filter(username="admin").exists():
            CustomUser.objects.create_superuser("admin", "admin@admin.com", "admin")
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
