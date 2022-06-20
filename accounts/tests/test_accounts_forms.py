import pytest
from django.urls import reverse

from accounts.forms import CustomerAddressForm, RegistrationForm


@pytest.mark.parametrize(
    "email, full_name, password, password2, validity",
    [
        ("admin@admin.com", "Full Name", "adminadmin", "adminadmin", True),
        ("admin@admin.com", "Full Name", "adminadmin", "", False),
        ("admin@admin.com", "Full Name", "adminadmin", "adminadmi", False),
        ("admin@.com", "Full Name", "adminadmin", "adminadmin", False),
    ],
)
@pytest.mark.django_db
def test_create_account(email, full_name, password, password2, validity):
    form = RegistrationForm(
        data={
            "email": email,
            "full_name": full_name,
            "password": password,
            "password2": password2,
            "validity": validity,
        }
    )
    print("FORM", email)
    print(form.errors)
    assert form.is_valid() is validity


@pytest.mark.parametrize(
    "phone, address_line, town_city, delivery_instructions, latitude, longitude, validity",
    [
        (
            "+99899 123 45 67",
            "addr is ...",
            "Tashkent",
            "leave it",
            45,
            45,
            True,
        ),
    ],
)
def test_address_form(
    phone,
    address_line,
    town_city,
    delivery_instructions,
    latitude,
    longitude,
    validity,
):
    form = CustomerAddressForm(
        data={
            "phone": phone,
            "address_line": address_line,
            "town_city": town_city,
            "delivery_instructions": delivery_instructions,
            "latitude": latitude,
            "longitude": longitude,
            "validity": validity,
        }
    )
    assert form.is_valid() is validity


def test_customer_create_address(client, customer):
    client.force_login(customer)
    url = reverse("accounts:add_address")
    response = client.post(url, data={"full_name": "Akbar Yusupov"})
    assert response.status_code == 200
