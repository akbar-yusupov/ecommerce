$( document ).ready(function() {
  $('#search-form').submit(function(e){
    if ($('#search-input').val().length < 3)
    {
      alert('Enter at least 3 characters');
      e.preventDefault(e);
    }
  });
});