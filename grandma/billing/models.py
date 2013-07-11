import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .fields import CurrencyField


logger = logging.getLogger(__name__)


class Plan(models.Model):
    """Subscription plans."""
    name = models.CharField(_('Name'), max_length=64)
    slug = models.SlugField(_('Slug'), max_length=64, default='')
    price = CurrencyField(_('Price'))

    class Meta:
        verbose_name = _('Plan')
        verbose_name_plural = _('Plans')

    def __unicode__(self):
        return self.name
