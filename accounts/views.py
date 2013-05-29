import logging
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from annoying.decorators import render_to
import pymill
from accounts.forms import PasswordResetForm, RegistrationForm
from django.conf import settings
from accounts.models import User


logger = logging.getLogger(__name__)

@render_to('register.html')
def register(request):
    form = RegistrationForm(request.POST or None)

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
        except Exception as e:
            logger.error('Payment error token:%(token)s client:%(client)s '
                         'card:%(card)s' % {
                             'token': token,
                             'client': client.id if client else 'NC',
                             'card': card.id if card else 'NC'})
            message = _('There was a problem processing your credit card. '
                        'Your account was not created. Please, try again in '
                        'a few minutes or with different payment informations.')
            messages.error(request, message)
            return { 'form': form }

        # So payment was created, and form data is valid
        # Let's create this user account
        data = form.cleaned_data
        user = User.objects.create_user(data['phone'], data['email'],
                                        paymill_client_id=client.id,
                                        paymill_card_id=card.id,
                                        paymill_subscription_id=subscription.id)
        user.reset_and_send_password()
        message = _('Congratulations! Your account was created. We will send '
                    'your password by sms.')
        messages.success(request, message)
        return redirect('login')

    return {
        'form': form,
        'PAYMILL_PUBLIC_KEY': settings.PAYMILL_PUBLIC_KEY,
    }

@render_to('password_reset.html')
def password_reset(request):
    """Login view using sms code."""
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        user = form.get_user()
        user.reset_and_send_password()
        messages.success(request, _('A new password was sent. It should be there'
                                    ' in less than a minute. Enjoy those few '
                                    'seconds of calm and relaxation.'))
        return redirect('login')

    return {
        'form': form,
    }
