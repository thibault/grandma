from annoying.decorators import render_to
from reminders.forms import ReminderForm


@render_to('home.html')
def home(request):
    form = ReminderForm(request.POST or None)
    return {
        'form': form
    }
