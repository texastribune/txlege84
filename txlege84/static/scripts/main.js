(function() {
  'use strict';

  var $sidebarButtonA = $('.sidebar-header-bills');
  var $sidebarButtonB = $('.sidebar-header-resources');
  var $sidebarContentA = $('.sidebar-content-bills');
  var $sidebarContentB = $('.sidebar-content-resources');
  var $categoryDropdown = $('#category-dropdown');

  function toggleBillSearch() {
    $sidebarContentA.toggleClass('collapse');
  }

  function toggleResources() {
    $sidebarContentB.toggleClass('collapse');
  }

  $sidebarButtonA.click(function() {
    toggleBillSearch();
  });

  $sidebarButtonB.click(function() {
    toggleResources();
  });

  $categoryDropdown.change(function() {
    document.location.href = $(this).val();
  });

  var $storyStream = $('.story-stream');

  $storyStream.slick({
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1
  });

  $('.flexible-video').fitVids();
})();
