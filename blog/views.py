from django.shortcuts import render, get_object_or_404,HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib import messages
from .filters import *
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic import ListView, CreateView
from .models import *
import time
from django.http import JsonResponse
from django.db.models import Q
import time
from datetime import datetime
from django.db.models import Count
import sys
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd
import random

now = datetime.now()
def home(request):
    if request.method == 'POST':
        forms = NewsletterForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request,'Email Submitted')
            return redirect('/')
    else:
        forms = NewsletterForm()
    post1= Post.objects.filter(publish=True).order_by('-date')
    post2= Post.objects.filter(publish=True).order_by('date')
    post3= Post.objects.filter(publish=True).order_by('-view_count')
    category = Category.objects.filter(approve=True)
    catego = Category.objects.filter(approve=True).annotate(posts_count = Count('post'))
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        name = request.POST['name']
        if Category.objects.filter(name=name).exists():
            messages.error(request,  'Category name already exists')
        else:
            form.save()
            return redirect('/')
    else:
        form = CategoryForm()
    context = {'forms': forms,
              'post1':post1,
              'form': form,
              'category': category,
              'post2':post2,
              'post3':post3,
              'catego': catego
               }
    template_name = 'blog/home.html'
    return render(request, template_name, context)

# @login_required
def all_category(request):
    context = {}
    category= Category.objects.filter(approve=True)
    filters = CategoryFilter(request.GET, queryset= category)
    filtered_post = filters.qs
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        category_name = request.POST['category_name']
        if Category.objects.filter(category_name=category_name).exists():
            messages.success(request, 'Category name already exists')
            return redirect('/categories')
        else:
            form.save()
            messages.success(request, 'Category Created, waiting for approval')
            return redirect('/categories')
    else:
        form = CategoryForm()
        context['form'] = form
    context = {
        'filters': filters,
        'category': filtered_post,
        'form': form,
    }
    return render(request, 'blog/category.html', context)

def postfilter(request, category_name):
	category= Category.objects.get(category_name=category_name)
	post = Post.objects.filter(category=category)
	post_length = len(post)
	context = {
	'category':category,
	'title': "All Category",
	'post': post,
	'post_length': post_length,
	}
	return render(request, 'blog/postfilters.html', context)



def post(request):
    post = Post.objects.filter(publish= True).order_by('-id')
    filters = PostFilter(request.GET, queryset=post)
    filtered_post = filters.qs
    paginator = Paginator(filtered_post, 9)
    page = request.GET.get('page')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        # category = request.POST['category']
        # title = request.POST['title']
        # image = request.FILES['image']
        # text = request.POST['text']
        # post = Post.objects.create(user=request.user,category=category,title=title,image=image,text=text)
        post = form.save(commit=False)
        post.user = request.user
        post.publish = True
        post.save()
        messages.success(request, 'Post Created, waiting for approval')
        return redirect('/post')
    else:
        form = PostForm()
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context = {
        'paginate': post_list,
        'page': page,
        'forms': forms,
        'post':  filtered_post,
        'filter': filters,
        'form': form,
        'forms': forms,
    }
    return render(request, 'blog/post.html', context)
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



def Details(request, slug):
    posts = Post.objects.filter(publish=True).order_by('-id')
    post = get_object_or_404(Post, slug = slug)
    post.view_count += 1
    post.save()
    postdetails = PostDetail.objects.filter(post=post)
    filters = DetailsFilter(request.GET, queryset=postdetails)
    postdetails = filters.qs
    if request.method == 'POST':
        forms = NewsletterForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request,'Email Submitted')
            return HttpResponseRedirect(reverse('details', args=(slug,)))
    else:
        forms = NewsletterForm()
    comment = Comment.objects.filter(post=post)
    print(time.timezone)

    dt = now.strftime('%d/%m/%Y %H:%M:%S')
    print(dt)
    if request.method == "POST":
        form = CommentForm(request.POST , None)
        body = request.POST['body']
        if is_ajax(request=request):
            if form.is_valid():
                Comment.objects.get_or_create(post=post, userprofile= request.user.userprofile,user=request.user,body=body)
                instance = form.save(commit=False)
                instance.user = request.user
                return JsonResponse({
                    'body': instance.body,
                    'created': dt,
                    'user': instance.user.username,
                    # 'image': request.user.userprofile.image.url,
                })
            # return HttpResponseRedirect(reverse('details', args=(slug,)))
    else:
        form = CommentForm()
    context = {
        'posts': posts,
        'post': post,
        'postdetails': postdetails,
        'comment': comment,
        'form': form,
        'forms': forms,
        'filters': filters,
    }

    return render(request, 'blog/post_details.html', context)

