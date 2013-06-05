from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from reminders.models import Reminder
from reminders.forms import ReminderForm
from reminders.tables import ReminderTable


@render_to('create_reminder.html')
@login_required
def create_reminder(request):
    return reminder_form_view(request, next_url='pending_reminders')


def reminder_form_view(request, next_url):
    """Reminder form processing view."""
    ip_address = request.META['REMOTE_ADDR']
    form = ReminderForm(request.POST or None, user=request.user,
                        ip_address=ip_address)

    if form.is_valid():
        reminder = form.save(commit=False)
        reminder.user = request.user if request.user.is_authenticated() else None
        reminder.created_by_ip = ip_address
        reminder.save()

        message = _('Your reminder was saved successfully. Sleep tight.')
        messages.success(request, message)

        return redirect(next_url)

    return {
        'form': form
    }


@render_to('reminder_list.html')
@login_required
def pending_reminders(request):
    qs = Reminder.objects.filter(user=request.user) \
        .filter(sent=False) \
        .order_by('when')

    return reminder_list_view(request, qs)


@render_to('reminder_list.html')
@login_required
def sent_reminders(request):
    qs = Reminder.objects.filter(user=request.user) \
        .filter(sent=True) \
        .order_by('when')

    return reminder_list_view(request, qs)


def reminder_list_view(request, qs):
    """Generic reminder list view."""
    # Delete selected reminders
    if request.method == 'POST':
        ids = request.POST.getlist('id')
        qs.filter(id__in=ids).delete()
        msg = _('Selected reminders were deleted')
        messages.success(request, msg)
        return redirect('pending_reminders')

    table = ReminderTable(qs)
    return {
        'table': table,
    }
