var lat, lon, map, infoWindow, latLng;


function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 41.258431, lng: -96.010453 },
    zoom: 16,
  });

  // Configure the click listener.
  infoWindow = new google.maps.InfoWindow();
  map.addListener("click", function (mapsMouseEvent) {
    // Close the current InfoWindow.
    infoWindow.close();

    var content =
      '<div class="submission-window">' +
      "<h4>Submit a new Pothole</h4>" +
      "<form " +
      'id="pothole-form" ' +
      'action="/submit/" ' +
      'method="post"' +
      ">" +
      '<div id="severity">' +
      '<label class="select-label">Severity:</label>' +
      '<select id="state-select" name="state" size="5">' +
      '<option class="severity-select" id="select-1" value=1>1</option>' +
      '<option class="severity-select" id="select-2" value=2>2</option>' +
      '<option class="severity-select" id="select-3" value=3>3</option>' +
      '<option class="severity-select" id="select-4" value=4>4</option>' +
      '<option class="severity-select" id="select-5" value=5>5</option>' +
      "</select>" +
      "</div>" +
      "<br/>" +
      '<input onclick="return onSubmit(this);" class="alignright" id="submit-button" type="submit" value="Submit pothole"/>' +
      "</form>" +
      "</div>";

    // Create a new InfoWindow.
    infoWindow = new google.maps.InfoWindow({
      position: mapsMouseEvent.latLng,
    });

    infoWindow.setContent(content);
    latLng = mapsMouseEvent.latLng
    lat = latLng.lat();
    lon = latLng.lng();

    infoWindow.open(map);
  });
}


function placeMarker(location) {
  var marker = new google.maps.Marker({
      position: location, 
      map: map
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
    }

    $.ajax({
      type: 'POST',
      url: '/submit/',
      data: potholeData,
      beforeSend: function (xhr, settings) {
        // get the cookie in order to extract the csrf token
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
        // add the csrf token to the submission header
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      success: function (data) {
        alert("Success");
        placeMarker(latLng);
        infoWindow.close();
      },
      error: function(data) {
        alert("Failure, please make sure you have selected a severity level for this pothole");
      }

    })
  });
}
