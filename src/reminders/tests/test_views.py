from django.core.urlresolvers import reverse
from django.test import TestCase

from accounts.tests.factories import UserFactory
from reminders.models import Reminder
from reminders.tests.factories import ReminderFactory


class CreateReminderTests(TestCase):
    def test_create_reminder(self):
        self.user = UserFactory(email='toto@tata.com', password='1234')
        self.client.login(username='toto@tata.com', password='1234')
        url = reverse('create_reminder')
        data = {
            'message': 'test',
            'phone': '+33612345678',
            'when': '2020-10-10 10:45',
        }
        self.client.post(url, data, follow=True)
        self.assertEqual(Reminder.objects.all().count(), 1)
        self.assertEqual(Reminder.objects.all()[0].message, 'test')


class ReminderListTests(TestCase):
    def setUp(self):
        self.user = UserFactory(email='toto@tata.com', password='1234')
        self.client.login(username='toto@tata.com', password='1234')
        self.pending_url = reverse('pending_reminders')
        self.sent_url = reverse('sent_reminders')

    def test_pending_reminders(self):
        m1 = ReminderFactory.create(user=self.user)
        m2 = ReminderFactory.create(user=self.user)
        m3 = ReminderFactory.create(user=self.user)

        res = self.client.get(self.pending_url)
        self.assertContains(res, m1.message)
        self.assertContains(res, m2.message)
        self.assertContains(res, m3.message)

    def test_sent_reminders(self):
        m1 = ReminderFactory.create(user=self.user, sent=True)
        m2 = ReminderFactory.create(user=self.user, sent=True)
        m3 = ReminderFactory.create(user=self.user, sent=True)

        res = self.client.get(self.pending_url)
        self.assertNotContains(res, m1.message)
        self.assertNotContains(res, m2.message)
        self.assertNotContains(res, m3.message)

        res = self.client.get(self.sent_url)
        self.assertContains(res, m1.message)
        self.assertContains(res, m2.message)
        self.assertContains(res, m3.message)

    def test_delete_pending_reminders(self):
        m1 = ReminderFactory.create(user=self.user)
        m2 = ReminderFactory.create(user=self.user)
        m3 = ReminderFactory.create(user=self.user)

        res = self.client.post(self.pending_url, {'id': [m1.id, m2.id]},
                               follow=True)
        self.assertNotContains(res, m1.message)
        self.assertNotContains(res, m2.message)
        self.assertContains(res, m3.message)

    def test_delete_sent_reminders(self):
        m1 = ReminderFactory.create(user=self.user, sent=True)
        m2 = ReminderFactory.create(user=self.user, sent=True)
        m3 = ReminderFactory.create(user=self.user, sent=True)

        res = self.client.post(self.sent_url, {'id': [m1.id, m2.id]},
                               follow=True)
        self.assertNotContains(res, m1.message)
        self.assertNotContains(res, m2.message)
        self.assertContains(res, m3.message)
