from django.test import TestCase

from accounts.tests.factories import UserFactory


class UserTests(TestCase):
    def test_reset_activation_key(self):
        user = UserFactory.create()
        self.assertIsNone(user.activation_key)
        user.reset_activation_key()
