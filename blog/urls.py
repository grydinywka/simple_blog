"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from blogapp.views import login, PostUpdateView, PostCreateView, PostDetailView, UserOwnerDetailView, UserOwnerListView
from blogapp.models import UserOwner, Post
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', login_required(TemplateView.as_view(template_name="blogapp/index.html")), name='home'),
    url(r'^logout/$', auth_views.logout, kwargs={'next_page':'auth_login'}, name='auth_logout'),
    url(r'^login/$', login, name='auth_login'),
    url(r'^blog/users/$', login_required(UserOwnerListView.as_view()), name='user_list'),
    url(r'^blog/users/(?P<pk>\d+)/$', login_required(UserOwnerDetailView.as_view()), name="user_posts"),
    url(r'^blog/(?P<pk>\d+)/$', login_required(PostDetailView.as_view()), name="post"),
    url(r'^blog/(?P<pk>\d+)/update/$', login_required(PostUpdateView.as_view()), name="post_update"),
    url(r'^blog/create/$', login_required(PostCreateView.as_view()), name="post_create"),
    url(r'^admin/', admin.site.urls),
]
