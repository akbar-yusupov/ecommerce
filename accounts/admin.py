from django.contrib import admin

from .models import Address, Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "created_at", "updated_at")
    list_filter = ("is_staff",)
    search_fields = ("email", "full_name")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.readonly_fields = ("created_at", "updated_at")
        return super().change_view(request, object_id, form_url, extra_context)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "town_city", "address_line")
    search_fields = ("full_name", "phone")
