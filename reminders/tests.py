from django.test import TestCase


class CreateReminderTests(TestCase):
    def setUp(self):
        self.create_url = '/reminders/create/'
        self.reminder_data = {
                'message': 'test',
                'phone': '+33612345678',
                'when': '2020-10-10 19:20',
        }

    def create_reminder(self, data):
        return self.client.post(self.create_url, data, follow=True)

    def test_reminder_duplicate(self):
        """User cannot create two identical reminders."""
        res = self.create_reminder(self.reminder_data)
        self.assertContains(res, 'Sleep tight')

        res = self.create_reminder(self.reminder_data)
        self.assertNotContains(res, 'Sleep tight')
        self.assertContains(res, 'already exists')

    def test_rate_limit(self):
        """Anonymous user cannot create more than 3 reminders at once."""
        res = self.create_reminder(self.reminder_data)
        self.assertContains(res, 'Sleep tight')

        self.reminder_data.update({'message': 'test2'})
        res = self.create_reminder(self.reminder_data)
        self.assertContains(res, 'Sleep tight')

        self.reminder_data.update({'message': 'test3'})
        res = self.create_reminder(self.reminder_data)
        self.assertContains(res, 'Sleep tight')

        self.reminder_data.update({'message': 'test4'})
        res = self.create_reminder(self.reminder_data)
        self.assertNotContains(res, 'Sleep tight')



