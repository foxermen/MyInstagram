# coding=utf-8
from django.http import HttpResponse


def user(request, username, page='1'):
    return HttpResponse('%s %s' % (username, page))
