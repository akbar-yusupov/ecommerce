import pytest


@pytest.mark.django_db
def test_product_admin(client, admin_customer):
    client.force_login(admin_customer)
    response = client.get('admin/store/product/')
    assert response.status_code == 200
