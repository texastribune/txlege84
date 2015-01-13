/* global Bloodhound */

(function() {
  'use strict';

  var $sidebarButtonA = $('.sidebar-header-bills');
  var $sidebarButtonB = $('.sidebar-header-resources');
  var $sidebarContentA = $('.sidebar-content-bills');
  var $sidebarContentB = $('.sidebar-content-resources');
  var $categoryDropdown = $('#category-dropdown');
  var $legislatorDropdown = $('#legislator-dropdown');
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

  $legislatorDropdown.change(function() {
    document.location.href = $(this).val();
  });

  $('.flexible-video').fitVids();

  var searchBills = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name', 'slug'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    limit: 10,
    sorter: function(a, b) {
      return (+a.name.match(/\d+/)[0]) - (+b.name.match(/\d+/)[0]);
    },
    prefetch: {
      url: '/search/bills/'
    },
    ttl: 3600000 // One hour
  });

  searchBills.initialize();

  var $billSearch = $('#bill-search').typeahead({
    autoselect: true,
    hint: false,
    highlight: false,
    minLength: 3
  }, {
    name: 'bills',
    displayKey: 'name',
    source: searchBills.ttAdapter()
  });

  $billSearch.on('typeahead:selected', function(e, datum) {
    e.stopPropagation();
    window.location = window.billSnippetURL + datum.slug + '/';
  });

  var streamMapping = {
    'house-stream': {
      subdomain: 'tlchouse',
      cameraId: '3'
    },
    'senate-stream': {
      subdomain: 'tlcsenate',
      cameraId: '8'
    }
  };

  var $streamPlaceholder = $('.stream-placeholder');

  $streamPlaceholder.one('click', function() {
    var $this = $(this);
    $this.addClass('stream-activated');
    var width = $this.parent().width();
    var height = width * 0.5625;
    $this.find('.stream-prompt').replaceWith(streamLoader(this.id, width, height));
  });

  function streamLoader(id, width, height) {
    var stream = streamMapping[id];
    var iframeHeight = height + 30;

    return '<iframe scrolling="no" style="border:0" width="' + width + '" height="' + iframeHeight + '" id="GranicusFlashPlayerFrame" src="http://' + stream.subdomain + '.granicus.com/mediaplayer.php?camera_id=' + stream.cameraId + '&embed=1&player_width=' + width + '&player_height=' + height + '"></iframe>';
  }
})();
