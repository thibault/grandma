import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from reminders.models import Reminder
from accounts.models import mobile_re, User


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ('message', 'when', 'phone')

    def __init__(self, *args, **kwargs):
        self.ip_address = kwargs.pop('ip_address')
        super(ReminderForm, self).__init__(*args, **kwargs)

    def clean_phone(self):
        """We must check that the user does not already exists."""
        phone = self.cleaned_data.get('phone', None)

        if not mobile_re.match(phone):
            raise forms.ValidationError(_('Use the international format (+336xxxxxxxx). Only french phone are allowed for now.'))

        return phone

    def clean(self):
        """Makes sure we did not overcome the rate limit."""
        data = self.cleaned_data
        if self.errors:
            return data

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

