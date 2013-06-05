from django.test import TestCase

from accounts.forms import RegistrationForm, PasswordResetForm
from accounts.tests.factories import UserFactory


class RegistrationFormTests(TestCase):
    def test_form_is_valid(self):
        form = RegistrationForm({'email': 'toto@tata.com',
                                 'phone': '+33612345678'})
        self.assertTrue(form.is_valid())

    def test_user_already_exists(self):
        UserFactory.create(email='toto@tata.com')
        form = RegistrationForm({'email': 'toto@tata.com',
                                 'phone': '+33612345678'})
        self.assertFalse(form.is_valid())
        self.assertTrue('email' in form.errors)


class PasswordResetFormTests(TestCase):
    def test_clean(self):
        form = PasswordResetForm({'password1': 'toto',
                                  'password2': 'toto'})
        self.assertTrue(form.is_valid())

    def test_different_password(self):
        form = PasswordResetForm({'password1': 'toto',
                                  'password2': 'tata'})
        self.assertFalse(form.is_valid())
