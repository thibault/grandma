from annoying.decorators import render_to
from reminders.forms import ReminderForm, AnonymousReminderForm


@render_to('home.html')
def home(request):
    if request.user.is_authenticated():
        form_class = ReminderForm
    else:
        form_class = AnonymousReminderForm
    form = form_class(request.POST or None)

    if form.is_valid():
        reminder = form.save()

    return {
        'form': form
    }

@render_to('reminder_list.html')
def reminder_list(request):
    reminders = request.user.reminders.all()

    return {
        'reminders': reminders,
    }
