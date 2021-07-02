from django import forms

  
class ImageForm(forms.Form):
    pic = forms.ImageField(required=False,label="Profile Pictue",allow_empty_file=True)
class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,label="Password")
