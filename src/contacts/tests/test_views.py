from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.translation import activate

from accounts.tests.factories import UserFactory
from contacts.tests.factories import ContactFactory


class ContactViewsTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.client.login(username='toto@tata.com', password='1234')
        self.url = reverse('contact_list')
        activate('en')

    def test_empty_contact_list(self):
        res = self.client.get(self.url)
        self.assertContains(res, 'There are no contacts here')

    def test_contact_list(self):
        ContactFactory.create(user=self.user)
        ContactFactory.create(user=self.user)
        ContactFactory.create(user=self.user)

        res = self.client.get(self.url)
        self.assertContains(res, 'John1 Doe1')
        self.assertContains(res, 'John2 Doe2')
        self.assertContains(res, 'John3 Doe3')

    def test_delete_contacts(self):
        c1 = ContactFactory.create(user=self.user)
        c2 = ContactFactory.create(user=self.user)
        c3 = ContactFactory.create(user=self.user)

        res = self.client.post(self.url, {'_delete': 'delete',
                                          'id': [c1.id, c2.id]},
                               follow=True)

        self.assertNotContains(res, c1.full_name)
        self.assertNotContains(res, c2.full_name)
        self.assertContains(res, c3.full_name)
        self.assertContains(res, 'Selected reminders were deleted')

    def test_create_contact(self):
        res = self.client.post(self.url, {'_create': 'create',
                                          'first_name': 'Harry',
                                          'last_name': 'Cotta',
                                          'mobile': '+33612345678'},
                               follow=True)
        self.assertContains(res, 'Your new contact was created')
        self.assertContains(res, 'Harry Cotta')

    def test_create_invalid_contact(self):
        res = self.client.post(self.url, {'_create': 'create',
                                          'first_name': 'Harry',
                                          'last_name': 'Cotta',
                                          'mobile': ''},
                               follow=True)
        self.assertNotContains(res, 'Your new contact was created')
        self.assertContains(res, 'This field is required')
