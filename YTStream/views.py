import email
from email.mime import audio
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
        video_info = fatch_video_info(video_id)

        if video_info is None:
            messages.info(request, 'Error in fatching the video')
            return redirect('/')
        
        # use context as a list in order to be able to add more feature like the youtube search that returns more items
        context = {
            'video_infos' : [video_info]
        }
        return render(request, 'index.html', context)
        
    return render(request, 'index.html')


@login_required(login_url='login')
def stream(request, pk):
    video_id = pk
    context = fatch_video_info(video_id)
    if context is None:
        messages.info(request, 'Error in fatching the video')
        return redirect('/')
    return render(request, 'stream.html', context)
        

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
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

# UTILS

def resolve_url(url):
    """
    url -> Youtube video link
    return "" if the format of the link is not correct
    else extract the video ID
    """
    if 'www.youtube.com/watch?v=' in url:
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
    # for link from app share 
    elif 'youtu.be/' in url:
        index1 = url.find('youtu.be/') + len('youtu.be/') 
        separator2 = url.find('?')
        
        if separator2 == -1:
            # ? key not found
            
            return ""
        
        id = url[index1:separator2]
        if len(id) != 11:
            # id is either too long or too short
            return ""
    
    return id

def fatch_video_info(video_id):
    """
    Fatch the video details and return a dict with all the infos
    If errors occurs it returns None
    """
    if video_id == "":
            return None

    url = "https://yt-api.p.rapidapi.com/dl"

    querystring = {"id":video_id}

    headers = {
        "X-RapidAPI-Key": "0311a97011msh0728878f346d7d8p19c90ejsnce0feef60c8e",
        "X-RapidAPI-Host": "yt-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        return None

    response_data = response.json()

    status = response_data.get('status', "")
    title = response_data.get('title', "")
    channelTitle = response_data.get('channelTitle', "")
    thumbnailSmall = response_data.get('thumbnail', [{}] )[0].get('url',"")
    thumbnail = response_data.get('thumbnail', [{}] )[-1].get('url',"")
    lengthSeconds = response_data.get('lengthSeconds', 0)

    # get all the adaptiveFormats
    adaptiveFormats = response_data.get('adaptiveFormats', [{}])
    # make a dict like audioQuality : url
    audioQuality_adaptiveFormats = {item['audioQuality']: item['url'] for item in adaptiveFormats if "audioQuality" in item.keys()}
    qualityList = ["AUDIO_QUALITY_ULTRAHIGH", "AUDIO_QUALITY_HIGH", "AUDIO_QUALITY_MEDIUM", "AUDIO_QUALITY_LOW", "AUDIO_QUALITY_ULTRALOW"]
    audio_url = ""
    #in this way we get always the best quality available
    for quality in qualityList:
        if quality in audioQuality_adaptiveFormats.keys():
            audio_url = audioQuality_adaptiveFormats[quality]
            print(quality)
            break


    if status == "" or audio_url == "":
        return None
    
    lengthSeconds = int(lengthSeconds)
    hours = int(lengthSeconds/(60*60))
    minutes = int(lengthSeconds/60 - hours*60)
    seconds = int(lengthSeconds - minutes*60 - hours*60**2)

    video_info = {
        'video_id' : video_id,
        'status' : status,
        'title' : title,
        'thumbnailSmall' : thumbnailSmall,
        'thumbnail' : thumbnail,
        'channelTitle' : channelTitle,
        'duration_text' : f"{hours}:{minutes:02}:{seconds:02}",
        'audio_url' : audio_url,
    }

    return video_info