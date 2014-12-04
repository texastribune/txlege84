$(function () {
  'use strict';

  var navcontent = $('.browse-topics');
  var body = $(document.body);
  var appbarElement = $('.nav-bar');
  var menuBtn = $('.menu');
  var icon = $('.menu-icon');

  function toggleMenu() {
    appbarElement.toggleClass('open');
    navcontent.toggleClass('open');
    icon.toggleClass('x');
  }

  $(menuBtn).click(function() {
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

