from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Person, EmailTemplate

@staff_member_required
def send_templated_email(request, email_template_id, person_id=None):
    email_template = EmailTemplate.objects.get(pk = email_template_id)
    if person_id:
        recipient = Person.objects.get(pk=person_id)
    else:
        recipient = None
    count = email_template.send(request.user, recipient)
    if count == 1:
        messages.success(request, 'Sent "{}" to "{}'.format(email_template, recipient))
    elif count == 0:
        messages.error(request, 'Failed to Send "{}" to "{}'.format(email_template, recipient))
    else:
        messages.info(request, "sending {} to {} recipients".format(email_template, count))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

