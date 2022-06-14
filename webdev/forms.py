from django import forms
from .models import Tickets, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class adding_new_ticket_form(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = [
            'title',
            'description',
            'ticket_status',
            'assigned_by'
        ]
        widgets = {
            'ticket': forms.RadioSelect
        }


form = adding_new_ticket_form(forms.ModelForm)


class login_form(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Create a UserUpdateForm to update username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Create a ProfileUpdateForm to update image
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']