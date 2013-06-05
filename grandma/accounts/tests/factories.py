import factory

from accounts.models import User


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    phone = '+33612345678'
    email = 'toto@tata.com'
    is_active = True
