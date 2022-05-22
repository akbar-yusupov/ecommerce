from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _

from .models import Address, Customer


class LoginForm(forms.Form):
    email = forms.CharField(
        min_length=4,
        max_length=64,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("Enter your email"),
            }
        ),
    )
    password = forms.CharField(
        min_length=8,
        max_length=64,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter your password"),
            }
        ),
    )


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        label=_("Email"),
        min_length=4,
        max_length=64,
        error_messages={"required": _("Sorry, you will need an email")},
    )
    full_name = forms.CharField(
        label=_("Full Name"),
        min_length=4,
        max_length=128,
        error_messages={"required": _("Sorry, you need to enter full name")},
    )
    password = forms.CharField(
        label=_("Password"),
        min_length=8,
        max_length=64,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Repeat Password"),
        min_length=8,
        max_length=64,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": _("Enter full name")}
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control mb-3",
                "placeholder": "test@email.com",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control mb-3",
                "placeholder": _("secured password"),
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control mb-3",
                "placeholder": _("same secured password"),
            }
        )

    def clean_password2(self):
        if self.cleaned_data["password"] == self.cleaned_data["password2"]:
            return self.cleaned_data["password2"]
        else:
            raise forms.ValidationError(_("Passwords do not match"))

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Email already exists"))
        return email

    class Meta:
        model = Customer
        fields = ("email", "full_name")


class CustomerEditForm(forms.ModelForm):

    email = forms.EmailField(
        label=_("Account Email"),
        min_length=4,
        max_length=64,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": _("Email")}
        ),
    )

    full_name = forms.CharField(
        label=_("First Name"),
        min_length=4,
        max_length=64,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "First Name"}
        ),
    )

    phone = forms.CharField(
        label=_("Phone"),
        min_length=4,
        max_length=16,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("Phone number"),
            }
        ),
    )

    class Meta:
        model = Customer
        fields = ("email", "full_name", "phone")


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=64,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("Email"),
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Customer.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError(
            _("Unfortunately we can not find that email address")
        )


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("New Password"),
            }
        ),
    )
    new_password2 = forms.CharField(
        label=_("Repeat password"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("New Password"),
            }
        ),
    )


class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "phone",
            "address_line",
            "town_city",
            "delivery_instructions",
            "latitude",
            "longitude",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": _("Enter phone"),
            }
        )
        self.fields["address_line"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": _("Address line"),
            }
        )
        self.fields["town_city"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": _("Enter town or city"),
            }
        )
        self.fields["delivery_instructions"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": _("Enter delivery instructions"),
            }
        )
        self.fields["latitude"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": _("Enter latitude"),
            }
        )
        self.fields["longitude"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": _("Enter longitude"),
            }
        )
