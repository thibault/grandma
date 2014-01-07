from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from django.conf import settings

from accounts.tests.factories import UserFactory
from reminders.forms import ReminderForm
from reminders.tests.factories import ReminderFactory


class ReminderFormTests(TestCase):
    def setUp(self):
        self.data = {'phone': '+33612345678',
                     'message': 'My message',
                     'when': timezone.now()}

    def test_anonymous_form_is_valid(self):
        form = ReminderForm(self.data, ip_address='127.0.0.1',
                            user=AnonymousUser())
        self.assertFalse(form.is_valid())

    def test_monthly_rate_limit(self):
        user = UserFactory()

        for i in xrange(settings.MONTHY_REMINDER_LIMIT - 1):
            ReminderFactory.create(user=user)

        form = ReminderForm(self.data,
                            ip_address='127.0.0.1',
                            user=user)
        self.assertTrue(form.is_valid())

        ReminderFactory.create(user=user)
        form = ReminderForm(self.data,
                            ip_address='127.0.0.1',
                            user=user)
        self.assertFalse(form.is_valid())
