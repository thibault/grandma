from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import UNUSABLE_PASSWORD
from accounts.models import User, mobile_re


class RegistrationForm(forms.Form):
    email = forms.EmailField(label=_('Your email'), max_length=254)
    phone = forms.CharField(label=_('Your mobile phone'), max_length=20)

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not mobile_re.match(phone):
            raise forms.ValidationError(_('Use the international format (+336xxxxxxxx). Only french phone are allowed for now.'))

        return phone

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_('This email is already registered'))


class PasswordResetForm(forms.Form):
    error_messages = {
        'unknown': _('This phone number is unknown. '
                     'Are you sure you\'ve registered?'),
        'unusable': _('The user account associated with this phone number '
                      'cannot reset the password.'),
        'invalid': _('Use the international format (+336xxxxxxxx). '
                     'Only french phones are allowed for now.'),
    }
    phone = forms.CharField(label=_('Phone:'), max_length=20)

    def clean_phone(self):
        """Checks the phone number format."""
        phone = self.cleaned_data.get('phone', None)
        self.users_cache = User._default_manager.filter(phone__iexact=phone)
        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        if not any(user.is_active for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        if any((user.password == UNUSABLE_PASSWORD)
                for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unusable'])

        if not mobile_re.match(phone):
            raise forms.ValidationError(self.error_messages['invalid'])

        return phone

    def get_user(self):
        """Get the user corresponding to submitted form.

        The form MUST be valid before calling this.

        """
        return self.users_cache[0]
