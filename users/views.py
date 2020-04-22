from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth.models import User


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

def validate_username(request):
    username = request.GET.get('username', None)
    result = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(result)

def check_email(request):
    email = request.GET.get('email', None)
    result = {
        'is_taken' : User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(result)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
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
