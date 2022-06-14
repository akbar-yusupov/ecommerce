<h1>How to use project</h1>
- <h3>Register using an email, reset password if you need</h3>
<hr>
<h2>Navigation bar:</h2>
<h3>Choose MPTT category</h3>
<h3>Change the language in the navigation bar</h3>
<h3>Search for desired product with infinite scroll pagination</h3>
<h3>Dashboard link</h3>
<h3>Basket link</h3>

<hr>
<h2>Main page:</h2>
<h3>Five random parent categories</h3>
<h3>Products of the day(can be changed from admin panel)</h3>
<h3>Most rated products</h3>
<h3>Most purchased products</h3>
<hr>

<h2>Single product page:</h2>
<h3>Number of purchases</h3>
<h3>Price(with discount)</h3>
<h3>Your product rating(you can rate product if you bought it)</h3>
<h3>Description and Specifications</h3>
<h3>Add to basket or Add to / Delete from Wishlist </h3>

<hr>
<h2>Account page:</h2>
<h3>Edit email, first name, phone number</h3>
<h3>Delete an account</h3>

<hr>
<h2>Dashboard page:</h2>
<h3>View Orders(address, total_paid, delivery status)</h3>
<h3>CRUD shipping Addresses</h3>
<h3>Wishlist(can be added from single product page): remove, add to the basket</h3>
<hr>

<h2>Basket page:</h2>
<h3>Delivery route: choose address and system will find nearest storage(map with details will be shown), delivery price will be calculated automatically</h3>
<h3>Products: update/delete/change quantity</h3>
<h3>Coupon(not required)</h3>
<h3>Submit and you will be redirected to the Payment page</h3>
<hr>

<h2>Payment page:</h2>
<h3>Enter credit or debit card</h3>
<h3>Confirm payment -> Order will be created </h3>
<hr>

<h1>Documentation for launching the project</h1>
<h3>1.Download <a href="https://stripe.com/docs/stripe-cli">Stripe CLI</a> for processing payment intent and place it in the root folder</h3>
<h3>2.Download <a href="https://dev.maxmind.com/geoip/geolite2-free-geolocation-data?lang=en">GeoLite2-City.mmdb and GeoLite2-Country.mmdb</a> and place it in "geoip" folder.</h3>

<hr>
<h1>Additional info</h1>
<h3>"python3 manage.py send_coupons" command will send all active coupons to all active users(except stuff)</h3>
<h3>periodic task will send product with the best discount percentage</h3>
