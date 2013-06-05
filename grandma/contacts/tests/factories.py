import factory

from accounts.tests.factories import UserFactory
from contacts.models import Contact


class ContactFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Contact

    user = factory.SubFactory(UserFactory)
    first_name = factory.Sequence(lambda n: 'John{0}'.format(n))
    last_name = factory.Sequence(lambda n: 'Doe{0}'.format(n))
    mobile = '+33612345678'
