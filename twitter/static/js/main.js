var spinnerOpts = {
    lines: 11            // The number of lines to draw
  , length: 5            // The length of each line
  , width: 3             // The line thickness
  , radius: 12           // The radius of the inner circle
  , scale: 1             // Scales overall size of the spinner
  , corners: 0.8         // Corner roundness (0..1)
  , color: '#fff'        // #rgb or #rrggbb or array of colors
  , opacity: 0.25        // Opacity of the lines
  , rotate: 0            // The rotation offset
  , direction: 1         // 1: clockwise, -1: counterclockwise
  , speed: 1.5           // Rounds per second
  , trail: 41            // Afterglow percentage
  , fps: 20              // Frames per second when using setTimeout() as a fallback for CSS
  , zIndex: 2e9          // The z-index (defaults to 2000000000)
  , className: 'spinner' // The CSS class to assign to the spinner
  , top: '50%'           // Top position relative to parent
  , left: '50%'          // Left position relative to parent
  , shadow: true         // Whether to render a shadow
  , hwaccel: true        // Whether to use hardware acceleration
  , position: 'absolute' // Element positioning
};


function parseQuerystr(qstr) {
  if (qstr === "") return {};
  var params = qstr.split('&');
  var param;
  var ret = {};

  for (var i = 0; i < params.length; i++) {
    param = params[i].split('=');
    ret[param[0]] = param[1] || '';
  }

  return ret;
}


function createQuerystr(obj) {
  var params = [];

  for (var k in obj) {
    if (obj.hasOwnProperty(k)) {
      params.push(k + '=' + obj[k]);
    }
  }

  return params.join('&');
}


function mapLatLng(items) {
  return items.map(function(item) {
    return new google.maps.LatLng(item[1], item[0]);
  });
}


$(function() {
  'use strict';

  var baseUrl = '/points.json?';
  var googleMap;
  var xhr;
  var pageParams = {k: 'hakaret', t: 'svm'};
  $.extend(pageParams, parseQuerystr(window.location.hash.substring(1)));


  // set active links initially
  for (var p in pageParams) {
    if (pageParams.hasOwnProperty(p)) {
      $('a[href="#' + p + '=' + pageParams[p] + '"]').addClass('active');
    }
  }


  // fetch all data once for fast initial display
  var initialData = {svm: {}, nb: {}};
  var classes = ['hakaret', 'irkcilik', 'homofobi'];
  var classifiers = ['svm', 'nb'];
  classifiers.map(function(klassifier) {
    classes.map(function(klass) {
      $.get(baseUrl + createQuerystr({k: klass, t: klassifier}), function(data) {
        initialData[klassifier][klass] = mapLatLng(data.results);
      });
    });
  });
  window.initialData = initialData;


  // capture hash links
  $('a[href^=#]').click(function(e) {
    e.preventDefault();
    xhr.abort();
    var href = $(this).attr('href').substring(1);
    $.extend(pageParams, parseQuerystr(href));
    if (pageParams.q) {
      $('#loading-layer').show();
      fetchData();
    } else {
      heatmap.setData(initialData[pageParams.t][pageParams.k]);
    }
    window.location.hash = createQuerystr(pageParams);

    // set active class
    $(this).siblings().removeClass('active');
    $(this).addClass('active');
  });


  // keyword filter
  $('#keyword-filter').click(function(e) {
    e.preventDefault();
    var q = $('#keyword-input').val();
    if (q) {
      xhr.abort();
      pageParams.q = q;
      window.location.hash = createQuerystr(pageParams);
      $('#loading-layer').show();
      fetchData();
    }
  });


  var heatmap = new google.maps.visualization.HeatmapLayer({
    data: [],
    radius: 20,
    maxIntensity: 10
  });


  function renderMap() {
    var turkey = new google.maps.LatLng(38.611, 34.831);

    googleMap = new google.maps.Map($('#map-canvas')[0], {
      center: turkey,
      zoom: 6,
      mapTypeId: google.maps.MapTypeId.SATELLITE,
    });

    heatmap.setMap(googleMap);
  }


  function fetchData() {
    xhr = $.get(baseUrl + createQuerystr(pageParams), function(data) {
      heatmap.setData(mapLatLng(data.results));
      $('#loading-layer').hide();
    });
  }

  renderMap();
  fetchData();

  setInterval(fetchData, 3000);
  new Spinner(spinnerOpts).spin($('#spinner')[0]);
});
