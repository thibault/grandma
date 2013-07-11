import logging

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect, get_object_or_404
from annoying.decorators import render_to

from billing.models import Plan
from accounts.forms import PasswordRequestForm, PasswordResetForm, RegistrationForm
from accounts.models import User


logger = logging.getLogger(__name__)


@render_to('my_account.html')
def my_account(request):
    plans = Plan.objects.order_by('-price').all()
    return {
        'plans': plans,
    }


@render_to('register.html')
def register(request):
    form = RegistrationForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(data['email'], data['phone'],
                                        is_active=False)
        user.reset_activation_key()
        user.send_activation_key()
        message = _('Congratulations! Your account was created. You will receive '
                    'your activation email in  a few seconds.')
        messages.success(request, message)
        return redirect('login')

    return {
        'form': form,
    }


@render_to('password_reset.html')
def password_reset(request):
    """Login view using sms code."""
    form = PasswordRequestForm(request.POST or None)
    if form.is_valid():
        user = form.get_user()
        user.reset_activation_key()
        user.send_activation_key()
        messages.success(request, _('A new password was sent. It should be there'
                                    ' in less than a minute. Enjoy those few '
                                    'seconds of calm and relaxation.'))
        return redirect('login')

    return {
        'form': form,
    }


@render_to('password_reset_confirm.html')
def password_reset_confirm(request, activation_key):
    user = get_object_or_404(User, activation_key=activation_key)
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data['password1']
        user.set_password(password)
        user.activation_key = None
        user.is_active = True
        user.save()
        msg = _('Your new password was saved successfully. You can now login '
                'on your account.')
        messages.success(request, msg)
        return redirect('login')

    return {
        'form': form,
    }
