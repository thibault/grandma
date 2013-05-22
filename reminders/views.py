from annoying.decorators import render_to
from reminders.forms import ReminderForm


@render_to('home.html')
def home(request):
    form = ReminderForm(request.POST or None)
    if form.is_valid():
        reminder = form.save()

    return {
        'form': form
    }

@render_to('reminder_list.html')
def reminder_list(request):
    return {}
