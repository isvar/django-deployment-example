from django.shortcuts import render
from .forms import UserForm, UserPorfileInfoForm

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

def registration(request):

    register = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserPorfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            
            profile.save()

            register = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserPorfileInfoForm()

    return render(request, 'basic_app/registration.html', context={
        'user_form':user_form,
        'profile_form':profile_form,
        'registered':register
        })

@login_required
def user_logut(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special_view(request):
    return HttpResponse('you are here bro!')

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')    

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse('Account Not Active')
        else:
            print('someone try to log in and failed')
            print(f'username: {username}, and password {password}')
            return HttpResponse('invalid log in details')
    else:
        return render(request, 'basic_app/login.html')



