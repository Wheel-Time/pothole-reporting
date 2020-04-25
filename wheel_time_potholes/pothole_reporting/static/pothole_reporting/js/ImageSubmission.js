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


$("#submit-image-form").submit(function (event) {
  event.preventDefault();

  var form = $('#submit-image-form')[0];
  var data = new FormData(form);
  
  $.ajax({
    type: "POST",
    url: "/submit/image",
    data: data,
    processData: false,
    contentType: false,
    cache: false,
    timeout: 600000,
    beforeSend: function (xhr, settings) {
      // add the csrf token to the submission header
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },
    success: function (data) {
      alert("Successfully created a new pothole");
      $("#submit-image-form")[0].reset();
    },
    error: function (data) {
      alert(data.responseText);
    },
  });
});

