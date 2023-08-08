from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


'''class SignupForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=[('client', 'Client'), ('professional', 'Professional')])

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'user_type']

    def save(self, commit=True):
        user = super().save(commit)
        user_type = self.cleaned_data.get('user_type')
        if user_type == 'client':
            client_group = Group.objects.using('default').get(name='Client')
            client_group.user_set.add(user)
        elif user_type == 'professional':
            professional_group = Group.objects.using('default').get(name='Professional')
            professional_group.user_set.add(user)
        if not commit:
            user.save(using='default')
        return user
'''


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'groups']

    def save(self, commit=True):
        user = super().save(commit)
        if not commit:
            user.save(using='default')
        return user