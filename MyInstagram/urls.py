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
    url(r'^$', views.user_subscriptions_or_subscribers),
    url(r'^(?P<page>\d+)/$', views.user_subscriptions_or_subscribers),
]

user_patterns = [
    url(r'^$', views.user_main),
    url(r'^(?P<page>\d+)/$', views.user_main),
    url(r'^post/(?P<post>\w+)/$', views.user_post),
    url(r'^(subscriptions|subscribers)/', include(user_to_users)),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^(?P<username>[\w-]+)/', include(user_patterns)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
