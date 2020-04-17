var map;
var icon_base = DJANGO_STATIC_URL + '/img/map-markers/';

function reloadGeoJson(event) {
  date = $("#historic-date").val();
  if (date) {
    map.data.forEach(function (feature) {
      map.data.remove(feature);
    });
    map.data.loadGeoJson("/pothole-geojson/?active=true&date=" + date);
  } else {
    alert("Please specify a date");
  }
}

function initMap() {
  const infoWindow = new google.maps.InfoWindow();
  // centered on UNO
  // TODO: center according to where the user is actually located
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 41.258431, lng: -96.010453 },
    zoom: 16,
  });

  map.data.setStyle(function(feature) {
    let severity = feature.getProperty("severity");
    console.log(severity);
    let icon = icon_base;
    if (severity <= 2) {
      icon += 'map-marker-level-1.png';
    } else if (severity <= 3) {
      icon += 'map-marker-level-2.png';
    } else if (severity <= 4) {
      icon += 'map-marker-level-3.png';
    } else if (severity <= 5) {
      icon += 'map-marker-level-4.png';
    }

    return {icon: icon};
  });

  map.data.loadGeoJson("/pothole-geojson/?active=true");

  map.data.addListener("mouseover", function (event) {
    var feature = event.feature;
    var content =
      '<div class="pothole-info">' +
      "<p>Active since: " +
      feature.getProperty("effective_date") +
      "</br>" +
      "Severity: " +
      feature.getProperty("severity") +
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

$("#change-to-historic").bind("click", function () {
  $("#change-to-historic").replaceWith(
    `<a href="#" onclick="return reloadGeoJson(this)" id="load-historic" class="subheading-button">Load Historic View</a>`
  );
  $("#historic-label").replaceWith(`<p id="historic-label" class="alignleft">
                                    Select a date to view the past pothole status</p>`);
  // min should be set to the first date the application records pothole data for
  $("#historic-label").after(`<div class="historic-date-container">
                                <input type="date" id="historic-date" name="historic-date"
                                min="2020-04-01">
                              </div>`);
});
