var stripe = Stripe(PUBLISHABLE_KEY);

var elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');


var elements = stripe.elements();
var style = {
    base: {
      color: "#000",
      lineHeight: '2.4',
      fontSize: '16px'
    }
};


var card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', function(event) {
    var displayError = document.getElementById('card-errors')
    if (event.error) {
          displayError.textContent = event.error.message;
          $('#card-errors').addClass('alert alert-info');
    } else {
          displayError.textContent = '';
          $('#card-errors').removeClass('alert alert-info');
    }
});

var form = document.getElementById('payment-form');


form.addEventListener('submit', function(ev) {
    ev.preventDefault();

    $.ajax({
        type: "POST",
        url: orders_add_url,
        data: {
            order_key: clientsecret,
            csrfmiddlewaretoken: CSRF_TOKEN,
            storage_pk: storage_pk,
            address_pk: address_pk,
            action: "add",
        },
        success: function (json) {
            console.log(json.success)

            stripe.confirmCardPayment(clientsecret, {
                payment_method: {
                    card: card
                }
            }).then(function(result) {
                if (result.error) {
                    console.log('payment error')
                    console.log(result.error.message);
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        window.location.replace(order_placed_url);
                    }
                }
            });

        },

       error: function (xhr, errmsg, err) {},
    });
});
