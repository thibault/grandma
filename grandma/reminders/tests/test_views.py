from django.core.urlresolvers import reverse
from django.test import TestCase


class CreateReminderTests(TestCase):
    def setUp(self):
        self.create_url = reverse('home')

    def post_reminder(self, data):
        return self.client.post(self.create_url, data, follow=True)

    def test_rate_limit(self):
        """Anonymous user cannot create more than 3 reminders at once."""
        reminder_data = {
            'message': 'test',
            'phone': '+33612345678',
            'when': '2020-10-10 19:20',
        }

        # First reminder, everything's ok
        res = self.post_reminder(reminder_data)
        self.assertContains(res, 'Sleep tight')

        # Second reminder, ok
        reminder_data.update({'message': 'test2'})
        res = self.post_reminder(reminder_data)
        self.assertContains(res, 'Sleep tight')

        # Third, still ok
        reminder_data.update({'message': 'test3'})
        res = self.post_reminder(reminder_data)
        self.assertContains(res, 'Sleep tight')

        # Fourth, forbidden
        reminder_data.update({'message': 'test4'})
        res = self.post_reminder(reminder_data)
        self.assertNotContains(res, 'Sleep tight')
