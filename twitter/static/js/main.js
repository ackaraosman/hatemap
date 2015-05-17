$(function() {
  $.get('/points.json', function(data) {
    var heatmapData = data.results.map(function(item) {
      return new google.maps.LatLng(item[1], item[0]);
    });
    renderHeatmap(heatmapData);
  });


  function renderHeatmap(heatmapData) {
    var turkey = new google.maps.LatLng(38.611, 34.831);

    var map = new google.maps.Map($('#map-canvas')[0], {
      center: turkey,
      zoom: 6,
      mapTypeId: google.maps.MapTypeId.SATELLITE
    });

    var heatmap = new google.maps.visualization.HeatmapLayer({
      data: heatmapData
    });

    heatmap.setMap(map);
  }
});
