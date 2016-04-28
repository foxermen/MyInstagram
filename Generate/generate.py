# coding=utf-8
from MyInstagram.models import User
from MyInstagram.models import City
from MyInstagram.models import Photo
from MyInstagram.models import Post
from MyInstagram.models import Comment
from django.core.files import File
from datetime import datetime
import random

users = User.objects.all()[:]
posts = Post.objects.all()[:]
likes = Post.like_users.through.objects.all()[:]
subscriptions = User.subscriptions.through.objects.all()[:]

f = open('Generate/names-m.txt')
names_m = f.readlines()
f.close()

f = open('Generate/names-f.txt')
names_f = f.readlines()
f.close()

f = open('Generate/surnames.txt')
surnames = f.readlines()
f.close()

f = open('Generate/cities.txt')
cities = f.readlines()
f.close()

f = open('Generate/comments.txt')
comments = f.readlines()
f.close()


def gen_username():
    s = ""
    for i in range(random.randint(8, 12)):
        s += random.choice("qwertyuiopasdfghjklzcvbxnm1234567890-_")
    return s


def gen_email():
    s = ""
    for i in range(random.randint(13, 20)):
        s += random.choice("qwertyuiopasdfghjklzcvbxnm1234567890")
    s += random.choice(["@gmail.com", "@mail.ru", "@yandex.ru", "@rambler.ru"])
    return s


def gen_password():
    s = ""
    for i in range(random.randint(20, 30)):
        s += random.choice("qwertyuiopasdfghjklzcvbxnm1234567890*.@#$%")
    return s


def gen_first_name(sex=0):
    if sex == 0:
        name = random.choice(names_m).strip()
    else:
        name = random.choice(names_f).strip()
    return name


def get_last_name(sex=0):
    surname = random.choice(surnames).strip()
    if sex == 1:
        surname += u"а".encode("utf-8")
    return surname


def get_random_city():
    city = random.choice(cities).strip()
    obj, created = City.objects.get_or_create(city=city)
    return obj


def gen_user():
    username = gen_username()
    email = gen_email()
    password = gen_password()
    usr = User(username=username, email=email, password=password)
    if random.randint(0, 30) <= 20:
        if random.randint(0, 1) == 0:
            usr.first_name = gen_first_name()
            usr.last_name = get_last_name()
        else:
            usr.first_name = gen_first_name(sex=1)
            usr.last_name = get_last_name(sex=1)
    if random.randint(0, 20) <= 15:
        usr.city = get_random_city()
    return usr


def gen_users(n=10000):
    usrs = []
    for i in range(n):
        usrs.append(gen_user())
    User.objects.bulk_create(usrs)
    global users
    users = User.objects.all()[:]
    subs = []
    ThroughModel = User.subscriptions.through
    for usr in usrs:
        u = users.get(username=usr.username)
        subs.append(ThroughModel(from_user_id=u.id, to_user_id=u.id))
    User.subscriptions.through.objects.bulk_create(subs)
    global subscriptions
    subscriptions = User.subscriptions.through.objects.all()


def get_random_user():
    return random.choice(users)


def get_random_post():
    return random.choice(posts)


def get_unique_photo_name():
    strq = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S_")
    strq += str(random.randint(0, 1000000000)) + ".jpg"
    return strq


def get_random_photo():
    name = str(random.randint(1, 11)) + ".jpg"
    p = Photo()
    with open('Generate/Image/' + name, 'r') as f:
        p.photo.save(get_unique_photo_name(), File(f), True)
    return p


def gen_post():
    user = get_random_user()
    photo = get_random_photo()
    post = Post(user=user, photo=photo)
    return post


def gen_posts(n=10000):
    pst = []
    for i in range(n):
        pst.append(gen_post())
    Post.objects.bulk_create(pst)
    global posts
    posts = Post.objects.all()


def gen_random_comment():
    comment = random.choice(comments).strip()
    return comment


def gen_comment():
    user = get_random_user()
    post = get_random_post()
    text = gen_random_comment()
    return Comment(user=user, post=post, text=text)


def gen_comments(n=10000):
    comments = []
    for i in range(n):
        comments.append(gen_comment())
    Comment.objects.bulk_create(comments)


def gen_like():
    post = get_random_post()
    usr = get_random_user()
    ThroughModel = Post.like_users.through
    return ThroughModel(post_id=post.id, user_id=usr.id)


def gen_likes(n=10000):
    global likes
    ThroughModel = Post.like_users.through
    lks = []
    for i in range(n):
        p = gen_like()
        while True:
            f = False
            for l in lks:
                if l.post_id == p.post_id and l.user_id == p.user_id:
                    f = True
                    break
            if f:
                p = gen_like()
                continue
            try:
                likes.get(post_id=p.post_id, user_id=p.user_id)
            except ThroughModel.DoesNotExist:
                break
            p = gen_like()
        lks.append(p)
    Post.like_users.through.objects.bulk_create(lks)
    likes = Post.like_users.through.objects.all()[:]


def gen_subscribe():
    usr1 = get_random_user()
    usr2 = get_random_user()
    ThroughModel = User.subscriptions.through
    return ThroughModel(from_user_id=usr1.id, to_user_id=usr2.id)


def gen_subscriptions(n=10000):
    global subscriptions
    ThroughModel = User.subscriptions.through
    subs = []
    for i in range(n):
        p = gen_subscribe()
        while True:
            f = False
            for l in subs:
                if l.from_user_id == p.from_user_id and l.to_user_id == p.to_user_id:
                    f = True
                    break
            if f:
                p = gen_subscribe()
                continue
            try:
                subscriptions.get(from_user_id=p.from_user_id, to_user_id=p.to_user_id)
            except ThroughModel.DoesNotExist:
                break
            p = gen_subscribe()
        subs.append(p)
    User.subscriptions.through.objects.bulk_create(subs)
    subscriptions = User.subscriptions.through.objects.all()[:]
