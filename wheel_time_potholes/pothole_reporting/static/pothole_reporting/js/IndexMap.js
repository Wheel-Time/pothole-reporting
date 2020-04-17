var map;
var icon_base = DJANGO_STATIC_URL + "/img/map-markers/";

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

function formatPotholeDate(timestamp) {
  // All dates are handled in UTC time
  var dateElements = timestamp.split(/[- :]/);
  var date = new Date(
    Date.UTC(
      dateElements[0],
      dateElements[1] - 1,
      dateElements[2],
      dateElements[3],
      dateElements[4],
      dateElements[5]
    )
  );

  // compute number of days between submission and current date
  var today = Date.now();
  var differenceTime = today - date.getTime();
  var differenceDays = parseInt(differenceTime / (1000 * 3600 * 24));

  var daysSince;
  if (differenceDays == 0) {
    daysSince = "today";
  } else if (differenceDays == 1) {
    daysSince = "1 day ago";
  } else {
    daysSince = differenceDays + " days ago";
  }
  return `${date.getMonth()}/${date.getDate()}/${date.getFullYear()} (${daysSince})`;
}

function initMap() {
  const infoWindow = new google.maps.InfoWindow();
  // centered on UNO
  // TODO: center according to where the user is actually located
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 41.258431, lng: -96.010453 },
    zoom: 16,
  });

  map.data.setStyle(function (feature) {
    let severity = feature.getProperty("severity");
    let icon = icon_base;
    if (severity <= 2) {
      icon += "map-marker-level-1.png";
    } else if (severity <= 3) {
      icon += "map-marker-level-2.png";
    } else if (severity <= 4) {
      icon += "map-marker-level-3.png";
    } else if (severity <= 5) {
      icon += "map-marker-level-4.png";
    }

    return { icon: icon };
  });

  map.data.loadGeoJson("/pothole-geojson/?active=true");

  map.data.addListener("mouseover", function (event) {
    var feature = event.feature;
    var content = 
      `<div class="pothole-info">
        <p>
          <span>Active since: ${formatPotholeDate(feature.getProperty("effective_date"))}</span>
          </br></br>
          <span>Severity: ${feature.getProperty("severity")}</span>
        </p>
        <p class="alignleft">Confirmations: ${feature.getProperty("pothole_reports")} 
        </p>
        <p class="alignright">Fixed: ${feature.getProperty("fixed_reports")}
        </p>
      </div>`;
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
