from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class SignupForm(UserCreationForm):
    # not using the regular signup for from django because we want to add groups
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'groups']

    def save(self, commit=True):
        user = super().save(commit)
        if not commit:
            user.save(using='default')
        return user