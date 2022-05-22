from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.OrderListView.as_view(), name="list"),
    path("add/", views.AddOrderView.as_view(), name="add"),
]
