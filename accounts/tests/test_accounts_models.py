import pytest


def test_customer_str(customer):
    assert str(customer) == "admin@admin.com"


def test_admin_customer_str(admin_customer):
    assert str(admin_customer) == "new_admin@email.com"


def test_customer_email_no_input(customer_factory):
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(email="")
    assert str(e.value) == "You must provide an email address"


def test_admin_customer_email_not_stuff(customer_factory):
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(
            email="test@test.com", is_superuser=True, is_staff=False
        )
    assert str(e.value) == "Superuser must be assigned to is_staff=True"


def test_admin_customer_email_not_superuser(customer_factory):
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(
            email="test@test.com", is_superuser=False, is_staff=True
        )
    assert str(e.value) == "Superuser must be assigned to is_superuser=True"


def test_address_str(address):
    assert str(address) == "my address line"
