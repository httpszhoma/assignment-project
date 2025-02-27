from django.core.management.base import BaseCommand
from ...models import Spectacle
from django.utils import timezone


class Command(BaseCommand):
    help = 'Delete spectacles that have already passed'

    def handle(self, *args, **kwargs):
        spectacles = Spectacle.objects.all()
        deleted_count = 0
        for spectacle in spectacles:
            if spectacle.datetime_passing < timezone.now():
                spectacle.delete_related_data()
                deleted_count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} old spectacles.'))
