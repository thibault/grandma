import datetime
from django.core.management.base import BaseCommand, CommandError
from reminders.models import Reminder


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        reminders = Reminder.objects.filter(when__lte=datetime.datetime.now) \
                .filter(sent=False)
        print reminders
