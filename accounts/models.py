from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        now = timezone.now()

        if not password:
            password = self.make_random_password(length=4,
                                                 allowed_chars='0123456789')
        user = self.model(phone=phone, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        u = self.create_user(phone, password, **extra_fields)
        u.is_staff = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    """Actual class for user accounts."""
    objects = UserManager()
    phone = models.CharField(_('Mobile'), max_length=20, unique=True,
                             help_text=_('Use international format, e.g +33612345678'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone
