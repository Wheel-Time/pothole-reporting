var map;
function initMap() {
  // centered on downtown Omaha
  // TODO: center according to where the user is actually located
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 41.2565, lng: -95.9345 },
    zoom: 16
  });
}
