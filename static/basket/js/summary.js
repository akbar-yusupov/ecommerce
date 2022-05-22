$(document).ready(function() {

  $( init );

  function init() {
    var address = $('#address-select option:selected').val();
    $.ajax({
      type: 'POST',
      url: basket_summary_url,
      data: {
        address: address,
        csrfmiddlewaretoken: CSRF_TOKEN,
        action: 'post'
      },
      success: function (json) {
        $('#map').html(json.map);
        $('#distance').text(json.distance);
        $('#customer_city').text(json.customer_city);
        $('#storage_city').text(json.storage_city);
        $('#delivery_price').text("$" + json.delivery_price);
        $('#total').text(json.total_price);
      },
      error: function (xhr, errmsg, err) {}
    });
  }

  $('#coupon-submit').click(function(){
    $.ajax({
      type: 'post',
      url: check_coupon_url,
      data: {
        csrfmiddlewaretoken: CSRF_TOKEN,
        coupon_code: $('#coupon-code').val(),
      },
      success: function(json) {
        console.log('success');
        if (json.coupon_discount != 0) {
          $('#coupon-discount').removeAttr('hidden');
          $('#coupon-discount').text("The coupon discount percentage is " + json.coupon_discount);
        }else{
          $('#coupon-discount').removeAttr('hidden');
          $('#coupon-discount').text("");
        }
      },
    });
  });


  $('.update-button').click(function() {
    var product_id = $(this).data('index');
    $.ajax({
      type: 'POST',
      url: basket_update_url,
      data: {
        product_id: product_id,
        product_qty: $('#select-' + product_id + ' option:selected').text(),
        csrfmiddlewaretoken: CSRF_TOKEN,
        action: 'post'
      },
      success: function (json) {
        document.getElementById("basket-qty").innerHTML = json.basket_qty
        document.getElementById("total").innerHTML = json.basket_total
        document.getElementById("subtotal").innerHTML = json.basket_subtotal
      },
      error: function (xhr, errmsg, err) {}
    });
  });

  $('.delete-button').click(function() {
    var product_id = $(this).data('index');
    $.ajax({
      type: 'POST',
      url: basket_delete_url,
      data: {
        product_id: product_id,
        csrfmiddlewaretoken: CSRF_TOKEN,
        action: 'post'
      },
      success: function(json) {
        $('.product-item[data-index="'+ product_id +'"]').remove();
        document.getElementById("basket-qty").innerHTML = json.basket_qty;
        document.getElementById("total").innerHTML = json.basket_total;
        document.getElementById("subtotal").innerHTML = json.basket_subtotal;
      },
    });
  });

  $('#address-select').change(function(){
    var address = $('#address-select option:selected').val();
    $.ajax({
      type: 'POST',
      url: basket_summary_url,
      data: {
        address: address,
        csrfmiddlewaretoken: CSRF_TOKEN,
        action: 'post'
      },
      success: function (json) {
        $('#map').html(json.map);
        $('#distance').text(json.distance);
        $('#customer_city').text(json.customer_city);
        $('#storage_city').text(json.storage_city);
        $('#delivery_price').text("$" + json.delivery_price);
        $('#total').text(json.total_price);
      },
      error: function (xhr, errmsg, err) {}
    });
  });

});