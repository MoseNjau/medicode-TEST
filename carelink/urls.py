from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register , name='register'),
    path('login/', views.login_view , name='login'),
    path('dashboard/', views.dashboard , name='dashboard'),
    path('logout',views.logout,name = "logout" ),
    #urls for sending messages
    path('send_message/', views.send_message, name='send_message'),
    path('check_messages/', views.check_messages, name='check_messages'), 
]

