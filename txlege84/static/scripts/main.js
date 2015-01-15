/* global Bloodhound */

(function() {
  'use strict';


  // Build sidebar accordion
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

  // Add fitvids to Texplainer, other video embeds
  $('.flexible-video').fitVids();

  // Bill Search
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

  // LegeStream
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

  // Rotating Ad
  var roofline = {
    interval: 15 * 1000,
    desktopAds: $('#rotating_ad').children('.mobile-hide').find('.rotating-ad'),
    mobileAds: $('#rotating_ad').children('.desktop-hide').find('.rotating-ad'),
    init: function(){
      if (roofline.desktopAds.length <= 1 && roofline.mobileAds.length <= 1) {
        return false;
      }
      roofline.desktopAds.eq(0).addClass('active');
      roofline.mobileAds.eq(0).addClass('active');
      roofline.desktopAds.filter(':gt(0)').removeClass('active').hide();
      roofline.mobileAds.filter(':gt(0)').removeClass('active').hide();
      this.timer = setTimeout(roofline.flip, roofline.interval);
    },
    showNext: function(ad){
      var next = ad.next('.rotating-ad');
      if (!next.length) {
        next = ad.siblings('.rotating-ad').eq(0);
      }
      next.addClass('active').show();
    },
    flip: function(){
      var active, self = roofline;
      if (self.timer) {
        // debounce
        clearTimeout(self.timer);
      }
      active = self.desktopAds.filter('.active').removeClass('active').hide();
      self.showNext(active);
      active = self.mobileAds.filter('.active').removeClass('active').hide();
      self.showNext(active);
      roofline.timer = setTimeout(roofline.flip, roofline.interval);
    },
    stop: function(){
      if (roofline.timer) {
        clearTimeout(roofline.timer);
      }
    }
  };

  roofline.init();
})();
