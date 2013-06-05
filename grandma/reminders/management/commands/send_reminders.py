from django.utils import timezone
from django.core.management.base import BaseCommand
from reminders.models import Reminder


class Command(BaseCommand):
    """This tasks sends all the waiting reminders."""
    def handle(self, *args, **kwargs):
        reminders = Reminder.objects.filter(when__lte=timezone.now()) \
            .filter(sent=False)

        for reminder in reminders:
            reminder.send()
