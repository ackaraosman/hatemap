$(function() {
  var googleMap;
  var oldLayer;

  function renderMap() {
    var turkey = new google.maps.LatLng(38.611, 34.831);

    googleMap = new google.maps.Map($('#map-canvas')[0], {
      center: turkey,
      zoom: 6,
      mapTypeId: google.maps.MapTypeId.SATELLITE
    });
  }

  renderMap();

  setInterval(function() {
    $.get('/points.json', function(data) {
      var heatmapData = data.results.map(function(item) {
        return new google.maps.LatLng(item[1], item[0]);
      });
      renderHeatmap(heatmapData);
    });
  }, 5000);

  function renderHeatmap(heatmapData) {
    var heatmap = new google.maps.visualization.HeatmapLayer({
      data: heatmapData
    });
    if (oldLayer) {
      oldLayer.setMap(null);
    }
    heatmap.setMap(googleMap);
    oldLayer = heatmap;
  }
});
