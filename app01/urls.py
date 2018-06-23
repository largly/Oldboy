"""Oldboy URL Configuration

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
from django.contrib import admin
from rest_framework import routers
from app01.views import *
from app01.viewsfile.course import CourseViewSet
from app01.viewsfile.login import Login
from app01.viewsfile.OrderCar import OrderCar
from app01.viewsfile.article import ArticleViewSet
from app01.viewsfile.collection import CollectionViewSet
route = routers.DefaultRouter()
# route.register('degreecourses',DegreeCourseView)
# route.register('teachers',TeacherViewSet)
route.register('pricepolicys',PricePolicyViewSet)
route.register('contenttypes',ContenttypeViewSet)

urlpatterns = [
    url(r'^degreecourses$', DegreeCourseView.as_view(actions={'get': 'list'}), name='degreecourse-list'),
    url(r'^courses/$', CourseViewSet.as_view(actions={'get': 'list'}), name='course-list'),
    url(r'^article/$', ArticleViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='article-list'),
    url(r'^article/(?P<pk>\d+)/$', ArticleViewSet.as_view(actions={'get': 'retrieve','post':'create'}), name='article-detail'),
    url(r'^courses/(?P<pk>\d+)/$', CourseViewSet.as_view(actions={'get': 'retrieve'}), name='course-detail'),
    url(r'^collections/$', CollectionViewSet.as_view(actions={'get': 'list','post':'create'}), name='collection-detail'),

    url(r'^degreecourses/(?P<pk>\d+)$', DegreeCourseView.as_view(actions={'get': 'retrieve'}),
        name='degreecourse-detail'),
    url(r'^car/$',OrderCar.as_view())


]

