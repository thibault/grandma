from django import forms
from django.utils.translation import ugettext_lazy as _
from reminders.models import Reminder
from accounts.models import mobile_re, User


class BaseReminderForm(forms.ModelForm):
    phone = forms.CharField(label=_('Phone:'), max_length=20,
            help_text=_('Use international format, e.g +33612345678'))
    class Meta:
        model = Reminder

    def clean_phone(self):
        """Checks the phone number format."""
        phone = self.cleaned_data.get('phone', None)
        if not phone:
            return u''

        if not mobile_re.match(phone):
            raise forms.ValidationError(_('Use the international format (+336xxxxxxxx). Only french phone are allowed for now.'))

        return phone


class AnonymousReminderForm(BaseReminderForm):
    error_messages = {
        'already_exists': _('This phone number is already registered. '
                            'Please, login first'),
    }
    class Meta(BaseReminderForm.Meta):
        exclude = ('sent', 'user')

    def clean_phone(self):
        """We must check that the user does not already exists."""
        phone = super(AnonymousReminderForm, self).clean_phone()
        self.users_cache = User._default_manager.filter(phone__iexact=phone)
        if len(self.users_cache):
            raise forms.ValidationError(self.error_messages['already_exists'])

        return phone

class ReminderForm(BaseReminderForm):
    class Meta(BaseReminderForm.Meta):
        exclude = ('sent', 'user', 'phone')

    def __init__(self, *args, **kwargs):
        super(ReminderForm, self).__init__(*args, **kwargs)
        # The exclude field won't work for phone
        del self.fields['phone']


