$(function() {
  var baseUrl = '/points.json?k=';
  var googleMap;
  var xhr;
  var klass = window.location.hash.substring(1) || 'hakaret';

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
    var url = baseUrl + klass;
    xhr = $.get(url, function(data) {
      setTopicData(klass, data);
      heatmap.setData(mapLatLng(data.results));
    });
  }

  window.addEventListener("hashchange", function(e) {
    klass = window.location.hash.substring(1);
    xhr.abort();
    heatmap.setData(mapLatLng(initialPointsData[klass]));
    fetchData();
  }, false);

  renderMap();
  fetchData();

  setInterval(fetchData, 3000);
});
