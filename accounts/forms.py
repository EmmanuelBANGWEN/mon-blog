from django import forms
from django.contrib.auth.models import User


class RegistrationForms(forms.ModelForm):
    username = forms.CharField(label="username", 
                               max_length=200, 
                               help_text='', 
                               required=True, 
                               widget=forms.TextInput(attrs={"type":"text", "id":"Username","class":"form-control",  "placeholder":"Username"}) )
    

    first_name = forms.CharField(label="Firs_Name", 
                                 max_length=200, 
                                 help_text='', 
                                 required=True, 
                                 widget=forms.TextInput(attrs={"type":"text", "id":"FirstName","class":"form-control",  "placeholder":"First Name"}) )
    

    last_name = forms.CharField(label="Last_Name", 
                                max_length=200, min_length=3,
                                help_text='', 
                                required=True, 
                                widget=forms.TextInput(attrs={"type":"text", "id":"LaststName", "class":"form-control",  "placeholder":"Last Name"}) )
    

    email = forms.EmailField(label="Email", 
                             max_length=200, min_length=5,
                             help_text='', 
                             required=True, 
                            widget=forms.TextInput(attrs={"type":"text", "id":"emailAddress", "class":"form-control",  "placeholder":"Email Address"}) )
    

    password = forms.CharField(label="Password", 
                               max_length=200, min_length=8,
                               help_text='', 
                               required=True, 
                               widget=forms.TextInput(attrs={"type":"text", "id":"password", "class":"form-control",  "placeholder":"Password"}) )
    

    repeatpassword = forms.CharField(label="Repeat_Password", 
                                     max_length=200, min_length=8,
                                     help_text='', 
                                     required=True, 
                                     widget=forms.TextInput(attrs={"type":"text", "id":"repeatpassword", "class":"form-control",  "placeholder":"Repeat Password"}) )
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')