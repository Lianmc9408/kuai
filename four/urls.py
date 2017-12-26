"""kuai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from four import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^tencent/$', views.tencentindex),
    url(r'^seri/$', views.serializers_ind),
    url(r'^artical/$', views.artical_list),
    url(r'^articals/$', views.ArticalList.as_view()),
    url(r'^articalss/$', views.ListGenerics.as_view()),
    url(r'^artical/(?P<pk>[0-9]+)$', views.artical_detail),
    url(r'^articals/(?P<pk>[0-9]+)$', views.ArticalDetail.as_view()),
    url(r'^articalss/(?P<pk>[0-9]+)$', views.DetailGenerics.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
