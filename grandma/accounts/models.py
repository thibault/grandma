import hashlib
import random

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        now = timezone.now()

        if not password:
            password = self.make_random_password(length=20)

        user = self.model(phone=phone, email=email, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password, **extra_fields):
        u = self.create_user(email, phone, password, **extra_fields)
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
    activation_key = models.CharField(_('activation key'), max_length=40,
                                      null=True, blank=True)
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    is_valid = models.BooleanField(
        _('valid'), default=False,
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

    def reset_activation_key(self):
        """Generates a new activation key."""
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        self.activation_key = hashlib.sha1(salt + self.email).hexdigest()
        self.save()

    def send_activation_key(self):
        """Sends a 'forgotten password' link to user."""
        context = {'activation_key': self.activation_key,
                   'site': Site.objects.get_current()}
        subject = render_to_string('registration/activation_email_subject.txt',
                                   context)
        subject = ''.join(subject.splitlines())
        message = render_to_string('registration/activation_email.txt',
                                   context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])

    # Those methods are required for admin access
    @property
    def is_staff(self):
        return self.is_superuser

    def has_perm(self, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
