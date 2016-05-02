"use strict"
$(document).ready(function(){
    var isLike = $('#varibles').data('isLike');
    var inProgressLike = false;
    var inProgressComment = false;
    var makeLikeUrl = $('#varibles').data('makeLikeUrl');
    var addCommentUrl = $('#varibles').data('addCommentUrl');
    var getCommentsUrl = $('#varibles').data('getCommentsUrl');
    var postId = $('#varibles').data('postId');
    var timerId;

    $('#like-button').click(function(){
        if (!inProgressLike) {
            $.ajax({
                url: makeLikeUrl,
                method: 'POST',
                dataType: 'json',
                data: {"isLike": isLike,
                       "postId": postId},
                beforeSend: function() {
                    inProgressLike = true;
                }
            }).done(function(data) {
                if (data.ok) {
                    isLike = data.isLike;
                    var text = " " + data.count + " likes";
                    $('#like-text').text(text);
                    var color = "silver";
                    if (isLike) {
                        color = "red";
                    }
                    $('#like-button-color').css("color", color);
                }
            }).always(function(){
                inProgressLike = false;
            });
        }
    });

    $('#comment-button').click(function(){
        var text = $('#comment-text').val();
        if (!inProgressComment && text.length > 0) {
            $.ajax({
                url: addCommentUrl,
                method: 'POST',
                dataType: 'json',
                data: {"text": text,
                       "postId": postId},
                beforeSend: function() {
                    inProgressComment = true;
                    $('#comment-text').val("");
                }
            }).done(function(data) {
                if (data.ok) {
                    $('#comments').append('<p><a href="' + data.user_url + '">' + data.username + '</a> ' + data.text + '</p>');
                    var commentsText = " " + data.count + " comments";
                    $('#comments-text').text(commentsText);
                }
            }).always(function(){
                inProgressComment = false;
            });
        }
    });

    function get_comments() {
        $.ajax({
            url: getCommentsUrl,
            method: 'POST',
            dataType: 'json',
            data: {"postId": postId}
        }).done(function(data){
            if (data.length > 0) {
                var s = ""
                $.each(data, function(index, post) {
                    s += ('<p><a href="' + post.user_url + '">' + post.username + '</a> ' + post.text + '</p>');
                });
                $('#comments').text("");
                $('#comments').append(s);
            }
            var count = data.length;
            if (count === undefined) {
                count = 0;
            }
            var commentsText = " " + count + " comments";
            $('#comments-text').text(commentsText);
        });
    }

    get_comments();
    timerId = setInterval(get_comments, 5000);
});