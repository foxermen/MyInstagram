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

user_to_users = [
    url(r'^$', views.user_subscriptions_or_subscribers, name='MyInstagram_user_subs_url'),
    url(r'^(?P<page>\d+)/$', views.user_subscriptions_or_subscribers, name='MyInstagram_user_subs_page_url'),
]

user_patterns = [
    url(r'^$', views.user_main, name='MyInstagram_user_url'),
    url(r'^(?P<page>\d+)/$', views.user_main, name='MyInstagram_user_page_url'),
    url(r'^(?P<mode>subscriptions|subscribers)/', include(user_to_users)),
]

likes_patterns = [
    url(r'^$', views.post_likes, name='MyInstagram_post_likes_url'),
    url(r'^(?P<page>\d+)/$', views.post_likes, name='MyInstagram_post_likes_page_url'),
]

post_patterns = [
    url(r'^$', views.user_post, name='MyInstagram_post_url'),
    url(r'likes/', include(likes_patterns))
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^post/(?P<post_id>\d+)/', include(post_patterns)),
    url(r'^user/(?P<username>[\w-]+)/', include(user_patterns)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
