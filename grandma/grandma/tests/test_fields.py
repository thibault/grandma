import datetime

from django.test import TestCase
from django.forms import ValidationError
from django.utils import timezone

from grandma.fields import PhoneField, DateTimeOrNowField


class PhoneFieldTests(TestCase):

    def test_strip_phone_number(self):
        field = PhoneField()
        self.assertEqual(field.clean('+33 6 12 34 56 78'), '+33612345678')
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

    def test_unicode_values(self):
        field = PhoneField()
        self.assertEqual(field.clean(u'+33 6 12 34 56 78'), '+33612345678')


class DateTimeOrNowFieldTests(TestCase):

    def test_empty_field(self):
        """Test if empty field is now."""
        field = DateTimeOrNowField()
        value = field.clean('')
        now = timezone.now()
        self.assertTrue(value - now < datetime.timedelta(seconds=1))
