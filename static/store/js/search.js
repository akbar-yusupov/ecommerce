var infinite = new Waypoint.Infinite({
  element: $('#infinite-container'),

  offset: 'bottom-in-view',

  onBeforePageLoad: function () {
    $('.loading').show();
  },

  onAfterPageLoad: function () {
    $('.loading').hide();
  }

});