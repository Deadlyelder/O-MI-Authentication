from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from security_node.models import Group, User_Group_Relation, Rule, Registered_Users
from django.contrib.auth.models import User
from security_node.form import UserForm, Registered_UsersForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect



@login_required
def home(request):
    #user = request.user
    #return HttpResponse("Hello, " + str(user)+ ". You're at the security_node index.")
    return render(request, "home.html")


@login_required
@csrf_protect
def authmodule(request):
    if request.method == 'POST':
        print ('--------------',request.POST['users_ingroup'])
    registered_users = Registered_Users.objects.all()
    return render(request, "authmodule.html",{"list_users":registered_users})


@login_required
@csrf_protect
def adduser_by_Superuser(request):
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'adduser':
            form = Registered_UsersForm(request.POST)
            if form.is_valid():
                form.save()
    return redirect('authmodule')


def logout(request):
    """
    View used for logging out of the service
    """
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('home')


def login(request):
    """
    View used for logging in to the service
    """
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                auth_login(request, user)
                return redirect('home')
        else:
            form = AuthenticationForm()
        return render(request, "login.html", {'form': form})
    else:
        return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})




