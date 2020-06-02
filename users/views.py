from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import *

class RegisterView(TemplateView):
    def get(self,request):
        form=UserRegisterForm()
        return render(request, 'users/register.html', {'form':form})
    def post(self,request):
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form':form})

# To return whether the same username exists or not.
def validate_username(request):
    username = request.GET.get('username', None)
    result = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(result)

# To check whether the email exists or not in the Database.
def check_email(request):
    email = request.GET.get('email', None)
    result = {
        'is_taken' : User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(result)

class FollowView(DetailView):

    def get(self, request, id):

        loggedIn = request.user.id
        loggedIn = User.objects.filter(id=loggedIn).first()
        toFollow = User.objects.filter(id=id).first()

        twt_user = User.objects.get(id=id)

        if request.user.is_authenticated:
            if UserFollowing.objects.filter(loggedInUser=request.user.id, toFollowUser=id).exists():
                UserFollowing.objects.filter(loggedInUser=loggedIn, toFollowUser=toFollow).delete()
                button_text = 'Follow'

            else:
                UserFollowing.objects.create(loggedInUser=loggedIn, toFollowUser=toFollow)
                button_text = 'Following'

            followers = twt_user.followers.count()
            following = twt_user.following.count()

            result = {
                        'followers' : followers,
                        'following' : following,
                        'button_text' : button_text,
                        'login' : 't'
                        }


        else:
            result = {
                        'login' : 'f'
                        }
        return JsonResponse(result)
    
def changepassword(request):
    if request.method == 'POST':
        r_form = PasswordChangeForm(request.user, request.POST)
        if r_form.is_valid():
            new = r_form.save()
            update_session_auth_hash(request, new)  # Important!
            messages.success(request, f'Your account has been updated.')
            return redirect('profile')
    else:
        r_form = PasswordChangeForm(request.user)

    return render(request, 'users/changepassword.html', {'r_form': r_form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()

            messages.success(request, f'Your account has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context={
    'u_form': u_form,
    'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
