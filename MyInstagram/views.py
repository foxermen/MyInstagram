# coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from MyInstagram.models import User, Post, Comment
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
import json

# must be div 3
PER_PAGE = 3


def user_main(request, username):
    user = get_object_or_404(User, username=username)

    posts_count = user.user_posts.count()
    subscriptions_count = user.subscriptions.count()
    subscribers_count = user.user_set.count()

    return render(request, 'user_profile.html', context={"username": username,
                                                         "user": user,
                                                         "posts_count": posts_count,
                                                         "subscriptions_count": subscriptions_count,
                                                         "subscribers_count": subscribers_count,
                                                         "PER_PAGE": PER_PAGE})


def user_post(request, post_id):
    try:
        id = int(post_id)
    except ValueError:
        raise Http404

    p = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post_id)
    return render(request, 'user_post.html', context={"post": p,
                                                      "comments": comments,})


def get_two_lists(list):
    list1 = []
    list2 = []
    i = 0
    for lst in list:
        if i % 2 == 0:
            list1.append(lst)
        else:
            list2.append(lst)
        i += 1

    return (list1, list2)


def user_following(request, username):
    user = get_object_or_404(User, username=username)
    list = user.subscriptions.all()
    list1, list2 = get_two_lists(list=list)

    return render(request, 'user_following.html', context={"username": username,
                                                           "list1": list1,
                                                           "list2": list2,})


def user_followers(request, username):
    user = get_object_or_404(User, username=username)
    list = user.user_set.all()
    list1, list2 = get_two_lists(list=list)

    return render(request, 'user_followers.html', context={"username": username,
                                                           "list1": list1,
                                                           "list2": list2,})


def post_likes(request, post_id):
    try:
        id = int(post_id)
    except ValueError:
        raise Http404
    post = get_object_or_404(Post, id=id)
    list = post.like_users.all()
    list1, list2 = get_two_lists(list=list)

    return render(request, 'post_likes.html', context={"post": post,
                                                       "list1": list1,
                                                       "list2": list2,})


@csrf_exempt
def next_posts(request):
    if request.is_ajax():
        if request.method == 'POST':
            try:
                start = int(request.POST['startFrom'])
            except ValueError:
                raise Http404
            username = request.POST['username']
            user = get_object_or_404(User, username=username)
            posts = user.user_posts.all()[start:start + PER_PAGE]
            pst = []
            for post in posts:
                pst.append({"id": post.id,
                            "photo_url": post.photo.photo.url,
                            "like_users_count": post.like_users.count(),
                            "comments_count": post.comments.count(),
                            "post_url": reverse("MyInstagram_post_url", kwargs={"post_id": post.id})})
            json_data = json.dumps(pst)
            return HttpResponse(json_data, content_type='application/json')
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=400)