from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from .models import Posts
from . import models
from .models import Comment
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
# from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import authenticate, login as auth_login , logout
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
# def test(request):
#     return render(request, 'blog/login.html')

class user_login(View):
    template_name = 'blog/login.html'
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('uname')
        password = request.POST.get('upassword')
        user = authenticate(request, username=name, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('/home')
        else:
            return redirect('/login')
        

class post_detail(View):
    def get(self, request, post_id):
        try:
            post = Posts.objects.get(id=post_id)
        except Posts.DoesNotExist:
            raise Http404("Post not found")

        comments = post.comments.all()
        return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

    def post(self, request, post_id):
        try:
            post = Posts.objects.get(id=post_id)
        except Posts.DoesNotExist:
            raise Http404("Post not found")

        content = request.POST.get('comment')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
        return redirect('post_detail', post_id=post.id)

class delete_post(DeleteView):
    model = Posts
    template_name = 'blog/confirm_delete.html' 
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('home')


def signup(request):
    if request.method== "POST":
        name = request.POST.get('uname')
        email = request.POST.get('uemail')
        password = request.POST.get('upassword')
        newuser = User.objects.create_user(username=name, email=email, password=password)
        newuser.save()
        return redirect('/login')
    return render(request, 'blog/signup.html')

def home(request):
    context = {
        'posts':Posts.objects.all()

    }
    return render(request, 'blog/home.html', context)
    
def newPost(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = models.Posts(title=title, content=content, author=request.user)
        post.save()
        return redirect('/home')
    
    return render(request, 'blog/newpost.html')


class myPost(ListView):
    model = Posts
    template_name = 'blog/mypost.html'  
    context_object_name = 'posts' 

    def get_queryset(self):
        """Override this method to filter posts by the logged-in user."""
        return Posts.objects.filter(author=self.request.user)

def signOut(request):
    logout(request)
    return redirect('/login')