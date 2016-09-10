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
from blogapp.views import home, login
from blogapp.models import UserOwner
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,TemplateView,DetailView
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^logout/$', auth_views.logout, kwargs={'next_page':'auth_login'}, name='auth_logout'),
    url(r'^login/$', login, name='auth_login'),
    url(r'^blog/users/$', login_required(ListView.as_view(model=UserOwner,
                                           template_name="blogapp/users.html",
                                           context_object_name='users')),
        name='user_list'),
    url(r'^blog/users/(?P<pk>\d+)/$', login_required(DetailView.as_view(model=UserOwner,
                                                         template_name="blogapp/user_posts.html",
                                                         context_object_name='userowner')), name="user_posts"),
    url(r'^admin/', admin.site.urls),
]
