from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# Create your views here.
def home(request):
    posts = Post.objects.all() # query: get all data from table Post
    return render(request, 'blog/home.html',{
        'posts': posts
    }) # return result as dict to show on home.html

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id) # query: get data from id

    return render(request, 'blog/post-detail.html',{
        'post': post
    })