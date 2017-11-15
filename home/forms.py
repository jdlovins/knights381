from django import forms
from django.contrib.auth.models import User
from home.validators import alphanumeric
from .models import Profile


class SignUpForm(forms.Form):

    user_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[alphanumeric],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-control',
                'tabindex': 1
            }
        )
    )

    email = forms.EmailField(
        max_length=50,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email Address',
                'class': 'form-control',
                'tabindex': 2
            }
        )
    )

    password = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control',
                'tabindex': 3
            }
        )
    )

    confirm_password = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password',
                'class': 'form-control',
                'tabindex': 4
            }
        )
    )

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('password', 'Sorry, passwords do not match!')
        return self.cleaned_data

    class Meta:
        model = User
        fields = {'user_name', 'email', 'password', 'confirm_password'}


class LoginForm(forms.Form):

    user_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[alphanumeric],
        widget=forms.TextInput(
            attrs={'placeholder': 'Username',
                   'class': 'form-control',
                   'tabindex': 1
                   }
        )
    )

    password = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control',
                'tabindex': 2
            }
        )
    )

    remember_me = forms.BooleanField(
        help_text="Remember me?",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'tabindex': 3
            }
        )
    )

    class Meta:
        fields = {'user_name', 'password', 'remember_me'}


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'email'}

# TODO: Link Profile model fields into form.
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {'steam_id'}

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['steam_id'].widget.attrs = {
            'placeholder': 'STEAM_0:0:12345',
            'size': 20
        }
