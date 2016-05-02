# coding=utf-8
import datetime
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from MyInstagram.models import User, Post, Comment, City, Photo
from django.contrib import auth
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from MyInstagram.forms import LoginForm, RegisterForm, NewPostForm
from django.core.exceptions import ValidationError
import json

# must be div 3
PER_PAGE = 9
PER_PAGE_MAIN = 5


def user_main(request, username):
    user = get_object_or_404(User, username=username)

    posts_count = user.user_posts.count()
    subscriptions_count = user.subscriptions.count() - 1
    subscribers_count = user.user_set.count() - 1

    return render(request, 'user_profile.html', context={"page_user": user,
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

    is_like = False
    if request.user.is_authenticated and request.user in p.like_users.all():
        is_like = True

    return render(request, 'user_post.html', context={"post": p,
                                                      "is_like": is_like})


def get_two_lists(list, followers_list, user=None, s=True):
    list1 = []
    list2 = []
    i = 0
    for lst in list:
        if not s and lst.id == user.id:
            continue
        if i % 2 == 0:
            list1.append({"user": lst,
                          "follow": lst in followers_list,})
        else:
            list2.append({"user": lst,
                          "follow": lst in followers_list,})
        i += 1

    return (list1, list2)


def user_following(request, username):
    user = get_object_or_404(User, username=username)
    list = user.subscriptions.all()
    list1, list2 = get_two_lists(list=list, followers_list=user.subscriptions.all(), user=user, s=False)

    return render(request, 'user_following.html', context={"username": username,
                                                           "list": [list1, list2],})


def user_followers(request, username):
    user = get_object_or_404(User, username=username)
    list = user.user_set.all()
    list1, list2 = get_two_lists(list=list, followers_list=user.subscriptions.all(), user=user, s=False)

    return render(request, 'user_followers.html', context={"username": username,
                                                           "list": [list1, list2],})


def post_likes(request, post_id):
    try:
        id = int(post_id)
    except ValueError:
        raise Http404
    post = get_object_or_404(Post, id=id)
    list = post.like_users.all()
    list1, list2 = get_two_lists(list=list, followers_list=post.user.subscriptions.all())

    return render(request, 'post_likes.html', context={"post": post,
                                                       "list": [list1, list2],})


@csrf_exempt
@require_POST
def next_posts(request):
    if request.is_ajax():
        if request.POST.__contains__('startFrom') and request.POST.__contains__('username'):
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
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


@csrf_exempt
@require_POST
def next_posts_main(request):
    if request.is_ajax() and request.user.is_authenticated():
        if request.POST.__contains__('startFrom'):
            try:
                start = int(request.POST['startFrom'])
            except ValueError:
                raise Http404
            following = request.user.subscriptions.all()
            query = Q()
            for f in following:
                query = query | Q(user=f.id)
            posts = Post.objects.filter(query)[start:start + PER_PAGE_MAIN]
            pst = []
            for post in posts:
                pst.append({"photo_url": post.photo.photo.url,
                            "create_user_url": reverse("MyInstagram_user_url", kwargs={"username": post.user.username}),
                            "create_username": post.user.username,
                            "date_time": datetime.datetime.strftime(post.date_time, "%d %b %Y, %H:%M:%S"),
                            "like_users_count": post.like_users.count(),
                            "comments_count": post.comments.count(),
                            "post_url": reverse("MyInstagram_post_url", kwargs={"post_id": post.id})})
            json_data = json.dumps(pst)
            return HttpResponse(json_data, content_type='application/json')
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


@csrf_exempt
@require_POST
def make_like(request):
    if request.is_ajax() and request.user.is_authenticated():
        if request.POST.__contains__('isLike') and request.POST.__contains__('postId'):
            is_like = False
            if request.POST["isLike"] == "True" or request.POST["isLike"] == "true":
                is_like = True
            try:
                post_id = int(request.POST["postId"])
            except ValueError:
                raise Http404
            post = get_object_or_404(Post, id=post_id)
            if is_like:
                if post.like_users.filter(user=request.user).count() == 1:
                    post.like_users.remove(request.user)
                    is_like = False
                else:
                    return HttpResponseBadRequest()
            else:
                if post.like_users.filter(user=request.user).count() > 0:
                    return HttpResponseBadRequest()
                else:
                    post.like_users.add(request.user)
                    is_like = True
            json_data = json.dumps({"count": post.like_users.count(),
                                    "isLike": is_like,
                                    "ok": True})
            return HttpResponse(json_data, content_type='application/json')
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


@csrf_exempt
@require_POST
def make_follow(request):
    if request.is_ajax() and request.user.is_authenticated():
        if request.POST.__contains__('isFollow') and request.POST.__contains__('username'):
            is_follow = False
            if request.POST["isFollow"] == "True" or request.POST["isFollow"] == "true":
                is_follow = True
            username = request.POST["username"]
            user = get_object_or_404(User, username=username)
            if is_follow:
                if request.user.subscriptions.filter(id=user.id).count() == 1:
                    request.user.subscriptions.remove(user)
                    is_follow = False
                else:
                    return HttpResponseBadRequest()
            else:
                if request.user.subscriptions.filter(id=user.id).count() > 0:
                    return HttpResponseBadRequest()
                else:
                    request.user.subscriptions.add(user)
                    is_follow = True
            json_data = json.dumps({"isFollow": is_follow,
                                    "ok": True})
            return HttpResponse(json_data, content_type='application/json')
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


@csrf_exempt
@require_POST
def add_comment(request):
    if request.is_ajax() and request.user.is_authenticated():
        if request.POST.__contains__('text') and request.POST.__contains__('postId'):
            text = request.POST["text"]
            if not text or len(text) > 1000:
                return HttpResponseBadRequest()
            try:
                post_id = int(request.POST["postId"])
            except ValueError:
                raise Http404
            post = get_object_or_404(Post, id=post_id)
            comment = Comment(user=request.user, post=post, text=text)
            comment.save()

            json_data = json.dumps({"ok": True,
                                    "user_url": reverse("MyInstagram_user_url", kwargs={"username": request.user.username}),
                                    "username": request.user.username,
                                    "text": text,
                                    "count": post.comments.count()})
            return HttpResponse(json_data, content_type='application/json')
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


@csrf_exempt
@require_POST
def get_comments(request):
    if request.is_ajax():
        if request.POST.__contains__('postId'):
            try:
                post_id = int(request.POST["postId"])
            except ValueError:
                raise Http404
            comments = []
            for comment in Comment.objects.filter(post=post_id):
                comments.append({"user_url": reverse("MyInstagram_user_url", kwargs={"username": comment.user.username}),
                                 "username": comment.user.username,
                                 "text": comment.text})

            json_data = json.dumps(comments)
            return HttpResponse(json_data, content_type='application/json')
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()



def main_page(request):
    if not request.user.is_authenticated():
        if request.method == 'GET':
            next = '/'
            if request.GET.__contains__("next"):
                next = request.GET.get("next", "/")
            login_form = LoginForm(initial={'next': next})
            register_form = RegisterForm(initial={'next': next})
            return render(request, 'home_page_not_login.html', {"login_form": login_form,
                                                                "register_form": register_form})
        else:
            HttpResponseBadRequest()
    else:
        following = request.user.subscriptions.all()
        query = Q()
        for f in following:
            query = query | Q(user=f.id)
        posts = Post.objects.filter(query)[0:PER_PAGE_MAIN]
        return render(request, 'home_page_login.html', {"PER_PAGE_MAIN": PER_PAGE_MAIN,})


@csrf_exempt
@require_POST
def login_page(request):
    next = request.POST.get('next', '/')
    if request.user.is_authenticated():
        return HttpResponseRedirect(next)
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(next)
            else:
                form.add_error(None, "Sorry, your password was incorrect. Please double-check your password.")

    return render(request, 'home_page_not_login.html', {"login_form": form,
                                                        "register_form": RegisterForm(request.POST),})


@csrf_exempt
@require_POST
def register_page(request):
    next = request.POST.get('next', '/')
    if request.user.is_authenticated():
        return HttpResponseRedirect(next)
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password != confirm_password:
                form.add_error('confirm_password', ValidationError("Passwords don't match",
                                                                   code="invalid"))
            else:
                user = form.save()
                user.set_password(password)
                user.subscriptions.add(user)
                city = request.POST.get('city', '')
                if city:
                    obj, created = City.objects.get_or_create(city=city)
                    user.city = obj
                user.save()
                user = auth.authenticate(username=request.POST.get("username"), password=password)
                auth.login(request, user)
                return HttpResponseRedirect(next)

    return render(request, 'home_page_not_login.html', {"login_form": LoginForm(request.POST),
                                                        "register_form": form,
                                                        "first": True})


@csrf_exempt
def add_new_post(request):
    if not request.user.is_authenticated():
        return render(request, 'new_post_not_login.html')
    else:
        if request.method == 'POST':
            form = NewPostForm(request.POST, request.FILES)
            if form.is_valid():
                f = request.FILES.get('photo')
                p = Photo(photo=f)
                p.save()
                post = Post(user=request.user, photo=p)
                post.save()
                return HttpResponseRedirect(reverse("MyInstagram_post_url"  , kwargs={"post_id": post.id}))
        else:
            form = NewPostForm()

    return render(request, 'new_post_login.html', {"form": form})


@csrf_exempt
def logout_page(request):
    next = request.GET.get('next', '/')
    if request.user.is_authenticated():
        print str(request.user.is_authenticated()) + " " + next
        auth.logout(request)
        print str(request.user.is_authenticated()) + " " + next

    return HttpResponseRedirect(next)