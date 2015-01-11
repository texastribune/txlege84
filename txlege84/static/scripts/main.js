/* global Bloodhound */

(function() {
  'use strict';

  var $sidebarButtonA = $('.sidebar-header-bills');
  var $sidebarButtonB = $('.sidebar-header-resources');
  var $sidebarContentA = $('.sidebar-content-bills');
  var $sidebarContentB = $('.sidebar-content-resources');
  var $categoryDropdown = $('#category-dropdown');
  var $arrowIconA = $('.arrow-a');
  var $arrowIconB = $('.arrow-b');

  function toggleBillSearch() {
    $sidebarContentA.toggleClass('collapse');
    $arrowIconA.toggleClass('collapse');
  }

  function toggleResources() {
    $sidebarContentB.toggleClass('collapse');
    $arrowIconB.toggleClass('collapse');
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

  $('.flexible-video').fitVids();

  var searchBills = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name', 'slug'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: [],
  });

  searchBills.initialize();

  var $billSearch = $('#bill-search').typeahead({
    autoselect: true,
    hint: false,
    highlight: false,
    minLength: 2
  }, {
    name: 'bills',
    displayKey: 'name',
    source: searchBills.ttAdapter()
  });

  $billSearch.on('typeahead:selected', function(e, datum) {
    e.stopPropagation();
    window.location = window.billSnippetURL + datum.slug + '/';
  });
})();
