from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import Clipboard, UserProfile


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField()
    email    = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data.get('password1'))

        if commit:
            user.save()
            user_profile = UserProfile()
            user_profile.user = user
            user_profile.save()
        return user

    # Assure that the provided email isn't already in use by another user.
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("There is already an account with that email.")

        return email


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')


# Update form for clipboard
# Allows the user to edit the contents of their clipboard
class ClipboardUpdateForm(forms.Form):
    content = forms.CharField()#widget=forms.Textarea)

    class Meta:
        model = Clipboard
        fields = ('content')

    def process(self, clipboard):
        clipboard.content = self.cleaned_data.get('content')
        clipboard.save()

        return clipboard
