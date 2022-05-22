$('#add-button').click(function(){
  $.ajax({
    type: 'POST',
    url: basket_add_url,
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      product_id: $('#add-button').val(),
      product_qty: $('#select option:selected').text(),
      action: 'post'
    },
    success: function(json) {
      window.location.href = redirect_url;
    },
  });
});
$(':submit').click(function(){
  $.ajax({
    type: 'POST',
    url: '',
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      stars: this.id
    },
    success: function(json) {},
  });
});