@login_required
def userdetails(request, slug):
    post = get_object_or_404(Post, slug = slug)
    postdetails = PostDetail.objects.filter(post=post)
    context = {
        'post': post,
        'postdetails': postdetails
    }
    return render(request, 'blog/userdetails.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
        messages.success(request, 'You Are Alredy Logged In')
    else:
        context = {}
        if request.method == "POST":
            users = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            password3 = request.POST['password1']
            checkbox = request.POST.get('checkbox')
            username = users.lower()
            print(checkbox)
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email Already Exist')
                return redirect('/register')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username Has Been Taken')
                return redirect('/register')
            elif password1 != password2:
                messages.error(request, 'Password does not match')
                return redirect('/register')
            # elif checkbox
            else:
                user_info = UserInfo.objects.create(username=username, password=password3, agree= True)
                user = User.objects.create_user(email=email,password=password1, username=username)
                user.save()
                messages.success(request,'Registration successfully')
                UserProfile.objects.get_or_create(user=user)
                print(checkbox)
                return redirect('/login')

        return render(request,'blog/registration.html', context)

def login_page(request):
    context = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        context['form'] = form
        next = request.GET.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')
        use = username.lower()
        user = authenticate(username=use, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Login Successful')
                if next:
                    return redirect(next)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Acdd')
        else:
            invalid = 'Invalid Credentials'
            context['invalid'] = invalid
    else:
        form = LoginForm()
        context['form'] = form
    return render(request,'blog/login.html', context)

def log_out(request):
    logout(request)
    return redirect('/')

@login_required
def userpost(request):
    if request.method == 'POST':
        category = request.POST['category']
        title = request.POST['title']
        image = request.FILES['image']
        text = request.POST['text']
        post = Post.objects.create(user=request.user,category=category,title=title,image=image,text=text)
        PostDetail.objects.create(post=post)
        messages.success(request, 'Post Created, waiting for approval')
        return redirect('/post')
    else:
        form = PostForm()
    template_name = 'blog/userpost.html'
    context= {
        'form': form,
        'forms': forms
        }
    return render(request, template_name, context)

@login_required
def update_post(request, slug):
    post = Post.objects.filter(user = request.user)
    post= get_object_or_404(post, slug = slug)
    if request.method == 'POST':
        u_form = PostForm(request.POST,request.FILES,instance=post)
        if u_form.is_valid():
            obj = u_form.save(commit= False)
            obj.save()
            return HttpResponseRedirect(reverse('details', args = (slug, )))
    else:
        u_form = PostForm(instance=post)
    return render(request,'blog/edit-post.html', {'u_form': u_form})

@login_required
def userprofile(request):
    context = {}
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if u_form.is_valid and p_form.is_valid():
            try:
                u_form.save()
            except:
                messages.error(request, 'Username Already Chosen')
                return redirect('/userprofile')
            p_form.save()
            print(f"profile_form: {p_form}, 'User_form': {u_form}")
            context['msz'] = 'Profile Updated Successfully'
    else:
        u_form = UserUpdateForm(instance=request.user)
        context['u_form'] = u_form
        p_form = ProfileUpdateForm(instance=request.user.userprofile)
        context['p_form'] = p_form

    post = Post.objects.filter(publish= True)

    return render(request, 'blog/user.html', {'post': post, 'u_form': u_form, 'p_form': p_form})

@login_required
def editprofile(request):
    context = {}
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        context['u_form'] = u_form
        context['p_form'] = p_form
        if u_form.is_valid and p_form.is_valid():
            try:
                u_form.save()
                print(f"profile_form: {p_form}, 'User_form': {u_form}")
                context['msz'] = 'Profile Updated Successfully'
            except:
                messages.error(request, 'Username Already Chosen')
            p_form.save()
    else:
        u_form = UserUpdateForm(instance=request.user)
        context['u_form'] = u_form
        p_form = ProfileUpdateForm(instance=request.user.userprofile)
        context['p_form'] = p_form

    post = Post.objects.filter(publish= True)

    return render(request, 'blog/edit-profile.html', context)


@login_required
def change_password(request):
    context = {}
    if request.method == 'POST':
        current = request.POST['cpwd']
        new = request.POST['pwd1']
        confirm = request.POST['pwd2']
        user = User.objects.get(id=request.user.id)
        un = user.username
        pwd = new
        check = user.check_password(current)
        print(check)
        if check == True:
            user.set_password(new)
            user.save()
            pro = authenticate(username=un, password=pwd)
            login(request, pro)
            context['msz'] = 'Password Changed Successfully'
            context['suc'] = 'success'
            print(pwd)
        else:
            context['msg'] = 'Incorrect Password, Try Again'
            context['col'] = 'danger'
    return render(request, 'blog/changepasword.html', context)


@login_required
def my_post(request):
    post = Post.objects.filter(user=request.user)
    filters = PostFilter(request.GET, queryset = post)
    post = filters.qs
    return render(request, 'blog/mypost.html', {'post': post})

@login_required
def mypost_details(request, slug):
    post = get_object_or_404(Post, slug = slug)
    postdetails = PostDetail.objects.filter(post=post)
    filters = DetailsFilter(request.GET, queryset=postdetails)
    postdetails = filters.qs
    if request.method == 'POST':
        forms = NewsletterForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request,'Email Submitted')
            return HttpResponseRedirect(reverse('details', args=(slug,)))
    else:
        forms = NewsletterForm()
    comment = Comment.objects.filter(post=post)
    if request.method == "POST":
        form = CommentForm(request.POST)
        body = request.POST['body']
        if form.is_valid():
            Comment.objects.get_or_create(post=post, userprofile= request.user.userprofile,user=request.user,body=body)
            return HttpResponseRedirect(reverse('details', args=(slug,)))
    else:
        form = CommentForm()
    context = {
        'post': post,
        'postdetails': postdetails,
        'comment': comment,
        'form': form,
        'forms': forms,
        'filters': filters,
        # 'is_liked': is_liked,
    }
    return render(request, 'blog/mypost_details.html', context)

# def like(request):
#     post = get_object_or_404(Post, id=request.POST.get('post_id'))
#     is_liked = False
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)
#         is_liked = True
#     return HttpResponseRedirect('/post')
@login_required
def delete_post(request, slug):
    post = Post.objects.filter(user = request.user)
    post = get_object_or_404(post, slug = slug)
    postdetails = PostDetail.objects.filter(post=post)
    if request.method == "POST":
        post.delete()
        return redirect('/post')
    return render(request, 'blog/delete.html', {'post': post})

