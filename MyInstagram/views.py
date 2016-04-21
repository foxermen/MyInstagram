# coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from MyInstagram.models import User, Post, Comment
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
import json

PER_PAGE = 9


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


def user_subscriptions_or_subscribers(request, mode, username, page='1'):
    try:
        p = int(page)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, username=username)
    if mode == "subscriptions":
        list = user.subscriptions.all()
    else:
        list = user.user_set.all()
    subs = []
    for l in list:
        if l.username != username:
            subs.append(l)

    if p == 1 and len(subs) == 0:
        return render(request, 'user_subs.html', context={"mode": mode,
                                                          "username": username,
                                                          "subs": subs})

    if (p - 1) * PER_PAGE >= len(subs):
        raise Http404

    next_page = p * PER_PAGE < len(subs)
    subs = subs[(p - 1) * PER_PAGE:p * PER_PAGE]

    return render(request, 'user_subs.html', context={"mode": mode,
                                                      "username": username,
                                                      "subs": subs,
                                                      "page": p,
                                                      "next_page": next_page})


def post_likes(request, post_id):
    try:
        id = int(post_id)
    except ValueError:
        raise Http404
    post = get_object_or_404(Post, id=id)
    likes = post.like_users.all()
    likes1 = []
    likes2 = []
    print likes.count()
    i = 0
    for like in likes:
        if i % 2 == 0:
            likes1.append(like)
        else:
            likes2.append(like)
        i += 1

    return render(request, 'post_likes.html', context={"post": post,
                                                       "likes1": likes1,
                                                       "likes2": likes2,})


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