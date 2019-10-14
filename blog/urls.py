from django.conf.urls import url
from blog.views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='blog'

urlpatterns=[
    url(r'^$', views.index, name='index')
]
