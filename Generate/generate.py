# coding=utf-8
from MyInstagram.models import User
from MyInstagram.models import City
from MyInstagram.models import Photo
from MyInstagram.models import Post
from MyInstagram.models import Comment
from django.core.files import File
from datetime import datetime
import random


def gen_username():
    s = ""
    for i in range(random.randint(8, 12)):
        s += random.choice("qwertyuiopasdfghjklzcvbxnm1234567890")
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
        f = open('Generate/names-m.txt')
    else:
        f = open('Generate/names-f.txt')
    names = f.readlines()
    name = random.choice(names).strip()
    f.close()
    return name


def get_last_name(sex=0):
    f = open('Generate/surnames.txt')
    surnames = f.readlines()
    surname = random.choice(surnames).strip()
    if sex == 1:
        surname += u"а".encode("utf-8")
    f.close()
    return surname


def get_random_city():
    f = open('Generate/cities.txt')
    cities = f.readlines()
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
    users = []
    for i in range(n):
        users.append(gen_user())
    User.objects.bulk_create(users)
    for usr in User.objects.all()[:]:
        usr.subscriptions.add(usr)


def get_random_user():
    users = User.objects.all()[:]
    return random.choice(users)


def get_random_post():
    posts = Post.objects.all()[:]
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
    posts = []
    for i in range(n):
        posts.append(gen_post())
    Post.objects.bulk_create(posts)


def gen_random_comment():
    f = open('Generate/comments.txt')
    comments = f.readlines()
    comment = random.choice(comments).strip()
    f.close()
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
    while post.like_users.count() == User.objects.all().count():
        post = get_random_post()
    usr = get_random_user()
    while usr in post.like_users.all()[:]:
        usr = get_random_user()
    post.like_users.add(usr)


def gen_likes(n=10000):
    for i in range(n):
        gen_like()


def gen_subscribe():
    usr1 = get_random_user()
    while usr1.subscriptions.count() == User.objects.all().count():
        usr1 = get_random_user()
    usr2 = get_random_user()
    while usr2 in usr1.subscriptions.all()[:]:
        usr2 = get_random_user()
    usr1.subscriptions.add(usr2)


def gen_subscriptions(n=10000):
    for i in range(n):
        gen_subscribe()
