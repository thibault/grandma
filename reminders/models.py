from django.utils.translation import ugettext_lazy as _
from django.db import models
from accounts.models import User
from messages.models import send_message
from django.conf import settings


class Reminder(models.Model):
    user = models.ForeignKey(User, related_name='reminders')
    message = models.CharField(_('Message'), max_length=150)
    when = models.DateTimeField(_('Date'))
    sent = models.BooleanField(_('Already sent?'), default=False)

    def send(self):
        """Use the Nexmo API to send the reminder."""
        send_message(self.user.phone, self.message)
        self.sent = True
        self.save()
