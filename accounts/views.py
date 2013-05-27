from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from annoying.decorators import render_to
import pymill
from accounts.forms import PasswordResetForm, RegistrationForm
from django.conf import settings
from accounts.models import User


@render_to('register.html')
def register(request):
    form = RegistrationForm(request.POST or None)

    if form.is_valid():
        token = request.POST['paymillToken']
        py = pymill.Pymill(settings.PAYMILL_PRIVATE_KEY)
        client = py.new_client(form.cleaned_data['email'])
        card = py.new_card(token, client.id)
        offer_id = settings.PAYMILL_OFFER_ID
        subscription = py.new_subscription(client.id, offer_id, card.id)

        # Store client_id, card_id, subscription_id
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
