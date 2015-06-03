$(function() {
  var baseUrl = '/points.json';
  var googleMap;
  var xhr;
  var klass = getKlass(window.location.hash.substring(1));
  var klassType = getKlassType(window.location.hash.substring(1));
  setActive(klass);

  var initialPointsData = {};
  var setTopicData = function(topic, data) {
    initialPointsData[topic] = data.results;
  };

  var topics = ['hakaret', 'irkcilik', 'homofobi'];
  for (var i = 0; i < topics.length; i++) {
    $.get(baseUrl + topics[i], setTopicData.bind(this, topics[i]));
  }

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

  function mapLatLng(items) {
    return items.map(function(item) {
      return new google.maps.LatLng(item[1], item[0]);
    });
  }

  function fetchData() {
    var url = baseUrl + '?k=' + klass + '&t=' + klassType;
    xhr = $.get(url, function(data) {
      setTopicData(klass, data);
      heatmap.setData(mapLatLng(data.results));
    });
  }

  function getKlass(hash) {
    if (!hash) {
      return 'hakaret';
    }
    if (hash.indexOf('&') > -1) {
      return hash.split('&')[0];
    }
    return hash;
  }

  function getKlassType(hash) {
    if (!hash) {
      return 'nb';
    }
    if (hash.indexOf('&') > -1) {
      return hash.split('&')[1];
    }
    return hash;
  }

  window.addEventListener("hashchange", function(e) {
    klass = getKlass(window.location.hash.substring(1));
    klassType = getKlassType(window.location.hash.substring(1));
    xhr.abort();
    setActive(klass);
    heatmap.setData(mapLatLng(initialPointsData[klass]));
    fetchData();
  }, false);

  function setActive(topic) {
    $('#classifications-layer a.active').removeClass('active');
    $('a[href="#' + topic + '"]').addClass('active');
  }

  renderMap();
  fetchData();

  setInterval(fetchData, 3000);
});
