from annoying.decorators import render_to
from contacts.models import Contact
from contacts.tables import ContactTable


@render_to('contact_list.html')
def contact_list(request):
    qs = Contact.objects.filter(user=request.user)
    table = ContactTable(qs)
    return {
        'table': table,
    }
