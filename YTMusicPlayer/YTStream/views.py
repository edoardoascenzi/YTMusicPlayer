import email
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
import requests


@login_required(login_url='login')
def index(request):
    if request.method == 'POST':
        YT_url = request.POST['YT_url']
        video_id = resolve_url(YT_url)
        if video_id == "":
            messages.info(request, 'Youtube URL invalid')
            return redirect('/')

        url = "https://yt-api.p.rapidapi.com/dl"

        querystring = {"id":video_id}

        headers = {
            "X-RapidAPI-Key": "0311a97011msh0728878f346d7d8p19c90ejsnce0feef60c8e",
            "X-RapidAPI-Host": "yt-api.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code != 200:
            messages.info(request, 'Video not found')
            return redirect('/')
        response_data = response.json()
        # print(response_data)

        #maybe it is better to wrap all the following code inside a try and except
        if response_data['status'] != 'OK': 
            messages.info(request, 'Error in fatching the video')
            return redirect('/')
        
        title = response_data.get('title', "")
        lengthSeconds = response_data.get('lengthSeconds', 0)
        channelTitle = response_data.get('channelTitle', "")
        # adaptiveFormats is a list of dict -> inside the 21th item there is the url of the audio stream
        audio_url = response_data.get('adaptiveFormats', [{}])[21].get('url',"")
        print(title)
        print(lengthSeconds)
        print(channelTitle)
        print(audio_url)

        
            
        return redirect('music')
        
            

    return render(request, 'index.html')

def resolve_url(url):
    """
    url -> Youtube video link
    return "" if the format of the link is not correct
    else extract the video ID
    """
    if 'www.youtube.com/watch?v=' not in url:
        return ""
    separator1 = url.find("=")
    separator2 = url.find("&")
    
    if separator1 == -1:
        # = key not found
        return ""
    
    if separator2 != -1:
        # & key found, so consider it
        id = url[separator1+1:separator2]
    else:
        # & key not found, so take till the end
        id = url[separator1+1:]

    if len(id) != 11:
        # id is either too long or too short
        return ""
    
    return id
    

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(email)
        print(password)
        user = auth.authenticate(username=username, password=password)

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
def logout(request): 
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def music(request):
    return render(request, 'music.html')
