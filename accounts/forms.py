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


class PasswordRequestForm(forms.Form):
    error_messages = {
        'unknown': _('This email is unknown. '
                     'Are you sure you\'ve registered?'),
        'unusable': _('The user account associated with this email '
                      'cannot reset the password.'),
    }
    email = forms.EmailField(label=_('Your email'), max_length=254)

    def clean_email(self):
        """Checks the email number format."""
        email = self.cleaned_data.get('email', None)
        self.users_cache = User._default_manager.filter(email__iexact=email)

        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])

        if not any(user.is_active for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])

        if any((user.password == UNUSABLE_PASSWORD)
                for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unusable'])

        return email

    def get_user(self):
        """Get the user corresponding to submitted form.

        The form MUST be valid before calling this.

        """
        return self.users_cache[0]

class PasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_("Password (again)"))


    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data
