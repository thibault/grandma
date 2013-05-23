from django.utils.translation import ugettext_lazy as _
from django.db import models
from messages.models import NexmoMessage
from django.conf import settings


class Reminder(models.Model):
    phone = models.CharField(_('Mobile'), max_length=20,
                             help_text=_('Use international format, e.g +33612345678'))
    message = models.CharField(_('Message'), max_length=150)
    when = models.DateTimeField(_('Date'))
    sent = models.BooleanField(_('Already sent?'), default=False)

    def send(self):
        """Use the Nexmo API to send the reminder."""
        params = {
            'username': settings.NEXMO_USERNAME,
            'password': settings.NEXMO_PASSWORD,
            'type': 'unicode',
            'from': settings.NEXMO_FROM,
            'to': self.phone,
            'text': self.message.encode('utf-8'),
        }
        sms = NexmoMessage(params)
        response = sms.send_request()
