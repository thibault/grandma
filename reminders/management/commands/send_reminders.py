from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from reminders.models import Reminder


class Command(BaseCommand):
    """This tasks sends all the waiting reminders."""
    def handle(self, *args, **kwargs):
        reminders = Reminder.objects.filter(when__lte=timezone.now()) \
                .filter(user__is_valid=True) \
                .filter(sent=False)

        for reminder in reminders:
            reminder.send()
