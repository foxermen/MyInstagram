"use strict"
$(document).ready(function() {
    var send_url = $('#varibles').data('sendUrl');
    var photo_id = 0;

    $('#photo-input').change(function(){
        var xhr = new XMLHttpRequest();
        var data = new FormData($('#upload-form')[0]);

        $('#progress-upload').attr("value", "0");
        $('#progress-upload').css("display", "block");

        data.append("photo_id", photo_id)

        xhr.upload.addEventListener("progress", function (evt) {
            if (evt.lengthComputable) {
                var progress = Math.round(evt.loaded * 100 / evt.total);
                $('#progress-upload').attr("value", progress + "");
            }
        }, false);

        xhr.open("POST", send_url);
        xhr.send(data);

        xhr.onreadystatechange = function() {
            if (xhr.readyState != xhr.DONE) {
                return ;
            }
            $('#progress-upload').css("display", "none");

            var data = JSON.parse(xhr.responseText);
            if (data.ok) {
                $('#errors').text("");
                $('#errors').css('display', 'none');
                $('#div-image').css('display', 'block');
                $('#id_id').val(data.photo_id);
                $('#crop').text("");
                $('#crop').append('<img id="image" src="' + data.photo_url + '" />');

                var setCoordinates = function(c) {
                    $('#id_x1').val(c.x);
                    $('#id_y1').val(c.y);
                    $('#id_x2').val(c.x2);
                    $('#id_y2').val(c.y2);
                    $('#id_w').val(c.w);
                    $('#id_h').val(c.h);
                };

                $('#image').Jcrop({
                    onChange: setCoordinates,
                    onSelect: setCoordinates,
                    aspectRatio: 1,
                    minSize: [400, 400],
                    maxSize: [1080, 1080],
                    setSelect: [0, 0, 400, 400],
                    canDelete: false,
                    allowSelect: false,
                });
                photo_id = data.photo_id

            } else {
                $('#errors').css('display', 'block');
                $('#errors').text("");
                $('#errors').append("<h3>" + data.error + "</h3>");
                $('#div-image').css('display', 'none');
                photo_id = 0;
            }
        };
    });
});