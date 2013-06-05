import factory

from django.utils import timezone

from accounts.tests.factories import UserFactory
from reminders.models import Reminder


class ReminderFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Reminder

    user = factory.SubFactory(UserFactory)
    phone = '+33612345678'
    message = factory.Sequence(lambda n: 'Message {0}'.format(n))
    when = timezone.now()
    sent = False
    created_by_ip = '127.0.0.1'
