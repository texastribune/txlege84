/* global Bloodhound, FastClick, streamMapping */

$(document).ready(function() {
  'use strict';

  // Fastclick initialize
  FastClick.attach(document.body);

  // Menu
  var $menuButton = $('#menu-button');
  var $menuIcon = $menuButton.find('i');
  var $menuNav = $('#menu-nav');
  var $subNavContainer = $('#sub-nav-container');
  var $menuSubNavTrigger = $('#sub-nav-trigger');
  var $menuSubNav = $('#sub-nav');

  $menuButton.on('click', function(e) {
    e.preventDefault();

    if ($menuNav.hasClass('menu-nav-open')) {
      $menuIcon.removeClass('fa-times').addClass('fa-bars');
    } else {
      $menuIcon.removeClass('fa-bars').addClass('fa-times');
    }

    $menuNav.toggleClass('menu-nav-open');
  });

  $menuSubNavTrigger.on('click', function(e) {
    e.preventDefault();

    $menuSubNav.toggleClass('sub-nav-open');
  });

  // hides the sub nav if it is open and someone clicks elsewhere
  $(document).on('click', function(event) {
  if (!$(event.target).closest($subNavContainer).length) {
    $menuSubNav.removeClass('sub-nav-open');
  }
});

  // Accordions AKA Shutters

  var $shutterToggles = $('.shutter-label');

  $shutterToggles.on('click', function() {
    var selected = $(this);
    selected.find('.shutter-icon').toggleClass('shutter-icon-open');
    selected.next('.shutter-content').toggleClass('shutter-content-open');
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
  if (typeof streamMapping !== 'undefined') {
    var streamLoader = function(id, width, height) {
      var stream = streamMapping[id];
      var iframeHeight = height + 30;

      if (stream.feedId) {
        return '<iframe scrolling="no" style="border:0" width="' + width + '" height="' + iframeHeight + '" id="GranicusFlashPlayerFrame" src="http://' + stream.subdomain + '.granicus.com/mediaplayer.php?feed_id=' + stream.feedId + '&event_id=' + stream.eventId + '&embed=1&player_width=' + width + '&player_height=' + height + '"></iframe>';
      } else {
        return '<iframe scrolling="no" style="border:0" width="' + width + '" height="' + iframeHeight + '" id="GranicusFlashPlayerFrame" src="http://' + stream.subdomain + '.granicus.com/mediaplayer.php?camera_id=' + stream.cameraId + '&embed=1&player_width=' + width + '&player_height=' + height + '"></iframe>';
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
  }

  // Rotating Ad
  var roofline = {
    interval: 15 * 1000,
    desktopAds: $('.rotating-ad-container').children('.mobile-hide').find('.rotating-ad'),
    mobileAds: $('.rotating-ad-container').children('.desktop-hide').find('.rotating-ad'),
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
});
