# coding=utf-8
from django.shortcuts import render, get_object_or_404
from MyInstagram.models import User, Post
from django.http import Http404


def user_main(request, username, page='1'):
    try:
        p = int(page)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, username=username)
    posts = user.user_posts.all()[:]
    if p == 1 and len(posts) == 0:
        return render(request, 'user_profile.html', context={"username": username, "empty_posts": True})

    if (p - 1) * 10 >= len(posts):
        raise Http404

    posts = posts[(p - 1) * 10:p * 10]
    return render(request, 'user_profile.html', context={"username": username, "posts": posts, "empty_posts": False})


def user_post(request, post_id):
    try:
        id = int(post_id)
    except ValueError:
        raise Http404

    p = get_object_or_404(Post, id=id)
    return render(request, 'user_post.html', context={"post": p})


def user_subscriptions_or_subscribers(request, mode, username, page='1'):
    pass
