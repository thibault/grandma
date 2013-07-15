from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.translation import activate
from django.contrib.auth import authenticate

from mock import patch, Mock, MagicMock

from accounts.models import User
from accounts.tests.factories import UserFactory


class Empty:
    """Empty object to use as return data in the Paymill mock."""
    id = 'value'
mock_data = Empty()

paymill_register_mock = Mock()
instance = paymill_register_mock.return_value
instance.new_client.return_value = mock_data
instance.new_card.return_value = mock_data
instance.new_subscription.return_value = mock_data


class RegisterTests(TestCase):
    """Test registering user, mocking the paymill lib."""

    def setUp(self):
        self.url = reverse('register')
        self.data = {
            'email': 'toto@tata.com',
            'phone': '+33612345678',
            'paymillToken': 'random_token',
        }

    @patch('pymill.Pymill', paymill_register_mock)
    def test_signing_up_creates_new_account(self):
        self.assertEqual(User.objects.all().count(), 0)
        res = self.client.post(self.url, self.data)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(User.objects.all()[0].email, self.data['email'])
        self.assertRedirects(res, reverse('login'))


class PasswordsTests(TestCase):
    """Testing the password reset feature."""

    def setUp(self):
        self.reset_url = reverse('password_reset')
        self.confirm_url = reverse('password_reset_confirm', args=['random_key'])
        activate('en')

    def test_password_reset(self):
        UserFactory.create(email='toto@tata.com')
        res = self.client.post(self.reset_url, {'email': 'toto@tata.com'},
                               follow=True)
        self.assertContains(res, 'A new password was sent')

    def test_password_reset_wrong_address(self):
        res = self.client.post(self.reset_url, {'email': 'titi@tutu.com'},
                               follow=True)
        self.assertNotContains(res, 'A new password was sent')
        self.assertContains(res, 'This email is unknown')

    def test_reset_confirm_wrong_key(self):
        res = self.client.get(self.confirm_url)
        self.assertEqual(res.status_code, 404)

    def test_reset_confirm_show_form(self):
        UserFactory.create(activation_key='random_key')
        res = self.client.get(self.confirm_url)
        self.assertEqual(res.status_code, 200)

    def test_reset_different_passwords(self):
        UserFactory.create(activation_key='random_key')
        res = self.client.post(self.confirm_url, {'password1': 'toto',
                                                  'password2': 'tata'})
        self.assertContains(res, 'The two password fields didn&#39;t match')

    def test_reset_password(self):
        UserFactory.create(email='toto@tata.com', activation_key='random_key')
        res = self.client.post(self.confirm_url, {'password1': 'toto',
                                                  'password2': 'toto'},
                               follow=True)
        self.assertContains(res, 'Your new password was saved successfully')
        user = authenticate(username='toto@tata.com', password='toto')
        self.assertIsNotNone(user)


subscription_mock = MagicMock(name='Subscription')
subscription_mock.return_value.next_capture_at = 1376471863  # Aug 14 2013


class MyAccountTests(TestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.client.login(username='toto@tata.com', password='1234')
        self.account_url = reverse('my_account')
        activate('en')

    @patch('pymill.Pymill', MagicMock())
    @patch('pymill.Subscription', subscription_mock)
    def test_password_reset(self):
        res = self.client.get(self.account_url)
        self.assertContains(res, 'Next billing date: Aug. 14, 2013')
