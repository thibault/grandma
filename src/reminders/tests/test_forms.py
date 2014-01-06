from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser

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
        self.assertTrue(form.is_valid())

    def test_anonymous_rate_limit(self):
        ReminderFactory.create(user=None)
        ReminderFactory.create(user=None)
        ReminderFactory.create(user=None)

        form = ReminderForm(self.data, ip_address='127.0.0.1',
                            user=AnonymousUser())
        self.assertFalse(form.is_valid())
