"use strict"
function make_follow(username, isFollow) {
    var makeFollowUrl = $('#varibles').data('makeFollowUrl');
    var inProgress = false;

    if (!inProgress) {
        $.ajax({
            url: makeFollowUrl,
            method: 'POST',
            dataType: 'json',
            data: {"username": username,
                   "isFollow": isFollow},
            beforeSend: function() {
                inProgress = true;
            }
        }).done(function(data) {
            if (data.ok) {
                isFollow = data.isFollow;
                var id_follow = '#follow-' + username;
                var id_unfollow = '#unfollow-' + username;
                if (isFollow) {
                    $(id_follow).css("display", "none");
                    $(id_unfollow).css("display", "block");
                } else {
                    $(id_follow).css("display", "block");
                    $(id_unfollow).css("display", "none");
                }
            }
        }).always(function() {
            inProgress = false;
        });
    }
}
