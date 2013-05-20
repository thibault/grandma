from django import forms
from reminders.models import Reminder


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder

    def clean_phone(self):
        mobile = self.cleaned_data.get('mobile', None)
        if not mobile:
            return u''

        if not mobile_re.match(mobile):
            raise forms.ValidationError(_('Use the international format (+336xxxxxxxx). Only french mobile are allowed for now.'))

        return mobile
