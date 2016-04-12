# coding=utf-8
from django.shortcuts import render, get_object_or_404
from MyInstagram.models import User, Post, Comment
from django.http import Http404

PER_PAGE = 10

def user_main(request, username, page='1'):
    try:
        p = int(page)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, username=username)
    posts = user.user_posts.all()[:]
    if p == 1 and len(posts) == 0:
        return render(request, 'user_profile.html', context={"username": username})

    if (p - 1) * PER_PAGE >= len(posts):
        raise Http404

    posts = posts[(p - 1) * PER_PAGE:p * PER_PAGE]
    return render(request, 'user_profile.html', context={"username": username, "posts": posts})


def user_post(request, post_id):
    try:
        id = int(post_id)
    except ValueError:
        raise Http404

    p = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post_id)[:]
    return render(request, 'user_post.html', context={"post": p, "comments": comments})


def user_subscriptions_or_subscribers(request, mode, username, page='1'):
    try:
        p = int(page)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, username=username)
    if mode == "subscriptions":
        list = user.subscriptions.all()[:]
    else:
        list = user.user_set.all()[:]
    subs = []
    for l in list:
        if l.username != username:
            subs.append(l)

    if p == 1 and len(subs) == 0:
        return render(request, 'user_subs.html', context={"mode": mode, "username": username, "subs": subs})

    if (p - 1) * PER_PAGE >= len(subs):
        raise Http404

    subs = subs[(p - 1) * PER_PAGE:p * PER_PAGE]

    return render(request, 'user_subs.html', context={"mode": mode, "username": username, "subs": subs})
