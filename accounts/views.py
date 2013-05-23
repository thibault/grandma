from annoying.decorators import render_to


@render_to('send_password.html')
def password_reset(self, request):
    """Login view using sms code."""
    return {}


