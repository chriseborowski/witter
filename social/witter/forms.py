from django import forms
from .models import Witt

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
