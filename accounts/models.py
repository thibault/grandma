import re
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from messages.models import send_message


# Regular expression to validate phone numbers
mobile_re = re.compile(r'^\+336\d{8}$')


class UserManager(BaseUserManager):
    def create_user(self, phone, email, password=None, **extra_fields):
        now = timezone.now()

        if not password:
            password = self.make_random_password(length=4,
                                                 allowed_chars='0123456789')
        user = self.model(phone=phone, email=email, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password, **extra_fields):
        u = self.create_user(phone, email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    """Actual class for user accounts."""
    objects = UserManager()
    phone = models.CharField(_('Mobile'), max_length=20,
                             help_text=_('Use international format, e.g +33612345678'))
    email = models.EmailField(_('email address'), unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True,
            help_text=_('Designates whether this user should be treated as '
                        'active. Unselect this instead of deleting accounts.'))
    is_valid = models.BooleanField(_('valid'), default=False,
            help_text=_('Designates whether this user has confirmed his '
                        'phone number.'))

    # Paymill subscription data
    paymill_client_id = models.CharField(max_length=100, null=True, blank=True)
    paymill_card_id = models.CharField(max_length=100, null=True, blank=True)
    paymill_subscription_id = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone

    def reset_and_send_password(self):
        """Changes the password, and send a new one."""
        password = User.objects.make_random_password(length=4,
                allowed_chars='0123456789')
        self.set_password(password)
        self.save()

        send_message(self.phone, _('Your new password is %(pwd)s') % {
                'pwd': password
        })
