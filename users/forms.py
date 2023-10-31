from django import forms 
from django.contrib.auth.models import User
from .models import Profile


# -----------------# Register Form # -----------------------------------------------#
class UserRegisterForm(forms.ModelForm):
    username   = forms.CharField(label='username', max_length=30, required=True, help_text='No space allowed')
    email      = forms.EmailField(label='E-Mail', max_length=100, required=True)
    first_name = forms.CharField(label='first name', max_length=30, required=True)
    last_name  = forms.CharField(label='last name', max_length=30, required=False)
    password1  = forms.CharField(label='password', min_length=8, required=True,help_text='use 8 and more', widget=forms.PasswordInput())
    password2  = forms.CharField(label='password configration', min_length=8,required=True, help_text='use 8 and more', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password1','password2')

    # validate that the tow passwords are identecal of password cleaned date
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('passwords not identical')
        return cd['password2']

    # validate that the username is unique of username cleaned date
    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('this username used by another user')
        return cd['username']


    




# -----------------# Login Form # -----------------------------------------------#
class LoginForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
        
    class Meta:
        model = User
        fields = ('username', 'password')






# -----------------# User update Form # -----------------------------------------------#
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='first name', max_length=30, required=True)
    last_name = forms.CharField(label='last name', max_length=30, required=False)
    email = forms.EmailField(label='E-Mail', max_length=100, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    
        
        


# --------profile update form --------------------
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)