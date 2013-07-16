from django.test import TestCase
from django.forms import ValidationError

from grandma.fields import PhoneField


class PhoneFieldTests(TestCase):

    def test_strip_phone_number(self):
        field = PhoneField()
        self.assertEqual(field.clean('+33 6 12 34 56 78'), '+33612345678')
        self.assertEqual(field.clean('+1-234-567-8901'), '+12345678901')
        self.assertEqual(field.clean('+1-234-567-8901'), '+12345678901')
        self.assertEqual(field.clean('+1 (234) 567-8901'), '+12345678901')
        self.assertEqual(field.clean('+1.234.567.8901'), '+12345678901')
        self.assertEqual(field.clean('+1/234/567/8901'), '+12345678901')
        self.assertEqual(field.clean('+12345678901'), '+12345678901')

    def test_invalid_phone_numbers(self):
        field = PhoneField()

        with self.assertRaises(ValidationError):
            field.clean('06 12 34 56 78')

        with self.assertRaises(ValidationError):
            field.clean('04 12 34 56 78')
