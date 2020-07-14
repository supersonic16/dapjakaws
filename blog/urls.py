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
    url(r'^aboutus/$',views.aboutus, name='aboutus'),
    url(r'^contact/$',views.contact, name='contact'),
    url(r'^contactnow/$',views.contactnow, name='contactnow'),
    url(r'^shop/$',views.shop, name='shop'),
    path('reportuser/', views.reportuser, name='reportuser'),

    path('subscribe/', Subcribeview.as_view(), name='subscribe'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('tech/', views.tech, name='tech'),
    path('post/<int:pk>/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('<str:category>/<int:pk>/<slug:slug>/', Categoryview.as_view(), name='category'),
    path('<str:category>/', Categoryview.as_view(), name='category'),
    # path('classifypost/<int:pk>', PostClassifyView.as_view(), name='classify-post'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
