from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from .models import *
# Create your views here.

def aboutus(request):
    return render(request, 'blog/aboutus.html')

def index(request):
    return render(request, 'blog/index.html')
