from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegisterForm(forms.ModelForm):
    """
    A form for creating new users with username, email, and password.
    """
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean(self):
        # check two password entries match
        print(self.cleaned_data)
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        print(password2, password1)
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match!")
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    """A profile form to update user photo."""
    class Meta:
        model = Profile
        fields = ('image', )
        widgets = {
            'image': forms.FileInput(),
        }


class UserLoginForm(forms.Form):
    """
    A form for logging in used by existing user.
    """
    username = forms.CharField(max_length=25)
    password = forms.CharField(widget=forms.PasswordInput())