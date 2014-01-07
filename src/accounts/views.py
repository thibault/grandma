import logging
import pymill
from datetime import datetime

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect, get_object_or_404
from annoying.decorators import render_to
from django.conf import settings
from django.contrib.auth.decorators import login_required

from reminders.models import Reminder
from accounts.forms import PasswordRequestForm, PasswordResetForm, RegistrationForm
from accounts.models import User


logger = logging.getLogger(__name__)


@render_to('my_account.html')
@login_required
def my_account(request):
    next_charge = ''
    try:
        py = pymill.Pymill(settings.PAYMILL_PRIVATE_KEY)
        py_client = py.get_client(request.user.paymill_client_id)
        py_subscription = pymill.Subscription(**py_client.subscription[0])
        next_charge = datetime.fromtimestamp(py_subscription.next_capture_at)
    except:
        # In case of error, we'll just display an error message
        # So do nothing here
        pass

    qs = Reminder.objects.filter(user=request.user)
    total_count = qs.filter(sent=True).count()
    upcoming_count = qs.filter(sent=False).count()

    return {
        'next_charge': next_charge,
        'total_count': total_count,
        'upcoming_count': upcoming_count,
    }


@render_to('register.html')
def register(request):
    form = RegistrationForm(request.POST or None)

    if form.is_valid():

        data = form.cleaned_data
        user = User.objects.create_user(data['email'], data['phone'],
                                        is_active=False)
        logger.warning('New user created: %s' % user.email)
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


@render_to('payment.html')
def payment(request):
    form = RegistrationForm(request.POST or None)
    context = {
        'form': form,
        'PAYMILL_PUBLIC_KEY': settings.PAYMILL_PUBLIC_KEY,
    }

    if form.is_valid():
        token = request.POST['paymillToken']

        try:
            # Let's request a payment with our provider
            client = card = subscription = None
            py = pymill.Pymill(settings.PAYMILL_PRIVATE_KEY)
            client = py.new_client(form.cleaned_data['email'])
            card = py.new_card(token, client.id)
            offer_id = settings.PAYMILL_OFFER_ID
            subscription = py.new_subscription(client.id, offer_id, card.id)
        except Exception:
            logger.error('Payment error token:%(token)s client:%(client)s '
                         'card:%(card)s' % {
                             'token': token,
                             'client': client.id if client else 'NC',
                             'card': card.id if card else 'NC'})
            message = _('There was a problem processing your credit card. '
                        'Your account was not created. Please, try again in '
                        'a few minutes or with different payment informations.')
            messages.error(request, message)
            return context

        # So payment was created, and form data is valid
        # Let's create this user account
        data = form.cleaned_data
        user = User.objects.create_user(data['email'], data['phone'],
                                        is_active=False,
                                        paymill_client_id=client.id,
                                        paymill_card_id=card.id,
                                        paymill_subscription_id=subscription.id)
        logger.warning('New user created: %s' % user.email)
        user.reset_activation_key()
        user.send_activation_key()
        message = _('Congratulations! Your account was created. You will receive '
                    'your activation email in  a few seconds.')
        messages.success(request, message)
        return redirect('login')

    return context
