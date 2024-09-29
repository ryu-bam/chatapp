from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

from .models import CustomUser, Message

class CustomUserModelForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email",  "image", "password1", "password2")
        
class LoginForm(AuthenticationForm):
    pass
        
class MessageModelForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("content",)

class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username",)

class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

class ImageUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("image",)

class PasswordUpdateForm(PasswordChangeForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'