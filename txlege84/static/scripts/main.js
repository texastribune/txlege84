$(function () {
  'use strict';

  var sidebarButton = $('.sidebar-header');
  var sidebarContent = $('.sidebar-content');

  function toggleMenu() {
    sidebarContent.toggleClass('collapse');
  }

  $(sidebarButton).click(function() {
    toggleMenu();
  });

})();

$(document).ready(function() {
  $('.story-stream').slick({
      dots: true,
      infinite: true,
      speed: 500,
      slidesToShow: 1,
      slidesToScroll: 1
  });

});

