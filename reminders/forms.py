from django import forms
from django.utils.translation import ugettext_lazy as _
from reminders.models import Reminder
from accounts.models import mobile_re


class ReminderForm(forms.ModelForm):

    class Meta:
        model = Reminder
        exclude = ('sent',)

    def clean_phone(self):
        """Checks the phone number format."""
        phone = self.cleaned_data.get('phone', None)
        if not phone:
            return u''

        if not mobile_re.match(phone):
            raise forms.ValidationError(_('Use the international format (+336xxxxxxxx). Only french phone are allowed for now.'))

        return phone
