from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.core.mail import BadHeaderError, send_mail
from django.template import Context
from django.db.models import Q
from users.models import UserFollowing
from .forms import *
from .models import *
# Create your views here.
class Indexview(TemplateView):
    template_name='blog/index.html'
    def get(self,request):
        if request.user.is_authenticated:
            current_user = request.user.id
        else:
            current_user = 1

        toFollowList = UserFollowing.objects.filter(loggedInUser = current_user)

        if toFollowList:
            sample_query = Post.objects.filter(author = UserFollowing.objects.filter(loggedInUser = current_user).first().toFollowUser.id)
            for follow_id in toFollowList[1:]:
                new = Post.objects.filter(author = follow_id.toFollowUser.id)
                sample_query = new | sample_query

            sample_query = sample_query.order_by('-date_posted')

        else:
            sample_query = Post.objects.none()

        post = Post.objects.all().order_by('-date_posted')
        posts = Post.objects.filter(author__is_superuser = 't').order_by('-date_posted')
        args={'posts':posts, 'post':post, 'followed_blogs': sample_query}
        return render(request, self.template_name, args)

def search(request):
    query=request.GET.get("q")
    post=Post.objects.all()

    post=post.filter(
        Q(content__icontains=query)|
        Q(title__icontains=query)|
        Q(sub_title__icontains=query)|
        Q(author__username__icontains=query)
        ).distinct()

    return render(request, 'blog/search.html', {'posts':post})

def aboutus(request):
    return render(request, 'blog/aboutus.html')

def shop(request):
    return render(request, 'blog/shop.html')

class Contactview(TemplateView):
    template_name='blog/contact.html'

    def get(self,request):
        form=ContactForm()
        return render(request, self.template_name, {'form':form})

    def post(self,request):
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            message=form.cleaned_data['message']
            form=ContactForm()

        args={'form':form, 'name':name, 'email':email, 'message':message}
        return render(request, self.template_name, args)

class Nameview(TemplateView):
    template_name='blog/subscribe.html'

    def get(self,request):
        form=NameForm()
        return render(request, self.template_name, {'form':form})

    def post(self,request):
        form=NameForm(request.POST)
        if form.is_valid():
            form.save()
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            form=NameForm()

        args={'form':form, 'name':name, 'email':email}

        return render(request, self.template_name, args)


class Categoryview(TemplateView):

    template_name='blog/category.html'
    def get(self,request,category):
        if request.user.is_authenticated:
            current_user = request.user.id
        else:
            current_user = 1

        toFollowList = UserFollowing.objects.filter(loggedInUser = current_user)
        if toFollowList:
            sample_query = Post.objects.filter(author = UserFollowing.objects.filter(loggedInUser = current_user).first().toFollowUser.id)
            for follow_id in toFollowList[1:]:
                new = Post.objects.filter(author = follow_id.toFollowUser.id)
                sample_query = new | sample_query

            sample_query = sample_query.filter(classification=category).order_by('-date_posted')

        else:
            sample_query = Post.objects.none()

        posts = Post.objects.filter(author__is_superuser = 't')
        posts = posts.filter(classification=category).order_by('-date_posted')
        args={'posts':posts, 'post': sample_query}
        return render(request, self.template_name, args)


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'

    def get(self, request, username="my123456"):
        user = get_object_or_404(User, username=username)
        twt_user = User.objects.get(id=user.id)
        followers = twt_user.followers.count()
        following = twt_user.following.count()
        post = Post.objects.filter(author=user).order_by('-date_posted')
        count = Post.objects.filter(author=user).count()

        if UserFollowing.objects.filter(loggedInUser=request.user.id, toFollowUser=user.id).exists():
            button_text = "Following"
        else:
            button_text = "Follow"

        args={'posts': post, 'user': user, 'count': count, 'followers': followers, 'following': following, 'button_text': button_text}
        return render(request, self.template_name,args)

class PostDetailView(DetailView):
    model = Post

    def get(self,request,pk,slug):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'sub_title', 'cover_image', 'credit', 'content', 'classification']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'sub_title', 'cover_image', 'credit', 'content', 'classification']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False

def reportuser(request):
    from_email = request.GET.get('from_email', None)
    report_id = request.GET.get('report_id', None)

    if from_email == "":
        return JsonResponse({"message": "Please login in order to report this article.", "login": "f"})
    else:
        send_mail('Report User ', 'Hi! I would like to report the post with id'+str(report_id), from_email , ['no-reply@dapjak.com',])
        return JsonResponse({"message": "Thank you for reporting. Our team will review your request and get back to you.", "login": "t"})