# def search(request):
#     q = request.GET.get('q')
#     post = Post.objects.filter(
#         Q(title__icontains='q') |

#         )

@login_required
def like_post(request):
    user = request.user
    post_id = request.POST.get('post_id')
    post_obj = Post.objects.get(id = post_id)

    if user in post_obj.likes.all():
        post_obj.likes.remove(user)
    else:
        post_obj.likes.add(user)

    like, create = Like.objects.get_or_create(user=user, post_id=post_id)

    if not create:
        if like.value == "Like":
            like.value == "Unlike"
        else:
            like.value == "Like"

    return redirect('/post')

@login_required
def like_home(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id = post_id)

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)

        like, create = Like.objects.get_or_create(user=user, post_id=post_id)

        if not create:
            if like.value == "Like":
                like.value == "Unlike"
            else:
                like.value == "Like"
    return redirect('/')

@login_required
def like_mypost(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id = post_id)

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)

        like, create = Like.objects.get_or_create(user=user, post_id=post_id)

        if not create:
            if like.value == "Like":
                like.value == "Unlike"
            else:
                like.value == "Like"
    return redirect('/my-posts')





@login_required
def custom_admin(request):
    posts= Post.objects.all()

    context ={
        'post': posts,
    }
    return render(request, 'blog/admin.html', context)

