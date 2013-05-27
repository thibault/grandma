from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from accounts.models import User
from reminders.models import Reminder
from reminders.forms import ReminderForm
from reminders.tables import ReminderTable


@render_to('create_reminder.html')
def create_reminder(request):
    ip_address = request.META['REMOTE_ADDR']
    form = ReminderForm(request.POST or None, ip_address=ip_address)

    if form.is_valid():
        reminder = form.save(commit=False)
        reminder.user = request.user if request.user.is_authenticated() else None
        reminder.created_by_ip = ip_address
        reminder.save()

        message = _('Your reminder was saved successfully. Sleep tight.')
        messages.success(request, message)

        if request.user.is_authenticated():
            next_url = 'reminder_list'
        else:
            next_url = 'create_reminder'
        return redirect(next_url)

    return {
        'form': form
    }

@render_to('reminder_list.html')
@login_required
def reminder_list(request):
    qs = Reminder.objects.filter(user=request.user) \
            .filter(sent=False) \
            .order_by('when')

    # Delete selected reminders
    if request.method == 'POST':
        ids = request.POST.getlist('id')
        qs.filter(id__in=ids).delete()
        msg = _('Selected reminders were deleted')
        messages.success(request, msg)
        return redirect('reminder_list')

    table = ReminderTable(qs)
    return {
        'table': table,
    }
