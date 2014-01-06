import factory

from accounts.models import User


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    phone = '+33612345678'
    email = 'toto@tata.com'
    is_active = True
    password = '1234'

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user
