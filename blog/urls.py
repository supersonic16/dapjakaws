from django.conf.urls import url
from django.urls import path
from blog.views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='blog'

urlpatterns=[
    url(r'^$',Indexview.as_view(), name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^subscribe/$', Nameview.as_view(), name='subscribe'),
    url(r'^aboutus/$',views.aboutus, name='aboutus'),
    url(r'^contact/$',Contactview.as_view(), name='contact'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('<str:category>/<int:pk>/<slug:slug>/', Categoryview.as_view(), name='category'),
    path('<str:category>/', Categoryview.as_view(), name='category'),
    path('reportuser/', views.reportuser, name='reportuser'),
    url(r'^shop/$',views.shop, name='shop'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
