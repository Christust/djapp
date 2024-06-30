from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from . import models


class LoginForm(AuthenticationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "Nombre de usuario"
        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["placeholder"] = "Contraseña del usuario"


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["email", "name", "last_name", "user_type", "password"]
        widgets = {
            "email": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un email",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un nombre",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un apellido",
                }
            ),
            "user_type": forms.Select(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un tipo de usuario",
                }
            ),
            "password": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un password",
                }
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["email", "name", "last_name", "user_type"]
        widgets = {
            "email": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un email",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un nombre",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un apellido",
                }
            ),
            "user_type": forms.Select(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un tipo de usuario",
                }
            ),
        }


class UserPasswordForm(forms.Form):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Ingrese la contraseña",
            }
        ),
    )
    password_confirmation = forms.CharField(
        label="Confirmación de contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Ingrese de nuevo la contraseña",
            }
        ),
    )

    def clean_password_confirmation(self):
        password_confirmation_clean = self.cleaned_data.get("password_confirmation")
        password_clean = self.cleaned_data.get("password")
        if password_confirmation_clean is not password_clean:
            raise ValidationError("La confirmación de contraseña debe ser igual")
        return password_confirmation_clean
