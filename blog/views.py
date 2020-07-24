from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.core.mail import BadHeaderError, send_mail
from django.template import Context
from django.db.models import Q
from users.models import UserFollowing
from django.contrib import messages
from blog.templatetags import extras
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
    ).distinct().order_by('-date_posted')

    return render(request, 'blog/search.html', {'posts':post})

def aboutus(request):
    return render(request, 'blog/aboutus.html')

def shop(request):
    return render(request, 'blog/shop.html')

def contact(request):
    return render(request, 'blog/contact.html')

def contactnow(request):
    name = request.GET.get('name', None)
    email = request.GET.get('email', None)
    message = request.GET.get('message', None)

    send_mail('User Contact:'+str(name)+' '+str(email), str(message), 'admin@dapjak.com' , ['no-reply@dapjak.com',])
    return JsonResponse({"message": "We have received your response. Our team will review your request and get back to you."})

class Subcribeview(SuccessMessageMixin, CreateView):
    model = Subscribe
    success_message = "Thank you for subscribing to our newsletter."
    fields = ['subscriber_name','subscriber_email']


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
        args={'posts':posts, 'post': sample_query, 'category':category}
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
        comments = BlogComment.objects.filter(post_id=pk, parent=None).order_by('-timestamp')
        totalcomments = BlogComment.objects.filter(post_id=pk, parent=None).count()
        replies = BlogComment.objects.filter(post_id=pk).exclude(parent=None).order_by('-timestamp')
        replyDict = {}
        replyCountDict = {}
        for reply in replies:
            if reply.parent.sno not in replyDict.keys():
                replyDict[reply.parent.sno] = [reply]
            else:
                replyDict[reply.parent.sno].append(reply)
        for key, value in replyDict.items():
            replyCountDict[key] = len([item for item in value if item])

        is_liked = False
        if post.likes.filter(id=request.user.id).exists():
            is_liked = True

        is_disliked = False
        if post.dislikes.filter(id=request.user.id).exists():
            is_disliked = True


        args={
                'post': post, 'comments':comments,
                'replyDict':replyDict,
                'replyCountDict': replyCountDict,
                'totalcomments': totalcomments,
                'is_liked': is_liked,
                'is_disliked': is_disliked,
                }

        return render(request, 'blog/post_detail.html', args)


class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post
    fields = ['title', 'sub_title', 'cover_image', 'credit', 'content', 'classification']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name_suffix = '_update_form'
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
        send_mail('Report User ', 'Hi! I would like to report the post with id '+str(report_id)+" by "+str(from_email), 'admin@dapjak.com' , ['no-reply@dapjak.com',])
        return JsonResponse({"message": "Thank you for reporting. Our team will review your request and get back to you.", "login": "t"})

@login_required
def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postId = request.POST.get('postId')
        post = Post.objects.get(id=postId)
        parentSno = request.POST.get('parentSno')

        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()

    return redirect(f"/post/{post.id}/{post.slug}")

# Logic for Like

class PostLike(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        post = get_object_or_404(Post, slug=slug)
        url_ = post.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in post.dislikes.all():
                post.dislikes.remove(user)
                post.likes.add(user)
            else:
                if user in post.likes.all():
                    post.likes.remove(user)
                else:
                    post.likes.add(user)
        return url_


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class PostLikeAPI(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug=None, pk=None, format=None):

            # slug = self.kwargs.get("slug")
        post = get_object_or_404(Post, slug=slug)
        url_ = post.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False

        if user.is_authenticated:
            if user in post.dislikes.all():
                post.dislikes.remove(user)
                post.likes.add(user)
                liked = True
            else:
                if user in post.likes.all():
                    liked = False
                    post.likes.remove(user)
                else:
                    liked = True
                    post.likes.add(user)

            totalLikes = post.likes.count()
            updated = True

        data = {
            "updated": updated,
            "liked": liked,
            "totalLikes": totalLikes,
        }
        return Response(data)
#

# Logic for Dislike

class PostDislike(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        post = get_object_or_404(Post, slug=slug)
        url_ = post.get_absolute_url()
        user = self.request.user

        if user.is_authenticated:
            if user in post.likes.all():
                post.likes.remove(user)
                post.dislikes.add(user)
            else:
                if user in post.dislikes.all():
                    post.dislikes.remove(user)
                else:
                    post.dislikes.add(user)
        return url_


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class PostDislikeAPI(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug=None, pk=None, format=None):
        post = get_object_or_404(Post, slug=slug)
        url_ = post.get_absolute_url()
        user = self.request.user
        updated = False
        disliked = False

        if user.is_authenticated:
            if user in post.likes.all():
                post.likes.remove(user)
                post.dislikes.add(user)
                disliked = True
            else:
                if user in post.dislikes.all():
                    disliked = False
                    post.dislikes.remove(user)
                else:
                    disliked = True
                    post.dislikes.add(user)

            totalDislikes = post.dislikes.count()
            updated = True

        data = {
            "updated": updated,
            "disliked": disliked,
            "totalDislikes": totalDislikes
        }
        return Response(data)
#
