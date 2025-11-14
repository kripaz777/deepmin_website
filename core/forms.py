from django import forms
from .models import ContactMessage, Application

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name','email','subject','message']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['job','name','email','cover_message','cv']
