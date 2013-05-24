import datetime
from django.utils.translation import ugettext_lazy as _
from django.utils.dateformat import format
from django.utils.formats import get_format
import django_tables2 as tables


class ReminderTable(tables.Table):
    id = tables.CheckBoxColumn()
    message = tables.Column(verbose_name=_('message'))
    when = tables.TemplateColumn(verbose_name=_('When'),
                                 template_name='tables/delta_date.html')

    class Meta:
        attrs = {
            'class': 'table table-striped table-condensed',
        }
        empty_text = _('There are no reminders here (yet).')
