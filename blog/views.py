from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import *
from .models import *
# Create your views here.
class Indexview(TemplateView):
    template_name='blog/index.html'
    def get(self,request):
        post=Post.objects.all().order_by('-date_posted')
        posts=Post.objects.filter(author = 1)
        args={'posts':posts, 'post':post}
        return render(request, self.template_name, args)


class Searchview(TemplateView):
    """docstring forSearchview."""

    def get(self, request):
        query=request.GET.get("q")
        post=Post.objects.all()

        if query:
            post=post.filter(
            Q(content__icontains=query)|
            Q(title__icontains=query)|
            Q(author__icontains=query)
            ).distinct()
            return render(request, 'blog/search.html', {'posts':post})
        else:
            return render(request, 'blog/index.html', {'posts':post})

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

# class Entertainmentview(TemplateView):
#     def get(self, request):
#         form = PostCreateForm()
#         args={'form': form}
#         return render(request, 'blog/new_post.html', args)
#
#     def post(self, request):
#         if request.method == 'POST':
#             form = PostCreateForm(request.POST, request.FILES)
#
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, f'Your post has been recorded.')
#                 return redirect('blog:index')
#         else:
#             form = PostCreateForm()
#
#         args={'form': form}
#         return render(request, 'blog/new_post.html', args)
class Entertainmentview(TemplateView):
    template_name='blog/entertainment.html'
    def get(self,request,id=14):
        post=Post.objects.all().order_by('-date_posted')
        posts=get_object_or_404(Post,id=id)
        args={'posts':posts, 'post':post,'id':id}
        return render(request, self.template_name, args)


class NewsView(ListView):
    model = Post
    template_name='blog/news.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class HomeView(ListView):
    model = Post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by = 2


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'

    def get(self, request, username="my123456"):
        user = get_object_or_404(User, username=username)
        post = Post.objects.filter(author=user).order_by('-date_posted')
        count = Post.objects.filter(author=user).count()
        args={'posts': post, 'user': user, 'count': count}
        return render(request, self.template_name,args)

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'sub_title', 'cover_image', 'credit', 'content', 'hashtag']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'sub_title', 'cover_image', 'credit', 'content', 'hashtag']

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
