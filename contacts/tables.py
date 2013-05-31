from django.utils.translation import ugettext_lazy as _
from django.utils.dateformat import format
from django.utils.formats import get_format
import django_tables2 as tables


class ContactTable(tables.Table):
    id = tables.CheckBoxColumn()
    full_name = tables.Column(verbose_name=_('Full name'))
    phone = tables.Column(verbose_name=_('Phone'))

    class Meta:
        attrs = {
            'class': 'table table-striped table-condensed',
        }
        empty_text = _('There are no contacts here (yet).')
