# YTMusicPlayer

### DISCLAIMER! This work is for academic purposes only. I just want to find a job in the software industry, so I am trying to do some projects to learn as much as possible.

### Description

- I am addicted to dj sets, mainly from youtube (Boiler Room TV ❤) and I hate that you have to pay to just lock the screen of your smartphone, from that the idea to try develop some kind of web app that streams just the audio of a youtube video.

- I am going to create a web app that works as a music player using youtube links as records. I will use Django, probably not the best choice, but I just want to learn how to use it.

- The Youtube stream will be played thorugh a YT API found on RAPID API (https://rapidapi.com/ytjar/api/yt-api). The free plan is limited to 500 request/day, that's okay for my purpose rn.

- The web app is deployed in on an EC2 istance (AWS - they have free ones) using nginx as web server and using gunicorn as supervisor

- I bought a domain on https://www.hostinger.it/ to host it. The web app is available at [edoardoascenzi.fun](https://edoardoascenzi.fun/) (I bought it for 1,5€/y so if you are trying to reach after 17/05/2025 and it is not working, probably it's cause I'm not paying anymore this domain). The certificate for https is done by certbot

### Future features to add

- Some kind of shazam thing that shows the track id while streaming the set

- Add the whole youtube features, not just the link, like the browsing, the playlist thing,..

- Save the history of the videos played

- Add remeber me and forgot password feature
