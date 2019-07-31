from .models import Blog, Comment, BlogLike
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from .form import Postform
from django.contrib import auth
from django.contrib.auth.decorators import login_required

@login_required
def comment_write(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Blog, pk=post_pk)
        content = request.POST.get('content')
        if not content:
            messages.info(request, "You dont write anything...")
            return redirect('/post/' + str(post_pk))

        Comment.objects.create(post_key = post, comment_contents=content, author=request.user)
        return redirect('/post/'+str(post_pk))

def delete1(request, comment_id, post_id):
    comment = get_object_or_404(Comment , pk = comment_id )
    comment.delete()
    return redirect('/post/'+str(post_id))


@login_required
def delete(request, post_id):
    post = get_object_or_404(Blog, pk = post_id)
    post.delete()
    return redirect('detail')

def post(request, post_id):
    post_detail = get_object_or_404(Blog, pk=post_id)
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user.get_username())
        return render(request, 'post.html', {'post':post_detail, 'user':user, 'post_id': post_detail.pk})
    else:
        return render(request, 'post.html', {'post':post_detail, 'post_id': post_detail.pk})


@login_required
def modify(request, post_id):
    post = get_object_or_404(Blog, pk = post_id)
    if request.method == "POST":
        form = Postform(request.POST, instance = post)
        if form.is_valid():
            post = form.save(commit=False)
            post.date = timezone.now()
            post.save()
            return redirect('post', post_id=post.pk)
    else:
        form = Postform(instance = post)
    return render(request, 'modify.html', {'form' : form, 'post_id':post.pk})

# def modify(request, post_id):
#     post = Blog.objects.get(id=post_id)
#     if request.method == 'POST':
#         form = Postform(request.POST, request.FILES)
#         if form.is_valid():
#             post.title = form.cleaned_data['title']   
#             post.content = form.cleaned_data['explain']
#             post.save()
#             return redirect('/post/' +str(post_id))
#     else:
#         form= Postform(instance=post)
#         return render(request,'modify.html',{'form':form})

@login_required
def new(request):
    if request.method == 'POST':
        form = Postform(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit = False)
            blog.writer=request.user
            blog.date = timezone.now()
            blog.save()
            return redirect('post', post_id=blog.pk)
    else :
        form = Postform()
        
    return render(request, 'new.html', {'form' : form})

def signup(request):
    if request.method == 'POST':
        if request.POST ['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': 'Username has already been taken'})
            except User.DoesNotExist:
              user = User.objects.create_user(
              request.POST['username'], password = request.POST['password1'])
              auth.login (request,user)
            return redirect('home')
        else:
            return render (request, 'accounts/signup.html', {'eror': 'Passwords must match'})
    else:
        return render(request,'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render (request, 'login.html', {'error':'username or password is incorrect.'})
    else:
        return render (request,'login.html')

def home(request):

    return render(request, 'home.html')

def detail(request):
    posts = Blog.objects.all()
    return render(request, 'detail.html', {'posts_list':posts})

@login_required
def like(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if BlogLike.objects.filter(blog=blog, user=request.user).count() == 0:
        BlogLike.objects.create(blog=blog, user=request.user)
    return redirect('post', post_id=pk)

# def search(request):
#     options = []
#     return render(request,'blog/detail.html', {'options':options})

# def result(request):
#     if request.method =="GET":
#         keyword1 = request.GET.get('keyword1')
#         keyword2 = request.GET.get('keyword2')
#         if ((keyword1 is not None) and (keyword2 is not None)):
#             posts = Blog.objects.filter(Q(find_place__icontains=keyword1) & Q(item_type__icontains=keyword2))
#             paginator = Paginator(posts, 3)
#             page = request.GET.get('page')
#             post_page = paginator.get_page(page)
#             return render(request, 'blog/detail.html', {'posts': posts, 'post_page': post_page, 'keyword1':keyword1, 'keyword2':keyword2}) 
#         else:
#             return render(request,'blog/detail.html')
#     else:
#         return render(request,'blog/detail.html')