from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import *
from .models import *
# Create your views here.
class Indexview(TemplateView):
    template_name='blog/index.html'
    def get(self,request,id=1):
        post=EntertainmentModel.objects.all()
        posts=get_object_or_404(EntertainmentModel,id=id)
        args={'posts':posts, 'post':post,'id':id }
        return render(request, self.template_name, args)


class Searchview(TemplateView):
    """docstring forSearchview."""

    def get(self, request, id=1):
        query=request.GET.get("q")
        post=EntertainmentModel.objects.all()
        posts=get_object_or_404(EntertainmentModel,id=id)

        if query:
            post=post.filter(
            Q(content__icontains=query)|
            Q(heading__icontains=query)|
            Q(author__icontains=query)
            ).distinct()

            args={'posts':post,'id':id }
            return render(request, 'blog/search.html', args)
        else:
            args={'posts':posts,'post':post,'id':id }
            return render(request, 'blog/index.html',args)

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

class Entertainmentview(TemplateView):
    template_name='blog/entertainment.html'

    def get(self,request,id=1):
        post=EntertainmentModel.objects.all()
        posts=get_object_or_404(EntertainmentModel,id=id)
        args={'posts':posts, 'post':post,'id':id }
        return render(request, self.template_name, args)

class NewsView(ListView):
    model = NewsModel
    template_name='blog/news.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class HomeView(ListView):
    model = Post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by = 2

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

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
    success_url = '/entertainment'
    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False
