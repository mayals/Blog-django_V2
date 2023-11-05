from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import UserRegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from blog.models import Post



# -----------------# Register  # create user object # -----------------------------------------------#
def registeruser(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit = False)
            username = form.cleaned_data['username']                         
            password = form.cleaned_data['password1']
            new_user.set_password(password) # To hash intered password
            new_user.save()
           
            # to login the new user
            user = authenticate(request, username=username, password=password)
            login(request,user)
            messages.success(request, 'Conguratulation ( {} ) you do success Registration and login, please edit your profile'.format(user.username))
            return redirect('users:profile')
    
        else:
            messages.warning(request, 'please complete * fields')  
    else:
        form = UserRegisterForm()

    context = {
        'title' : "Register page",
        'form' : form ,
    }    
    return render(request,'users/register.html', context)




# -----------------# login  # -----------------------------------------------#
def loginuser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Conguratulation ( {} ) you do success login '.format(username))
            return redirect('blog:posts')
        
        else:
            messages.warning(request, 'Please enter valid username and password!')  
            return redirect('users:login')

    else:
        form = LoginForm()
               
    context = {
        'title' : 'Login page' ,
        'form'  :  form ,
    }
    return render(request,'users/login.html',context )



# -----------------# logout  # -----------------------------------------------#
@login_required(login_url='users:login')
def logoutuser(request):
    logout(request)

    context = {
        'title': "Logout page",
    }
    return render(request,'users/logout.html',context)




# -----------------# My Porfile update Form  # -----------------------------------------------#
@login_required(login_url='users:login')
def myprofile_update(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid() :
            user_form.save()
            profile_form.save()
            first_name=user_form.cleaned_data['first_name']
            email =user_form.cleaned_data['email']
            messages.success(request, 'profile is updated successfully')  
            return redirect('users:myprofile')
        else:
            messages.warning(request, 'please complete * fields')  
            return redirect('users:myprofile_update')
        
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'Edit profile',
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/myprofile_update.html', context)   





# -----------------# My Porfile informations display # -----------------------------------------------#
@login_required(login_url='users:login')
def myprofile(request):
    my_posts  = Post.objects.all().filter(p_author=request.user).filter(p_status='p')
    
    # ----- pagination -----
    paginator = Paginator(my_posts, 10)
    page = request.GET.get('page')
    try:
         my_posts_pag = paginator.page(page)
    except PageNotAnInteger:
         my_posts_pag = paginator.page(1)
    except EmptyPage:
         my_posts_pag = paginator.page(paginator.num_page)

    context = {
        'title': 'personal profile',
        'my_posts': my_posts,
        'my_posts_pag':my_posts_pag,
        'page': page,
    } 
    return render(request,'users/myprofile.html',context)