@login_required
def custom_admin_category(request):
    category= Category.objects.all()
    context ={
        'category': category,
    }
    return render(request, 'blog/admin_category.html', context)

@login_required
def custom_admin_update(request, slug):
    context = {}
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = AdminPostForm(request.POST, request.FILES, instance = post)
        if form.is_valid():
            obj = form.save(commit= False)
            obj.save()
            success ='updated'
            context['success'] = success
            messages.success(request, 'Post Updated Successfully')
            return redirect('/custom-admin')
    else:
        form = AdminPostForm(instance=post)
    context['form'] = form
    template_name = 'blog/custom_admin_update.html'
    return render(request, template_name, context)
@login_required
def custom_admin_delete(request, slug):
    post = get_object_or_404(Post, slug = slug)
    postdetails = PostDetail.objects.filter(post=post)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted Successfully')
        return redirect('/custom-admin')
    return render(request, 'blog/custom_admin_delete.html', {'post': post})


@login_required
def user_info(request):
    user = User.objects.all()
    return render(request, 'blog/users-info.html', {'user': user})

def user_details(request, p_id):
    user  = User.objects.get(id = p_id)
    return render(request, 'blog/user_details.html', {'user': user})

@login_required
def admin_registration(request):
    if request.method== "POST":
        form = AdminRegister(request.POST)
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password1')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Exists')
            return redirect('/custom-admin/register')
        elif form.is_valid():
            user = User.objects.create_user(username=username, password=password, email = email)
            user.save()
            UserProfile.objects.get_or_create(user=user)
            return redirect('/users-info')
            messages.success(request, 'Registration successful')
    else:
        form = AdminRegister()
    context = {
        'form': form
    }
    return render(request, 'blog/admin_register.html', context)

@login_required
def admin_add_post(request):
    if request.method == "POST":
        form = AdminPostForm(request.POST, request.FILES)
        text = request.POST['text']
        image = request.FILES['image']
        category = request.POST['category']
        title = request.POST['title']
        if form.is_valid():
            post = Post.objects.create(user=request.user, title = title, text=text, category= category, publish = True,image = image)
            PostDetail.objects.get_or_create(post=post)
            messages.success(request, 'Post Created Successfully')
            return redirect('/custom-admin')

    else:
        form = AdminPostForm()
    context = {
        'form': form
    }
    return render(request,'blog/admin_add_post.html', context)


def contact(request):
    context = {}
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        body = request.POST['body']

        Contact.objects.create(name = name, email = email, body = body)
        context['success'] = 'Information Submitted'
    return render(request,'blog/contact.html', context)


def search(request):
    q = request.GET.get('q')
    post = Post.objects.filter(
        Q(title__icontains=q) |
        Q(category__icontains=q) |
        Q(text__icontains=q) |
        Q(date__icontains=q)).distinct()

    context = {
        'post': post,
        't': f'Search result for {q}'
    }
    return render(request,'blog/all.html', context)



def bea(request):
    try:
        page = requests.get('https://www.cricbuzz.com')
        print(page)
    except:
        pass


    soup = bs(page.text, 'html.parser')

    links = soup.find_all('div', attrs={'class': 'cb-nws-intr'})
