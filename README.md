# <a href="https://vevnjpf.pythonanywhere.com/en/portfolio/e-commerce">Description</a>

# How to launch the project

- In "ecommerce/settings" path create local_settings.py file

- Extract <a href="https://dev.maxmind.com/geoip/geolite2-free-geolocation-data">GeoLite2-City.mmdb</a> and <a href="https://dev.maxmind.com/geoip/geolite2-free-geolocation-data">GeoLite2-Country.mmdb</a> and place it in "geoip" folder

- Create at least one Storage model instance

- To process the payment, you will need a <a href="https://stripe.com/docs/stripe-cli"> Stripe CLI </a> , extract it in the main directory.
After that you can run command for handling payment events
```
  stripe listen --forward-to <ip>:<port>/payment/webhook/
```

# Celery

- Celery beat every week will send the most profitable product to customers

- Command will send active coupons to all active customer:

```
  python3 manage.py send_coupons
```
