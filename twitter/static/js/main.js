$(function() {
  var heatmapData = [
    new google.maps.LatLng(39.903, 32.767),
    new google.maps.LatLng(39.903, 32.765),
    new google.maps.LatLng(39.903, 32.763),
    new google.maps.LatLng(39.903, 32.761),
    new google.maps.LatLng(39.903, 32.759),
    new google.maps.LatLng(39.903, 32.757),
    new google.maps.LatLng(39.903, 32.755),
    new google.maps.LatLng(39.906, 32.753),
    new google.maps.LatLng(39.906, 32.751),
    new google.maps.LatLng(39.906, 32.749),
    new google.maps.LatLng(39.906, 32.747),
    new google.maps.LatLng(39.906, 32.745),
    new google.maps.LatLng(39.906, 32.743),
    new google.maps.LatLng(39.906, 32.741),
    new google.maps.LatLng(37.906, 32.741)
  ];

  var sanFrancisco = new google.maps.LatLng(38.611, 34.831);

  var map = new google.maps.Map(document.getElementById('map-canvas'), {
    center: sanFrancisco,
    zoom: 6,
    mapTypeId: google.maps.MapTypeId.SATELLITE
  });

  var heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatmapData
  });

  heatmap.setMap(map);
});
