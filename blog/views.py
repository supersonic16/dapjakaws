from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
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



def search(request,id=1):
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
