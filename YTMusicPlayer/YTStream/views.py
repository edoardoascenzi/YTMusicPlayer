import email
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST["password"]
        print(email)
        print(password)
        user = auth.authenticate(email=email, password=password)

        print(user)
        if user is None:
            #not logged in
            messages.info(request, 'Credential Invalid')
            return redirect('login')
        
        auth.login(request, user)
        return redirect('/')

    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        # if we load this page through POST medhod it means we ar signing up
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            # if the passwords does not match we need to show the alert and redirect to the same page
            messages.info(request, 'Password Not Matching') # we need to add the messages div
            return redirect('signup')

        if User.objects.filter(email = email).exists():
            messages.info(request, 'Email Already Exists') 
            return redirect('signup')
        
        if User.objects.filter(username = username).exists():
            messages.info(request, 'Username Already Exists') 
            return redirect('signup')
        
        # here if all the check are ok

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        #log the user in
        user_login = auth.authenticate(username=username, password=password)
        auth.login(request, user_login)
        return redirect('/') #redirect to the home page

    else:
        # if we load this page normally, without the POST method we just render it
        return render(request, 'signup.html')
    
@login_required(login_url='login')
def logout(request): #funziona ma non funziona il bottone del logout
    auth.logout(request)
    return redirect('login')


