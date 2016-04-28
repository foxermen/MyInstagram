"""helloworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from MyInstagram import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

user_patterns = [
    url(r'^$', views.user_main, name='MyInstagram_user_url'),
    url(r'^following/$', views.user_following, name='MyInstagram_user_following'),
    url(r'^followers/$', views.user_followers, name='MyInstagram_user_followers'),
]

post_patterns = [
    url(r'^$', views.user_post, name='MyInstagram_post_url'),
    url(r'^likes/$', views.post_likes, name='MyInstagram_post_likes_url')
]

urlpatterns = [
    url(r'^$', views.main_page, name="MyInstagram_main_page"),
    url(r'^login/$', views.login_page, name="MyInstagram_login_page"),
    url(r'^register/$', views.register_page, name='MyInstagram_register_page'),
    url(r'^new-post/$', views.add_new_post, name='MyInstagram_add_new_post'),
    url(r'^admin/', admin.site.urls),
    url(r'^post/(?P<post_id>\d+)/', include(post_patterns)),
    url(r'^user/(?P<username>[\w-]+)/', include(user_patterns)),
    url(r'^next-posts/$', views.next_posts, name="MyInstagram_next_posts"),
    url(r'^make-like/$', views.make_like, name="MyInstagram_make_like"),
    url(r'^add-comment/$', views.add_comment, name="MyInstagram_add_comment"),
    url(r'^get-comments/$', views.get_comments, name="MyInstagram_get_comments")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()
