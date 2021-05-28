from django.shortcuts import render, redirect

# Create your views here.
from .models import ContactDetails
from .forms import ContactForm, NoteForm
# from django.core.mail import send_mail as sm
from django.core.mail import BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from store.models import Contact, Note
from django.forms.formsets import formset_factory

def send_mail(request):
    #envoyer un email
    contactdetails = ContactDetails.objects.last()
    template = 'contact/contact.html'

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        note_form = NoteForm(request.POST)
        
        if all([contact_form.is_valid(), note_form.is_valid()]):
            
            email = contact_form.cleaned_data['email']
            name = contact_form.cleaned_data['name']
            message = note_form.cleaned_data['notes']

            try:
                with transaction.atomic():
                    # sm(
                    # 'Demande de {} {} adresse email: {}'.format(prenom, nom, email), #sujet
                    # message, #message
                    # email, #de l'adresse email
                    # ['traveleagle29@gmail.com'], #envoyer un email
                    # fail_silently=False,
                    # )
                
                    contact = Contact.objects.filter(email=email)
                    if not contact.exists():
                        # Si le contact n'existe pas, créer un nouveau.
                        contact = Contact.objects.create(
                            email=email,
                            name=name,
                           
                        )
                    else:
                        contact = contact.first() # Si le contact existe, prends le premier

                    note = Note.objects.create(
                            notes = message,
                            contact=contact
                        )
                    note.save()

            except BadHeaderError:
                return HttpResponse('invalid header')

            return redirect('contact:success')
    else:
        contact_form = ContactForm()
        note_form = NoteForm()

    context = {
        'contactdetails':contactdetails,
        'contact_form':contact_form,
        'note_form':note_form
    }
    return render(request, template, context)

def success(request):
    
    return render(request,'contact/send.html', {})
