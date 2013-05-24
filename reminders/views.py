from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from annoying.decorators import render_to
from accounts.models import User
from reminders.models import Reminder
from reminders.forms import ReminderForm, AnonymousReminderForm
from reminders.tables import ReminderTable


@render_to('home.html')
def home(request):

    # If user is already authenticated, don't even ask phone number
    if request.user.is_authenticated():
        form_class = ReminderForm
    else:
        form_class = AnonymousReminderForm
    form = form_class(request.POST or None)

    if form.is_valid():
        reminder = form.save(commit=False)

        # if user is logged in, just create the reminder and redirect
        # else, we need to create it's account first
        if request.user.is_authenticated():
            user = request.user
            message = _('Your reminder was saved successfully. Sleep tight.')
            next_url = 'reminder_list'
        else:
            phone = form.cleaned_data['phone']
            user = User.objects.create_user(phone)
            user.reset_and_send_password()
            message = _('We must validate that you are the owner of this phone '
                        'number. Please, type in the four digits code you '
                        'have received (or will in a few seconds). Don\'t '
                        'worry, we will only ask this once.')
            next_url = 'login'

        reminder.user = user
        reminder.save()

        messages.success(request, message)
        return redirect(next_url)

    return {
        'form': form
    }

@render_to('reminder_list.html')
def reminder_list(request):
    qs = Reminder.objects.filter(user=request.user) \
            .filter(sent=False) \
            .order_by('when')
    table = ReminderTable(qs)

    return {
        'table': table,
    }
