"use strict"
$(document).ready(function(){
    var inProgress = false;
    var startFrom = 0;
    var perPage = $('#varibles').data('perPage');
    var nextPostsUrl = $('#varibles').data('nextPostsUrl');
    var username = $('#varibles').data('username');
    var timerId;

    function reaction() {
        if (($(window).scrollTop() + $(window).height() >= $(document).height() - 200) && !inProgress) {
            $.ajax({
                url: nextPostsUrl,
                method: 'POST',
                dataType: 'json',
                data: {"startFrom": startFrom,
                       "username": username},
                beforeSend: function() {
                    inProgress = true;
                }
            }).done(function(data) {
                if (data.length > 0) {
                    var s = ""
                    $.each(data, function(index, post) {
                        if (index % 3 == 0) {
                            s += '<div class="row text-center">';
                        }
                        s += '<div class="col-md-4 text-center"><a href="' + post.post_url + '"><img src="' + post.photo_url + '" alt="' + username + ' post ' + post.id + '" class="img-thumbnail" style="height: 250px; width: 250px;"  /><br /><p><span class="glyphicon glyphicon-heart"></span> ' + post.like_users_count + '  <span class="glyphicon glyphicon-comment"></span> ' + post.comments_count + '</p></a></div>';
                        if (index % 3 == 2) {
                            s += "</div>";
                            $("#photos").append(s);
                            s = "";
                        }
                    });
                    if (s != "") {
                        s += "</div>";
                        $("#photos").append(s);
                        s = "";
                    }
                }
                startFrom += perPage;
            }).always(function(){
                inProgress = false;
            });
            if ($(window).height() < $(document).height() - 200 && !(timerId === undefined)) {
                clearInterval(timerId);
                timerId = undefined;
            }
        }
    }

    timerId = setInterval(reaction, 100);
    $(window).scroll(reaction);
});