from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)
from user.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "User Name*"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    class Meta:
        model = User
        fields = ("username", "password")


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Введите имя"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Введите фамилию"})
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"placeholder": "Введите Email"})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Введите имя пользователя"})
    )
    password1 = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Введите пароль"})
    )
    password2 = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Подтвердите пароль"})
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        )


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control py-4"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control py-4"})
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "form-control py-4", "readonly": True})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control py-4", "readonly": True})
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "custom-file-input"}), required=False
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "image", "username", "email")
