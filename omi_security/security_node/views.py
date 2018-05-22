from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from security_node.models import Group, User_Group_Relation, Rule
from django.contrib.auth.models import User
from security_node.form import UserForm, GroupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
import json
import jwt


@login_required                                                             #check first if user is logged in or not
def home(request):
    response = render(request, "home.html")                                 #checks and prints if user is superuser or a normal user
    token = jwt.encode({'email': request.user.email, 'is_superuser': request.user.is_superuser}, 'MySecretKey', algorithm='HS256').decode('utf-8') #The decode call here doesn't decode the jwt, it converts the encoded jwt from a byte string to a utf-8 string.
    #token = jwt.encode({'email': request.user.email, 'is_superuser':request.user.is_superuser}, 'MySecretKey', algorithm='HS256')       #Creates jwt token
    #response.set_cookie("email", request.user.email)
    response.set_cookie("token", token)                                     #use the token in session cookie
    return response                                                         #return cookie to client/user


@login_required
def about(request):                                                         #now when user tries to access/request the "about" page, the token is send by client
    token = request.COOKIES.get('token')
    print(token)
    token = jwt.decode(token, 'MySecretKey', algorithm=['HS256'])            #decode the token
    #token = jwt.decode(eval(token), 'MySecretKey', algorithm=['HS256'])
    return render(request, "about.html",{'token':token})                    #send the decoded token to about page




@login_required
@csrf_protect
def authmodule(request):
    if request.user.is_superuser:                                           #only super user can access the webclient and not the normal user
        message = ''                                                        #initialize a variable "message" and make it empty
        if request.method == 'POST':
            users_added = request.POST.getlist('users_ingroup')             #get list of user ids added in the group
            action = request.POST['action']                                 #gets the save button's name = action into the "action" variable
            if action == 'addgroup':                                        #if action value is "add group"
                form = GroupForm(request.POST)                              #get the GroupForm defined in forms.py
                if form.is_valid():                                         #check validity of the GroupForm
                    form.save()                                             #save values in Group table
                else:
                    message = form.errors['group_name'].as_text()           #if validity fails, get error message as text form and save in message variable
                group_added_id = Group.objects.get(group_name=request.POST["group_name"])   #gets group id of the group just added
                #print('11111111111', group_added_id)
                for user in users_added:
                    instance = User_Group_Relation()                        #get User_Group_Relation table
                    #instance.user_id = Registered_Users.objects.get(id=int(user))
                    instance.user_id = User.objects.get(id=int(user))       #get user id in User_Group_Relation table by matching user id of User table and in users-added list of user ids
                    instance.group_id = group_added_id                      #get group id in User_Group_Relation table
                    instance.save()                                         #save values in table
            #elif action == 'adduser':
                #form = Registered_UsersForm(request.POST)
                #if form.is_valid():
                    #form.save()
        #registered_users = Registered_Users.objects.all()
        users = User.objects.filter(is_superuser=False)                     #get all users who are not super users
        registered_groups = Group.objects.all()                             #get all groups
        return render(request, "authmodule.html",{"list_users":users, "list_groups":registered_groups, 'errormessage':message })    #send users, groups and error message(if any) to authmodule.html file
    else:
        return redirect('home')                                             #if user is not a superuser, redirect him to home page



def logout(request):
    """
    View used for logging out of the service
    """
    if request.user.is_authenticated:
        auth_logout(request)
        response = redirect('home')
        response.delete_cookie('token')
        return response
    return redirect('home')


def login(request):
    """
    View used for logging in to the service
    """
    if not request.user.is_authenticated:                             #if user is not logged in
        if request.method == 'POST':                                  #after filling username and password fields and pressing login button, a post request is made
            form = AuthenticationForm(data=request.POST)              #django.contrib.auth provides AuthenticationForm to which requested data is send
            if form.is_valid():                                       #is_valid() method to run validation and return a boolean designating whether the data was valid
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)   # authenticate() to verify username and password
                auth_login(request, user)                             #built-in login function
                return redirect('home')                               #after successful login, user redirected to home page
        else:
            form = AuthenticationForm()
        return render(request, "login.html", {'form': form})          #if no post method, then go to the login page again
    else:
        return redirect('home')                                       #if user is already logged in , redirect him to home page

def signup(request):                                                 #function used for sign-up
    if request.method == 'POST':
        form = UserForm(request.POST)                                #UserForm is defined in forms.py
        if form.is_valid():                                          #Checks validity
            form.save()                                              #saves the credentials in database
            return redirect('home')                                  #redirected the user to home where he will be asked to login (after sign-up)
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})


def omi_authquery(request):
    email = request.GET.get('email')
    token = request.COOKIES.get('token')
    print('--------------',token)
    #try:
    status=False                                                #set a variable "status" to false initially
    user = User.objects.get(email=email)                        #get the user from User table by matching with requested email address
    if user.is_superuser:                                       #if he is a super user then status is changed to true
        status=True
    decoded_token = jwt.decode(token, 'MySecretKey', algorithm=['HS256'])
    decoded_email = decoded_token['email']
    print(decoded_token, '------********------', decoded_email)
    users_id = User.objects.get(email=email).pk                                              #gets user id from the User  table after matching with requested email address
    relation_group_id = User_Group_Relation.objects.filter(user_id=int(users_id))            #gets group id of in which that user belongs
    for r in relation_group_id:
        print('555555',r.group_id.id)
    reply = json.dumps({'email': email, 'userExist': True, 'isAdmin':status})                #making json response if user is in a group: user exists status, admin status and his email address
    #except:
        #reply=json.dumps({'email':email, 'userExist':False, 'isAdmin':status})              #making json response if user is not in a group: user exists status, admin status and his email address
    #{'allow': [<paths>], 'deny': [<paths>], 'isAdmin': true|false}
    return HttpResponse(reply)









