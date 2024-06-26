from django.urls import URLPattern, path 
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('login', views.login, name='login'), 
    path('signup', views.signup, name='signup'), 
    path('logout', views.logout, name='logout'), 
    path('stream/<str:pk>/', views.stream, name='stream'), 
]