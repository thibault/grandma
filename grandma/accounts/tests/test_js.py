# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from django.utils.translation import activate

from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException


class RegisterFormTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(RegisterFormTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(RegisterFormTests, cls).tearDownClass()

    def setUp(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/account/register/'))
        activate('en')

    def test_payment_fields_have_no_names(self):
        """Payment fields exists, but have no names.

        This is required by the Paymill api, so payment data does not
        crosses our server.

        A field with no name…
        Laaaaaa laaaaa la la la la laaaa…

        """
        self.selenium.find_element_by_class_name('card-number')
        try:
            self.selenium.find_element_by_name('card-number')
            self.fail('The element should have no name')
        except NoSuchElementException:
            pass

    def test_error_message_is_hidden(self):
        error = self.selenium.find_element_by_id('payment-errors')
        self.assertFalse(error.is_displayed())

    def test_missing_card_number_raises_error(self):
        self.selenium.find_element_by_id('submit-btn').click()

        error = self.selenium.find_element_by_id('payment-errors')
        self.assertTrue(error.is_displayed())
        self.assertEqual(error.text, 'Invalid card number')

    def test_missing_cvc_raises_error(self):
        self.selenium.find_element_by_class_name('card-number') \
            .send_keys('4111111111111111')
        self.selenium.find_element_by_id('submit-btn').click()

        error = self.selenium.find_element_by_id('payment-errors')
        self.assertTrue(error.is_displayed())
        self.assertEqual(error.text, 'Invalid validation code')

    def test_missing_expiration_date_raises_error(self):
        self.selenium.find_element_by_class_name('card-number') \
            .send_keys('4111111111111111')
        self.selenium.find_element_by_class_name('card-cvc') \
            .send_keys('123')
        self.selenium.find_element_by_id('submit-btn').click()

        error = self.selenium.find_element_by_id('payment-errors')
        self.assertTrue(error.is_displayed())
        self.assertEqual(error.text, 'Invalid expiration date')
