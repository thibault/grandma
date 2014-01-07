import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from grandma.fields import PhoneField, DateTimeOrNowField
from reminders.models import Reminder


class ReminderForm(forms.ModelForm):
    phone = PhoneField(required=True,
                       label=_('Recipient cell:'),
                       widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    when = DateTimeOrNowField(label=_('Date and time:'))
    message = forms.CharField(label=_('Your message:'),
                              widget=forms.Textarea(attrs={'rows': 2}),
                              help_text=_('Don\'t forget to sign your message'))

    class Meta:
        model = Reminder
        fields = ('phone', 'when', 'message')

    def __init__(self, *args, **kwargs):
        self.ip_address = kwargs.pop('ip_address')
        self.user = kwargs.pop('user')
        super(ReminderForm, self).__init__(*args, **kwargs)

    def clean(self):
        """Makes sure we did not overcome the rate limit."""
        data = self.cleaned_data
        if self.errors:
            return data

        # Anonymous users are no longer allowed
        if not self.user.is_authenticated():
            raise forms.ValidationError(_('Oops, only authenticated users can'
                                          ' send reminders.'))

        # Check rate limit
        today = datetime.date.today()
        reminders = Reminder.objects.filter(user=self.user) \
            .filter(created_at__year=today.year) \
            .filter(created_at__month=today.month) \

        if reminders.count() >= settings.MONTHY_REMINDER_LIMIT:
            raise forms.ValidationError(_('You have exceeded the monthly limit '
                                          'of reminders for your account'))

        return data
