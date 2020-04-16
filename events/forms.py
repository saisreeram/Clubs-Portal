from django import forms
from .models import Events

class AddEventForm(forms.ModelForm):
    about_event = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}))
    venue = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}))
    event_from = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM'}))
    event_to = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM'}))
    class Meta:
        model = Events
        fields = ['event_name','about_event','event_from','event_to','venue']
