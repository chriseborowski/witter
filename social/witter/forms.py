from django import forms
from .models import Witt, UserProfile
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


class SignUpForm(UserCreationForm):
  email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your email address'}))
  first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your first name'}))
  last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your last name'}))

  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

  def __init__(self, *args, **kwargs):
    self(superSignUpForm, self).__init__(*args, **kwargs)

    self.fields['username'].widget.attrs['class'] = 'form-control'
    self.fields['username'].widget.attrs['placeholder'] = 'Your username'
    self.fields['username'].label = ''
    self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

    self.fields['password1'].widget.attrs['class'] = 'form-control'
    self.fields['password1'].widget.attrs['placeholder'] = 'Your password'
    self.fields['password1'].label = ''
    self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

    self.fields['password2'].widget.attrs['class'] = 'form-control'
    self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'
    self.fields['password2'].label = ''
    self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class ProfileUpdateForm(forms.ModelForm):
  email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Your email address'}))
  first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your first name'}))
  last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your last name'}))

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email')

  def __init__(self, *args, **kwargs):
    super(ProfileUpdateForm, self).__init__(*args, **kwargs)
    self.fields['email'].label = "Email address"
