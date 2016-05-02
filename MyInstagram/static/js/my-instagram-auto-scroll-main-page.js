"use strict"
$(document).ready(function(){
    var inProgress = false;
    var startFrom = 0;
    var perPage = $('#varibles').data('perPage');
    var nextPostsUrl = $('#varibles').data('nextPostsUrl');
    var timerId;

    function reaction() {
        if (($(window).scrollTop() + $(window).height() >= $(document).height() - 200) && !inProgress) {
            $.ajax({
                url: nextPostsUrl,
                method: 'POST',
                dataType: 'json',
                data: {"startFrom": startFrom},
                beforeSend: function() {
                    inProgress = true;
                }
            }).done(function(data) {
                if (data.length > 0) {
                    $.each(data, function(index, post) {
                        var s = '<div class="row text-center" style="margin-top: 30px;">\
                                <div class="col-md-3">\
                                </div>\
                                <div class="col-md-6" style="border: 1px solid #edeeee;\
                                                             width: 600px;\
                                                             padding-left: 0px;\
                                                             padding-right: 0px;">\
                                    <div class="row">\
                                        <div class="col-md-8 text-left" style="padding-left: 25px;">\
                                            <h3 style="margin-top: 10px;">\
                                                <a href="' + post.create_user_url + '">' + post.create_username + '</a>\
                                            </h3>\
                                        </div>\
                                        <div class="col-md-4" style="padding-left: 40px; padding-top: 12px;">\
                                            <a href="' + post.post_url + '">\
                                                ' + post.date_time + '\
                                            </a>\
                                        </div>\
                                    </div>\
                                    <a href="' + post.post_url + '">\
                                        <img src="' + post.photo_url + '" style="height: 600px;\
                                                                                     width: 600px;\
                                                                                     border: 1px solid #edeeee;" />\
                                        <h3 style="margin-top: 10px;">\
                                            <span class="glyphicon glyphicon-heart"></span>' + post.like_users_count + '\
                                            <span class="glyphicon glyphicon-comment"></span>' + post.comments_count + '\
                                        </h3>\
                                    </a>\
                                </div>\
                                <div class="col-md-3">\
                                </div>\
                            </div>'
                        $('#posts').append(s);
                    });
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
