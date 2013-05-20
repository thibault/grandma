import re
from django import forms
from django.utils.translation import ugettext_lazy as _
from reminders.models import Reminder


mobile_re = re.compile(r'^\+336\d{8}$')

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', None)
        if not phone:
            return u''

        if not mobile_re.match(phone):
            raise forms.ValidationError(_('Use the international format (+336xxxxxxxx). Only french phone are allowed for now.'))

        return phone
