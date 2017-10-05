from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Questions

# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
            widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'Username'}))
    password = forms.CharField(label="Password", max_length=30, 
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'Password'}))


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(
    	max_length=30, 
    	widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name', 'placeholder': 'First Name'}), 
    	required=False)
    
    last_name = forms.CharField(
    	max_length=30, required=False, 
    	widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name', 'placeholder': 'Last Name'}))

    phone_number = forms.CharField(
        max_length=30, required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'phone_number', 'placeholder': 'Phone Number'}))
    
    email = forms.EmailField(max_length=254, 
    	widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'email', 'placeholder': 'Email'}))

    username = forms.CharField(
    	max_length=30, 
    	widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'Username'}), 
    	required=False)

    password1 = forms.CharField(label="Password", max_length=30, 
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'Password'}))

    password2 = forms.CharField(label="Confirm Password", max_length=30, 
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number','email', 'password1', 'password2', )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user_type', 'user_interests')

class QuestionsForm(forms.Form):
    user = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea)
