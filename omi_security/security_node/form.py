from django import forms
from django.contrib.auth.models import User

from security_node.models import Group, User_Group_Relation, Rule



class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=64, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(label='Last Name', max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(min_length=6, label='Username', max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(label='Email', max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(min_length=6, max_length=32, label='Password', widget=forms.PasswordInput)
    password1 = forms.CharField(min_length=6, max_length=32, label='Password confirmation', widget=forms.PasswordInput)
    is_staff = forms.BooleanField(label='Superuser', required=False)
    class Meta:
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password1', 'is_staff']
        model=User
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        password1 = cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError(
                "Password and Confirm Password does not match"
            )
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    '''
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Duplicate User Exists')
    '''


