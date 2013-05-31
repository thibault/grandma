from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from annoying.decorators import render_to
from contacts.models import Contact
from contacts.tables import ContactTable
from contacts.forms import ContactForm


@render_to('contact_list.html')
def contact_list(request):

    # Contact creation
    form = ContactForm(request.POST or None)
    if '_create' in request.POST and form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()
        msg = _('Your new contact was created')
        messages.success(request, msg)
        return redirect('contact_list')

    # Contact deletion
    qs = Contact.objects.filter(user=request.user)
    if '_delete' in request.POST:
        ids = request.POST.getlist('id')
        qs.filter(id__in=ids).delete()
        msg = _('Selected reminders were deleted')
        messages.success(request, msg)
        return redirect('contact_list')

    table = ContactTable(qs)
    return {
        'table': table,
        'form': form,
    }
