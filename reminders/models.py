from django.utils.translation import ugettext_lazy as _
from django.db import models


class Reminder(models.Model):
    phone = models.CharField(_('Mobile'), max_length=20,
                             help_text=_('Use international format, e.g +33612345678'))
    message = models.CharField(_('Message'), max_length=150)
    when = models.DateTimeField(_('Date'))
    sent = models.BooleanField(_('Already sent?'), default=False)
