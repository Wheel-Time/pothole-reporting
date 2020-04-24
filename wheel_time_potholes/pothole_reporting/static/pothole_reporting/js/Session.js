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

$("#logout-button").bind("click", function () {
  $.ajax({
    type: "POST",
    url: "/logout/",
    beforeSend: function (xhr, settings) {
      // add the csrf token to the submission header
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },
    success: function (data) {
      alert("Successfully logged out");
      $("#logout-button").replaceWith(`<li><a href="/signup/">Sign up</a></li>`)
    },
    error: function (data) {
      alert("Failed to log out");
    },
  });
})
