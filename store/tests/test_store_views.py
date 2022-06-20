import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_store_home_url(client):
    url = reverse("store:store_home")
    response = client.get(url)
    assert response.status_code == 200
