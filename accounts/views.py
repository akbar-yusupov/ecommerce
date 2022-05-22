from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import DeleteView, ListView, UpdateView

from store.models import Product

from .forms import (
    CustomerAddressForm,
    CustomerEditForm,
    LoginForm,
    RegistrationForm,
)
from .models import Address, Customer
from .tokens import account_activation_token


class RegisterView(View):
    template_name = "accounts/registration/register.html"
    form_class = RegistrationForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            current_site = get_current_site(request)
            subject = "Activate your account"
            message = render_to_string(
                "accounts/registration/account_activation_email.html",
                {
                    "full_name": user.full_name,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                (user.email,),
            )
            return render(
                request, "accounts/registration/register_email_confirm.html"
            )
        else:
            return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name = "accounts/login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("store:store_home")

        return render(request, self.template_name, {"form": form})


class DashboardView(LoginRequiredMixin, View):
    template_name = "accounts/dashboard/dashboard.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerEditForm
    template_name = "accounts/dashboard/edit_user.html"
    success_url = reverse_lazy("store:store_home")

    def get_object(self, queryset=None):
        return self.request.user


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = "accounts/dashboard/delete_confirm.html"

    def get_object(self, queryset=None):
        return self.request.user


class AccountActivationView(LoginRequiredMixin, View):
    template_name = "accounts/registration/activation_invalid.html"

    def get(self, request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.filter(pk=uid).first()
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("accounts:dashboard")
        return render(request, "accounts/registration/activation_invalid.html")


# Addresses
class AddressListView(LoginRequiredMixin, ListView):
    model = Address.objects.all()
    template_name = "accounts/dashboard/address-list.html"
    context_object_name = "addresses"

    def get_queryset(self):
        queryset = self.model.filter(customer=self.request.user)
        if queryset.count() == 1:
            address = queryset.first()
            address.default = True
            address.save()
        return queryset


class AddressCreateView(LoginRequiredMixin, View):
    template_name = "accounts/dashboard/edit_address.html"
    form = CustomerAddressForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form})

    def post(self, request, *args, **kwargs):
        form = CustomerAddressForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.customer = request.user
            form.full_name = request.user.full_name
            form.save()
            return redirect("accounts:address-list")
        else:
            return render(request, self.template_name, {"form": form})


class AddressUpdateView(LoginRequiredMixin, View):
    model = Address
    template_name = "accounts/dashboard/edit_address.html"
    form = CustomerAddressForm

    def get(self, request, *args, **kwargs):
        address = get_object_or_404(
            Address, pk=self.kwargs["pk"], customer=request.user
        )
        form = self.form(instance=address)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        address = get_object_or_404(
            Address, pk=self.kwargs["pk"], customer=request.user
        )
        form = CustomerAddressForm(instance=address, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:address-list")
        else:
            return render(request, self.template_name, {"form": form})


class AddressDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        address = get_object_or_404(
            Address, pk=self.kwargs["pk"], customer=request.user
        )
        address.delete()
        return redirect("accounts:address-list")


class SetDefaultAddressView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        Address.objects.filter(customer=request.user, default=True).update(
            default=False
        )
        Address.objects.filter(
            customer=request.user, pk=self.kwargs["pk"]
        ).update(default=True)
        return redirect("accounts:address-list")


# Wish List
class WishlistListView(LoginRequiredMixin, ListView):
    model = Product.objects.all()
    template_name = "accounts/dashboard/user_wishlist.html"
    context_object_name = "wishlist"

    def get_queryset(self):
        return (
            self.model.filter(users_wishlist=self.request.user)
            .select_related("category")
            .prefetch_related("product_image")
        )


class UpdateWishlistView(LoginRequiredMixin, View):
    model = Product

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(self.model, pk=self.kwargs["pk"])
        if product.users_wishlist.filter(pk=request.user.pk).exists():

            product.users_wishlist.remove(request.user)
            messages.success(
                request,
                f'"{product.title.title()}" has been removed from your Wishlist',
            )
        else:

            product.users_wishlist.add(request.user)
            messages.success(
                request, f'"{product.title.title()}" added to your Wishlist'
            )

        referer = request.META.get("HTTP_REFERER", None)
        if referer:
            return HttpResponseRedirect(referer)
        else:
            return redirect("accounts:dashboard")
