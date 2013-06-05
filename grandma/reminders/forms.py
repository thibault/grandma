import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from grandma.fields import PhoneField
from reminders.models import Reminder


class ReminderForm(forms.ModelForm):
    phone = PhoneField(required=True,
                       label=_('Recipient mobile:'),
                       widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    when = forms.DateTimeField(required=True,
                               label=_('Date and time:'))
    message = forms.CharField(label=_('Your message:'),
                              widget=forms.Textarea(attrs={'rows': 2}))

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

        # Only anonymous users have a rate limit
        if not self.user.is_authenticated():
            today = datetime.date.today()
            reminders = Reminder.objects.filter(created_by_ip=self.ip_address) \
                .filter(created_at__year=today.year) \
                .filter(created_at__month=today.month) \
                .filter(created_at__day=today.day)

            if reminders.count() >= Reminder.ANONYMOUS_DAILY_LIMIT:
                raise forms.ValidationError(_('You have exceded the numbers of free '
                                              'reminders a day. Subscribe to an '
                                              'account to create more.'))

        return data
