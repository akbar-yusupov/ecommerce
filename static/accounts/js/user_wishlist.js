$('#add-button').click(function(){
  console.log('xot tut');
  $.ajax({
    type: 'POST',
    url: basket_add_url,
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      product_id: $('#add-button').val(),
      product_qty: 1,
      action: 'post'
    },
    success: function(json) {
      window.location.href = redirect_url;
    },
  });
});