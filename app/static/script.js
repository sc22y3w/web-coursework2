$(document).ready(function() {
  var csrf_token = $('meta[name=csrf-token]').attr('content');

  // Set up AJAX to send the CSRF token with each request
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrf_token);
      }
    }
  });

  // init tablesorter plugin
  $(function() {
    $("#gamesList").tablesorter();
  });

  // like button
  $("a.like").on("click", function() {
    var self = $(this);
    var heart_icon = $(self.children()[0]);
    var like_count = $(self.children()[1]);

    var game_id = self.data("game_id");
    var action = self.data("action");

    // sending ajax request
    $.ajax({
      url: '/manage-likes',
      type: 'POST',
      data: JSON.stringify({
        game_id: game_id,
        action: action
      }),
      contentType: "application/json; charset=utf-8",
      datatype:"json",

      //update like count and button appearance
      success: function(response) {
        var json = JSON.parse(response);
        if(action === "add") {
          heart_icon.removeClass("fa-regular").addClass("fa-solid");
          heart_icon.attr('aria-label', 'Unlike');
          self.data("action", "remove");
        } else {
          heart_icon.addClass("fa-regular").removeClass("fa-solid");
          heart_icon.attr('aria-label', 'Like');
          self.data("action", "add");
        }

        like_count.text(json.new_like_count);
      },
      // debug purposes
      error: function(error) {
        alert("Error: " + error.status + ": " + error.responseText);
      }
    })
  })
});

document.onkeydown = (pressed) => {
  if (pressed.key === "Enter") {
    document.activeElement.click();
  }
}