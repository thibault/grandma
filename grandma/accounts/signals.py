from django.contrib.auth.signals import user_logged_in


def user_first_login(sender, user, request, **kwargs):
    """Set account as valid on first login."""
    if not user.is_valid:
        user.is_valid = True
        user.save()
user_logged_in.connect(user_first_login)
