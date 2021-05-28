from django import forms
from store.models import Contact, Note

# MyModel = apps.get_model('')

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['notes']