from .nexmomessage import NexmoMessage
from django.conf import settings


def send_message(to, message):
    """Shortcut to send a sms using nexmo api."""
    params = {
        'username': settings.NEXMO_USERNAME,
        'password': settings.NEXMO_PASSWORD,
        'type': 'unicode',
        'from': settings.NEXMO_FROM,
        'to': to,
        'text': message.encode('utf-8'),
    }
    sms = NexmoMessage(params)
    response = sms.send_request()
    return response
