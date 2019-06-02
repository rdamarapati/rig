$(function () {
    $(".js-upload-photos").click(function () {
        $("#fileupload").click();
    });

    $("#fileupload").fileupload({
        dataType: 'json',
        done: function (e, data) {
              if (data.result.is_valid) {
                  $("#gallery tbody").prepend(
                      "<tr><td>" + data.result.name + "</td></tr>"
                  )
            }
        }
    });
});
