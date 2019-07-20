from django import forms
from django.core.exceptions import ValidationError

from myapp.models import Member


class SignupForm(forms.ModelForm):

    class Meta:
        model = Member
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ['username', 'email', 'address', 'password',]

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 50:
            raise ValidationError('Username must be at most 50 characters')
        elif len(username) < 4:
            raise ValidationError('Username must be at least 4 characters')
        return username

    def save(self, commit=True):
        instance = super(SignupForm, self).save(commit=False)
        if commit:
            instance.set_password(self.cleaned_data['password'])
            instance.save()
        return instance


class LoginForm(forms.ModelForm):
    class Meta:
        model = Member
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ['username', 'password',]




