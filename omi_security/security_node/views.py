from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from security_node.models import Group, User_Group_Relation, Rule, Registered_Users
from django.contrib.auth.models import User
from security_node.form import UserForm, Registered_UsersForm, GroupForm
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
    response = render(request, "home.html")
    response.set_cookie("email", request.user.email)
    return response
    #return render(request, "home.html")


@login_required
@csrf_protect
def authmodule(request):
    #if request.user.is_superuser:
    if request.method == 'POST':
        users_added = request.POST.getlist('users_ingroup')
        action = request.POST['action']
        if action == 'addgroup':
            form = GroupForm(request.POST)
            if form.is_valid():
                form.save()
            group_added_id = Group.objects.get(group_name=request.POST["group_name"])
            for user in users_added:
                instance = User_Group_Relation()
                instance.user_id = Registered_Users.objects.get(id=int(user))
                instance.group_id = group_added_id
                instance.save()
        elif action == 'adduser':
            form = Registered_UsersForm(request.POST)
            if form.is_valid():
                form.save()
    registered_users = Registered_Users.objects.all()
    registered_groups = Group.objects.all()
    return render(request, "authmodule.html",{"list_users":registered_users, "list_groups":registered_groups})
    #else:
    #    return redirect('home')



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
                response = redirect('home')
                response.set_cookie("email", user.email)
                return response
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




