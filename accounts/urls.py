from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import PwdResetConfirmForm, PwdResetForm

app_name = "accounts"

urlpatterns = [
    # Authorization, Authentication
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path(
        "logout",
        auth_views.LogoutView.as_view(next_page="accounts:login"),
        name="logout",
    ),
    path(
        "activate/<slug:uidb64>/<slug:token>/",
        views.AccountActivationView.as_view(),
        name="activate",
    ),
    # Dashboard
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("edit/", views.CustomerUpdateView.as_view(), name="edit_user"),
    path(
        "delete-user/", views.CustomerDeleteView.as_view(), name="delete_user"
    ),
    # Addresses
    path(
        "add-address/", views.AddressCreateView.as_view(), name="add_address"
    ),
    path(
        "address-list/", views.AddressListView.as_view(), name="address-list"
    ),
    path(
        "address/edit/<int:pk>/",
        views.AddressUpdateView.as_view(),
        name="edit_address",
    ),
    path(
        "address/delete/<int:pk>/",
        views.AddressDeleteView.as_view(),
        name="delete_address",
    ),
    path(
        "address/set_default/<int:pk>/",
        views.SetDefaultAddressView.as_view(),
        name="set_default_address",
    ),
    # Wish List
    path("wishlist", views.WishlistListView.as_view(), name="wishlist"),
    path(
        "wishlist/<int:pk>",
        views.UpdateWishlistView.as_view(),
        name="update_wishlist",
    ),
    # Password reset
    path(
        "logout_for_password_reset",
        auth_views.LogoutView.as_view(next_page="accounts:password_reset"),
        name="logout_for_password_reset",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset/password_reset_form.html",
            success_url="password_reset_email_confirm",
            email_template_name="accounts/password_reset/password_reset_email.html",
            form_class=PwdResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password_reset/password_reset_email_confirm/",
        TemplateView.as_view(
            template_name="accounts/password_reset/reset_status.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset/password_reset_confirm.html",
            success_url="/accounts/password_reset_complete/",
            form_class=PwdResetConfirmForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        TemplateView.as_view(
            template_name="accounts/password_reset/reset_status.html"
        ),
        name="password_reset_complete",
    ),
]
