$(function () {
  'use strict';

  var sidebarButtonA = $('.sidebar-header-bills');
  var sidebarButtonB = $('.sidebar-header-resources');
  var sidebarContentA = $('.sidebar-content-bills');
  var sidebarContentB = $('.sidebar-content-resources');

  function toggleBillSearch() {
    sidebarContentA.toggleClass('collapse');
  }

  function toggleResources() {
    sidebarContentB.toggleClass('collapse');
  }

  $(sidebarButtonA).click(function() {
    toggleBillSearch();
  });

  $(sidebarButtonB).click(function() {
    toggleResources();
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

