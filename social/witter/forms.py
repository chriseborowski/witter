from django import forms
from .models import Witt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class WittForm(forms.ModelForm):
    body = forms.CharField(required=True,
    widget=forms.widgets.Textarea(
      attrs={
        "placeholder": "Enter your Witt here...",
        "class": "form-control",
      }
    ),
    label="",
    )
    
    class Meta:
        model = Witt
        exclude = ("user", )
