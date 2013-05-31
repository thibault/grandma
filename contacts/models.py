from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import User


class Contact(models.Model):
    user = models.ForeignKey(User, related_name='contacts')
    first_name = models.CharField(_('First name'), max_length=128)
    last_name = models.CharField(_('Last name'), max_length=128)
    mobile = models.CharField(_('Mobile'), max_length=20,
                              help_text=_('Use international format, e.g +33612345678'))

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
        ordering = ('last_name', 'first_name')

    def __unicode__(self):
        return self.full_name

    @property
    def full_name(self):
        name = '%s %s' % (self.first_name, self.last_name)
        return name.title()
