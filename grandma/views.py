from annoying.decorators import render_to
from reminders.views import reminder_form_view


@render_to('home.html')
def home(request):
    return reminder_form_view(request, next_url='home')
