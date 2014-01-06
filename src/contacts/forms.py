from django import forms
from django.utils.translation import ugettext_lazy as _

from grandma.fields import PhoneField
from contacts.models import Contact


class ContactForm(forms.ModelForm):
    mobile = PhoneField(label=_('Phone'), required=True)

    class Meta:
        model = Contact
        exclude = ('user',)
