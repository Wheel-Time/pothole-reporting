var lat, lon, map, infoWindow, latLng;
var icon_base = DJANGO_STATIC_URL + '/img/map-markers/';
var activeFeature = null;

function reloadGeoJson() {
  map.data.forEach(function(feature) {
    map.data.remove(feature);
  });
  map.data.loadGeoJson("/pothole-geojson/?active=false");
  map.data.setStyle(function(feature) {
    let active = feature.getProperty("active");
    let fixed = feature.getProperty("fixed");
    let icon = icon_base;
    if (active) {
      icon += 'map-marker-confirmed.png';
    } else if (fixed) {
      icon += 'map-marker-fixed.png';
    } else {
      icon += 'map-marker-unconfirmed.png';
    }

    return {icon: icon};
  });
}

// get the cookie in order to extract information, such as the csrf token
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == name + "=") {
        cookieValue = decodeURIComponent(
          cookie.substring(name.length + 1)
        );
        break;
      }
    }
  }
  return cookieValue;
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
  return `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()} (${daysSince})`;
}

function initMap(latlng={ lat: 41.258431, lng: -96.010453 }) {
  map = new google.maps.Map(document.getElementById("map"), {
    center: latlng,
    zoom: 16,
  });

  reloadGeoJson();
  infoWindow = new google.maps.InfoWindow();

  // Configure the click listener.
  map.addListener("click", function (mapsMouseEvent) {
    // Close the current InfoWindow.
    activeFeature = null;
    infoWindow.close();

    var content =
    `<div class="submission-window">
      <h4>Submit a new Pothole</h4>
      <form 
      id="pothole-form"
      action="{% url "submit" %}"
      method="post">
        <div id="severity">
          <label class="select-label">Severity:</label>
          <select id="state-select" name="state" size="5">
            <option class="severity-select" id="select-1" value=1>1</option>
            <option class="severity-select" id="select-2" value=2>2</option>
            <option class="severity-select" id="select-3" value=3>3</option>
            <option class="severity-select" id="select-4" value=4>4</option>
            <option class="severity-select" id="select-5" value=5>5</option>
          </select>
        </div>
        <br/>
        <input onclick="return onSubmit(this);" class="alignright" id="submit-button" type="submit" value="Submit pothole"/>
      </form>
    </div>`;

    // Create a new InfoWindow.
    infoWindow = new google.maps.InfoWindow({
      position: mapsMouseEvent.latLng,
    });

    infoWindow.setContent(content);
    latLng = mapsMouseEvent.latLng;
    lat = latLng.lat();
    lon = latLng.lng();

    infoWindow.open(map);
  });

  // Configure the mouseover listener
  map.data.addListener("mouseover", function (event) {
    var feature = event.feature;
    activeFeature = feature;
    var content =
      "<div class='pothole-info' id='pothole-" + feature.getId() + "'>" +
      '<div class="row">';
    if (feature.getProperty("active")) {
      content +=
      "<p>Active since: " +
      formatPotholeDate(feature.getProperty("effective_date")) +
      "</p>";
    } else if (feature.getProperty("fixed")) {
      content +=
      "<p>Fixed since: " +
      formatPotholeDate(feature.getProperty("fixed_date")) +
      "</p>";
    } else {
      // create_date is a mysql datetime, so must remove timezone information
      var dateNoTZ = feature.getProperty("create_date").split(/[+]/)[0]
      content +=
      "<p>Submitted: " +
      formatPotholeDate(dateNoTZ) +
      "</p>";
    }
    content +=
      `<p class="alignleft">Confirmations: ${feature.getProperty("pothole_reports")}
      </p>
      <p class="alignright">Fixed: ${feature.getProperty("fixed_reports")}
      </p>
      </div>
      <div class='row'>
        <input onclick="return onConfirm(this);" class="alignleft" id="confirm-button" type="submit" value="Confirm"/>
        <input onclick="return onUpdate(this, true);" class="alignright" id="fixed-button" type="submit" value="Fixed"/>
      </div>
      </div>`;
    infoWindow.setContent(content);
    infoWindow.setPosition(event.feature.getGeometry().get());
    infoWindow.setOptions({ pixelOffset: new google.maps.Size(0, -30) });
    infoWindow.open(map);
  });
}

function onConfirm(event) {
  let content =
      `<div class="submission-window">
        <h4>Confirm this Pothole</h4>
        <div id="severity">
          <label class="select-label">Severity:</label>
          <select id="state-select" name="state" size="5">
            <option class="severity-select" id="select-1" value=1>1</option>
            <option class="severity-select" id="select-2" value=2>2</option>
            <option class="severity-select" id="select-3" value=3>3</option>
            <option class="severity-select" id="select-4" value=4>4</option>
            <option class="severity-select" id="select-5" value=5>5</option>
          </select>
        </div>
        <br/>
        <input onclick="return onUpdate(this);" class="alignright" id="submit-button" type="submit" value="Confirm pothole"/>
      </div>`;
  $(event).parent().parent().html(content)
}

function onUpdate(event, fixed=false) {
  let potholeData;
  if (fixed) {
    potholeData = {
      pothole_id: activeFeature.getId(),
      state: 0,
    }
  } else {
    potholeData = {
      pothole_id: activeFeature.getId(),
      state: $("#state-select").val(),
    }
  }

  $.ajax({
    type: "POST",
    url: "/update/",
    data: potholeData,
    beforeSend: function (xhr, settings) {
      // add the csrf token to the submission header
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },
    success: function (data) {
      reloadGeoJson();
      alert("Success");
      infoWindow.close();
    },
    error: function (data) {
      alert(
        "Failure, please make sure you have selected a severity level for this pothole"
      );
    },
  });
}

function onSubmit(event) {
  //Append lat, long, and csrf token from click to form submission
  $("#pothole-form").submit(function (event) {
    event.preventDefault();

    var potholeData = {
      state: $("#state-select").val(),
      lat: lat,
      lon: lon,
    };

    $.ajax({
      type: "POST",
      url: "/submit/",
      data: potholeData,
      beforeSend: function (xhr, settings) {
        // add the csrf token to the submission header
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      success: function (data) {
        reloadGeoJson();
        alert("Success");
        infoWindow.close();
      },
      error: function (data) {
        alert(
          "Failure, please make sure you have selected a severity level for this pothole"
        );
      },
    });
  });
}
