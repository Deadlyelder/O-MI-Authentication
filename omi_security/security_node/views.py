from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from security_node.models import Group, User_Group_Relation, Rule
from security_node.form import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404




@login_required
def home(request):
    return HttpResponse("Hello, world. You're at the security_node index.")


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
        form = AuthenticationForm()
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                auth_login(request, user)
                return redirect('home')
        return render(request, "login.html", {'form': form})
    else:
        return redirect('home')





