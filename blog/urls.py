from django.conf.urls import url
from django.urls import path
from blog.views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='blog'

urlpatterns=[
    url(r'^$',Indexview.as_view(), name='index'),
    url(r'^search/$',Searchview.as_view(), name='search'),
    url(r'^subscribe/$', Nameview.as_view(), name='subscribe'),
    url(r'^aboutus/$',views.aboutus, name='aboutus'),
    url(r'^contact/$',Contactview.as_view(), name='contact'),
    url(r'^entertainment/(?P<id>[0-9]+)/$',Entertainmentview.as_view(), name='entertainment'),
    url(r'^entertainment/$',Entertainmentview.as_view(), name='entertainment'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('news/<int:pk>/',NewsView.as_view(), name='news'),
    path('news/',NewsView.as_view(), name='news'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('reportuser/', views.reportuser, name='reportuser'),
    url(r'^shop/$',views.shop, name='shop'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
