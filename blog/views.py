from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Blog, Comment
from .forms import BlogForm, CommentForm

def home(request):
    blogs = Blog.objects
    return render(request, 'blog/home.html', {'blogs': blogs})

def login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else :
            return render(request, 'blog/login.html')
    else :
        return render(request, 'blog/login.html')

def singup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                request.POST['username'],
                password=request.POST['password1']
            )
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    return render(request,'blog/signup.html')    

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return render(request, 'blog/signup.html')

def create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BlogForm()
    return render(request, 'blog/create.html', {'form': form})


def detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        comment_form.instance.blog_id = pk
        if comment_form.is_valid():
            comment = comment_form.save()
    comment_form = CommentForm()
    comments = blog.comments.all()
    return render(request, 'blog/detail.html', {'blog': blog, 'comments': comments,'comment_form': comment_form})

def update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('/blog/'+str(blog.id))
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/update.html', {'form': form})


def delete(request, pk):
    blog = Blog.objects.get(pk=pk)
    blog.delete()
    return redirect('home')

#comment 기능 #
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    blog = get_object_or_404(Blog, pk=comment.blog.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('/blog/'+str(blog.id))
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_update.html', {'form': form})

def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    blog = get_object_or_404(Blog, pk=comment.blog.id)

    if request.method == 'POST':
        comment.delete()
        return redirect('/blog/'+str(blog.id))
    else:
        return render(request,'blog/comment_delete.html',{'object': comment})

