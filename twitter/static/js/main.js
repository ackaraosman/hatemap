$(function() {
  var googleMap;
  var klass = window.location.hash.substring(1) || 'hakaret';

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
    var url = '/points.json?k=' + klass;
    $.get(url, function(data) {
      var heatmapData = data.results.map(function(item) {
        return new google.maps.LatLng(item[1], item[0]);
      });
      heatmap.setData(heatmapData);
    });
  }

  window.addEventListener("hashchange", function(e) {
    klass = window.location.hash.substring(1);
    fetchData();
  }, false);

  renderMap();
  fetchData();

  setInterval(fetchData, 3000);
});
