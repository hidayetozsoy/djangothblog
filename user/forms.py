from collections import namedtuple
from django import forms

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=20,min_length=2,label="İsim")
    surname = forms.CharField(max_length=20,min_length=2,label="Soyisim")
    username = forms.CharField(max_length=50,min_length=4,label="Kullanıcı Adı")
    email = forms.EmailField(label="Email")
    password = forms.CharField(max_length=20,min_length=6,label="Parola",widget=forms.PasswordInput)
    confirm = forms.CharField(label="Parolayı Onayla",widget=forms.PasswordInput)
    
    def clean(self):
        name = self.cleaned_data.get("name")
        surname = self.cleaned_data.get("surname")
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar uyuşmuyor")
        values = {
            "name" : name,
            "surname" : surname,
            "username" : username,
            "email" : email,
            "password" : password,
        }
        return values

class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Şifre",widget=forms.PasswordInput)
    