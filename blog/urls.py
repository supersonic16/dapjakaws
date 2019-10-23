from django.conf.urls import url
from blog.views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='blog'

urlpatterns=[
    url(r'^$',Indexview.as_view(), name='index'),
    url(r'^search/$',views.search, name='search'),
    url(r'^subscribe/$', Nameview.as_view(), name='subscribe'),
    url(r'^aboutus/$',views.aboutus, name='aboutus'),
    url(r'^contact/$',Contactview.as_view(), name='contact'),
    url(r'^entertainment/(?P<id>[0-9]+)/$',Entertainmentview.as_view(), name='entertainment'),
    url(r'^entertainment/$',Entertainmentview.as_view(), name='entertainment'),
    url(r'^shop/$',views.shop, name='shop')
]
