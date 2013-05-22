import datetime
from django.core.management.base import BaseCommand, CommandError
from reminders.models import Reminder


class Command(BaseCommand):
    """This tasks sends all the waiting reminders."""
    def handle(self, *args, **kwargs):
        reminders = Reminder.objects.filter(when__lte=datetime.datetime.now) \
                .filter(sent=False)

        for reminder in reminders:
            reminder.send()
