from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('name', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('name', 'email')


class CustomSignupForm(SignupForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Full name'}))

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.save()
        return user
