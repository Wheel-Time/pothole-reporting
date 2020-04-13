function initMap() {
  const infoWindow = new google.maps.InfoWindow();
  // centered on UNO
  // TODO: center according to where the user is actually located
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 41.258431, lng: -96.010453 },
    zoom: 16,
  });

  map.data.setStyle({
    icon: DJANGO_STATIC_URL + "/img/map-markers/map-marker-confirmed.png",
  });

  map.data.loadGeoJson("/pothole-geojson/?active=true");

  map.data.addListener("mouseover", function (event) {
    var feature = event.feature;
    var content =
      '<div class="pothole-info">' +
      "<p>Active since: " +
      feature.getProperty("effective_date") +
      "</p>" +
      '<p class="alignleft">Confirmations: ' +
      feature.getProperty("pothole_reports") +
      "</p>" +
      '<p class="alignright">Fixed: ' +
      feature.getProperty("fixed_reports") +
      "</p>" +
      "</div>";
    infoWindow.setContent(content);
    infoWindow.setPosition(event.feature.getGeometry().get());
    infoWindow.setOptions({ pixelOffset: new google.maps.Size(0, -30) });
    infoWindow.open(map);
  });
}
