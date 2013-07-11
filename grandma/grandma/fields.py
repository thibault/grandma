import re

from django import forms
from django.utils.translation import ugettext as _


mobile_re = re.compile(r'^\+336\d{8}$')


class PhoneField(forms.CharField):
    """Validate international phone fields."""

    default_error_messages = {
        'invalid': _('Use international format e.g +336xxxxxxxx. '
                     'Only french numbers are allowed (for now).'),
    }
    help_text = _('Use international format, e.g +336xxxxxxxx')
    placeholder = '+336'

    def __init__(self, max_length=20, *args, **kwargs):
        super(PhoneField, self).__init__(
            max_length, help_text=self.help_text, *args, **kwargs)

    def clean(self, value):
        super(PhoneField, self).clean(value)

        if not mobile_re.match(value):
            raise forms.ValidationError(self.error_messages['invalid'])

        return value

    def widget_attrs(self, widget):
        attrs = super(PhoneField, self).widget_attrs(widget)
        attrs.update({'placeholder': self.placeholder})
        return attrs
