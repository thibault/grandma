from django import forms
from django.utils.translation import ugettext_lazy as _
from reminders.models import Reminder
from accounts.models import mobile_re, User


class BaseReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        exclude = ('sent', 'user')


class AnonymousReminderForm(BaseReminderForm):
    error_messages = {
        'already_exists': _('This phone number is already registered. '
                            'Please, login first'),
    }
    phone = forms.CharField(label=_('Phone:'), max_length=20,
            help_text=_('Use international format, e.g +33612345678'))

    def clean_phone(self):
        """We must check that the user does not already exists."""
        phone = self.cleaned_data.get('phone', None)
        if not phone:
            return u''

        if not mobile_re.match(phone):
            raise forms.ValidationError(_('Use the international format (+336xxxxxxxx). Only french phone are allowed for now.'))

        self.users_cache = User._default_manager.filter(phone__iexact=phone)
        if len(self.users_cache):
            raise forms.ValidationError(self.error_messages['already_exists'])

        return phone

class ReminderForm(BaseReminderForm):
    pass

