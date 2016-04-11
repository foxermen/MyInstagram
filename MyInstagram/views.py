# coding=utf-8
from django.http import HttpResponse


def user_main(request, username, page='1'):
    return HttpResponse('%s %s' % (username, page))


def user_post(request, username, post_id):
    pass


def user_subscriptions_or_subscribers(request, mode, username, page='1'):
    pass
