from annoying.decorators import render_to


@render_to('send_password.html')
def send_password(self, request):
    """Login view using sms code."""
    return {}


