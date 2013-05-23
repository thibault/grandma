from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from annoying.decorators import render_to
from accounts.forms import PasswordResetForm


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
