import debug_toolbar
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += i18n_patterns(
    path("", include("store.urls", namespace="store")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("basket/", include("basket.urls", namespace="basket")),
    path("payment/", include("payment.urls", namespace="payment")),
    path("orders/", include("orders.urls", namespace="orders")),
    path(
        "favicon.ico",
        RedirectView.as_view(
            url=staticfiles_storage.url("images/favicon.ico")
        ),
    ),
)


if settings.DEBUG:
    urlpatterns.append(path("__debug__", include(debug_toolbar.urls)))
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
